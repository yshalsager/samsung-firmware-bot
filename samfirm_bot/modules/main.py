""" SamFirm Bot main module"""

from telethon import events

from samfirm_bot.samfirm_bot import BOT


@BOT.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is sent."""
    await event.reply("Hi!")
    raise events.StopPropagation  # Other handlers won't have an event to work with

# @BOT.on(events.NewMessage)
# async def echo(event):
#     """Echo the user message."""
#     await event.respond(event.text)
