import inspect
import os,sys
import time
from telethon import TelegramClient
from telethon.errors import (
    AccessTokenExpiredError,
    AccessTokenInvalidError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
)
from telethon import utils as telethon_utils

from userver.helpers.logger import log,TelethonLogger
from userver.config import del_key, get_int, get_str

class UserverClient(TelegramClient):
    
    def __init__(
        self,
        session,
        api_id= None,
        api_hash = None,
        bot_token = None,
        logger = log,
        log_attempt=True,
        handle_auth_error=True, 
        *args,
        **kwargs,
    ):
        self._cache = {}
        self._dialogs = []
        self._handle_error = handle_auth_error
        self._log_at = log_attempt
        self.logger = logger
        kwargs["api_id"] = api_id or get_int("API_ID")
        kwargs["api_hash"] = api_hash or get_str("API_HASH")
        kwargs["base_logger"] = TelethonLogger
        super().__init__(session, **kwargs)
        
        try:
            self.run_in_loop(self.start_client(bot_token=bot_token))
        except ValueError as valerr:
            log.exception(valerr)
            super().__init__(session, **kwargs)
            self.run_in_loop(self.start_client(bot_token=bot_token))
            
        self.dc_id = self.session.dc_id
            
    
    @property
    def __dict__(self):
        if self.me:
            return self.me.to_dict()
    
    
    async def start_client(self, **kwargs):
        log.info("Starting Client")
        
        try:
            await self.start(**kwargs)
        except (AuthKeyDuplicatedError, EOFError) as er:
            if self._handle_error:
                self.logger.error("String session expired. Create new!")
                return sys.exit()
            raise er
        except AccessTokenExpiredError or AccessTokenInvalidError:
            # AccessTokenError can only occur for Bot account
            # And at Early Process, Its saved in Redis.
            del_key("BOT_TOKEN")
            self.logger.error(
                "Bot token expired or Revoked. Create new from @Botfather and add in BOT_TOKEN env variable!"
            )
            sys.exit()
        except Exception as e:
            self.logger.error(e)
            sys.exit()
        
        
        self.me = await self.get_me()
        if not self.me.bot:
            setattr(self.me, "phone", None)
            me = self.full_name
            log.info("Logged in as {}".format(me))
    
    
    def run(self):
        """run asyncio loop"""
        self.run_until_disconnected()
    
    def add_handler(self, func, *args, **kwargs):
        """Add new event handler, ignoring if exists"""
        for f_, _ in self.list_event_handlers():
            if f_ == func:
                return
        self.add_event_handler(func, *args, **kwargs)
    
    def run_in_loop(self, function):
        """run inside asyncio loop"""
        return self.loop.run_until_complete(function)
    
    @property
    def utils(self):
        return telethon_utils
    
    @property
    def full_name(self):
        """full name of Client"""
        return self.utils.get_display_name(self.me)
    
    @property
    def uid(self):
        """Client's user id"""
        return self.me.id
    
    @property
    def username(self):
        """Client's user id"""
        return self.me.username

    def to_dict(self):
        return dict(inspect.getmembers(self))
    
    async def parse_id(self, text):
        try:
            text = int(text)
        except ValueError:
            pass
        return await self.get_peer_id(text)