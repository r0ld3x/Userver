
"""
`{i}{cmd_name}` :- **Away From Keyboard**
"""

from datetime import datetime as dt
import os
import time
from telegraph import upload_file
from telethon.events import NewMessage

from userver import asst
from userver.dec import user_cmd
from userver import LOG_CHAT, rdb, u_bot
from userver.helpers.locals import mediainfo


def is_afk():
    data = rdb.get_key("IS_AFK")
    if data:
        start_time = dt.strptime(data[3], "%b %d %Y %I:%M:%S%p")
        afk_since = str(dt.now().replace(microsecond=0) - start_time)
        return data[0], data[1], data[2],afk_since
    else:
        return False


def add_afk(reason, media_type, media):
    time = dt.now().strftime("%b %d %Y %I:%M:%S%p")
    x = rdb.set_key("IS_AFK", [reason , media_type, media,time])
    return x


@user_cmd(pattern='afk( (.*)|$)')
async def _(e):
    if is_afk():
        return
    reason, media_type , url = None,None, None
    if match:=  e.pattern_match.group(1).strip():
        reason = match
    if e.reply_to_msg_id:
        replied_msg = await e.get_reply_message()
        if not reason and replied_msg.text:
            reason = replied_msg.text
        if replied_msg.media:
            media_type = mediainfo(replied_msg.media)
            if media_type.startswith(('pic', 'gif')):
                file = await u_bot.download_media(replied_msg.media)
                up = upload_file(file)
                url = f"https://telegra.ph{up[0]}"
                os.unlink(file)
            else:
                url = replied_msg.file.id
    if add_afk(reason, media_type , url):
        u_bot.add_handler(remove_afk, NewMessage(outgoing= True))
        u_bot.add_handler(on_afk, NewMessage(incoming= True, func=lambda e: bool(e.mentioned or e.is_private)))
        await e.send_main("Done", time = 5)
    else:
        await e.send_main("Error", time = 5)


async def remove_afk(e):

    if "afk" in e.text.lower():
        return
    if _:= is_afk():
        rdb.del_key("IS_AFK")
        await e.send_main("You Was Afk For {}".format(_[3]), time = 5)
        await asst.send_message(LOG_CHAT, "You Was Afk For {}".format(_[3]))



async def on_afk(e):
    if not is_afk():
        return
    sender = await e.get_sender()
    if sender.bot or sender.verified:
        return
    reason , media_type, media,time = is_afk()
    reas = f"Beacause Of `{reason}`" if len(reason) > 1 else "Without Any Reason."
    text = f"""
Soory [{sender.first_name}](tg://user?id={sender.id})
I Am Afk Since {time}.
{reas}"""
    if media and media_type:
        await e.send_main(text, file = media, time = 5)
    else:
        await e.send_main(text, time = 5)
