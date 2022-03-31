"""
`{i}{cmd_name} username` :- **Get Full Instagram Information From usernaem.**
ex: `{i}{cmd_name} instagram` .

`{i}{cmd_name} @username` :- **Get Full Instagram Information From Instagram @username.**
ex: `{i}{cmd_name}  @instagram` 

`{i}{cmd_name} user link` :- **Get Full Instagram Information From Instagram User Link.**
ex: `{i}{cmd_name}  https://www.instagram.com/instagram/` 

Made By `@r0ld3x`
"""

import json
import re
import time
import urllib3
from userver.config import get_str

from userver.dec import user_cmd
from userver import PIC, start_time, USER_ID, USER_NAME, __version__
from userver.helpers.locals import send_main, time_formatter, send
from userver.helpers.utils import check_ping, json_parser

regex_pattern = re.compile(
        r'^(?:https)?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'instagram' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        # r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)



def extract_hobbies(data: list):
    new_ = []
    for a in data:
        new_.append(a.pop(0))
    return new_



@user_cmd(pattern='insta( (.*))')
async def _(e):
    url = e.pattern_match.group(1).strip()
    req = urllib3.PoolManager()
    sess = get_str('INSTA_SESSIONID')
    if not sess: 
        await e.reply("ADD INSTAGRAM SESSIONID IN config file.")
        return
    head = {
'authority': 'www.instagram.com',
'method': 'GET',
'path': '/',
'scheme': 'https',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
'cache-control': 'max-age=0',
'cookie': 'sessionid={sess}',
'dnt': '1',
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
}
    if 'instagram.com' not in url:
        if '@' in url:
            username = url.replace('@','')
        else:
            username = url
        full_url = 'https://www.instagram.com/'+ username + '/?__a=1'
        result= req.request('GET',full_url, headers = head)
        if result.status != 200:
            await e.reply("Invalid Url. ex: `https://www.instagram.com/instagram`")
        else:
            try:
                data = json.loads(result.data.decode('utf-8'))
            except:
                await e.reply("Invalid Url. ex: `https://www.instagram.com/instagram`")
            else:
                user = data['graphql']['user']
                text = f"""
[@{user['username']}]({full_url.replace('/?__a=1', '')}) User Info in Instagram:
**Name**: [{user['full_name']}]({full_url.replace('/?__a=1', '')})
**Id**: `{user['id']}`
**Bio**: `{user['biography']}`
**Verified**: {user['is_verified']}
**Private**: {user['is_private']}
**Category Name**: {user['category_name']}
**Profile Pic Url**: [Click Here]({user['profile_pic_url_hd'] if 'profile_pic_url_hd' in user else 'not found'})
**professional Account**: {user['is_professional_account']}
**Business Account**: {user['is_business_account']}
**Business Category Name**: `{user['business_category_name']}`
**Business Contact Number**: `{user['business_phone_number']}`
**Business Contact Email**: `{user['business_email']}`
**Followers**: `{user['edge_followed_by']['count']}`
**Followed**: `{user['edge_follow']['count']}`
**Facebook Id**: `{user['fbid']}`
**Highlighted Reels Count**: `{user['highlight_reel_count']}`
"""
                await e.reply(
                    text,
                    file = user['profile_pic_url_hd'] if 'profile_pic_url_hd' in user else PIC,
                    force_document = True,
                    link_preview=False,
                    parse_mode = 'md'
                    
                )
    elif re.match(regex_pattern, url):
        full_url = url + '?__a=1'
        result= req.request('GET',full_url, headers = head)
        if result.status != 200:
            await e.reply("Invalid Url. ex: `https://www.instagram.com/instagram`")
        else:
            try:
                data = json.loads(result.data.decode('utf-8'))
            except:
                await e.reply("Invalid Url. ex: `https://www.instagram.com/instagram`")
            else:
                user = data['graphql']['user']
                text = f"""
[@{user['username']}]({full_url.replace('?__a=1', '')}) User Info in Instagram:
**Name**: [{user['full_name']}]({full_url.replace('?__a=1', '')})
**Id**: `{user['id']}`
**Bio**: `{user['biography']}`
**Verified**: {user['is_verified']}
**Private**: {user['is_private']}
**Category Name**: {user['category_name']}
**Profile Pic Url**: [Click Here]({user['profile_pic_url_hd'] if 'profile_pic_url_hd' in user else 'not found'})
**professional Account**: {user['is_professional_account']}
**Business Account**: {user['is_business_account']}
**Business Category Name**: `{user['business_category_name']}`
**Business Contact Number**: `{user['business_phone_number']}`
**Business Contact Email**: `{user['business_email']}`
**Followers**: `{user['edge_followed_by']['count']}`
**Followed**: `{user['edge_follow']['count']}`
**Facebook Id**: `{user['fbid']}`
**Highlighted Reels Count**: `{user['highlight_reel_count']}`
"""
                await e.reply(
                    text,
                    file = user['profile_pic_url_hd'] if 'profile_pic_url_hd' in user else PIC,
                    force_document = True,
                    link_preview=False,
                    parse_mode = 'md'
                    
                )
    else:
        await e.reply("Invalid Url. ex: `https://www.instagram.com/instagram`")