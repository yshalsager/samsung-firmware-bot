""" SamFirm Bot check updates module"""
import subprocess

from telethon import events

from samfirm_bot import TG_LOGGER
from samfirm_bot.samfirm_bot import BOT, SAM_FIRM
from samfirm_bot.utils.checker import is_device, is_region


@BOT.on(events.NewMessage(pattern=r'/samcheck(?: )(.*)(?: )([a-zA-Z]{3})(?: )?(.*)?'))
async def check(event):
    """Send a message when the command /samcheck is sent."""
    model = event.pattern_match.group(1).upper()
    region = event.pattern_match.group(2).upper()
    try:
        version = event.pattern_match.group(3).upper()
    except IndexError:
        version = None
    if not await is_device(model) or not await is_region(region):
        await event.reply("**Either model or region is incorrect!**")
        return
    command = SAM_FIRM.check_update(model, region, version)
    bot_reply = await event.reply("__Checking...__")
    # process = subprocess.Popen(command,
    #                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1,
                          universal_newlines=True, shell=True) as p:
        output = p.stdout.read()
        if output and "Could not fetch info" in output:
            await bot_reply.edit("**Not Found!**")
            return
        if output and "Version" in output:
            update = SAM_FIRM.parse_output(output)
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
