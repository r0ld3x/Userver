
"""
`{i}{cmd_name}` : **Leave Chat**

"""
import time
import calendar
from datetime import datetime
from telethon.tl.functions.channels import LeaveChannelRequest

from userver.strings.lang import get_string, get_strings
from userver.dec import user_cmd
from userver import start_time, USER_ID, USER_NAME, __version__
from userver.helpers.locals import send_main, time_formatter, send
from userver.helpers.utils import check_ping, json_parser


@user_cmd(pattern='date$')
async def _(e):
    m = datetime.now().month
    y = datetime.now().year
    d = datetime.now().strftime("Date - %B %d, %Y\nTime- %H:%M:%S")
    k = calendar.month(y, m)
    await e.send_main(f"`{k}\n\n{d}`")