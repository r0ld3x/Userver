

"""
`{i}help` | `{i}help <cmd name>` :- **Get help about cmd name.**
"""

from pkgutil import extend_path
import re
from telethon.errors.rpcerrorlist import (
    BotInlineDisabledError,
    BotMethodInvalidError,
    BotResponseTimeoutError,
)
from telethon.tl.custom import Button
from platform import python_version
from asyncio import sleep
from userver.config import get_int, get_str
from userver.plugins.alive import page_num

from userver.strings.lang import get_strings
from userver.dec import asst_cmd, callback, in_pattern, user_cmd
from userver import PIC, USER_ID, USER_NAME, asst, u_bot
from userver.plugins import HELP


@in_pattern("usrvr", owner=True)
async def inline_handler(event):  # {len({HELP.keys()})}
    lengthofhelp = len(HELP)
    text = f"""
Hello [{USER_NAME}](tg://user?id={USER_ID})
I Am Userver The Advance MultiTasking Userbot For My [Master](tg://user?id={USER_ID})

Total Commands Available- {lengthofhelp}
Github: [TheUserver](https://www.github.com/r0ld3x/Userver)
License:  [GNU Affero General Public License](https://www.github.com/r0ld3x/Userver/LICENSE")
Channel: @TheUserver || @TheUserverSupport
©[Userver](https://www.github.com/r0ld3x/Userver)
"""
    if PIC:
        result = await event.builder.photo(
            file=PIC,
            link_preview=False,
            text=text,
            buttons=page_num_x(0),
        )
    else:
        result = await event.builder.article(
            title="Userver Help Menu", text=text, buttons=page_num_x(0)
        )
    await event.answer([result], private=True, cache_time=300, gallery=True)


@user_cmd(pattern='help( (.*)|$)')
async def _(e):
    match = e.pattern_match.group(1).strip()
    chat = await e.get_chat()
    if not match:
        try:
            res = await u_bot.inline_query(asst.username, 'usrvr')
        except BotMethodInvalidError:
            lengthofhelp = len(HELP)
            text = f"""
Hello [{USER_NAME}](tg://user?id={USER_ID})
I Am Userver The Advance MultiFunctional Userbot For My [Master](tg://user?id={USER_ID})

Total Commands Available- {lengthofhelp}
Github: [Userver](https://www.github.com/r0ld3x/Userver)
License:  ["GNU Affero General Public License"](https://www.github.com/r0ld3x/Userver/LICENSE)
Channel: @TheUserver 
©[Userver](https://www.github.com/r0ld3x/Userver)
"""
            await e.reply(text,
                          buttons=page_num_x(0),
                          )
        await res[0].click(chat.id, reply_to=e.reply_to_msg_id, hide_via=True)
    else:
        text = f"""
**Plugin Name**- `{match}`
{HELP.key(match)}

Github: [Userver](https://www.github.com/r0ld3x/Userver)
©[Userver](@TheUserver)
"""
        await e.edit(text)


def short_list(list, index):
    new_list = []
    while list:
        new_list.extend([list[:index]])
        list = list[index:]
    return new_list


def page_num_x(index):
    p_key = HELP.keys()
    rows = get_int("HELP_ROWS") or 4
    col = get_int("HELP_COLUMNS") or 2
    emoji = get_str('HELP_EMOJI') or '🗹'
    cmds = [
        Button.inline(f"{emoji} {x} {emoji}", data=str(f"plugin_{x}_{index}").encode('utf-8')) for x in sorted(p_key)
    ]

    all_rows = short_list(cmds, rows)
    all_cols = short_list(all_rows, col)
    try:
        buttons = all_cols[index]

    except IndexError:
        buttons = all_cols[0] if all_cols else []
        index = 0
    if index == 0 and all_cols == 1:
        buttons.append([Button.inline("✖", data="close")])
    else:
        buttons.append(
            [
                Button.inline(
                    "◄",
                    data=f"help_{index-1}",
                ),
                Button.inline("✖", data="close"),
                Button.inline(
                    "►",
                    data=f"help_{index+1}",
                ),
            ]
        )
    return buttons
