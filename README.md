
# Userver

A Simple Userbot For Telegram made With Python And Telethon.


## Table of contents

* [General info](#general-info)   
* [Deployment](#deployment)
* [Setup](#setup)
* [Authors](#Authors)
* [Support](#Support)
* [License](#License)
* [Credits](#Credits)


## Deployment
* [Heroku](#Deploy-to-Heroku) (`Soon`)
* [Local Machine](#Deploy-Locally)


## Necessary Variables
- `API_ID` -You api id, from my.telegram.org or [ScrapperRoBot](https://t.dog/ScrapperRoBot).
- `API_HASH` - You api hash, from my.telegram.org or [ScrapperRoBot](https://t.dog/ScrapperRoBot).
- `SESSION` - SessionString for your accounts login session. Get it from [here](#Session-String)
- `BOT_TOKEN` - Make from [Botfather](https://t.dog/botfather)

One of the following database:
- For **Redis** (tutorial [here](#Tutorial-To-Get-Redis-DB-URL-and-Password))
  - `REDIS_URI` - Redis endpoint URL, from [redislabs](http://redislabs.com/).
  - `REDIS_PASS` - Redis endpoint Password, from [redislabs](http://redislabs.com/).


<!-- ## Deploy to Heroku
Get the [Necessary Variables](#Necessary-Variables) and then click the button below!  

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/r0ld3x/Userver)
 -->

## Deploy Locally
- Get your [Necessary Variables](#Necessary-Variables)
- Clone the repository:    
`git clone https://github.com/r0ld3x/Userver.git`
- Go to the cloned folder:
`cd Userver`
- Create a virtual env:      
`python3 -m virtualenv env` (linux)
`virtualenv env` (windows)
- Activate Virtual Env
`source env/bin/activate`
- Install Requirements
`pip install -U -r requirements.txt`                                                                                                             
- Fill your details in a config.yaml file, as given in config.yaml.sample. (You can either edit and rename the file or make a new file named config.yaml.)
- Run the bot:
    - `bash start.sh` (linux)
    - `.\start.bat` (windows)



## Session String
Different ways to get your `SESSION`:
* [![Run on Repl.it](https://replit.com/@r0ld3x/userver-session-generator)](https://replit.com/@r0ld3x/userver-session-generator)
* TelegramBot : [@SessionGeneratorBot](https://t.me/SessionGeneratorBot)
* `python ses_gen.py`



## Tutorial To Get Redis DB URL and Password
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

#### Process For Creating DB :- 
- Go To [Redis.com](Https://redis.com) and click "`Try Free`" in Top Right Corner.   
- Fill All The Required Details Like email, first and last name, password, etc.   
- Tick Below "I agree the corresponding...Privacy Policy." and Click "Get Started".   
- Now Check Your Email, and click the "Activate Now" sent by redislabs via email.   
- Now Login and Chose Free Plan in "Fixed Size" Area and Write any name in "Subscription Area".   
- On the Next Page Write Database Name and click Activate.   
   
> Congrats! Your DB has been created 🥳   


#### Process For Getting DB Credentials:-   
- Wait 5 mins after DB creation.   
- Then There Would Be 2 Things Named "`Endpoint`" and "`Access Control & Security`".   
- Copy Both Of Them and Paste Endpoint url in `REDIS_URI` and "Access ...Security" in `REDIS_PASS`.   




# Authors

- [@r0ld3x](https://www.github.com/r0ld3x)


## Support

* For support
    - [Telgram Support](https://t.me/TheUserver)
    - [Dev](https://t.me/r0ld3x)


# License
[![License](https://www.gnu.org/graphics/gplv3-127x51.png)](LICENSE)   

Userver is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.


---
# Credits

* [UltroidDevs](https://github.com/TeamUltroid/Ultroid/)
* [Lonami](https://github.com/LonamiWebs/) for [Telethon.](https://github.com/LonamiWebs/Telethon)

---



> Made with 💕 by [@r0ld3x](https://t.me/r0ld3x).    
