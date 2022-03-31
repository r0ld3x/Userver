
"""
`{i}{cmd_name}`: **Get logs File**.
`{i}{cmd_name} carbon` | `{i}{cmd_name} c`: **Get Last 10 lines Carbonised Logs. (image)**
`{i}{cmd_name} open` | `{i}{cmd_name} o`:- **Send Last 10 Logs In Chat.**
"""

from userver.helpers.utils import Carbon1
from userver.dec import user_cmd


@user_cmd(pattern='logs( (.*)|$)')
async def _(e):
    match = e.pattern_match.group(1).strip()
    if match in ['c', 'carbon']:
        log_file = open('userver.log', 'r')
        text = ''
        for line in log_file.readlines()[-10:]:
            text += line + '\n'
        x = await Carbon1(text)
        await e.reply(
            f"last 10 Lines Carbonised logs",
            file=x,
        )
    elif match in ['o', 'open']:
        log_file = open('userver.log', 'r')
        text = ''
        for line in log_file.readlines()[-20:]:
            text += line + '\n'
        await e.reply(
            f"**LOGS OF USERVER**:\n`{text}`"
        )
    else:
        await e.reply(file = 'userver.log')