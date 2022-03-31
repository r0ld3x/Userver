"""
`{i}{cmd_name}` :- **Check if Userbot Alive**
"""

import time
from platform import python_version
from asyncio import sleep
from telethon.tl.custom.inlinebuilder import InlineBuilder
from telethon import Button, __version__ as tele_ver

from userver.config import get_int
from userver.strings.lang import get_string, get_strings
from userver.dec import in_pattern, user_cmd
from userver import PIC, adb, start_time,USER_ID, USER_NAME, __version__
from userver.helpers.locals import time_formatter
from userver.dec import IN_BTTS as buttons
from . import HELP



@user_cmd(pattern = 'alive( (.*)|$)')
@get_strings('alive')
async def _(e, string):
    uptime = time_formatter((time.time() - start_time) * 1000)
    ALIVE_TEXT = await adb.get_key("ALIVE_TEXT") or string['ALIVE_TEXT']
    text = ALIVE_TEXT.format(
        owner = USER_NAME,
        user_id = USER_ID,
        version = __version__,
        py_ver = python_version(),
        tele_version = tele_ver,
        up_time = uptime
    )
    await e.reply(
        text,
        parse_mode = 'md',
        file = PIC,
        link_preview=False
    )
    await e.try_delete()


def split_list(List, index):
    new_ = []
    while List:
        new_.extend([List[:index]])
        List = List[index:]
    return new_



def page_num(index, key):
    rows = get_int("HELP_ROWS") or 5
    cols = get_int("HELP_COLUMNS") or 2
    loaded = HELP.keys()
    emoji = get_int("EMOJI_IN_HELP") or "✘"
    List = [
        Button.inline(f"{emoji} {x} {emoji}", data=f"plugin_{key}_{x}|{index}")
        for x in sorted(loaded)
    ]
    all_ = split_list(List, cols)
    fl_ = split_list(all_, rows)
    try:
        new_ = fl_[index]
    except IndexError:
        new_ = fl_[0] if fl_ else []
        index = 0
    if index == 0 and len(fl_) == 1:
        new_.append([Button.inline("« Bᴀᴄᴋ »", data="open")])
    else:
        new_.append(
            [
                Button.inline(
                    "« Pʀᴇᴠɪᴏᴜs",
                    data=f"uh_{key}_{index-1}",
                ),
                Button.inline("« Bᴀᴄᴋ »", data="open"),
                Button.inline(
                    "Nᴇxᴛ »",
                    data=f"uh_{key}_{index+1}",
                ),
            ]
        )
    return new_





@in_pattern("alive", owner=True)
async def inline_alive(ult):
    strings = await get_string('alive')
    ALIVE_TEXT = await adb.get_key("ALIVE_TEXT") or strings['ALIVE_TEXT']
    uptime = time_formatter((time.time() - start_time) * 1000)
    text = ALIVE_TEXT.format(
        owner = USER_NAME,
        user_id = USER_ID,
        version = __version__,
        py_ver = python_version(),
        tele_version = tele_ver,
        up_time = uptime
    )
    results = [
                await ult.builder.photo(
                    file = PIC,
                    text=text,
                    parse_mode="md",
                    buttons=buttons,
                )
                ]
    return await ult.answer(results, cache_time=300)