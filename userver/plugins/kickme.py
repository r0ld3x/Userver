"""
`{i}{cmd_name} ` :- **Leave Chat**
"""

import time
from telethon.tl.functions.channels import LeaveChannelRequest

from userver.strings.lang import get_string, get_strings
from userver.dec import user_cmd
from userver import start_time, USER_ID, USER_NAME, __version__
from userver.helpers.locals import send_main, time_formatter, send
from userver.helpers.utils import check_ping, json_parser



@user_cmd(pattern='kickme( (.*)|$)')
async def _(e):
    try:
        await e.client(LeaveChannelRequest(e.chat_id))
    except :
        await e.send_main("Error While Leaving. Make Sure this is not a private group/channel.")
    else:
        await e.send_main(f'I [{USER_NAME}](tg://user?id={USER_ID}) Leaved This Chat. By By!!')
    