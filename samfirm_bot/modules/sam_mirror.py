""" SamFirm Bot mirror module"""
import re
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE
from shutil import rmtree

from telethon import events, Button

from samfirm_bot import TG_LOGGER, TG_BOT_ADMINS
from samfirm_bot.samfirm_bot import BOT, SAM_FIRM, SF
from samfirm_bot.utils.checker import is_device, is_region


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern=r'/samup(?: )(.*)(?: )([a-zA-Z]{3})(?: )?(.*)?'))
async def mirror(event):
    """ Mirror Samsung firmware """
    try:
        version = event.pattern_match.group(3).upper()
    except IndexError:
        version = None
    model = event.pattern_match.group(1).upper()
    region = event.pattern_match.group(2).upper()
    if not await is_device(model) or not await is_region(region):
        await event.reply("**Either model or region is incorrect!**")
        return
    bot_reply = await event.reply("__Preparing...__")
    command = SAM_FIRM.download_update(model, region, version)
    sf_path = None
    process = await create_subprocess_shell(command, stdin=PIPE, stdout=PIPE)
    while True:
        output = await process.stdout.readline()
        if output:
            line = output.decode("utf-8").strip()
            if "Could not" in line:
                await bot_reply.edit("**Not Found!**")
                return
            if "Checking" in line:
                await bot_reply.edit("__Checking...__")
            if "Version:" in line:
                version = re.search(r"(?:Version: )(.*)", line).group(1).split('/')[0]
                sf_path = f"{SF.project}/{model}/{region}/{version}"
                if await SF.sftp.isdir(sf_path):
                    await event.reply(f"**This firmware ({version}) is already mirrored!**", buttons=[
                        Button.url("Check here", f"{SF.url}/files/{model}/{region}/{version}")])
                    process.kill()
                    return
                else:
                    await bot_reply.edit(f"**Firmware {version} found, starting download!**")
            if "Downloading" in line:
                await bot_reply.edit("__Downloading...__")
            if "Decrypting" in line:
                await bot_reply.edit("__Decrypting...__")
            if "Finished" in line:
                await bot_reply.edit("__Download Finished!...__")
        else:
            break
    await process.wait()
    download = SAM_FIRM.get_downloaded(model, region)
    TG_LOGGER.info(f"Mirroring {download}")
    if download:
        download_folder = '/'.join(download.split('/')[:-1]) + '/'
        await bot_reply.edit(f"**Downloaded {download} Successfully!**")
        SAM_FIRM.extract_files(download)
        await bot_reply.edit(f"**Extracted files, upload is going to start!**")
        await SF.upload(sf_path, download_folder)
        await bot_reply.edit(f"**Uploaded Successfully!**")
        await event.reply(f"**Download from SourceForge**", buttons=[
            Button.url(version, f"{SF.url}/files/{model}/{region}/{version}")])
        TG_LOGGER.info(f"Mirrored {SF.url}/files/{model}/{region}/{version}")
        rmtree(download_folder)
