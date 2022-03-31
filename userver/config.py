import yaml
import os
from envparse import env
from userver.helpers.locals import where_hosted
from userver.helpers.logger import log
from typing import Any


DEFAULTS = {}

where = where_hosted()
if where == "local":
    if os.name == 'nt':
        PATH = os.getcwd() + '\config.yaml'
        log.info("Using Windows Vars.")
    else:
        PATH = os.getcwd() + '/config.yaml'
        log.info("Using Linux Vars.")

    with open(PATH) as buffer:
        data = yaml.load(buffer, Loader= yaml.FullLoader)
        log.info("Adding {} vars from {}".format(len(data), PATH))
        for x in data:
            DEFAULTS[x.upper()] = data[x]



def set_key(key: Any, value: Any, check = False) -> Any:
    if check and key in DEFAULTS:
        return DEFAULTS[key]
    else:
        DEFAULTS[key.upper()] = value


def del_key(key: Any) -> Any:
    if key in DEFAULTS:
        del DEFAULTS[key.upper()]


def get_int(name, req = True):
    default = DEFAULTS[name] if name in DEFAULTS else None
    data = env.int(name, default = default)
    if data and req:
        return data
    elif not data and req:
        return None
    elif not data and not req:
        log.warn("No Var found: {}".format(name))
        exit()
    else: return  data



def get_str(name, req = True):
    default = DEFAULTS[name] if name in DEFAULTS else None
    data = env.str(name, default = default)
    if data and req:
        return data
    elif not data and req:
        # log.warn("No Var found: {}".format(name))
        return None
    elif not data and not req:
        log.warn("No Var found: {}".format(name))
        exit()
    else: return  data

def get_bool(name, req = True):
    default = DEFAULTS[name] if name in DEFAULTS else None
    data = env.bool(name, default = default)
    if data and req:
        return data
    elif not data and req:
        # log.warn("No Var found: {}".format(name))
        return None
    elif not data and not req:
        log.warn("No Var found: {}".format(name))
        exit()
    else: return  data



def get_list(name, req = True):
    default = DEFAULTS[name] if name in DEFAULTS else None
    data = env.list(name, default = default)
    if data and req:
        return data
    elif not data and req:
        # log.warn("No Var found: {}".format(name))
        return None
    elif not data and not req:
        log.warn("No Var found: {}".format(name))
        exit()
    else: return  data

if red:= get_str("REDIS_URI"):
    if ':' in red:
        uri, port = red.split(':')
        set_key("REDIS_URI", uri)
        set_key("REDIS_PORT", port)