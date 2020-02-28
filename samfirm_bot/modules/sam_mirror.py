""" SamFirm Bot mirror module"""
import re
import signal
import subprocess
from os import setsid, killpg, getpgid
from shutil import rmtree

from telethon import events, Button

from samfirm_bot import TG_LOGGER, TG_BOT_ADMINS
from samfirm_bot.samfirm_bot import BOT, SAM_FIRM, SF
from samfirm_bot.utils.checker import is_device, is_region


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern=r'/samup(?: )(.*)(?: )([A-Z]{3})(?: )?(.*)?'))
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
    with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1,
                          universal_newlines=True, shell=True, preexec_fn=setsid) as p:
        for line in p.stdout:
            if line == '\n':
                continue
            if line and "Could not" in line:
                await bot_reply.edit("**Not Found!**")
                return
            if line and "Checking" in line:
                await bot_reply.edit("__Checking...__")
            if line and "Version:" in line:
                version = re.search(r"(?:Version: )(.*)", line).group(1).split('/')[0]
                sf_path = f"{SF.project}/{model}/{region}/{version}"
                if SF.sftp.isdir(sf_path):
                    await event.reply(f"**This firmware ({version}) is already mirrored!**", buttons=[
                        Button.url("Check here", f"{SF.url}/files/{model}/{region}/{version}")])
                    killpg(getpgid(p.pid), signal.SIGTERM)
                    return
                else:
                    await bot_reply.edit(f"**Firmware {version} found, starting download!**")
            if line and "Downloading" in line:
                await bot_reply.edit("__Downloading...__")
            if line and "Decrypting" in line:
                await bot_reply.edit("__Decrypting...__")
            if line and "Finished" in line:
                await bot_reply.edit("__Download Finished!...__")
    download = SAM_FIRM.get_downloaded(model, region)
    TG_LOGGER.info(f"Mirroring {download}")
    if download:
        download_folder = '/'.join(download.split('/')[:-1])
        await bot_reply.edit(f"**Downloaded {download} Successfully!**")
        SAM_FIRM.extract_files(download)
        await bot_reply.edit(f"**Extracted files, upload is going to start!**")
        SF.sftp.makedirs(sf_path)
        SF.sftp.put_r(download_folder, sf_path, preserve_mtime=True)
        await bot_reply.edit(f"**Uploaded Successfully!**")
        await event.reply(f"**Download from SourceForge**", buttons=[
            Button.url(version, f"{SF.url}/files/{model}/{region}/{version}")])
        TG_LOGGER.info(f"Mirrored {SF.url}/files/{model}/{region}/{version}")
        rmtree(download_folder)
