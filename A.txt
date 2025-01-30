Telegram bot ရေးဖို့အတွက် အသေးစိတ်ရှင်းပြမယ်နော်။ ဒီ bot ကို JavaScript နဲ့ရေးထားပြီး၊ Telegram Bot API ကိုအသုံးပြုထားပါတယ်။ ဒီ bot က V2RAY keys တွေကိုရယူဖို့အတွက် command တွေကိုလက်ခံပြီး၊ အသုံးပြုသူတွေကို keys တွေပေးပို့ပေးပါတယ်။

### 1. **Bot Token နဲ့ Base URL သတ်မှတ်ခြင်း**
   - `TELEGRAM_BOT_TOKEN` ဆိုတဲ့ variable မှာ bot token ကိုသတ်မှတ်ထားပါတယ်။ ဒီ token ကို Telegram ကပေးတဲ့ BotFather ကနေရယူနိုင်ပါတယ်။
   - `BASE_URL` ကတော့ Telegram Bot API ကိုခေါ်ဖို့အတွက် base URL ဖြစ်ပါတယ်။

```javascript
const TELEGRAM_BOT_TOKEN = "7799384444:AAE3M7tllVK7_6Qaqp7Js-pfWviybBs0Cw0";
const BASE_URL = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}`;
```

### 2. **Telegram Update ကိုလက်ခံခြင်း**
   - `handleTelegramUpdate` function က Telegram ကပို့လာတဲ့ update ကိုလက်ခံပြီး၊ အဲ့ဒီ update ထဲမှာ message ပါမပါစစ်ဆေးပါတယ်။
   - Message ပါရင်၊ chat ID နဲ့ message text ကိုထုတ်ယူပါတယ်။
   - Group ဒါမှမဟုတ် supergroup ထဲမှာဆိုရင်၊ command က `/` နဲ့စပြီး bot username ပါမပါစစ်ဆေးပါတယ်။ မပါရင် return လုပ်ပါတယ်။

```javascript
async function handleTelegramUpdate(update) {
    if (!update.message) return;

    const chatId = update.message.chat.id;
    const text = update.message.text;

    if (update.message.chat.type === "group" || update.message.chat.type === "supergroup") {
        if (!text.startsWith("/") || !text.includes(`@${update.message.bot_username}`)) {
            return;
        }
    }
```

### 3. **Command ကိုခွဲခြားခြင်း**
   - Command ကိုခွဲခြားဖို့ `commandText` နဲ့ `command` variable တွေကိုသတ်မှတ်ပါတယ်။
   - Command က `/start` ဆိုရင်၊ bot ကို start လုပ်ဖို့ message ပို့ပါတယ်။
   - Command က `/help` ဆိုရင်၊ ရနိုင်တဲ့ commands တွေကိုပြသပါတယ်။

```javascript
    const commandText = text.split(" ")[0];
    const command = commandText.replace(/@[\w_]+$/, "").trim();

    try {
        if (command === "/start") {
            await sendTelegramMessage(
                chatId,
                "V2RAY Key များရယူနိုင်ပါပြီ! စတင်ရန် /help ကိုနှိပ်ပြီး command များကြည့်ပါ."
            );
        } else if (command === "/help") {
            const helpMessage = `
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
                        `;
            await sendTelegramMessage(chatId, helpMessage);
```

### 4. **Command များအလိုက် URL များကိုခွဲခြားခြင်း**
   - Command တစ်ခုချင်းစီအတွက် URL တွေကိုသတ်မှတ်ထားပါတယ်။
   - Command ကို URL နဲ့တွဲပြီး၊ `fetchAndSendMultipleLines` function ကိုခေါ်ပါတယ်။

```javascript
        } else if (command.startsWith("/")) {
            const urls = {
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
            };

            if (urls[command]) {
                await fetchAndSendMultipleLines(chatId, urls[command]);
            } else {
                await sendTelegramMessage(chatId, "Unknown command. Use /help to see available commands.");
            }
        }
    } catch (error) {
        console.error("Error handling update:", error);
        await sendTelegramMessage(chatId, "An error occurred. Please try again.");
    }
}
```

### 5. **URL ကနေ Data ကိုယူပြီး Message ပို့ခြင်း**
   - `fetchAndSendMultipleLines` function က URL ကနေ data ကိုယူပြီး၊ အဲ့ဒီ data ထဲက 10 ကြောင်းကိုရွေးပါတယ်။
   - ရွေးထားတဲ့ lines တွေကို message အဖြစ်ပို့ပါတယ်။

```javascript
async function fetchAndSendMultipleLines(chatId, url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to fetch data from URL: ${url}`);

        const data = await response.text();
        const lines = data
            .split("\n")
            .filter(line => line.trim() !== "" && !line.startsWith("#")) // Remove empty lines and those with `#`
            .map(line => line.split("#")[0].trim()); // Remove comments after `#`

        if (lines.length === 0) throw new Error("No valid keys found.");

        // Select 10 random lines
        const selectedLines = [];
        while (selectedLines.length < 10 && lines.length > 0) {
            const randomIndex = Math.floor(Math.random() * lines.length);
            selectedLines.push(lines[randomIndex]);
            lines.splice(randomIndex, 1); // Remove the selected line to avoid duplicates
        }

        const formattedText = selectedLines.join("\n\n");
        await sendTelegramMessage(chatId, `\`\`\`\n${formattedText}\n\`\`\``);
    } catch (error) {
        console.error("Error fetching subscription:", error);
        await sendTelegramMessage(chatId, `Error retrieving data for the provided URL.`);
    }
}
```

### 6. **Telegram Message ပို့ခြင်း**
   - `sendTelegramMessage` function က Telegram API ကိုအသုံးပြုပြီး message ပို့ပါတယ်။

```javascript
async function sendTelegramMessage(chatId, text) {
    const url = `${BASE_URL}/sendMessage`;
    const payload = { chat_id: chatId, text, parse_mode: "Markdown" };

    await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
}
```

### 7. **Export လုပ်ခြင်း**
   - `export default` က bot ကို webhook အနေနဲ့အသုံးပြုဖို့အတွက် export လုပ်ထားပါတယ်။

```javascript
export default {
    async fetch(request) {
        if (request.method === "POST") {
            const update = await request.json();
            await handleTelegramUpdate(update);
            return new Response("OK", { status: 200 });
        }
        return new Response("https://t.me/v2subpro_bot is online!", { status: 200 });
    },
};
```

### 8. **Bot ကိုအသုံးပြုခြင်း**
   - Bot ကို `/start` command နဲ့စတင်နိုင်ပါတယ်။
   - `/help` command နဲ့ရနိုင်တဲ့ commands တွေကိုကြည့်နိုင်ပါတယ်။
   - `/key1`, `/key2`, `/hk`, `/jp` စတဲ့ commands တွေနဲ့ V2RAY keys တွေကိုရယူနိုင်ပါတယ်။

ဒီ bot ကို Cloudflare Workers လိုမျိုး serverless platform တွေမှာအသုံးပြုနိုင်ပါတယ်။