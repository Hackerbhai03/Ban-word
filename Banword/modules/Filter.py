import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Banword import Banword as app
from config import OTHER_LOGS, BOT_USERNAME

# List of 18+ or abusive words (expandable)
BAD_WORDS = [
    # 18+ related words
    "sex", "porn", "nude", "fuck", "bitch", "dick", "pussy", "slut", "boobs", "cock", "asshole", "chudai", "rand", "chhinar", "sexy", "hot girl", "land", "lund",
    "रंडी", "चोद", "मादरचोद", "गांड", "लंड", "भोसड़ी", "हिजड़ा", "पागल", "नंगा",
    # ✅ Common Hindi Gaaliyan
    "चूतिया", "मादरचोद", "बहनचोद", "गांडू", "रंडी", "भोसड़ी", "हिजड़ा", "लंड", "चोद", "झाटू", "हरामी", "कमीन", 
    "साला", "गांड", "पागल", "भड़वा", "चुत", "बेवकूफ", "कमीना", "निकम्मा", "हरामखोर", "चालू", "फट्टू", "ढक्कन", 
    "गधे", "कुत्ते", "साले", "बंदर", "सुअर", "बेशरम", "भोसड़ीवाले", "तेरी मां की", "तेरी बहन की", "चूतड़", "हरामज़ादा", 
    "हराम की औलाद", "सुअर का बच्चा", "गधे का लौड़ा", "लौंडा", "भड़वी", "मुफ्तखोर", "चालाक लोमड़ी", "आवारा", "फटीचर", 
    "फेंकू", "धोखेबाज", "मतलबी", "कायर", "नाकारा", "आवारा लड़का", "बेशर्म", "नालायक", "फेकू", "गंदा आदमी", "नाकाम", 
    "निकम्मी", "अकड़ू", "गटर का कीड़ा", "अंधभक्त", "गंजा", "पाखंडी", "चिरकुट", "घटिया", "सड़ियल", "चोर", "गटरछाप", 
    "लुटेरा", "छिछोरा", "बदतमीज़", "बददिमाग", "फ्रॉड", "नालायक", "बेवड़ा", "संडास", "गंदा", "ढोंगी", "भिखारी", 
    "फालतू", "कचरा", "पागल कुत्ता", "बदमाश", "आलसी", "कंजूस", "घमंडी", "फर्जी", "धूर्त", "बकचोद", "गप्पी", "फेंकू", 
    "बेवकूफी", "बेवड़ा", "फ्रॉड", "टटी", "भांड", "नाकारा", "कमीनी", "लंपट", "सैडिस्ट", "लफंगा", "बकवास", "घटिया", 
    "चिचोरा", "छिछोरा", "मक्खनचूस", "लफंगा", "तेरा बाप", "तेरी मां", "तेरी बहन", "तेरी औकात", "तेरी औकात क्या", 
    "तेरी फटी", "तेरी बैंड", "तेरा बैंड", "तेरी वाट", "तेरी बैंड बजा दूं", "तेरी ऐसी की तैसी", "तेरी टांग तोड़ दूं", 
    "तेरी खोपड़ी फोड़ दूं", "तेरा भेजा निकाल दूं", "तेरी हड्डी तोड़ दूं", "तेरी चप्पल से पिटाई करूंगा", "तेरी हड्डियां चूर-चूर",
    

    # ✅ Common Hindi Gaaliyan in English Font
    "chutiya", "madarchod", "Madhrachod", "Madharchod", "betichod", "behenchod", "gandu", "randi", "bhosdi", "hijda", "lund", "chod", "jhaatu", 
    "harami", "kamina", "saala", "gand", "pagal", "bhadwa", "chut", "bevkoof", "nikkamma", "haramkhor", 
    "chaalu", "fattuu", "dhakkan", "gadha", "kutta", "suvar", "besharam", "bhosdike", "teri maa ki", 
    "teri behan ki", "chutad", "haramzaada", "haram ki aulaad", "suvar ka baccha", "gand ka keeda", 
    "chirkut", "ghatiya", "sadela", "choor", "lutera", "chichora", "badtameez", "baddimag", "fraud", 
    "nalayak", "bewda", "sandass", "ganda", "dhongi", "bhikhari", "faltu", "kachra", "pagal kutta", 
    "badmash", "aalsi", "kanjoos", "ghamandi", "farzi", "dhurt", "bakchod", "gappi", "nakli", "chalu", 
    "lafanga", "bakwas", "bikau", "chapri", "nalla", "tatti", "jhantu", "ullu ka pattha", "ulloo", 
    "chindi", "panauti", "lukkha", "kuttiya", "kaminey", "kamzarf", "budbak", "chirkut", "sust", "tharki", 
    "bhagoda", "kutta kamina", "bhains ki aankh", "teri taang tod dunga", "teri band baja dunga", 
    "tera dimaag kharab hai", "teri waat laga dunga", "teri maa ka bhosda", "teri gaand maar dunga",

    
    # ✅ Common Porn & NSFW Terms (Mix of Hindi & English)
    "sex", "porn", "nude", "nangi", "chudai", "bhabhi chudai", "lund", "gaand", "bhosda", "chut", 
    "maal", "jism", "randi", "randi khana", "desi sex", "hot video", "nangi ladki", "bhabhi nudes", 
    "bhabhi sex", "sexy aunty", "nude aunty", "bhabhi ki chut", "aunty ki chut", "boobs", "tits", 
    "nipple", "dildo", "pussy", "vagina", "penis", "cock", "dick", "cum", "anal", "squirt", "deepthroat", 
    "hentai", "bdsm", "lesbian", "gay sex", "futa", "69", "screwing", "sex chat", "incest", "stepmom", 
    "stepsis", "stepbro", "honeymoon sex", "bhabhi nude", "hot indian actress", "desi nudes", 
    "sexy saree", "lingerie", "erotic", "kinky", "naughty", "sensual", "lust", "muth", "muthi", 
    "masturbation", "call girl", "escort", "sex worker", "rape porn", "forced porn", "underage porn", 
    "child porn", "pedo", "loli", "teen sex", "schoolgirl porn", "hijab porn", "casting couch", 
    "sex tape", "strip club", "naked", "uncensored", "bikini photos", "hot saree", "sexy photos", 
    "onlyfans", "patreon nudes", "hot cam", "sex cam", "live sex", "private parts", "exposed", 
    "naked selfie", "sex video", "desi sex video", "bollywood sex", "lingam massage", "tantra sex", 
    "milf", "hotwife", "swinger", "erotic massage", "boobs press", "licking", "lick pussy", 
    "moaning", "dirty talk", "hot girl", "big boobs", "tight pussy", "wet pussy", "hard cock", 
    "big cock", "blowjob", "handjob", "sexy dance", "strip tease", "sex position", "saree sex", 
    "sexy aunty video", "hot desi bhabhi", "bollywood hot", "item girl", "hot indian model", 
    "desi randi", "desi call girl", "sexy night", "hijra sex", "chudai story", "sex story", 
    "suhagraat sex", "honeymoon night", "love making", "hot romance", "desi romance", "hot chat", 
    "sexy time", "naughty chat", "dirty video", "hidden cam", "bathroom sex", "hotel sex", 
    "massage sex", "body to body massage", "saree romance", "choli romance", "cleavage show", 
    "hot navel", "desi thighs", "big ass", "backside show"
]

BAD_PATTERN = re.compile(r"|".join([re.escape(word) for word in BAD_WORDS]), re.IGNORECASE)

@app.on_message(filters.group & filters.text & ~filters.via_bot)
async def filter_18(client: Client, message: Message):
    text = message.text or ""

    if not BAD_PATTERN.search(text):
        return

    user = message.from_user
    if not user:
        return

    try:
        await message.delete()
    except:
        return

    # Send warning in group
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    warn_text = f"{mention}, 18+ messages are not allowed!"
    cancel_btn = InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="close")]])

    try:
        warn = await message.reply(warn_text, reply_markup=cancel_btn)
        await asyncio.sleep(10)
        await warn.delete()
    except:
        pass

    # Logging to OTHER_LOGS group
    username = f"@{user.username}" if user.username else "No username"
    group_name = message.chat.title
    chat_id = message.chat.id

    log_text = f"""
🚫 **18+ or Abusive Message Deleted**

**👤 User:** {mention}
**🆔 User ID:** `{user.id}`
**🔗 Username:** {username}
**🏷️ Group:** `{group_name}`
**🆔 Chat ID:** `{chat_id}`
**💬 Message:** `{text}`

🤖 **Bot:** @{BOT_USERNAME}
"""

    try:
        await client.send_message(
            OTHER_LOGS,
            log_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add to Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]
            ])
        )
    except Exception as e:
        print(f"[LOG SEND ERROR] {e}")

# Optional: Handle cancel button
@app.on_callback_query(filters.regex("close"))
async def close_btn(client, callback_query):
    try:
        await callback_query.message.delete()
    except:
        pass
