#!/usr/bin/env python3.7
""" SamFirm Telegram Bot"""
import asyncio
import pickle
from os import path, remove

from telethon.sync import TelegramClient

from samfirm_bot import API_KEY, API_HASH, BOT_TOKEN, TG_LOGGER, LOCAL_STORAGE, WEB_STORAGE, PARENT_DIR, WORK_DIR
from samfirm_bot.classes.local_client import LocalClient
from samfirm_bot.modules import ALL_MODULES
from samfirm_bot.classes.samfirm import SamFirm
from samfirm_bot.utils.loader import load_modules

BOT = TelegramClient('samfirm_bot', API_KEY, API_HASH).start(bot_token=BOT_TOKEN)
BOT.parse_mode = 'markdown'
BOT_INFO = {}
SAM_FIRM = SamFirm(BOT.loop)
STORAGE = LocalClient(LOCAL_STORAGE, WEB_STORAGE)


def main():
    """Main"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


async def run():
    """Run the bot."""
    bot_info = await BOT.get_me()
    BOT_INFO.update({'name': bot_info.first_name,
                     'username': bot_info.username, 'id': bot_info.id})
    TG_LOGGER.info("Bot started as %s! Username is %s and ID is %s",
                   BOT_INFO['name'], BOT_INFO['username'], BOT_INFO['id'])
    TG_LOGGER.info(f"Storage location: {LOCAL_STORAGE} - Website URL:{WEB_STORAGE}")
    TG_LOGGER.info(f"Work directory: {WORK_DIR} - Parent directory: {PARENT_DIR}")
    load_modules(ALL_MODULES, __package__)
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        await BOT.edit_message(restart_message['chat'], restart_message['message'], 'Restarted Successfully!')
        remove('restart.pickle')
    async with BOT:
        await BOT.run_until_disconnected()
