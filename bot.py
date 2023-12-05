import logging
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from config import cfg
import random, asyncio

logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.INFO)

bot = Client(
    name='Auto-bot',
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

CHID=cfg.CHAT_ID
TEXT="**Hello {mention}!\nYour request to join {title} has been approved\n\n__Thanks for joining**"
BLOG="**{mention} Just joined in {title}**"
NUSER="**{mention} Start bot**"
APPROVED = (cfg.APPROVED_WELCOME).lower()

@bot.on_message(filters.private & filters.command(["start"]))
async def start(client: bot, message: Message):
    approvedbot = await client.get_me()
    user=message.from_user
    add_user(message.from_user.id)
    button=[[
      InlineKeyboardButton("Main Channel", url="https://t.me/anime_Sub_Dub"),
      InlineKeyboardButton("Anime News", url="https://t.me/Anime_news_latest")
      ],[
      InlineKeyboardButton(
                        "➕ Add me to your Group", url=f"https://t.me/Auto_accept_Join_Request_RoBot?startchannel=true")
      ]]
    await message.reply_text(text="**𝙷𝙴𝙻𝙻𝙾...⚡\n\n𝙸𝙰𝙼 𝙰 𝚂𝙸𝙼𝙿𝙻𝙴 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝙰𝚄𝚃𝙾 𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙰𝙲𝙲𝙴𝙿𝚃 𝙱𝙾𝚃.**", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)
    await bot.send_message(chat_id=CHID, text=NUSER.format(mention=user.mention), disable_web_page_preview=True)

@bot.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client: bot, message: Message):
    chat=message.chat # Chat
    user=message.from_user # User
    try:
        print(f"{user.first_name} 𝙹𝙾𝙸𝙽𝙴𝙳 ⚡") # Logs
        await bot.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        if APPROVED == "on":
            await bot.send_message(chat_id=CHID, text=BLOG.format(mention=user.mention, title=chat.title), disable_web_page_preview=True)
            add_group(message.chat.id)
            await bot.send_message(chat_id=user.id, text=TEXT.format(mention=user.mention, title=chat.title), disable_web_page_preview=True)
            add_user(user.id) 
    except errors.PeerIdInvalid as e:
        print("user isn't start bot(means group)")
    except Exception as err:
        print(str(err)) 
        
@bot.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, message : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await message.reply_text(text=f"""
Chats Stats
Users : `{xx}`
Groups : `{x}`
Total users & groups : `{tot}` """)

@bot.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

@bot.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👽 Found `{blocked}` Blocked users \n💀 Found `{deactivated}` Deactivated users.")
    

if __name__ == "__main__":
    print("𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")
    bot.run()

