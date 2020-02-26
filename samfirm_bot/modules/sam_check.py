""" SamFirm Bot check updates module"""
import re
import subprocess

from telethon import events

from samfirm_bot import TG_LOGGER
from samfirm_bot.samfirm_bot import BOT, SAM_FIRM


@BOT.on(events.NewMessage(pattern=r'/samcheck(?: )(.*)(?: )([A-Z]{3})(?: )?(.*)?'))
async def check(event):
    """Send a message when the command /samcheck is sent."""
    model = event.pattern_match.group(1).upper()
    region = event.pattern_match.group(2).upper()
    try:
        version = event.pattern_match.group(3).upper()
    except IndexError:
        version = None
    command = SAM_FIRM.check_update(model, region, version)
    bot_reply = await event.reply("__Checking...__")
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
            update = SAM_FIRM.parse_output(output.decode("utf-8"))
            TG_LOGGER.info(update)
            message = f"**Model:** {update['model']}\n" \
                      f"**System Version:** {update['system']}\n" \
                      f"**Android Version:** {update['android']}\n" \
                      f"**CSC Version:** {update['csc']}\n" \
                      f"**Bootloader Version:** {update['bootloader']}\n" \
                      f"**Release Date:** {update['date']}\n" \
                      f"**Size:** {update['size']}"
            await bot_reply.edit(message)
            return
