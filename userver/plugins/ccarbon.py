"""
`{i}{cmd_name} <colour name> text`: **Get carbonise image of given text. with givven backgroud colout hex or colour code**.
"""

import os
from userver.helpers.utils import  Carbon1
from userver.dec import user_cmd
from telegraph import upload_file
from userver import HANDLER
from colour import Color



@user_cmd(pattern='ccarbon( (.*)|$)')
async def _(e):
    match = e.pattern_match.group(1)
    striped = match.split(" ",maxsplit = 1)
    if not len(striped) >1:
        await e.send_main(f"Give me valid input please. for help send `{HANDLER}help ccarbon", time = 5)
        return
    hex_val = striped[0].lower()
    match = striped[1]
    if not match:
        if e.reply_to_msg_id:
            replied_msg = await e.get_reply_message()
            text = replied_msg.text
        else:
            await e.send_main(f"Give me text please. for help send `{HANDLER}help ccarbon", time = 5)
            return
    else:
        text = match
    if '#' in hex_val or 'rbg' in hex_val or 'rgba' in hex_val:
        await e.send_main(f"You Didnt Passed colour name please give me a colour name or use `{HANDLER}carbon match`. for help send `{HANDLER}help ccarbon", time = 5)
        return
    try:
        c = Color(hex_val)
        col = c.hex_l
    except Exception:
        await e.send_main(f"You Didnt Passed colour name please give me a colour name or use `{HANDLER}carbon match`. for help send `{HANDLER}help ccarbon", time = 5)
        return Exception
    x = await Carbon1(text, bgcolour = col)
    with open('userver/images/carbon_userver.jpg' , 'wb') as r:
        r.write(x.read())
    if os.path.exists('userver/images/carbon_userver.jpg'):
        link = upload_file('userver/images/carbon_userver.jpg')
        url = f"https://telegra.ph{link[0]}"
        msg = f"""
url: {url}
Colour: {hex_val}
Colour Hex: {col}
Text: `{text}`
"""
        await e.reply(msg,file='userver/images/carbon_userver.jpg')
        os.unlink('userver/images/carbon_userver.jpg')
    else:
        await e.send_main("Error While Capturing Image. Check Logs From Log Chat For More.", time = 5)