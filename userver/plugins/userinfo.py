"""
`{i}{cmd_name} ` | `{i}user_info <username> or <user_id>`  :- **get user info**
"""

import os
import time
import calendar
from datetime import datetime
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import GetUserPhotosRequest


from userver.strings.lang import get_string, get_strings
from userver.dec import user_cmd
from userver import start_time, USER_ID, USER_NAME, __version__, u_bot
from userver.helpers.locals import send_main, time_formatter, send
from userver.helpers.utils import check_ping, json_parser



@user_cmd(pattern='userinfo( (.*)|$)')
async def _(e):
    match = e.pattern_match.group(1).strip()
    if 'bot' in match: await e.send_main("I Doesn't Support Bot Info Now.")
    if match and not 'bot' in  match:
        full = await e.client(GetFullUserRequest(match))
        x = await u_bot.download_profile_photo(match, file = f'userver/images/user_image_{match}.jpg')
        text = f"""
User Info:-
User: [{full.user.first_name} + ' ' + {full.user.last_name or ''}](@{full.user.username})
User ID: `{full.user.id}`
Contact: `{full.user.contact}`
Mutual Contact: `{full.user.mutual_contact}`
Bot: {full.user.bot}
Restricted: {full.user.restricted}
Scam: {full.user.scam}
Phone: {'`sent in log chat`' if full.user.phone else '`not found`'}
Can Pin Messages: {full.can_pin_message}
About: `{full.about}`
Blocked: {full.blocked}
I Seen Him In {full.common_chats_count} Chats.
""" 
        if x:
            await e.reply(text, file = f'userver/images/user_image_{match}.jpg')
            os.unlink(f'userver/images/user_image_{match}.jpg')
        else:
            await e.reply(text)
        if full.user.phone:
            await e.send_main(f"Number Of [{full.user.first_name}](@{full.user.username}) is `{full.user.phone}`")
        # print(full)
#     else:
#         full = await e.client(GetFullUserRequest(match))
#         x = await u_bot.download_profile_photo(match, file = f'userver/images/user_image_{match}.jpg')
#         text = f"""
# User Info:-
# User: [{full.user.first_name} + ' ' + {full.user.last_name or ''}](@{full.user.username})
# User ID: `{full.user.id}`
# Contact: `{full.user.contact}`
# Mutual Contact: `{full.user.mutual_contact}`
# Bot: {full.user.bot}
# Restricted: {full.user.restricted}
# Scam: {full.user.scam}
# Phone: {'`sent in log chat`' if full.user.phone else '`not found`'}
# Can Pin Messages: {full.can_pin_message}
# About: `{full.about}`
# Blocked: {full.blocked}
# I Seen Him In {full.common_chats_count} Chats.
# """ 
#         if x:
#             await e.reply(text, file = f'userver/images/user_image_{match}.jpg')
#             os.unlink(f'userver/images/user_image_{match}.jpg')
#         else:
#             await e.reply(text)
#         if full.user.phone:
#             await e.send_main(f"Number Of [{full.user.first_name}](@{full.user.username}) is `{full.user.phone}`")
#         # print(full)