import os
from telegraph import Telegraph

from userver import u_bot, rdb as adb
from userver.helpers.logger import log

class UserverGraph(Telegraph):
    
    def __init__(self, u_bot, adb, access_token=None):
        super().__init__(access_token)
        self.adb = adb
        self.u_bot = u_bot
        
        
    async def create_token(self, *args, **kwargs):
        author_url = f'https://t.me/{self.u_bot.username}'
        _ = await self.create_account(
            self.u_bot.username if self.u_bot.username else 'Userver',
            author_name= self.u_bot.username,
            author_url= author_url, 
            *args, **kwargs
        )
        return _
    
    async def post(self,  *args, **kwargs):
        _ = await self.create_page(*args, **kwargs)
        return _
    
    async def up(self,file= None, *args,**kwargs):
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} not found to upload.")
        _ = await self.upload_file(file, *args, **kwargs)
        return _







def userver_graph():
    token = adb.get_key("TELEGRAPH_TOKEN") or None
    
    if token:
        return Telegraph(token)
    author_url = f'https://t.me/{u_bot.username}'
    try:
        _ = Telegraph.create_account(
            author_name= u_bot.full_name,
            author_url= author_url,
            short_name=u_bot.full_name[:10]
        )
    except:
        try:
            _ = Telegraph.create_account(
            author_name= 'Userver',
            author_url= author_url,
            short_name= 'userver'
        )
        except Exception as e:
            log.critical(e)
            return False
        else:
            adb.set_key("TELEGRAPH_TOKEN", Telegraph.get_access_token())
            return Telegraph(adb.get_key("TELEGRAPH_TOKEN") or None)
    else:
        adb.set_key("TELEGRAPH_TOKEN", Telegraph.get_access_token())
        return Telegraph(adb.get_key("TELEGRAPH_TOKEN") or None)