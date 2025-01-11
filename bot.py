import logging
import random
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler,
CallbackContext
# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7799384444:AAHyJovEz1bPhXqzTMtMK8eOAkWLrATpsw0"
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %
(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
# Dictionary with the URLs for the keys
urls = {
 "/key1": "https://raw.githubusercontent.com/lagzian/SSCollector/main/SS/VM_Trinity.txt",
 "/key2": "https://raw.githubusercontent.com/SonzaiEkkusu/
V2RayDumper/main/config.txt",
 "/key3": "https://raw.githubusercontent.com/iboxz/freev2ray-collector/main/main/mix",
 "/key4": "https://raw.githubusercontent.com/roosterkid/
openproxylist/main/V2RAY_RAW.txt",
 "/key5": "https://raw.githubusercontent.com/MrMohebi/xrayproxy-grabber-telegram/master/collected-proxies/row-url/
actives.txt",
 "/key6": "https://raw.githubusercontent.com/miladtahanian/
V2RayCFGDumper/main/config.txt",
 "/hk": "https://raw.githubusercontent.com/SoliSpirit/v2rayconfigs/main/Countries/Hong_Kong.txt",
 "/jp": "https://raw.githubusercontent.com/SoliSpirit/v2rayconfigs/main/Countries/Japan.txt",
 "/sg": "https://raw.githubusercontent.com/SoliSpirit/v2rayconfigs/main/Countries/Singapore.txt",
 "/us": "https://raw.githubusercontent.com/SoliSpirit/v2rayconfigs/main/Countries/United_States.txt",
 "/tw": "https://raw.githubusercontent.com/SoliSpirit/v2rayconfigs/main/Countries/Taiwan.txt",
 "/uk": "https://raw.githubusercontent.com/SoliSpirit/v2rayconfigs/main/Countries/United_Kingdom.txt",
}
# Command handler functions
def start(update: Update, context: CallbackContext) -> None:
 update.message.reply_text("V2RAY Key များရယူင်ပါ! စတင်ရန် /
help ကို command များည့်ပါ.")
def help(update: Update, context: CallbackContext) -> None:
 help_message = """
* 2 :*
/key1 - Get free V2RAY key1
/key2 - Get free V2RAY key2
/key3 - Get free V2RAY key3
/key4 - Get free V2RAY key4
/key5 - Get free V2RAY key5
/key6 - Get free V2RAY key6
/hk - Get Hong Kong server keys
/jp - Get Japan server keys
/sg - Get Singapore server keys
/us - Get United States server keys
/tw - Get Taiwan server keys
/uk - Get United Kingdom server keys
_Servers are updated over time. Developed by @shayshayblack._
 """
 update.message.reply_text(help_message,
parse_mode='Markdown')
  def fetch_and_send_multiple_lines(update: Update, context:
  CallbackContext, url: str) -> None:
   try:
   # Fetch the data from the URL
   response = requests.get(url)
   response.raise_for_status() # Will raise an HTTPError
  for bad responses
   # Process the data
   data = response.text
   lines = [line.split("#")[0].strip() for line in
  data.split("\n") if line.strip() != "" and not
  line.startswith("#")]

   if len(lines) == 0:
   update.message.reply_text("No valid keys found.")
   return
  # Randomly select 10 lines
   selected_lines = random.sample(lines, 10)
   formatted_text = "\n\n".join(selected_lines)
   # Send the selected lines as a code block
   update.message.reply_text(f"```\n{formatted_text}
  \n```", parse_mode='MarkdownV2')
   except requests.exceptions.RequestException as e:
   # Handle any errors that occur during the request
   logger.error(f"Error fetching data: {e}")
   update.message.reply_text("Error retrieving data for
  the provided URL.")
  def handle_command(update: Update, context: CallbackContext) ->
  None:
   text = update.message.text
   chat_id = update.message.chat.id
   command = text.split(" ")[0].strip()

# Check if the command is in the urls dictionary
 if command in urls:
 fetch_and_send_multiple_lines(update, context,
urls[command])
 else:
 update.message.reply_text("Unknown command. Use /help
to see available commands.")
def main() -> None:
 # Create the Updater and pass it your bot's token.
 updater = Updater(TELEGRAM_BOT_TOKEN)
 # Get the dispatcher to register handlers
 dispatcher = updater.dispatcher
 # Add handlers for /start, /help, and dynamic commands (key
fetching)
 dispatcher.add_handler(CommandHandler("start", start))
 dispatcher.add_handler(CommandHandler("help", help))
 dispatcher.add_handler(CommandHandler("key1",
handle_command))
 dispatcher.add_handler(CommandHandler("key2",
handle_command))
 dispatcher.add_handler(CommandHandler("key3",
handle_command))
  dispatcher.add_handler(CommandHandler("key4",
  handle_command))
  dispatcher.add_handler(CommandHandler("key5",
  handle_command))
  dispatcher.add_handler(CommandHandler("key6",
  handle_command))
  dispatcher.add_handler(CommandHandler("hk",
  handle_command))
  dispatcher.add_handler(CommandHandler("jp",
  handle_command))
  dispatcher.add_handler(CommandHandler("sg",
  handle_command))
  dispatcher.add_handler(CommandHandler("us",
  handle_command))
  dispatcher.add_handler(CommandHandler("tw",
  handle_command))
  dispatcher.add_handler(CommandHandler("uk",
  handle_command))

  # Start the Bot
   updater.start_polling()
   # Run the bot until you send a signal to stop it
   updater.idle()
  if __name__ == '__main__':
   main()
