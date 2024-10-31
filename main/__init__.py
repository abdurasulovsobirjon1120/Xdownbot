import logging.handlers
from pyrogram import Client

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

import logging, time, sys

from config import API_HASH, API_ID, TG_BOT_TOKEN, SESSION, OWNER_ID, TG_BOT_WORKERS, OWNER_TAG

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

log_handler = logging.handlers.RotatingFileHandler(
    filename='logs.txt', maxBytes=50000000, backupCount=5
)

log_handler.setFormatter(logging.Formatter(
    '[%(levelname)s/%(asctime)s] %(name)s:%(lineno)d: %(message)s'))

logging.getLogger().addHandler(log_handler)

logging.getLogger().setLevel(logging.WARNING)


# variables
API_ID = API_ID
API_HASH = API_HASH
BOT_TOKEN = TG_BOT_TOKEN
SESSION = SESSION
AUTH = OWNER_ID
OWNER_TAG = OWNER_TAG

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

userbot = Client("saverestricted", session_string=SESSION, api_hash=API_HASH, api_id=API_ID) 

try:
    userbot.start()
except BaseException:
    print("Userbot Error ! Have you added SESSION while deploying??")
    sys.exit(1)

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH,
    workers=TG_BOT_WORKERS,
)    

try:
    Bot.start()
except Exception as e:
    print(e)
    sys.exit(1)
