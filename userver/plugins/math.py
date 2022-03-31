
"""
`{i}{cmd_name}`: **Get evaluated value**.
`{i}{cmd_name} expression` | `{i}{cmd_name} 5 + 10`: **get division, multiplication, addition, substraction **
"""

from userver import HANDLER
from userver.helpers.utils import Carbon1
from userver.dec import user_cmd



@user_cmd(pattern='math( (.*)|$)')
async def _(e):
    match = e.pattern_match.group(1)
    if not match: await e.reply(f"your data is empty. ex: `{HANDLER}math 5 + 10`")
    x = eval(match)
    await e.send_main(f'`{match}` = `{x}`', time = 5)
