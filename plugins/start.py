import asyncio
import base64
import logging
import os
import random
import re
import string as piroayush
import time

from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import (
    ADMINS,
    FORCE_MSG,
    START_MSG,
    CUSTOM_CAPTION,
    IS_VERIFY,
    VERIFY_EXPIRE,
    SHORTLINK_API,
    SHORTLINK_URL,
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    TUT_VID,
    OWNER_ID,
)
from helper_func import subscribed, encode, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import *
from shortzy import Shortzy

"""add time in seconds for waiting before delete 
1 min = 60, 2 min = 60 × 2 = 120, 5 min = 60 × 5 = 300"""
# SECONDS = int(os.getenv("SECONDS", "1200"))

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    text = message.text
    try:
        base64_string = text.split(" ", 1)[1]
    except:
        return
    string = await decode(base64_string)

    owner_id = int("666666666")
    verify_status = await get_verify_status(id)
  # Fetch the owner's ID from config

    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass

    # Check if the user is the owner
    if id == owner_id:
        # Owner-specific actions
        # You can add any additional actions specific to the owner here
        await message.reply("You are the owner! Additional actions can be added here.")
        return
    
    
    elif message.text.lower() == "/start" and not verify_status['is_verified'] and not string.startswith("get") and not string.startswith("premium") and not await is_premium_user(message.from_user.id):
        print("1st blank start")
        verify_status = await get_verify_status(id)
        if IS_VERIFY:
            token = ''.join(random.choices(piroayush.ascii_letters + piroayush.digits, k=10))
            await update_verify_status(id, verify_token=token, link="")
            link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API,f'https://telegram.dog/{client.username}?start=verify_{token}')
            btn = [
                [InlineKeyboardButton("• ᴏᴘᴇɴ ʟɪɴᴋ", url=link)],
                [InlineKeyboardButton('ᴛᴜᴛᴏʀɪᴀʟ •', url=TUT_VID)]
            ]
            await message.reply(f"Your Ads token is expired, refresh your token and try again.\n\nToken Timeout: {get_exp_time(VERIFY_EXPIRE)}\n\nWhat is the token?\n\nThis is an ads token. If you pass 1 ad, you can use the bot for 24 Hour after passing the ad.", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)

    else:
        print("non admin starting")
        verify_status = await get_verify_status(id)
        if verify_status['is_verified'] and not await is_premium_user(message.from_user.id) and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
            await update_verify_status(id, is_verified=False)

        if "verify_" in message.text:
            _, token = message.text.split("_", 1)
            if verify_status['verify_token'] != token:
                return await message.reply("Your token is invalid or Expired. Try again by clicking /start")
            await update_verify_status(id, is_verified=True, verified_time=time.time())
            if verify_status["link"] == "":
                reply_markup = None
            await message.reply(f"Your token successfully verified and valid for: 24 Hour", reply_markup=reply_markup, protect_content=False, quote=True)
#----------------------------------------------------------------------------------
        elif len(message.text) > 7 and string.startswith("premium") and not string.startswith("get"):
            print("post, premium")
            try:
                base64_string = text.split(" ", 1)[1]
            except:
                return
            string = await decode(base64_string)
            if string.startswith("premium"):
                if not await is_premium_user(message.from_user.id):
                    if not await is_premium_user(message.from_user.id):
                        await message.reply_text("Buy premium to access this content\nTo Buy Contact @rohit_1888")
                        return
            argument = string.split("-")
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    return
                if start <= end:
                    ids = range(start, end+1)
                else:
                    ids = []
                    i = start
                    while True:
                        ids.append(i)
                        i -= 1
                        if i < end:
                            break
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except:
                    return
            temp_msg = await message.reply("Please wait...")
            try:
                messages = await get_messages(client, ids)
            except:
                await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()
            
            snt_msgs = []
            
            for msg in messages:
                if bool(CUSTOM_CAPTION) & bool(msg.document):
                    caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if DISABLE_CHANNEL_BUTTON:
                    reply_markup = msg.reply_markup
                else:
                    reply_markup = None

                try:
                    snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                    snt_msgs.append(snt_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    snt_msgs.append(snt_msg)
                except:
                    pass

            SD = await message.reply_text("Baka! Files will be deleted After 300 seconds. Save them to the Saved Message now!")
            await asyncio.sleep(300)

            for snt_msg in snt_msgs:
                try:
                    await snt_msg.delete()
                    await SD.delete()
                except:
                    pass
            return
#----------------------------------------------------------------------------------
        elif len(message.text) > 7 and verify_status['is_verified'] and string.startswith("get"):
            print("post, verefied, non premium")
            try:
                base64_string = message.text.split(" ", 1)[1]
            except:
                return
            _string = await decode(base64_string)
            argument = _string.split("-")
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    return
                if start <= end:
                    ids = range(start, end+1)
                else:
                    ids = []
                    i = start
                    while True:
                        ids.append(i)
                        i -= 1
                        if i < end:
                            break
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except:
                    return
            temp_msg = await message.reply("Please wait...")
            try:
                messages = await get_messages(client, ids)
            except:
                await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()
            
            snt_msgs = []
            
            for msg in messages:
                if bool(CUSTOM_CAPTION) & bool(msg.document):
                    caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if DISABLE_CHANNEL_BUTTON:
                    reply_markup = msg.reply_markup
                else:
                    reply_markup = None

                try:
                    snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                    snt_msgs.append(snt_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    snt_msgs.append(snt_msg)
                except:
                    pass

            SD = await message.reply_text("Baka! Files will be deleted After 300 seconds. Save them to the Saved Message now!")
            await asyncio.sleep(300)

            for snt_msg in snt_msgs:
                try:
                    await snt_msg.delete()
                    await SD.delete()
                except:
                    pass

        elif verify_status['is_verified']:
            print("no post and verified")
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("⚡️ ᴀʙᴏᴜᴛ", callback_data = "about"),
                  InlineKeyboardButton('🍁 sᴇʀɪᴇsғʟɪx', url='https://t.me/Team_Netflix/40')]]
            )
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
        elif len(message.text) > 7 and not verify_status['is_verified'] and string.startswith("get"):
            print("no post")
            verify_status = await get_verify_status(id)
            if IS_VERIFY and not verify_status['is_verified']:
                token = ''.join(random.choices(piroayush.ascii_letters + piroayush.digits, k=10))
                await update_verify_status(id, verify_token=token, link="")
                print(f'https://telegram.dog/{client.username}?start=verify_{token}')
                link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API,f'https://telegram.dog/{client.username}?start=verify_{token}')
                btn = [
                    [InlineKeyboardButton("• ᴏᴘᴇɴ ʟɪɴᴋ", url=link)],
                    [InlineKeyboardButton('ᴛᴜᴛᴏʀɪᴀʟ •', url=TUT_VID)]
                ]
                await message.reply(f"Your Ads token is expired, refresh your token and try again.\n\nToken Timeout: {get_exp_time(VERIFY_EXPIRE)}\n\nWhat is the token?\n\nThis is an ads token. If you pass 1 ad, you can use the bot for 24 Hour after passing the ad.", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)

        else:
            print("blank start")
            verify_status = await get_verify_status(id)
            if IS_VERIFY and not verify_status['is_verified']:
                token = ''.join(random.choices(piroayush.ascii_letters + piroayush.digits, k=10))
                await update_verify_status(id, verify_token=token, link="")
                link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API,f'https://telegram.dog/{client.username}?start=verify_{token}')
                btn = [
                    [InlineKeyboardButton("• ᴏᴘᴇɴ ʟɪɴᴋ", url=link)],
                    [InlineKeyboardButton('ᴛᴜᴛᴏʀɪᴀʟ •', url=TUT_VID)]
                ]
                await message.reply(f"Your Ads token is expired, refresh your token and try again.\n\nToken Timeout: {get_exp_time(VERIFY_EXPIRE)}\n\nWhat is the token?\n\nThis is an ads token. If you pass 1 ad, you can use the bot for 24 Hour after passing the ad.", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)


    
        
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •",
                url = client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = '• ʀᴇʟᴏᴀᴅ •',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()


@Bot.on_message(filters.private & filters.command('addpaid') & filters.user(ADMINS))
async def add_premium_user(client: Client, msg: Message):
    if len(msg.command) != 3:
        await msg.reply_text("usage: /addpremium user_id time_limit_months")
        return
    try:
        user_id = int(msg.command[1])
        time_limit_months = int(msg.command[2])
        await add_premium(user_id, time_limit_months)
        await msg.reply_text(f"User {user_id} added as a paid user with {time_limit_months}-days plan.")
        await client.send_message(
                chat_id= user_id,
                text=f"**ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs ɴᴏᴡ ʏᴏᴜ ᴀʀᴇ ᴜᴘɢʀᴀᴅᴇᴅ ᴛᴏ {time_limit_months} ᴅᴀʏs sᴜʙsᴄʀɪᴘᴛɪᴏɴ**",
                parse_mode=ParseMode.MARKDOWN
            )
    except ValueError:
        await msg.reply_text("Invalid user_id or time_limit. Please recheck.")

@Bot.on_message(filters.private & filters.command('removepaid') & filters.user(ADMINS))
async def pre_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("useage: /removeuser user_id ")
        return
    try:
        user_id = int(msg.command[1])
        await remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")

from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid

@Bot.on_message(filters.private & filters.command('listpaid') & filters.user(ADMINS))
async def list_premium_users_command(client, message):
    premium_users = collection.find({})
    premium_user_list = ['Premium Users in database:']

    for user in premium_users:
        user_ids = user["user_id"]
        try:
            user_info = await client.get_users(user_ids)
            username = user_info.username
            first_name = user_info.first_name
            expiration_timestamp = user["expiration_timestamp"]
            xt = (expiration_timestamp - time.time())
            x = round(xt / (24 * 60 * 60))
            premium_user_list.append(f"UserID- <code>{user_ids}</code>\nUser- @{username}\nName- <code>{first_name}</code>\nExpiry- {x} days")
        except PeerIdInvalid:
            premium_user_list.append(f"UserID- <code>{user_ids}</code>\nUser- <code>Invalid ID</code>\nName- <code>Unknown</code>\nExpiry- <code>N/A</code>")
        except Exception as e:
            premium_user_list.append(f"UserID- <code>{user_ids}</code>\nUser- <code>Error: {str(e)}</code>\nName- <code>Unknown</code>\nExpiry- <code>N/A</code>")

    if premium_user_list:
        formatted_list = [f"{user}" for user in premium_user_list]
        await message.reply_text("\n\n".join(formatted_list))
    else:
        await message.reply_text("I found 0 premium users in my DB")


            