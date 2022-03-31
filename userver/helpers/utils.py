import urllib.request
import re
import time
import json
from json.decoder import JSONDecodeError
import aiogram
import markdown
import aiohttp
from io import BytesIO
from userver.plugins import HELP
from carbonnow import Carbon

def ping_main(host):
    t1 = time.time()
    urllib.request.urlopen(host).read()
    return (time.time() - t1) * 1000.0


def check_ping(host):
    delay = int(ping_main(host))
    return f'`{delay} [ms]`'


def json_parser(data, indent=None):
    parsed = {}
    try:
        if isinstance(data, str):
            parsed = json.loads(str(data))
            if indent:
                parsed = json.dumps(json.loads(str(data)), indent=indent)
        elif isinstance(data, dict):
            parsed = data
            if indent:
                parsed = json.dumps(data, indent=indent)
    except JSONDecodeError:
        parsed = eval(data)
    return parsed



async def all_cmds_in_telegraph(m: object, Telegraph):
    text = ''
    for x in HELP.keys():
        text += f"PLUGNS NAME: {x}\n"
        xx = markdown.markdown(HELP[x])
        text += xx + '\n'
        text+= '\n\n'
    _ = Telegraph.create_page(title="Userver All Commands", html_content =text)
    await m.send_main(f"All Ultroid Commands : [Click Here]({_['url']})", link_preview=True)
    return _
    

async def Carbon1(code: str = None, bgcolour: str = 'rgba(120, 19, 254, 100)'):
    async with aiohttp.ClientSession() as client:
        url = f'https://carbonara-42.herokuapp.com/api/cook'
        params = {
'code': code,
'theme': 'darcula',
'backgroundColor': bgcolour,
'dropShadow':True,
'dropShadowBlurRadius': '50px',
'dropShadowOffsetY': '25px',
'fontFamily': 'ubuntu',
'widthAdjustment':True,
'windowControls':True,
        }

        _ = await client.post(url, json = params)
        data =  await _.read()
        buffer = BytesIO(data)
        buffer.name = 'userver_log.jpg'
        return buffer


async def get_carbonise(code):
    carbon = Carbon(code = code,
                background='#4a90e6',  # Optional: Hex-Color for Background
        drop_shadow=True,  # Optional: Drop Shadow on div Box
        drop_shadow_blur='68px',  # Optional: Drop Shadow Blur on div Box
        drop_shadow_offset='20px',  # Optional: Drop Shadow Offset on div Box
        export_size='4x',  # Optional: Export Size (1x, 2x, 4x)
        font_size='14px',  # Optional: Font size
        font_family='Fira Code',  # Optional: support FontFamily on carbon.now.sh
        first_line_number=1,  # Optional: Starting Line Numbers if Line Numbers Exist
        language='javascript',  # Optional: Programming Language of Choice
        line_height='133%',  # Optional: Line Height
        line_numbers=False,  # Optional: Line Numbers
        padding_horizontal='56px',  # Optional: Horizontal Padding
        padding_vertical='56px',  # Optional: Vertical Padding
        theme='Material',  # Optional: Carbon Theme
        watermark=False,  # Optional: Carbon Watermark
        width_adjustment=True,  # Optional: Width Adjustment
        window_controls=False,  # Optional: Window Controls
        window_theme='Material')  # Optional: Window Theme)
    return await carbon.save('carbon_photo')



async def get_uinfo(e): ##Ultroid
    user, data = None, None
    reply = await e.get_reply_message()
    if reply:
        user = await e.client.get_entity(reply.sender_id)
        data = e.pattern_match.group(1)
    else:
        ok = e.pattern_match.group(1).split(maxsplit=1)
        if len(ok) > 1:
            data = ok[1]
        try:
            user = await e.client.get_entity(await e.client.parse_id(ok[0]))
        except IndexError:
            pass
        except ValueError as er:
            await e.send_main(str(er), time = 5)
            return None, None
    return user, data