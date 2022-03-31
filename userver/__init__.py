import os
import platform
import time
import asyncio
from telethon import __version__ as tele_version
from userver.database.aioredis import UserverAioRedis

from userver.helpers.locals import session_file, where_hosted
from userver.config import get_int, get_str
from userver.helpers.logger import log
from userver.database.redis import UserverRedis
from userver.misc.BaseClient import UserverClient

__version__ = '1.0'

startt = """

█▀ ▀█▀ ▄▀█ █▀█ ▀█▀   █▀▄ █▀▀ █▀█ █░░ █▀█ █▄█ █▀▄▀█ █▀▀ █▄░█ ▀█▀
▄█ ░█░ █▀█ █▀▄ ░█░   █▄▀ ██▄ █▀▀ █▄▄ █▄█ ░█░ █░▀░█ ██▄ █░▀█ ░█░                        
"""

print(startt)

log.info("STARTING BOT...")

start_time = time.time()
HOSTED_ON = where_hosted()
API_ID = get_int("API_ID")
API_HASH = get_str("API_HASH")
BOT_TOKEN = get_str("BOT_TOKEN")

HANDLER = get_str("HANDLER") or "."
PIC = get_str("PIC_URL") or 'https://te.legra.ph/file/139bb3846b6a43bc13de3.jpg'

u_bot = UserverClient(
        session_file(),
        app_version=__version__,
        device_model="Userver",
    )

USER_ID = u_bot.uid
OWNER_ID = u_bot.uid
USERNAME = u_bot.username
USER_NAME = u_bot.full_name


asst = UserverClient('userver', API_ID,API_HASH, bot_token = BOT_TOKEN)

BOT_ID = asst.uid
BOT_USERNAME = asst.username
BOTNAME = asst.full_name

log.info("Bot ID: %s",BOT_ID)
log.info("Bot USERNAME: %s",BOT_USERNAME)
log.info("Bot NAME: %s",BOTNAME)

LOG_CHAT = get_int("LOG_CHAT")


rdb = UserverRedis(
    host = get_str("REDIS_URI"),
    port = get_int("REDIS_PORT"),
    password = get_str("REDIS_PASS") or '' ,
)

adb = UserverAioRedis(
    host = get_str("REDIS_URI"),
    port = get_int("REDIS_PORT"),
    password = get_str("REDIS_PASS") or '' ,
)

if rdb.ping():
    log.info("Redis Started Successfully...")





log.info(f"Python version - {platform.python_version()}")
log.info(f"Userver Version - {__version__}")
log.info(f"Telethon Version - {tele_version}")
log.info(f"Hosted On  ['{HOSTED_ON}']")