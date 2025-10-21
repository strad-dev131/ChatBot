# EnaChatBot/__init__.py - COMPLETE & WORKING VERSION

"""
🚀 ULTIMATE AI GIRLFRIEND CHATBOT - Enhanced Package Initialization
World-class implementation with Indian personality and Hinglish support
Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X
"""

import logging
import time
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client
from pyrogram.enums import ParseMode
import config
import uvloop

# Try to import Abg, if not available create patch function
try:
    from Abg import patch
except ImportError:
    def patch(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

ID_CHATBOT = None
CLONE_OWNERS = {}
uvloop.install()

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

boot = time.time()
mongodb = MongoCli(config.MONGO_URL)
db = mongodb.Anonymous
mongo = MongoClient(config.MONGO_URL)
OWNER = config.OWNER_ID
_boot_ = time.time()

clonedb = None

# Use proper MongoDB collections without overriding the database object
cloneownerdb = db.clone_owners

# -------------- CLONE OWNER FUNCTIONS -------------- #

async def load_clone_owners():
    try:
        async for entry in cloneownerdb.find():
            bot_id = entry["bot_id"]
            user_id = entry["user_id"]
            CLONE_OWNERS[bot_id] = user_id
    except:
        pass

async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.update_one(
        {"bot_id": bot_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def get_clone_owner(bot_id):
    data = await cloneownerdb.find_one({"bot_id": bot_id})
    if data:
        return data["user_id"]
    return None

async def delete_clone_owner(bot_id):
    await cloneownerdb.delete_one({"bot_id": bot_id})
    CLONE_OWNERS.pop(bot_id, None)

async def save_idclonebot_owner(clone_id, user_id):
    await cloneownerdb.update_one(
        {"clone_id": clone_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def get_idclone_owner(clone_id):
    data = await cloneownerdb.find_one({"clone_id": clone_id})
    if data:
        return data["user_id"]
    return None

# ---------------- BOT CLASS ---------------- #

class EnaChatBot(Client):
    def __init__(self):
        super().__init__(
            name="EnaChatBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.DEFAULT,
        )

        # default values (agar start se pehle access hua to crash na ho)
        self.id = None
        self.name = None
        self.username = "UnknownBot"
        self.mention = "Bot"

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.id = me.id
        self.name = me.first_name + " " + (me.last_name or "")
        self.username = me.username or "EnaChatBot"
        self.mention = me.mention

    async def stop(self):
        await super().stop()

# ---------------- UTILS ---------------- #

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]

    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

# ---------------- INIT OBJECTS ---------------- #

# Fixed: Proper initialization
EnaChatBot = EnaChatBot()

# Fixed: Create userbot client properly
if getattr(config, "STRING_SESSION", ""):
    userbot = Client(
        name="userbot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.STRING_SESSION,
        in_memory=True
    )
else:
    userbot = None

# ===============================================
# 🚀 ENHANCED IMPORTS FOR AI GIRLFRIEND SYSTEM
# ===============================================

# Enhanced AI system imports with error handling
try:
    from .openrouter_ai import get_ai_response, get_flirty_response, get_cute_response
    LOGGER.info("✅ Ultimate AI girlfriend system imported successfully")
    AI_SYSTEM_AVAILABLE = True
except ImportError as e:
    LOGGER.warning(f"⚠️ Ultimate AI system not available: {e}")
    AI_SYSTEM_AVAILABLE = False

# Voice and media imports
try:
    from gtts import gTTS
    VOICE_SYSTEM_AVAILABLE = True
    LOGGER.info("✅ Voice message system available")
except ImportError as e:
    LOGGER.warning(f"⚠️ Voice system not available: {e}")
    VOICE_SYSTEM_AVAILABLE = False

# Enhanced features flag
ENHANCED_FEATURES = {
    "ai_system": AI_SYSTEM_AVAILABLE,
    "voice_messages": VOICE_SYSTEM_AVAILABLE,
    "hinglish_support": True,  # Always available
    "indian_personality": True,  # Always available
    "relationship_system": True,  # Always available
    "virtual_life": True  # Always available
}

LOGGER.info("🚀 Enhanced ChatBot initialization completed!")
LOGGER.info(f"💕 Features available: {sum(ENHANCED_FEATURES.values())}/{len(ENHANCED_FEATURES)}")

if AI_SYSTEM_AVAILABLE:
    LOGGER.info("✨ World-class AI girlfriend system ready!")
else:
    LOGGER.warning("⚠️ Running with basic responses - install lexica-api for full features")

# System information
SYSTEM_INFO = {
    "version": "2.0.0-ultimate",
    "creator": "@SID_ELITE (Siddhartha Abhimanyu)",
    "team": "Team X Technologies",
    "personality": "Indian Girlfriend (Ena)",
    "language_support": "Hinglish + English + Hindi",
    "ai_models": "GPT, Gemini, Bard, LLaMA, Mistral" if AI_SYSTEM_AVAILABLE else "Offline only",
    "features": "Voice Messages, Anime Pictures, Smart Stickers, Relationship System"
}

LOGGER.info("=" * 60)
LOGGER.info("🤖 Ultimate AI Girlfriend ChatBot System")
LOGGER.info(f"👨‍💻 Created by: {SYSTEM_INFO['creator']}")
LOGGER.info(f"🏢 Team: {SYSTEM_INFO['team']}")
LOGGER.info(f"🎭 Personality: {SYSTEM_INFO['personality']}")
LOGGER.info(f"🗣️ Languages: {SYSTEM_INFO['language_support']}")
LOGGER.info(f"🧠 AI Models: {SYSTEM_INFO['ai_models']}")
LOGGER.info(f"✨ Features: {SYSTEM_INFO['features']}")
LOGGER.info("=" * 60)

# ===============================================
# 🔧 CRITICAL FIX: Custom Decorators - WORKING VERSION
# ===============================================

import pyrogram.handlers
from pyrogram import filters

# Command decorator class
class CommandDecorator:
    def __init__(self, bot_instance):
        self.bot = bot_instance
    
    def __call__(self, commands, group=0):
        def decorator(func):
            try:
                # Create command filters
                if isinstance(commands, str):
                    command_list = [commands]
                else:
                    command_list = commands
                    
                # Create the filter for commands
                cmd_filter = filters.command(command_list) & ~filters.bot
                
                # Register the handler
                self.bot.add_handler(
                    pyrogram.handlers.MessageHandler(func, cmd_filter),
                    group=group
                )
                LOGGER.info(f"✅ Registered command handler: {command_list}")
                return func
            except Exception as e:
                LOGGER.error(f"❌ Error registering command {commands}: {e}")
                return func
        return decorator

# Message decorator class
class MessageDecorator:
    def __init__(self, bot_instance):
        self.bot = bot_instance
    
    def __call__(self, filters_param=None, group=0):
        def decorator(func):
            try:
                self.bot.add_handler(
                    pyrogram.handlers.MessageHandler(func, filters_param),
                    group=group
                )
                return func
            except Exception as e:
                LOGGER.error(f"❌ Error registering message handler: {e}")
                return func
        return decorator

# Callback decorator class
class CallbackDecorator:
    def __init__(self, bot_instance):
        self.bot = bot_instance
    
    def __call__(self, filters_param=None, group=0):
        def decorator(func):
            try:
                from pyrogram.handlers import CallbackQueryHandler
                self.bot.add_handler(
                    CallbackQueryHandler(func, filters_param),
                    group=group
                )
                return func
            except Exception as e:
                LOGGER.error(f"❌ Error registering callback handler: {e}")
                return func
        return decorator

# ===============================================
# 🎯 ATTACH DECORATORS TO BOT INSTANCE
# ===============================================

# Attach decorators to the EnaChatBot instance
try:
    EnaChatBot.on_cmd = CommandDecorator(EnaChatBot)
    EnaChatBot.on_message = MessageDecorator(EnaChatBot)
    EnaChatBot.on_callback_query = CallbackDecorator(EnaChatBot)
    
    LOGGER.info("✅ Custom decorators attached successfully")
except Exception as e:
    LOGGER.error(f"❌ Error attaching decorators: {e}")

# ===============================================
# 🌟 ADDITIONAL HELPER FUNCTIONS
# ===============================================

async def is_owner(user_id):
    """Check if user is the bot owner"""
    return user_id == config.OWNER_ID

async def is_sudo(user_id):
    """Check if user is a sudo user"""
    return user_id in getattr(config, 'SUDO_USERS', []) or user_id == config.OWNER_ID

def format_time(seconds):
    """Format time in a readable format"""
    return get_readable_time(seconds)

# ===============================================
# 🚀 COMPATIBILITY EXPORTS
# ===============================================

# Export important variables for modules
__all__ = [
    'EnaChatBot', 'userbot', 'LOGGER', 'db', 'mongodb', 'mongo',
    'OWNER', 'CLONE_OWNERS', 'load_clone_owners', 'save_clonebot_owner',
    'get_clone_owner', 'delete_clone_owner', 'save_idclonebot_owner',
    'get_idclone_owner', 'get_readable_time', 'is_owner', 'is_sudo',
    'format_time', 'AI_SYSTEM_AVAILABLE', 'VOICE_SYSTEM_AVAILABLE',
    'ENHANCED_FEATURES', 'SYSTEM_INFO'
]

# ===============================================
# 🎉 INITIALIZATION COMPLETE
# ===============================================

LOGGER.info("🎉 EnaChatBot package initialization completed successfully!")
LOGGER.info("💕 Ready to serve as the ultimate AI girlfriend!")
LOGGER.info("✨ All systems operational - Ena is ready to chat!")

# Final status check
if AI_SYSTEM_AVAILABLE and VOICE_SYSTEM_AVAILABLE:
    LOGGER.info("🏆 FULL FEATURE MODE: All advanced features available!")
elif AI_SYSTEM_AVAILABLE:
    LOGGER.info("🤖 AI MODE: AI features available, voice disabled")
else:
    LOGGER.info("💬 BASIC MODE: Using fallback responses only")
