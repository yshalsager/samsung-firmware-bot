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
    bot_reply = await event.reply("__Checking...__")
    command = SAM_FIRM.download_update(model, region, version)
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while True:
        output = process.stdout.read()
        if output == '' and process.poll() is not None:
            break
        if output and b"Could not fetch info" in output:
            await bot_reply.edit("**Not Found!**")
            return
        if output and b"Version" in output:
            await bot_reply.edit("**Firmware found, starting download**")
        if output and b"Downloading" in output:
            await bot_reply.edit("__Downloading...__")
        if output and b"Decrypting" in output:
            await bot_reply.edit("__Decrypting...__")
        if output and b"Finished" in output:
            await bot_reply.edit("__Download Finished!...__")
            break
    await event.reply(f"**Downloaded {SAM_FIRM.get_downloaded()}**")


