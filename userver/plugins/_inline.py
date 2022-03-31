"""
`{i}inline` | `{i}inline <cmd name>` :- **Get inline about cmd name.**
"""

import re, os
from telethon.errors.rpcerrorlist import (
    BotInlineDisabledError,
    BotMethodInvalidError,
    BotResponseTimeoutError,
)
from telethon.tl.custom import Button
from platform import python_version
from asyncio import sleep
from userver.config import get_str
from userver.plugins.alive import page_num

from userver.helpers.logger import log
from userver.dec import asst_cmd, callback, in_pattern, user_cmd
from ._help import page_num_x
from userver import HANDLER, PIC, USER_ID, USER_NAME, asst, u_bot
from userver.plugins import HELP


_main_help_menu = [
    [
        Button.inline('ᴏᴘᴇɴ ᴀɢᴀɪɴ', data="help_0")
    ]
]

@callback(re.compile("plugin_(.*)"), owner=True)
async def help_func(e):
    key , index = e.data_match.group(1).decode("utf-8").split('_')
    doc = HELP.get(key) or f"No plugin Help Found For `{key}` Command."
    text = f"""
**Plugin Name**- `{key}`
{doc}

Github: [Userver](https://www.github.com/r0ld3x/Userver)
©[Userver]({get_str("GITHUB_REPO")})
"""
    buttons = [
        [
            Button.inline('ꜱᴇɴᴅ ᴘʟᴜɢɪɴ', f"send_{key}_{index}")
        ],
        [
            Button.inline('ʙᴀᴄᴋ', f"help_{index}")
        ]
    ]
    
    try:
        await e.edit(text, buttons=buttons)
    except Exception as ee:
        log.exception(ee)
        await e.edit(f"Send `{HANDLER}help {key}` To Check Help.", buttons = buttons)






@callback(re.compile("send_(.*)"), owner=True)
async def help_func(e):
    key , index = e.data_match.group(1).decode("utf-8").split('_')
    await e.answer("Sending....")
    plugin_dir = f"userver/plugins/{key}.py"
    if os.path.exists(plugin_dir):
        await u_bot.send_file(e.chat_id,file = plugin_dir, force_document = True, caption = HELP[key] if key in HELP else None)
        await e.answer("File Sent To Save Messages.")
        buttons = [
            [
            Button.inline('ʙᴀᴄᴋ', f"help_{index}")
            ]
        ]
        await e.edit("File Sent To Save Messages.", buttons=buttons)
    else:
        await e.answer("File not Found.")






@callback(re.compile("help_(.*)"), owner=True)
async def help_func(e):
    index = int(e.data_match.group(1).decode("utf-8"))
    lengthofhelp = len(HELP)
    
    text = f"""
Hello [{USER_NAME}](tg://user?id={USER_ID})
I Am Userver The Advance MultiFunctional Userbot For My [Master](tg://user?id={USER_ID})

Total Commands Available- {lengthofhelp}
Github: [TheUserver](https://www.github.com/r0ld3x/Userver)
License:  [GNU Affero General Public License](https://www.github.com/r0ld3x/Userver/LICENSE")
Channel: @TheUserver || @TheUserverSupport
©[Userver](https://www.github.com/r0ld3x/Userver)
"""
    await e.edit(text,
        buttons=page_num_x(index),
    )
    



@callback(re.compile("close"), owner=True)
async def help_func(e):
    try:
        lengthofhelp = len(HELP)
        text = f"""
Hello [{USER_NAME}](tg://user?id={USER_ID})
I Am Userver The Advance MultiFunctional Userbot For My [Master](tg://user?id={USER_ID})

Total Commands Available- {lengthofhelp}
Github: [TheUserver](https://www.github.com/r0ld3x/Userver)
License:  [GNU Affero General Public License](https://www.github.com/r0ld3x/Userver/LICENSE")
Channel: @TheUserver || @TheUserverSupport
©[Userver](https://www.github.com/r0ld3x/Userver)
"""
        await e.edit(text,
        buttons=_main_help_menu,
    )
    except Exception as xe:
        pass

