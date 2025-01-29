import os
import requests
import json
import random

TELEGRAM_BOT_TOKEN = "7799384444:AAE3M7tllVK7_6Qaqp7Js-pfWviybBs0Cw0"
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

async def handle_telegram_update(update):
    if not update.get("message"):
        return

    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")

    if update["message"]["chat"]["type"] in ["group", "supergroup"]:
        if not text.startswith("/") or f"@{update['message']['from']['username']}" not in text:
            return

    command_text = text.split(" ")[0]
    command = command_text.replace(f"@{update['message']['from']['username']}", "").strip()

    try:
        if command == "/start":
            await send_telegram_message(chat_id, "V2RAY Key များရယူနိုင်ပါပြီ! စတင်ရန် /help ကိုနှိပ်ပြီး command များကြည့်ပါ.")
        elif command == "/help":
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
            await send_telegram_message(chat_id, help_message)
        elif command.startswith("/"):
            urls = {
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

            if command in urls:
                await fetch_and_send_multiple_lines(chat_id, urls[command])
            else:
                await send_telegram_message(chat_id, "Unknown command. Use /help to see available commands.")
    except Exception as error:
        print(f"Error handling update: {error}")
        await send_telegram_message(chat_id, "An error occurred. Please try again.")

async def fetch_and_send_multiple_lines(chat_id, url):
    try:
        response = requests.get(url)
        if not response.ok:
            raise Exception(f"Failed to fetch data from URL: {url}")

        data = response.text
        lines = [line.split("#")[0].strip() for line in data.split("\n") if line.strip() and not line.startswith("#")]

        if not lines:
            raise Exception("No valid keys found.")

        selected_lines = []
        while len(selected_lines) < 10 and lines:
            random_index = random.randint(0, len(lines) - 1)
            selected_lines.append(lines.pop(random_index))

        formatted_text = "\n\n".join(selected_lines)
        await send_telegram_message(chat_id, f"```\n{formatted_text}\n```")
    except Exception as error:
        print(f"Error fetching subscription: {error}")
        await send_telegram_message(chat_id, "Error retrieving data for the provided URL.")

async def send_telegram_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}

    requests.post(url, json=payload)

async def handle_request(request):
    if request.method == "POST":
        update = await request.json()
        await handle_telegram_update(update)
        return {"status": 200, "body": "OK"}
    return {"status": 200, "body": "https://t.me/v2subpro_bot is online!"}
    
    
