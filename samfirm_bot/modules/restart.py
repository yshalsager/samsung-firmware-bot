""" SamFirm Bot restart module"""
import pickle
from os import execl
from sys import executable

from telethon import events

from samfirm_bot import TG_BOT_ADMINS
from samfirm_bot.samfirm_bot import BOT


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern=r'/samrestart'))
async def restart(event):
    """ restart Samsung bot """
    restart_message = await event.reply("Restarting, please wait...")
    chat_info = {
        'chat': restart_message.chat_id,
        'message': restart_message.id
    }
    with open(f"restart.pickle", "wb") as out:
        pickle.dump(chat_info, out)
    execl(executable, executable, "-m", "samfirm_bot")
