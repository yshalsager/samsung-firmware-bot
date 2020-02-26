""" SamFirm Bot check updates module"""

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
    update = SAM_FIRM.check_update(model, region, version)
    if update:
        TG_LOGGER.info(update)
        reply = f"**Model:** {update['model']}\n" \
                f"**System Version:** {update['system']}\n" \
                f"**Android Version:** {update['android']}\n" \
                f"**CSC Version:** {update['csc']}\n" \
                f"**Bootloader Version:** {update['bootloader']}\n" \
                f"**Release Date:** {update['date']}\n" \
                f"**Size:** {update['size']}"
        await event.reply(reply)
    else:
        await event.reply("**Not Found!**")
    raise events.StopPropagation
