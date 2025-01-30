import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Bot Token နဲ့ Base URL သတ်မှတ်ခြင်း
TOKEN = '7799384444:AAH96qotMpXECg6VpkVLsiaxPmoYSEIC6wA'
BASE_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)

# Command တွေအတွက် URL တွေကိုသတ်မှတ်ခြင်း
COMMAND_URLS = {
    "/key1": "https://raw.githubusercontent.com/lagzian/SS-Collector/main/SS/VM_Trinity.txt",
    "/key2": "https://raw.githubusercontent.com/SonzaiEkkusu/V2RayDumper/main/config.txt",
    "/key3": "https://raw.githubusercontent.com/iboxz/free-v2ray-collector/main/main/mix",
    "/key4": "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "/key5": "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/actives.txt",
    "/key6": "https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/main/config.txt",
    "/hk": "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/Countries/Hong_Kong.txt",
    "/jp": "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/Countries/Japan.txt",
    "/sg": "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/Countries/Singapore.txt",
    "/us": "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/Countries/United_States.txt",
    "/tw": "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/Countries/Taiwan.txt",
    "/uk": "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/Countries/United_Kingdom.txt",
}

# Telegram Update ကိုလက်ခံခြင်း
def handleTelegramUpdate(update: Update, context: CallbackContext):
    if update.message:
        chat_id = update.message.chat_id
        message_text = update.message.text

        # Group ဒါမှမဟုတ် supergroup ထဲမှာဆိုရင်၊ command က / နဲ့စပြီး bot username ပါမပါစစ်ဆေးပါတယ်။
        if update.message.chat.type in ['group', 'supergroup']:
            if not message_text.startswith('/') or f'@{context.bot.username}' not in message_text:
                return

        # Command ကိုခွဲခြားခြင်း
        command = message_text.split()[0].split('@')[0]  # Remove bot username if present
        if command in COMMAND_URLS:
            fetchAndSendMultipleLines(chat_id, COMMAND_URLS[command])
        elif command == '/start':
            sendTelegramMessage(chat_id, "Welcome to the V2RAY Key Bot! Use /help to see available commands.")
        elif command == '/help':
            help_message = """
            *𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗳𝗼𝗿 𝗩2𝗥𝗔𝗬 𝗞𝗘𝗬𝗦:*

            /key1 - Get free V2RAY key1  
            /key2 - Get free V2RAY key2  
            /key3 - Get free V2RAY key3  
            /key4 - Get free V2RAY key4  
            /key5 - Get free V2RAY key5  
            /key6 - Get free V2RAY key6  
            /hk   - Get Hong Kong server keys  
            /jp   - Get Japan server keys  
            /sg   - Get Singapore server keys  
            /us   - Get United States server keys  
            /tw   - Get Taiwan server keys  
            /uk   - Get United Kingdom server keys  

            _Servers are updated over time. Developed by @shayshayblack._
            """
            sendTelegramMessage(chat_id, help_message)

# URL ကနေ Data ကိုယူပြီး Message ပို့ခြင်း
def fetchAndSendMultipleLines(chat_id, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            selected_lines = lines[:10]  # Get first 10 lines
            message = "\n".join(selected_lines)
            sendTelegramMessage(chat_id, message)
        else:
            sendTelegramMessage(chat_id, "Failed to fetch data from the server.")
    except Exception as e:
        sendTelegramMessage(chat_id, f"An error occurred: {str(e)}")

# Telegram Message ပို့ခြင်း
def sendTelegramMessage(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    requests.post(url, json=payload)

# Bot ကို Start လုပ်ခြင်း
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command Handlers
    dp.add_handler(CommandHandler("start", handleTelegramUpdate))
    dp.add_handler(CommandHandler("help", handleTelegramUpdate))
    dp.add_handler(CommandHandler("key1", handleTelegramUpdate))
    dp.add_handler(CommandHandler("key2", handleTelegramUpdate))
    dp.add_handler(CommandHandler("key3", handleTelegramUpdate))
    dp.add_handler(CommandHandler("key4", handleTelegramUpdate))
    dp.add_handler(CommandHandler("key5", handleTelegramUpdate))
    dp.add_handler(CommandHandler("key6", handleTelegramUpdate))
    dp.add_handler(CommandHandler("hk", handleTelegramUpdate))
    dp.add_handler(CommandHandler("jp", handleTelegramUpdate))
    dp.add_handler(CommandHandler("sg", handleTelegramUpdate))
    dp.add_handler(CommandHandler("us", handleTelegramUpdate))
    dp.add_handler(CommandHandler("tw", handleTelegramUpdate))
    dp.add_handler(CommandHandler("uk", handleTelegramUpdate))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
    