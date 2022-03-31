import os, sys
from telethon.sessions import StringSession
from telethon.tl.types import MessageService
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from asyncio import sleep

from .logger import log
from userver.config import get_str


def where_hosted() -> str:
    if os.getenv("DYNO"):
        return "heroku"
    if os.getenv("RAILWAY_STATIC_URL"):
        return "railway"
    if os.getenv("KUBERNETES_PORT"):
        return "qovery"
    if os.getenv("WINDOW") and os.getenv("WINDOW") != "0":
        return "windows"
    if os.getenv("RUNNER_USER") or os.getenv("HOSTNAME"):
        return "github actions"
    if os.getenv("ANDROID_ROOT"):
        return "termux"
    return "local"



def session_file():
    _ = get_str("SESSION", True)
    if _:
        if len(_) != 353:
            log.error("invalid Session Id.")
            sys.exit()
        else:
            return StringSession(_)
    else:
        log.error("No string session found.")
        sys.exit()

async def send_main(m: object, text: int| str = None,**kwargs):
    time = kwargs.get("time", None)
    edit_time = kwargs.get("edit_time", None)
    if time:
        del kwargs['time']
    if edit_time:
        del kwargs['edit_time']
    if "link_preview" not in kwargs:
        kwargs.update({"link_preview": False})
    if m.out and not isinstance(m, MessageService):
        if edit_time:
            await sleep(edit_time)
        ok = await m.edit(text, **kwargs)
    else:
        kwargs["reply_to"] = m.reply_to_msg_id or m
        ok = await m.client.send_message(m.chat_id, text, **kwargs)
    if time or not time:
        await sleep(time or 5)
        return await ok.delete()
    return ok


async def send(m: object, text: str = None, **kwargs):
    kwargs["time"] = kwargs.get("time", 7)
    return await send_main(m, text, **kwargs)


def time_formatter(milliseconds):
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if not tmp:
        return "0 s"

    if tmp.endswith(":"):
        return tmp[:-1]
    return tmp



async def delete_message(e):
    try:
        await e.delete()
    except MessageDeleteForbiddenError:
        pass
    except BaseException as er:
        log.exception(er)




def mediainfo(media):
    xx = str((str(media)).split("(", maxsplit=1)[0])
    m = ""
    if xx == "MessageMediaDocument":
        mim = media.document.mime_type
        if mim == "application/x-tgsticker":
            m = "sticker animated"
        elif "image" in mim:
            if mim == "image/webp":
                m = "sticker"
            elif mim == "image/gif":
                m = "gif as doc"
            else:
                m = "pic as doc"
        elif "video" in mim:
            if "DocumentAttributeAnimated" in str(media):
                m = "gif"
            elif "DocumentAttributeVideo" in str(media):
                i = str(media.document.attributes[0])
                if "supports_streaming=True" in i:
                    m = "video"
                m = "video as doc"
            else:
                m = "video"
        elif "audio" in mim:
            m = "audio"
        else:
            m = "document"
    elif xx == "MessageMediaPhoto":
        m = "pic"
    elif xx == "MessageMediaWebPage":
        m = "web"
    return m
