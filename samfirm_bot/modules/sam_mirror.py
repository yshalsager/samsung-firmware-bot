""" SamFirm Bot mirror module"""
import subprocess

from telethon import events

from samfirm_bot import TG_LOGGER
from samfirm_bot.samfirm_bot import BOT, SAM_FIRM
from samfirm_bot.utils.checker import is_device, is_region


@BOT.on(events.NewMessage(pattern=r'/sam_mirror(?: )(.*)(?: )([A-Z]{3})(?: )?(.*)?'))
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
                          universal_newlines=True, shell=True) as p:
        for line in p.stdout:
            if line and "Could not" in line:
                await bot_reply.edit("**Not Found!**")
                return
            if line and "Checking" in line:
                await bot_reply.edit("__Checking...__")
            if line and "Version" in line:
                await bot_reply.edit("**Firmware found, starting download**")
            if line and "Downloading" in line:
                await bot_reply.edit("__Downloading...__")
            if line and "Decrypting" in line:
                await bot_reply.edit("__Decrypting...__")
            if line and "Finished" in line:
                await bot_reply.edit("__Download Finished!...__")
    await event.reply(f"**Downloaded {SAM_FIRM.get_downloaded()}**")


