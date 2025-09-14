# Helper functions and constants for EnaChatBot modules
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from EnaChatBot import db

# Database connections
chatai = db.Word.WordDb if hasattr(db, 'Word') else None

# Language mappings
languages = {
    "english": "en",
    "hindi": "hi", 
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "russian": "ru",
    "arabic": "ar",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko",
    "bengali": "bn",
    "urdu": "ur",
    "turkish": "tr",
    "dutch": "nl",
    "swedish": "sv",
    "norwegian": "no",
    "danish": "da",
    "finnish": "fi"
}

# Inline keyboards
START_BOT = [
    [
        InlineKeyboardButton("❍ Aʙᴏᴜᴛ ❍", callback_data="ABOUT"),
        InlineKeyboardButton("❍ Hᴇʟᴘ ❍", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton("❍ Sᴏᴜʀᴄᴇ ❍", callback_data="SOURCE"),
    ],
    [
        InlineKeyboardButton("❍ Sᴜᴘᴘᴏʀᴛ ❍", url="https://t.me/TeamsXchat"),
        InlineKeyboardButton("❍ Uᴘᴅᴀᴛᴇ ❍", url="https://t.me/TeamXUpdate"),
    ],
]

HELP_BTN = [
    [
        InlineKeyboardButton("❍ Cʜᴀᴛʙᴏᴛ ❍", callback_data="CHATBOT_CMD"),
        InlineKeyboardButton("❍ Tᴏᴏʟs ❍", callback_data="TOOLS_DATA"),
    ],
    [
        InlineKeyboardButton("❍ Bᴀᴄᴋ ❍", callback_data="BACK"),
        InlineKeyboardButton("❍ Cʟᴏsᴇ ❍", callback_data="CLOSE"),
    ],
]

HELP_BUTN = [
    [
        InlineKeyboardButton("❍ Hᴇʟᴘ ❍", url="https://t.me/EnaChatBot?start=help"),
    ],
]

HELP_START = [
    [
        InlineKeyboardButton("❍ Sᴇᴛ Lᴀɴɢᴜᴀɢᴇ ❍", callback_data="choose_lang"),
    ],
    [
        InlineKeyboardButton("❍ Hᴇʟᴘ ❍", callback_data="HELP"),
    ],
]

DEV_OP = [
    [
        InlineKeyboardButton("❍ Aʙᴏᴜᴛ ❍", callback_data="ABOUT"),
        InlineKeyboardButton("❍ Hᴇʟᴘ ❍", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton("❍ Sᴏᴜʀᴄᴇ ❍", callback_data="SOURCE"),
    ],
]

PNG_BTN = [
    [
        InlineKeyboardButton("❍ Sᴜᴘᴘᴏʀᴛ ❍", url="https://t.me/TeamsXchat"),
        InlineKeyboardButton("❍ Uᴘᴅᴀᴛᴇ ❍", url="https://t.me/TeamXUpdate"),
    ],
]

BACK = [
    [
        InlineKeyboardButton("❍ Bᴀᴄᴋ ❍", callback_data="BACK"),
    ],
]

ABOUT_BTN = [
    [
        InlineKeyboardButton("❍ Sᴜᴘᴘᴏʀᴛ ❍", url="https://t.me/TeamsXchat"),
        InlineKeyboardButton("❍ Uᴘᴅᴀᴛᴇ ❍", url="https://t.me/TeamXUpdate"),
    ],
    [
        InlineKeyboardButton("❍ Bᴀᴄᴋ ❍", callback_data="BACK"),
    ],
]

CLOSE_BTN = [
    [
        InlineKeyboardButton("❍ Cʟᴏsᴇ ❍", callback_data="CLOSE"),
    ],
]

CHATBOT_ON = [
    [
        InlineKeyboardButton("Eɴᴀʙʟᴇ", callback_data="enable_chatbot"),
        InlineKeyboardButton("Dɪsᴀʙʟᴇ", callback_data="disable_chatbot"),
    ],
]

CHATBOT_BACK = [
    [
        InlineKeyboardButton("❍ Bᴀᴄᴋ ❍", callback_data="BACK_HELP"),
    ],
]

MUSIC_BACK_BTN = [
    [
        InlineKeyboardButton("❍ Bᴀᴄᴋ ❍", callback_data="BACK_HELP"),
    ],
]

# Text constants
START = """**🤖 ʜᴇʏ ᴅᴇᴀʀ {0}**

**ɪ ᴀᴍ ᴀ sɪᴍᴘʟᴇ ᴄʜᴀᴛʙᴏᴛ**

**📊 ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs:**
**• ᴜsᴇʀs :** `{1}`
**• ᴄʜᴀᴛs :** `{2}`
**• ᴜᴘᴛɪᴍᴇ :** `{3}`

**💫 ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ɪɴ ɢʀᴏᴜᴘs ᴏʀ ɪɴ ᴅɪʀᴇᴄᴛ ᴍᴇssᴀɢᴇ.**

**ᴛʜᴀɴᴋs ғᴏʀ ᴜsɪɴɢ ᴍᴇ ✨**"""

HELP_READ = """**🤖 ʜᴇʟᴘ ᴍᴇɴᴜ**

**ʜᴇʀᴇ ᴀʀᴇ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:**

**👑 ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:**
• `/clone` - ᴄʟᴏɴᴇ ᴀ ʙᴏᴛ ᴜsɪɴɢ ᴛᴏᴋᴇɴ
• `/delallclone` - ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs
• `/gcast` - ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴄʜᴀᴛs

**📱 ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs:**
• `/start` - sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
• `/help` - sʜᴏᴡ ʜᴇʟᴘ ᴍᴇɴᴜ
• `/ping` - ᴄʜᴇᴄᴋ ʙᴏᴛ ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ
• `/id` - ɢᴇᴛ ʏᴏᴜʀ ᴜsᴇʀ ɪᴅ
• `/lang` - ᴄʜᴀɴɢᴇ ʙᴏᴛ ʟᴀɴɢᴜᴀɢᴇ
• `/chatbot on/off` - ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ
• `/status` - ᴄʜᴇᴄᴋ ᴄʜᴀᴛʙᴏᴛ sᴛᴀᴛᴜs
• `/shayri` - ɢᴇᴛ ʀᴀɴᴅᴏᴍ sʜᴀʏʀɪ"""

ABOUT_READ = """**🤖 ᴀʙᴏᴜᴛ ᴇɴᴀᴄʜᴀᴛʙᴏᴛ**

**ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɪ-ᴘᴏᴡᴇʀᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀᴛʙᴏᴛ**

**✨ ғᴇᴀᴛᴜʀᴇs:**
• 🤖 ᴀɪ-ᴘᴏᴡᴇʀᴇᴅ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴs
• 🔄 ʙᴏᴛ ᴄʟᴏɴɪɴɢ sʏsᴛᴇᴍ
• 🌍 ᴍᴜʟᴛɪ-ʟᴀɴɢᴜᴀɢᴇ sᴜᴘᴘᴏʀᴛ
• 📊 sᴛᴀᴛɪsᴛɪᴄs & ᴀɴᴀʟʏᴛɪᴄs
• 💬 ɢʀᴏᴜᴘ & ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ sᴜᴘᴘᴏʀᴛ

**👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ:** @SID_ELITE
**📱 ᴠᴇʀsɪᴏɴ:** 2.0
**🔗 sᴏᴜʀᴄᴇ:** ᴏᴘᴇɴ sᴏᴜʀᴄᴇ"""

SOURCE_READ = """**📦 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ**

**✨ ᴇɴᴀᴄʜᴀᴛʙᴏᴛ ɪs ᴀɴ ᴏᴘᴇɴ sᴏᴜʀᴄᴇ ᴘʀᴏᴊᴇᴄᴛ**

**🔗 ɢɪᴛʜᴜʙ:** https://github.com/strd-dev131/ChatBot

**⭐ ɪғ ʏᴏᴜ ʟɪᴋᴇ ᴛʜɪs ᴘʀᴏᴊᴇᴄᴛ, ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ɪᴛ ᴀ sᴛᴀʀ!**

**🤝 ᴄᴏɴᴛʀɪʙᴜᴛɪᴏɴs ᴀʀᴇ ᴡᴇʟᴄᴏᴍᴇ**"""

ADMIN_READ = """**👑 ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs**

**ᴄᴏᴍᴍᴀɴᴅs ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ʙᴏᴛ ᴀᴅᴍɪɴs:**

**• /clone** - ᴄʟᴏɴᴇ ᴀ ʙᴏᴛ ᴜsɪɴɢ ᴛᴏᴋᴇɴ
**• /delallclone** - ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs
**• /gcast** - ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴄʜᴀᴛs
**• /stats** - ɢᴇᴛ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs
**• /restart** - ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"""

CHATBOT_READ = """**🤖 ᴄʜᴀᴛʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs**

**ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴄʜᴀᴛʙᴏᴛ:**

**• /chatbot on** - ᴇɴᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ ɪɴ ᴄʜᴀᴛ
**• /chatbot off** - ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ ɪɴ ᴄʜᴀᴛ
**• /status** - ᴄʜᴇᴄᴋ ᴄʜᴀᴛʙᴏᴛ sᴛᴀᴛᴜs
**• /lang** - sᴇᴛ ᴄʜᴀᴛʙᴏᴛ ʟᴀɴɢᴜᴀɢᴇ
**• /chatlang** - ᴄʜᴇᴄᴋ ᴄᴜʀʀᴇɴᴛ ʟᴀɴɢᴜᴀɢᴇ
**• /resetlang** - ʀᴇsᴇᴛ ʟᴀɴɢᴜᴀɢᴇ ᴛᴏ ᴅᴇғᴀᴜʟᴛ"""

TOOLS_DATA_READ = """**🛠️ ᴛᴏᴏʟs ᴀɴᴅ ᴜᴛɪʟɪᴛɪᴇs**

**ᴀᴅᴅɪᴛɪᴏɴᴀʟ ᴛᴏᴏʟs ᴀᴠᴀɪʟᴀʙʟᴇ:**

**• /ping** - ᴄʜᴇᴄᴋ ʙᴏᴛ ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ
**• /id** - ɢᴇᴛ ʏᴏᴜʀ ᴜsᴇʀ ɪᴅ
**• /shayri** - ɢᴇᴛ ʀᴀɴᴅᴏᴍ sʜᴀʏʀɪ
**• /repo** - ɢᴇᴛ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ"""

# Storage function
def storeai():
    """Placeholder for store AI function"""
    pass

# Helper function to check if user is owner
def is_owner(user_id: int) -> bool:
    """Check if user is bot owner"""
    from config import OWNER_ID
    return user_id == int(OWNER_ID)

# Helper function for handling command decorators
def on_cmd(commands, group=0):
    """Decorator for command handlers"""
    from pyrogram import filters
    return filters.command(commands) & filters.group if group else filters.command(commands)
