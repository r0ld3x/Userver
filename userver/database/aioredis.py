import sys,os
from aioredis import Redis as aior
# from redis import Redis
from userver.helpers.locals import where_hosted

# from userver.config import get_int,get_str
from userver.helpers.logger import log




class UserverAioRedis(aior):

    def __init__(self,
        host: str,
        port :int = None,
        encoding :str = 'utf-8',
        logger=log,
        platform: str = where_hosted(),
        decode: bool = True,
        password: str | None = None,
        socket_connect_timeout: int = 20,
        socket_timeout: int = 20,
        *args,
        **kwargs):
        if ':' in host:
            data = host.split(':')
            host = data[0]
            port = int(data[1])
        if host.startswith("http"):
            logger.error("Your REDIS_URI should not start with http !")
            sys.exit()
        elif not host or not port:
            logger.error("Port Number not found")
            sys.exit()
        kwargs["host"] = host
        kwargs["password"] = password or ''
        kwargs["port"] = port
        kwargs['encoding'] = encoding
        kwargs['decode_responses'] = decode
        kwargs['client_name'] = 'userver'
        kwargs['socket_connect_timeout'] = socket_connect_timeout
        kwargs['socket_timeout'] = socket_timeout
        if platform.lower() == "qovery" and not host:
            var, hash_, host, password = "", "", "", ""
            for vars_ in os.environ:
                if vars_.startswith("QOVERY_REDIS_") and vars.endswith("_HOST"):
                    var = vars_
            if var:
                hash_ = var.split("_", maxsplit=2)[1].split("_")[0]
            if hash:
                kwargs["host"] = os.environ(f"QOVERY_REDIS_{hash_}_HOST")
                kwargs["port"] = os.environ(f"QOVERY_REDIS_{hash_}_PORT")
                kwargs["password"] = os.environ(f"QOVERY_REDIS_{hash_}_PASSWORD")
        try:
            super().__init__(**kwargs)
        except Exception as ex:
            log.exception("Error while connecting to redis.: ",ex)
            exit()
        
    async def re_cache(self):
        self._cache = {}
        for keys in self.keys():
            self._cache.update({keys:await self.get_key(keys)})

    async def get_key(self,key):
        _ = await self.get(key)
        if _:
            try:
                _ = eval(_)
            except:
                pass
        return _

    async def set_key(self, key ,value, **kwargs):
        try:
            value = eval(value)
        except:
            pass
        return await self.set(key, value)
    
    
    @property
    async def get_db(self):
        x = await self.info('keyspace')
        data = []
        for a in x:
            data.append(a)
        return data

    async def del_key(self,key):
        return await self.delete(key)