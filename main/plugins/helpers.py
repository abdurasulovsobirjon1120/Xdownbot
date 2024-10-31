from pyrogram.errors import FloodWait, InviteHashInvalid, InviteHashExpired, UserAlreadyParticipant
from telethon import errors, events

import asyncio, subprocess, re, os, time
from pathlib import Path
from datetime import datetime as dt
from telethon import events, Button
from threading import Lock


from .. import bot as Drone, AUTH, OWNER_TAG

#leave private chat
async def leave(client, link):
    try:
        await Drone.send_message(
        entity=AUTH,
        message=f"Message for @{OWNER_TAG}\nLeave this group\n[Link]{link}\n",
        )
    except Exception as e:
        print(f"Leave this group\n`{link}`\nError : {e}")

#Join private chat-------------------------------------------------------------------------------------------------------------

async def join(client, invite_link):
    try:
        await client.join_chat(invite_link)
        return "Kanalga muvaffaqiyatli kirildi."
    except UserAlreadyParticipant:
        return "Allaqachon mavjudman."
    except (InviteHashInvalid, InviteHashExpired):
        return "Qo'shila olmadim, link eskirgan yoki xato."
    except FloodWait:
        return "Juda ko'p urinishlar, keyinroq urinib ko'ring."
    except Exception as e:
        print(e)
        return "Qo'shila olmadim, iltimos sabr qiling. Men qayta urinaman!"
    
#Regex---------------------------------------------------------------------------------------------------------------
#to get the url from event

def get_link(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)   
    try:
        link = [x[0] for x in url][0]
        if link:
            return link
        else:
            return False
    except Exception:
        return False
    
#Screenshot---------------------------------------------------------------------------------------------------------------

def hhmmss(seconds):
    x = time.strftime('%H:%M:%S',time.gmtime(seconds))
    return x

async def screenshot(video, duration, sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    time_stamp = hhmmss(int(duration)/2)
    out = dt.now().isoformat("_", "seconds") + ".jpg"
    cmd = ["ffmpeg",
           "-ss",
           f"{time_stamp}", 
           "-i",
           f"{video}",
           "-frames:v",
           "1", 
           f"{out}",
           "-y"
          ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    x = stderr.decode().strip()
    y = stdout.decode().strip()
    if os.path.isfile(out):
        return out
    else:
        None       

async def start_srb(event, st):
    await event.reply(st)
    
