from babel.core import Locale
import os,sys
import yaml

from userver.helpers.logger import log
from userver import adb



LANGUAGES = {}


for file in os.listdir('userver/strings/strings'):
    if not file.endswith('.yaml'): continue
    with open("userver/strings/strings/" + file, "r", encoding="utf8") as f:
        lang = yaml.load(f, Loader=yaml.CLoader)
        lang_code = lang['code']
        log.info(f"Loading {lang_code} Language.")
        LANGUAGES[lang_code] = lang




async def get_string(module: str):
    lang = await adb.get_key("language") or "en"
    if lang in LANGUAGES:
        if module in LANGUAGES[lang]:
            return LANGUAGES[lang][module]
        else:
            return {}


def get_strings(module: str):
    def inner(func):
        async def wrapped(*args,**kwargs):
            _ = await get_string(module.lower())
            await func(*args, _ ,**kwargs)
        return wrapped
    return inner

    #     if key in LANGUAGES[lang]:
    #         return LANGUAGES[lang][key]
    #     else:
    #         log.info(f"{key} not found in languages.")
    #         return 'None'
    # else:
    #     log.info(f"{key} Language not found.")