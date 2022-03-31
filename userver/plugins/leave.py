"""
`{i}{cmd_name} ` :- **Leave Chat**
"""

from telethon.tl.functions.channels import LeaveChannelRequest

from userver.dec import user_cmd
from userver import start_time, USER_ID, USER_NAME, __version__



@user_cmd(pattern='leave( (.*)|$)')
async def _(e):
    try:
        await e.client(LeaveChannelRequest(e.chat_id))
    except :
        await e.send_main("Error While Leaving. Leave Manually")
    else:
        await e.send_main(f'I [{USER_NAME}](tg://user?id={USER_ID}) Leaved This Chat. By By!!')
    