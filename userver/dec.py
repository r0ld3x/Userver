import inspect
from io import BytesIO
import platform
import re
import sys
from time import gmtime, strftime
from traceback import format_exc
from telethon import Button, events, __version__ as tele_version
from telethon.errors.rpcerrorlist import *
from telethon.events import CallbackQuery, InlineQuery, NewMessage
from telethon.utils import get_display_name
from asyncio import sleep
from telethon.tl.types import InputWebDocument


from userver.config import get_str, get_int, get_list
from userver.helpers.locals import send, send_main
from userver.helpers.logger import log
from userver.plugins import OWNER_ID, OWNER_NAME
from . import HOSTED_ON, PIC, USER_ID, USER_NAME, USERNAME, u_bot,HANDLER,asst,LOG_CHAT, __version__
from telethon.errors.common import *


IN_BTTS = [
    [
        Button.url(
            "Repository",
            url="https://github.com/r0ld3x/Userver",
        ),
        Button.url("Support", url="https://t.me/TheUserver"),
    ]
]



def compile_pattern(data, hndlr):
    if data.startswith("^"):
        data = data[1:]
    if data.startswith("."):
        data = data[1:]
    if hndlr in [" ", "NO_HNDLR"]:
        # No Hndlr Feature
        return re.compile("^" + data)
    return re.compile("\\" + hndlr + data)




def user_cmd(pattern = None,*args, **kwargs):
    groups_only = kwargs.get("groups_only", False)
    admins_only = kwargs.get("admins_only", False)
    funcc = kwargs.get("func", lambda e: not e.via_bot_id)
    if not pattern:
        log.critical("Not Pattern Found.")
        exit()
    r_pattern = HANDLER or "."
    
    def innner_dec(dec):
        async def wrap(m):
            chat = m.chat
            if groups_only and not m.is_private:
                return await send(m, "`Use this in Group or Channel.`")
            if admins_only:
                if m.is_private: return await send(m, "`Use this in Group or Channel.`")
                if not (chat.admin_rights or chat.creator):
                    return await send(m, "`I am not an admin here.`")
            try:
                await dec(m)
            except FloodWaitError  as f:
                await asst.send_message(LOG_CHAT, f"I have to sleep for {f.seconds + 5}s")
                await u_bot.disconnect()
                await sleep(f.seconds + 10)
                await u_bot.connect()
                await asst.send_message(LOG_CHAT, f"I Working Again After {f.seconds + 5}s Later.")
                return
            except AlreadyInConversationError:
                return await send(m,"Conversation Is Already On, Kindly Wait Sometime Then Try Again.")
            except AuthKeyDuplicatedError as au:
                await asst.send_message(LOG_CHAT, f"Session Dublicated. Make new Session.")
                exit()
            except events.StopPropagation:
                    raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except Exception as e:
                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                name = get_display_name(chat)
                ftext = f"""
**Userver Error**
__Python version__: {platform.python_version()}
__Userver Version__: {__version__}
__Telethon Version__: {tele_version}
__Hosted At__: {HOSTED_ON}
__Owner__: [{OWNER_NAME}](tg://user?id={OWNER_ID})
**---------- LOGS ----------**
__DATE__: {date}
__Chat__: {name} - `{m.chat_id}`
__Sender Id__: `{m.sender_id}`
__Event Trigger__: `{m.text}`
__Error Message__: `{str(sys.exc_info()[1])}`
**---------- Traceback Info ----------**
`{format_exc()}`
"""

                if len(ftext) > 4096:
                    with BytesIO(ftext.encode()) as file:
                        file.name = "logs.txt"
                        error_log = await asst.send_file(LOG_CHAT,
                            file,
                            caption=f"**Userver Error**.\n **Date**: `{date}`\n**Event Trigger**: {m.text}**",
                        )
                else:
                    error_log = await asst.send_message(LOG_CHAT,ftext, parse_mode = 'md')
                    return error_log
        cmd = compile_pattern(pattern, r_pattern)
        u_bot.add_event_handler(
            wrap,
            NewMessage(
                pattern = cmd,
                incoming= True,
                forwards= False,
                func = funcc,
                outgoing=True
                
            )
        )
        return wrap
    return innner_dec






def callback(data=None, from_users=[], owner=False, **kwargs):
    """Assistant's callback decorator"""
    if "me" in from_users:
        from_users.remove("me")
        from_users.append(u_bot.uid)

    def ultr(func):
        async def wrapper(event):
            if from_users and event.sender_id not in from_users:
                return await event.answer("Not for You!", alert=True)
            elif owner and event.sender_id != USER_ID:
                return await event.answer(f"This is {USER_ID}'s bot!!")
            try:
                await func(event)
            except Exception as er:
                log.exception(er)

        asst.add_event_handler(wrapper, CallbackQuery(data=data, **kwargs))

    return ultr



def asst_cmd(pattern=None, load=None, owner=False, **kwargs):
    """Decorator for assistant's command"""
    name = inspect.stack()[1].filename.split("/")[-1].replace(".py", "")
    kwargs["forwards"] = False

    def ult(func):
        if pattern:
            kwargs["pattern"] = re.compile("^/" + pattern)
        asst.add_event_handler(func, NewMessage(**kwargs))
    return ult




def in_pattern(pattern=None, owner=False, **kwargs):
    """Assistant's inline decorator."""

    def don(func):
        async def wrapper(event):
            if owner and event.sender_id != USER_ID:
                MSG = f"""
**Userver UserBot**
➖➖➖➖➖➖➖➖➖➖
**Owner**: [{USER_NAME}](tg://user?id={u_bot.uid})
**Support**: @TheUserver
➖➖➖➖➖➖➖➖➖➖
"""
                res = [
                    await event.builder.article(
                        title="Userver Userbot",
                        url="https://t.me/TheUserver",
                        description="(c) Userver",
                        text=MSG,
                        thumb=InputWebDocument(
                            PIC,
                            0,
                            "image/jpeg",
                            [],
                        ),
                        buttons=IN_BTTS,
                    )
                ]
                return await event.answer(
                    res,
                    switch_pm=f"Userver Assistant of @{USERNAME}",
                    switch_pm_param="start",
                )
            try:
                await func(event)
            except Exception as er:
                log.exception(er)
            return wrapper

        asst.add_event_handler(wrapper, InlineQuery(pattern=pattern, **kwargs))

    return don
