import os
from .. import bot as Drone
from telethon import events, Button
from .database import Database
S = '/' + 's' + 't' + 'a' + 'r' + 't'
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest


db = Database()
async def start_srb(event, st):
    buttons = [
        [Button.url("Yangiliklar", url="https://t.me/yaxshi_jiyan")],
    ]
    await Drone.send_file(event.chat.id, file="https://telegra.ph/file/801289ebfeadd84e08578.jpg", caption=st, buttons=buttons)
                                                 

async def force_sub(client, channel, id, ft):
    s, r = False, None
    try:
        x = await client(GetParticipantRequest(channel=channel, participant=int(id)))
        left = x.stringify()
        if 'left' in left:
            s, r = True, f"{ft}"
        else:
            s, r = False, None
    except UserNotParticipantError:
        s, r = True, f"Botdan foydalanish uchun avval @ixvauz kanaliga obuna bo'ling."
    except Exception:
        s, r = True, "Afsuski kanal to'gri sozlanmadi."
    return s, r

ft = "Botdan foydalanish uchun avval @ixvauz kanaliga obuna bo'ling."

cbutton = [
    [Button.url("Kanal", url="https://t.me/ixvauz")],
]

@Drone.on(events.NewMessage(incoming=True, pattern=f"{S}"))
async def start(event):
    if db.get_user(event.sender_id) is None:
        db.add_user(event.sender_id)
    s, r = await force_sub(event.client, "ixvauz", event.sender_id, ft)
    if s == True:
        await event.reply(r, buttons=cbutton)
        return
    text = """
🇺🇿👋 Salom, men kontent saqlash taqiqlangan kanallardan postlarni linki orqali yuklab bera olaman!
Agar kanal shaxsiy bo'lsa, taklif havolasini yuboring!

🇺🇸 Hello I can help you to download any content from restricted channels, just send me post link and thats it!
If channel is private, firstly send me invite link!

🇷🇺 Привет я могу помочь тебе скачать любой контент с ограниченных каналов, просто пришли мне ссылку на публикацию и все!
Если канал частный, пришлите мне ссылку-приглашение!"""
    await start_srb(event, text)