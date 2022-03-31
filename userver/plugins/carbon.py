
"""
`{i}{cmd_name} text`: **Get carbonise image of given text.**.
"""

import os
from userver.helpers.utils import  Carbon1
from userver.dec import user_cmd
from telegraph import upload_file



@user_cmd(pattern='carbon( (.*)|$)')
async def _(e):
    match = e.pattern_match.group(1).strip()
    em = await e.send_main("Wait...",time = 3)
    if not match:
        if e.reply_to_msg_id:
            replied_msg = await e.get_reply_message()
            text = replied_msg.text
        else:
            text = match
    else:
        tex = e.text.split(" ",maxsplit = 1)
        text = tex[1]
    x = await Carbon1(text)
    with open('userver/images/carbon_userver.png' , 'wb') as r:
        r.write(x.read())
    if os.path.isfile('userver/images/carbon_userver.png'):
        link = upload_file('userver/images/carbon_userver.png')
        url = f"https://telegra.ph{link[0]}"
        msg = f"""
url: {url}

Text: `{text}`
"""
        await e.reply(msg, file=url)
        os.unlink('userver/images/carbon_userver.png')
    else:
        await e.send_main("Error While Capturing Image. Check Logs From Log Chat For More.", time = 5)