import os,sys
from telethon.tl.types import Message

from userver.helpers.locals import delete_message, send, send_main, where_hosted



HOSTED_ON = where_hosted()
setattr(Message, "send_main", send_main)
setattr(Message, "try_delete", delete_message)