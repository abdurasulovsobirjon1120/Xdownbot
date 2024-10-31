import time, os

from .. import bot as Drone
from .. import userbot, Bot
from main.plugins.pyroplug import get_msg
from main.plugins.helpers import get_link, join, leave

from telethon import events, Button
from pyrogram.errors import FloodWait
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

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
message = "Iltimos menga saqlab olmoqchi bolgan post linkini yuboring..."

buttons = [
    [Button.url("Kanal", url="https://t.me/ixvauz")],
]

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.text == message:
            return
    try:
        link = get_link(event.text)
        if not link:
            return
    except TypeError:
        return
    
    s, r = await force_sub(event.client, "ixvauz", event.sender_id, ft)
    if s == True:
        await event.reply(r, buttons=buttons)
        return
    edit = await event.reply("Tayyorlanmoqda!")
    try:
        if 't.me/+' in link:
            q = await join(userbot, link)
            await edit.edit(q)
            if 'successfully' in q.lower():
                await Drone.send_message(event.sender_id, "Siz bergan linkga muvaffaqiyatli qo'shildim, menga post linkini yuboring...")
                return
            elif 'already' in q.lower():
                await Drone.send_message(event.sender_id, "Siz bergan linkga muvaffaqiyatli qo'shildim, menga post linkini yuboring...")
                return
            elif 'expired' in q.lower():
                await Drone.send_message(event.sender_id, "Ushbu link eskirgan yoki noto'g'ri")
                return
            elif 'Too' in q.lower():
                await Drone.send_message(event.sender_id, "Birozdan so'ng qayta urining")
                return
            elif 'manually' in q.lower():
                await Drone.send_message(event.sender_id, "Meningcha ushbu kanal so'rovli kanal, men unga so'rov yubordim.")
                return
        if 't.me/' in link:
            await get_msg(userbot, Bot, Drone, event.sender_id, edit.id, link, 0)
            q = await leave(userbot, link)
    except FloodWait as fw:
        return await Drone.send_message(event.sender_id, f"Iltimos {fw.x} soniyadan so'ng qayta urining!")
    except Exception as e:
        try:
            print(e)
            if "int" in e.lower():
                q = await join(userbot, link)
                await edit.edit(q)
                if 'successfully' in q.lower():  
                    await Drone.send_message(event.sender_id, "Siz bergan linkga muvaffaqiyatli qo'shildim, menga post linkini yuboring...")
                return
        except Exception as e:
            print(e)
            await Drone.send_message(event.sender_id, f"`{link}` ushbu postni yuklab olishda qanaqadir muammoga duch keldim: \n\n**Error:** {e}")
    
    