"""
`{i}{cmd_name}`  :- **Ping Userbot.**
"""

import time

from userver.strings.lang import get_string, get_strings
from userver.dec import user_cmd
from userver import PIC, adb, start_time, USER_ID, USER_NAME, __version__
from userver.helpers.locals import send_main, time_formatter, send
from userver.helpers.utils import check_ping



@user_cmd(pattern='ping$')
async def _(e):
    x = check_ping('https://www.google.com') or "0.0"
    await e.send_main(x, parse_mode = 'md')
