#!/usr/bin/env python3.7
""" SamFirm Telegram Bot"""
import asyncio

from telethon.sync import TelegramClient

from samfirm_bot import API_KEY, API_HASH, BOT_TOKEN, TG_LOGGER
from samfirm_bot.modules import ALL_MODULES
from samfirm_bot.classes.samfirm import SamFirm
from samfirm_bot.utils.loader import load_modules

BOT = TelegramClient('samfirm_bot', API_KEY, API_HASH).start(bot_token=BOT_TOKEN)
BOT.parse_mode = 'markdown'
BOT_INFO = {}
SAM_FIRM = SamFirm()


def main():
    """Main"""
    # # samfirm.check_update("SM-A015F", "TUR")
    # update = samfirm.check_update("SM-G970F", "DBT")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


async def run():
    """Run the bot."""
    bot_info = await BOT.get_me()
    BOT_INFO.update({'name': bot_info.first_name,
                     'username': bot_info.username, 'id': bot_info.id})
    TG_LOGGER.info("Bot started as %s! Username is %s and ID is %s",
                   BOT_INFO['name'], BOT_INFO['username'], BOT_INFO['id'])
    load_modules(ALL_MODULES, __package__)
    async with BOT:
        await BOT.run_until_disconnected()
