import asyncio, time, os

from .. import bot as Drone
from main.plugins.progress import progress_for_pyrogram
from main.plugins.helpers import screenshot

from pyrogram import Client, filters
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.enums import MessageMediaType
from ethon.pyfunc import video_metadata
from ethon.telefunc import fast_upload
from telethon.tl.types import DocumentAttributeVideo
from telethon import events

def thumbnail(sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    else:
         return None
      
async def get_msg(userbot, client, bot, sender, edit_id, msg_link, i):
    
    """ userbot: PyrogramUserBot
    client: PyrogramBotClient
    bot: TelethonBotClient """
    
    edit = ""
    chat = ""
    round_message = False
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    msg_id = int(msg_link.split("/")[-1]) + int(i)
    height, width, duration, thumb_path = 90, 90, 0, None
    if ('t.me/c/' in msg_link) or ('t.me/b/' in msg_link):
        if 't.me/b/' in msg_link:
            chat = str(msg_link.split("/")[-2])
        else:
            chat = int('-100' + str(msg_link.split("/")[-2]))
        file = ""
        try:
            msg = await userbot.get_messages(chat, msg_id)
            if msg.media:
                if msg.media==MessageMediaType.WEB_PAGE:
                    edit = await client.edit_message_text(sender, edit_id, "Ko'chirilmoqda.")
                    await client.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    edit = await client.edit_message_text(sender, edit_id, "Ko'chirilmoqda.")
                    await client.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            edit = await client.edit_message_text(sender, edit_id, "Yuklab olishga urinyapman...")
            print("downloading")
            file = await userbot.download_media(
                msg,
                progress=progress_for_pyrogram,
                progress_args=(
                    client,
                    "**Yuklanmoqda:**\n",
                    edit,
                    time.time()
                )
            )
            print(file)
            try:
                print("uploading")
                await edit.edit('Yuborishga urinyapman!')
                caption = None
                if msg.caption is not None:
                    caption = msg.caption
                if msg.media==MessageMediaType.VIDEO_NOTE:
                    print("video_note message type")
                    round_message = True
                    print("Trying to get metadata")
                    data = video_metadata(file)
                    height, width, duration = data["height"], data["width"], data["duration"]
                    print(f'd: {duration}, w: {width}, h:{height}')
                    try:
                        thumb_path = await screenshot(file, duration, sender)
                    except Exception:
                        thumb_path = None
                    await client.send_video_note(
                        chat_id=sender,
                        video_note=file,
                        length=height, duration=duration, 
                        thumb=thumb_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            '**Yuklanmoqda:**\n',
                            edit,
                            time.time()
                        )
                    )
                elif msg.media==MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:
                    print("video message type")
                    print("Trying to get metadata")
                    data = video_metadata(file)
                    height, width, duration = data["height"], data["width"], data["duration"]
                    print(f'd: {duration}, w: {width}, h:{height}')
                    try:
                        thumb_path = await screenshot(file, duration, sender)
                    except Exception:
                        thumb_path = None
                    await client.send_video(
                        chat_id=sender,
                        video=file,
                        caption=caption,
                        supports_streaming=True,
                        height=height, width=width, duration=duration, 
                        thumb=thumb_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            '**Yuklanmoqda:**\n',
                            edit,
                            time.time()
                        )
                    )

                elif msg.media==MessageMediaType.PHOTO:
                    print("photo message type")
                    await edit.edit("Rasmni yuklamoqdaman.")
                    await bot.send_file(sender, file, caption=caption)

                elif msg.media == MessageMediaType.AUDIO:
                    print("audio message type")
                    await client.edit_message_text(sender, edit_id, "Audioni yuklamoqdaman...")
                    await client.send_audio(
                        chat_id=sender,
                        audio=file,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            '**Yuklanmoqda:**\n',
                            edit,
                            time.time()
                        )
                    )
                elif msg.media == MessageMediaType.VOICE:
                    print("voice message type")
                    await client.edit_message_text(sender, edit_id, "ovozli habar yuklanmoqda...")
                    await client.send_voice(
                        chat_id=sender,
                        voice=file,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            '**Yuklanmoqda:**\n',
                            edit,
                            time.time()
                        )
                    )
                elif msg.media == MessageMediaType.STICKER:
                    print("sticker message type")
                    await client.edit_message_text(sender, edit_id, "stiker yuboryapman.")
                    await client.send_sticker(
                        chat_id=sender,
                        sticker=file,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            '**Yuklanmoqda:**\n',
                            edit,
                            time.time()
                        )
                    )
                elif msg.media == MessageMediaType.ANIMATION:
                    print("animation message type")
                    await client.edit_message_text(sender, edit_id, "stiker yuboryapman.")
                    await client.send_animation(
                        chat_id=sender,
                        animation=file,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            '**Yuklanmoqda:**\n',
                            edit,
                            time.time()
                        )
                    )
                else:
                    thumb_path=thumbnail(sender)
                    print("document message type")
                    await client.send_document(
                        sender,
                        file, 
                        caption=caption,
                        thumb=thumb_path,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            client,
                            '**Yuklanmoqda:**\n',
                            edit,
                            time.time()
                        )
                    )
            except (TimeoutError) :
                await edit.edit('Fayl qo`llab quvvatlanmaydi.')
                                
            try:
                os.remove(file)
                if os.path.isfile(file) == True:
                    os.remove(file)
            except Exception:
                pass
            await edit.delete()
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await client.edit_message_text(sender, edit_id, "Ushbu kanalda men mavjud emasman, avval menga kanal linkini yuboring!!")
            return
        except PeerIdInvalid:
            chat = msg_link.split("/")[-3]
            try:
                int(chat)
                new_link = f"t.me/c/{chat}/{msg_id}"
            except:
                new_link = f"t.me/b/{chat}/{msg_id}"
            return await get_msg(userbot, client, bot, sender, edit_id, msg_link, i)
        except Exception as e:
            print(e)
            if "messages.SendMedia" in str(e) \
            or "SaveBigFilePartRequest" in str(e) \
            or "SendMediaRequest" in str(e) \
            or str(e) == "File size equals to 0 B":
                try: 
                    if msg.media==MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:
                        UT = time.time()
                        uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**Yuklanmoqda:**')
                        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, round_message=round_message, supports_streaming=True)] 
                        await bot.send_file(sender, uploader, caption=caption, thumb=thumb_path, attributes=attributes, force_document=False)
                    elif msg.media==MessageMediaType.VIDEO_NOTE:
                        uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**Yuklanmoqda:**')
                        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, round_message=round_message, supports_streaming=True)] 
                        await bot.send_file(sender, uploader, caption=caption, thumb=thumb_path, attributes=attributes, force_document=False)
                    else:
                        UT = time.time()
                        uploader = await fast_upload(f'{file}', f'{file}', UT, bot, edit, '**Yuklanmoqda:**')
                        await bot.send_file(sender, uploader, caption=caption, thumb=thumb_path, force_document=True)
                    if os.path.isfile(file) == True:
                        os.remove(file)
                except Exception as e:
                    print(e)
                    await client.edit_message_text(sender, edit_id, f'Saqlashda muammo: `{msg_link}`\n\nError: {str(e)}')
                    try:
                        os.remove(file)
                    except Exception:
                        return
                    return 
            else:
                await client.edit_message_text(sender, edit_id, f'Saqlashda muammo: `{msg_link}`\n\nError: {str(e)}')
                try:
                    os.remove(file)
                except Exception:
                    return
                return
        try:
            os.remove(file)
            if os.path.isfile(file) == True:
                os.remove(file)
        except Exception:
            pass
        await edit.delete()
    else:
        edit = await client.edit_message_text(sender, edit_id, "Nusxalanmoqda.")
        chat =  msg_link.split("t.me")[1].split("/")[1]
        try:
            msg = await client.get_messages(chat, msg_id)
            if msg.empty:
                new_link = f't.me/b/{chat}/{int(msg_id)}'
                #recurrsion 
                return await get_msg(userbot, client, bot, sender, edit_id, new_link, i)
            await client.copy_message(sender, chat, msg_id)
        except Exception as e:
            print(e)
            return await client.edit_message_text(sender, edit_id, f'Saqlashda muammo: `{msg_link}`\n\nError: {str(e)}')
        await edit.delete()
        
async def get_bulk_msg(userbot, client, sender, msg_link, i):
    x = await client.send_message(sender, "tayyorlanmoqda...!")
    await get_msg(userbot, client, Drone, sender, x.id, msg_link, i)
