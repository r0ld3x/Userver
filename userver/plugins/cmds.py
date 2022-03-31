
"""
`{i}{cmd_name}` :- **Get All Commands Link**
"""

from userver.helpers.utils import all_cmds_in_telegraph
from userver.dec import user_cmd
from . import TelegraphClient


@user_cmd(pattern='cmds$')
async def _(e):
    await all_cmds_in_telegraph(e,TelegraphClient)