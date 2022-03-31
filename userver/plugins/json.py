"""
`{i}{cmd_name}` | `{i}json  <reply to message>` :- **Get Serialize Of Message..**
"""
import time
import io

from userver.strings.lang import get_string, get_strings
from userver.dec import user_cmd
from userver import PIC, adb, start_time, USER_ID, USER_NAME, __version__
from userver.helpers.locals import send_main, time_formatter, send
from userver.helpers.utils import check_ping, json_parser



@user_cmd(pattern='json( (.*)|$)')
async def _(e):
    match = e.pattern_match.group(1).strip()
    if e.reply_to_msg_id:
        reply_to_msg_id = e.reply_to_msg_id
        msg = await e.get_reply_message()
    else:
        msg = e
        reply_to_msg_id = msg.message.id
    
    text = json_parser(msg.to_json(), indent = 2)
    if len(text) > 4096:
        with io.BytesIO(str.encode(text)) as data:
            data.name = f'json_{reply_to_msg_id}.json'
            await e.client.send_file(
                e.chat_id,
                data,
                force_document=True,
                allow_cache=False,
                reply_to=reply_to_msg_id,
            )
            await e.delete()
    else:
        await e.send_main(text)
    