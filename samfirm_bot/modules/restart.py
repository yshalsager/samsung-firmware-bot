""" SamFirm Bot restart module"""
from os import execl
from sys import executable
from telethon import events

from samfirm_bot import TG_BOT_ADMINS
from samfirm_bot.samfirm_bot import BOT


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern=r'/samrestart'))
async def restart(event):
    """ restart Samsung bot """
    execl(executable, executable, "-m", "samfirm_bot")

