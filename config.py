
import os
import logging
from logging.handlers import RotatingFileHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7401282886:AAHxKsKu9U7vVgEfKFWIf3xgbvudUZQT5CY")
APP_ID = int(os.environ.get("APP_ID", "26258063"))
API_HASH = os.environ.get("API_HASH", "be0a0e2ecd938bfc5401d35a399deeb7")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002008354608"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "7328629001"))
PORT = os.environ.get("PORT", "8039")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://koyeb77user:rohit870@cluster0.wgdkp.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "codeflix_bots")

#Shortner (token system) 

SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "publicearn.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "adabe1c0675be8ffc5ccbc84a9a65bc5a5d3ec69")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 60)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/redlight_howto/2") 

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002215102799"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}, Thanks for using me :D @Javpostr ⚡️.")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "5149937796").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "ʜᴇʟʟᴏ {first}\n\n<b>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ.</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>• ʙʏ @rohit_1888</b>")

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"

#==========================(BUY PREMIUM)====================#

PREMIUM_BUTTON = reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("Remove Ads In One Click", callback_data="buy_prem")]]
)

PREMIUM_BUTTON2 = reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("Remove Ads In One Click", callback_data="buy_prem")]]
) 

OWNER_TAG = os.environ.get("OWNER_TAG", "rohit_1888")

#UPI ID
UPI_ID = os.environ.get("UPI_ID", "rohit23pnb@axl")

#UPI QR CODE IMAGE
UPI_IMAGE_URL = os.environ.get("UPI_IMAGE_URL", "https://t.me/paymentbot6/2")

#SCREENSHOT URL of ADMIN for verification of payments
SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", f"t.me/{OWNER_TAG}")



#Time and its price

#7 Days
PRICE1 = os.environ.get("PRICE1", "20 rs")

#1 Month
PRICE2 = os.environ.get("PRICE2", "49 rs")

#3 Month
PRICE3 = os.environ.get("PRICE3", "135 rs")

#6 Month
PRICE4 = os.environ.get("PRICE4", "250 rs")

#1 Year
PRICE5 = os.environ.get("PRICE5", "500 rs")


#===================(END)========================#

ADMINS.append(OWNER_ID)
ADMINS.append(5149937796)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
