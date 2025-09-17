# File: config.py 

"""
🚀 ULTIMATE AI GIRLFRIEND CHATBOT CONFIGURATION
World-class implementation with Indian personality and Hinglish support
Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Helper function to get environment variables with validation
def get_env_var(var_name: str, default_value=None, required: bool = True):
    """
    Get environment variable with proper error handling
    
    Args:
        var_name (str): Environment variable name
        default_value: Default value if not found
        required (bool): Whether the variable is required
    
    Returns:
        Variable value or default
    """
    value = os.getenv(var_name, default_value)
    
    if required and not value:
        print(f"❌ Error: Required environment variable '{var_name}' not found!")
        print(f"💡 Please set {var_name} in your .env file")
        if var_name in ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "OWNER_ID"]:
            print("🔧 Check .env.example for reference")
        sys.exit(1)
    
    return value

# ===============================================
# 🔧 BASIC CONFIGURATION
# ===============================================

# Telegram API Configuration (Required)
try:
    API_ID = int(get_env_var("API_ID", "25387587"))
except ValueError:
    print("❌ Error: API_ID must be a number")
    sys.exit(1)

API_HASH = get_env_var("API_HASH", "7b8e2e5bb84c617a474656ad7439ea6a")

# Bot Token (Required)
BOT_TOKEN = get_env_var("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ Error: BOT_TOKEN is required!")
    print("💡 Get bot token from @BotFather")
    sys.exit(1)

# String Session (Optional)
STRING1 = get_env_var("STRING_SESSION", required=False)
STRING_SESSION = STRING1  # Alias for compatibility

# Database Configuration (Required)
MONGO_URL = get_env_var("MONGO_URL")
if not MONGO_URL:
    print("❌ Error: MONGO_URL is required!")
    print("💡 Get free MongoDB from https://cloud.mongodb.com/")
    sys.exit(1)

# Owner Configuration (Required)
try:
    OWNER_ID = int(get_env_var("OWNER_ID", "7784241637"))
except ValueError:
    print("❌ Error: OWNER_ID must be a number")
    sys.exit(1)

OWNER_USERNAME = get_env_var("OWNER_USERNAME", "SID_ELITE", required=False)

# Support & Updates Configuration (Optional)
SUPPORT_GRP = get_env_var("SUPPORT_GRP", "TeamsXchat", required=False)
UPDATE_CHNL = get_env_var("UPDATE_CHNL", "TeamXUpdate", required=False)

# ===============================================
# 🚀 ENHANCED AI GIRLFRIEND CONFIGURATION
# ===============================================

# AI Configuration - Enhanced for Indian Personality
ENABLE_AI_CHAT = get_env_var("ENABLE_AI_CHAT", "True", required=False).lower() == "true"
AI_PERSONALITY = get_env_var("AI_PERSONALITY", "indian_girlfriend", required=False)
MAX_AI_TOKENS = int(get_env_var("MAX_AI_TOKENS", "200", required=False))  # Increased for better responses

# Indian Personality Settings
ENABLE_HINGLISH = get_env_var("ENABLE_HINGLISH", "True", required=False).lower() == "true"
INDIAN_ACCENT = get_env_var("INDIAN_ACCENT", "True", required=False).lower() == "true"
MUMBAI_REFERENCES = get_env_var("MUMBAI_REFERENCES", "True", required=False).lower() == "true"

# Virtual Life Simulation
ENABLE_VIRTUAL_LIFE = get_env_var("ENABLE_VIRTUAL_LIFE", "True", required=False).lower() == "true"
DAILY_MOOD_CHANGES = get_env_var("DAILY_MOOD_CHANGES", "True", required=False).lower() == "true"
TIME_BASED_RESPONSES = get_env_var("TIME_BASED_RESPONSES", "True", required=False).lower() == "true"

# Voice Messages Configuration - Enhanced
ENABLE_VOICE_MESSAGES = get_env_var("ENABLE_VOICE_MESSAGES", "True", required=False).lower() == "true"
VOICE_LANGUAGE = get_env_var("VOICE_LANGUAGE", "en", required=False)
VOICE_ACCENT = get_env_var("VOICE_ACCENT", "co.in", required=False)  # Indian accent
VOICE_SCENARIOS = get_env_var("VOICE_SCENARIOS", "romantic,morning,night,caring", required=False).split(",")

# Anime Pictures Configuration - Enhanced
ENABLE_ANIME_PICS = get_env_var("ENABLE_ANIME_PICS", "True", required=False).lower() == "true"
ANIME_API_SOURCES = get_env_var("ANIME_API_SOURCES", "waifu.pics,nekos.best,waifu.im", required=False).split(",")
PICTURE_RESPONSE_STYLE = get_env_var("PICTURE_RESPONSE_STYLE", "indian_girl", required=False)

# Sticker System Configuration
ENABLE_SMART_STICKERS = get_env_var("ENABLE_SMART_STICKERS", "True", required=False).lower() == "true"
STICKER_EMOTIONS = get_env_var("STICKER_EMOTIONS", "happy,shy,romantic,playful,caring", required=False).split(",")
CONTEXTUAL_STICKER_CHANCE = float(get_env_var("CONTEXTUAL_STICKER_CHANCE", "0.35", required=False))

# Relationship System Configuration
ENABLE_RELATIONSHIP_SYSTEM = get_env_var("ENABLE_RELATIONSHIP_SYSTEM", "True", required=False).lower() == "true"
MAX_RELATIONSHIP_LEVEL = int(get_env_var("MAX_RELATIONSHIP_LEVEL", "5", required=False))
RELATIONSHIP_PROGRESSION_RATE = float(get_env_var("RELATIONSHIP_PROGRESSION_RATE", "0.12", required=False))

# Random Interactions Configuration
ENABLE_RANDOM_INTERACTIONS = get_env_var("ENABLE_RANDOM_INTERACTIONS", "True", required=False).lower() == "true"
RANDOM_INTERACTION_CHANCE = float(get_env_var("RANDOM_INTERACTION_CHANCE", "0.02", required=False))
PROACTIVE_CONVERSATIONS = get_env_var("PROACTIVE_CONVERSATIONS", "True", required=False).lower() == "true"

# Identity & Creator Attribution
BOT_IDENTITY_DENIAL = get_env_var("BOT_IDENTITY_DENIAL", "True", required=False).lower() == "true"
CREATOR_NAME = get_env_var("CREATOR_NAME", "Siddhartha Abhimanyu", required=False)
CREATOR_USERNAME = get_env_var("CREATOR_USERNAME", "@SID_ELITE", required=False)
CREATOR_TITLE = get_env_var("CREATOR_TITLE", "Tech Leader of Team X", required=False)

# ===============================================
# 🌍 LANGUAGE & LOCALIZATION
# ===============================================

# Primary language settings
DEFAULT_LANGUAGE = get_env_var("DEFAULT_LANGUAGE", "hinglish", required=False)
ENABLE_AUTO_LANG_DETECT = get_env_var("ENABLE_AUTO_LANG_DETECT", "True", required=False).lower() == "true"
SUPPORTED_LANGUAGES = get_env_var("SUPPORTED_LANGUAGES", "en,hi,hinglish", required=False).split(",")

# Indian Time Zone
TIMEZONE = get_env_var("TIMEZONE", "Asia/Kolkata", required=False)
TIMEZONE_COMMON_NAME = TIMEZONE

# ===============================================
# 📊 PERFORMANCE & LIMITS
# ===============================================

# Log Group (Optional)
LOG_GROUP_ID = get_env_var("LOG_GROUP_ID", required=False)
if LOG_GROUP_ID:
    try:
        LOG_GROUP_ID = int(LOG_GROUP_ID)
    except ValueError:
        LOG_GROUP_ID = None

# Rate Limiting - Enhanced for girlfriend personality
RATE_LIMIT_MESSAGES = int(get_env_var("RATE_LIMIT_MESSAGES", "6", required=False))  # More lenient for girlfriend
RATE_LIMIT_WINDOW = int(get_env_var("RATE_LIMIT_WINDOW", "4", required=False))  # 4 seconds window
RELATIONSHIP_RATE_BONUS = int(get_env_var("RELATIONSHIP_RATE_BONUS", "2", required=False))  # Extra messages for higher relationship

# Clone Bot Configuration
MAX_CLONES_PER_USER = int(get_env_var("MAX_CLONES_PER_USER", "5", required=False))
ALLOW_BOT_CLONING = get_env_var("ALLOW_BOT_CLONING", "True", required=False).lower() == "true"

# Broadcast Configuration
BROADCAST_DELAY = float(get_env_var("BROADCAST_DELAY", "0.1", required=False))
MAX_BROADCAST_MESSAGES = int(get_env_var("MAX_BROADCAST_MESSAGES", "1000", required=False))

# ===============================================
# 🔒 SECURITY & AUTHORIZATION
# ===============================================

# Authorized users
AUTHORIZED_USERS = get_env_var("AUTHORIZED_USERS", required=False)
if AUTHORIZED_USERS:
    try:
        AUTHORIZED_USERS = [int(user_id.strip()) for user_id in AUTHORIZED_USERS.split(",")]
    except ValueError:
        AUTHORIZED_USERS = []
else:
    AUTHORIZED_USERS = []

# Add owner to authorized users
if OWNER_ID not in AUTHORIZED_USERS:
    AUTHORIZED_USERS.append(OWNER_ID)

# ===============================================
# 🗄️ DATABASE CONFIGURATION
# ===============================================

# Database collection names
DB_NAME = get_env_var("DB_NAME", "Anonymous", required=False)
CHATS_COLLECTION = get_env_var("CHATS_COLLECTION", "chats", required=False)
USERS_COLLECTION = get_env_var("USERS_COLLECTION", "users", required=False)
CLONES_COLLECTION = get_env_var("CLONES_COLLECTION", "clones", required=False)
RELATIONSHIPS_COLLECTION = get_env_var("RELATIONSHIPS_COLLECTION", "relationships", required=False)
VOICE_CACHE_COLLECTION = get_env_var("VOICE_CACHE_COLLECTION", "voice_cache", required=False)

# Database performance
MONGODB_MAX_CONNECTIONS = int(get_env_var("MONGODB_MAX_CONNECTIONS", "100", required=False))
CONCURRENT_UPDATES = get_env_var("CONCURRENT_UPDATES", "True", required=False).lower() == "true"

# ===============================================
# 🎭 PERSONALITY PRESETS
# ===============================================

# Indian Girlfriend Personality Configuration
PERSONALITY_TRAITS = {
    "indian_girlfriend": {
        "name": "Ena",
        "age": 22,
        "location": "Mumbai",
        "language_style": "hinglish",
        "personality_type": "caring_romantic",
        "energy_level": 80,
        "flirt_level": 70,
        "intelligence": 85,
        "humor": 75,
        "supportiveness": 90
    }
}

# Mood system configuration
MOOD_SYSTEM = {
    "enable_mood_changes": True,
    "time_based_moods": True,
    "weather_awareness": False,  # Future feature
    "mood_persistence": True,
    "mood_sharing": True  # Share mood with users
}

# Daily life simulation
VIRTUAL_LIFE_CONFIG = {
    "has_job": True,
    "job_type": "software_developer",  # Relatable to tech audience
    "has_family": True,
    "has_friends": True,
    "daily_activities": True,
    "random_events": True,
    "life_problems": True,
    "achievements": True
}

# ===============================================
# 🎨 FEATURE FLAGS
# ===============================================

# Core features
ENABLE_CLONE_FEATURE = get_env_var("ENABLE_CLONE_FEATURE", "True", required=False).lower() == "true"
ENABLE_BROADCAST_FEATURE = get_env_var("ENABLE_BROADCAST_FEATURE", "True", required=False).lower() == "true"
ENABLE_CHATBOT_FEATURE = get_env_var("ENABLE_CHATBOT_FEATURE", "True", required=False).lower() == "true"
ENABLE_LANGUAGE_DETECTION = get_env_var("ENABLE_LANGUAGE_DETECTION", "True", required=False).lower() == "true"

# Advanced features
ENABLE_LEARNING_SYSTEM = get_env_var("ENABLE_LEARNING_SYSTEM", "True", required=False).lower() == "true"
ENABLE_CONTEXT_MEMORY = get_env_var("ENABLE_CONTEXT_MEMORY", "True", required=False).lower() == "true"
ENABLE_EMOTIONAL_INTELLIGENCE = get_env_var("ENABLE_EMOTIONAL_INTELLIGENCE", "True", required=False).lower() == "true"

# ===============================================
# 🚀 DEPLOYMENT CONFIGURATION
# ===============================================

# Advanced Configuration
WEBHOOK_URL = get_env_var("WEBHOOK_URL", required=False)
PORT = int(get_env_var("PORT", "8080"))
HEROKU_APP_NAME = get_env_var("HEROKU_APP_NAME", required=False)

# Debug Configuration
DEBUG = get_env_var("DEBUG", "False", required=False).lower() == "true"
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

# ===============================================
# 🔗 BACKWARDS COMPATIBILITY
# ===============================================

# Maintain compatibility with original config
SUPPORT_CHAT = SUPPORT_GRP
UPDATE_CHANNEL = UPDATE_CHNL

# Legacy OpenRouter configuration (now using lexica-api)
OPENROUTER_API_KEY = None  # Not needed anymore - using free lexica-api
OPENROUTER_MODEL = None    # Using multiple lexica models

# ===============================================
# ✅ CONFIGURATION VALIDATION
# ===============================================

def validate_config():
    """Validate configuration settings"""
    errors = []
    warnings = []
    
    # Basic validation
    if len(str(API_ID)) < 7:
        errors.append("API_ID seems invalid (too short)")
    
    if len(API_HASH) != 32:
        errors.append("API_HASH seems invalid (should be 32 characters)")
    
    if not BOT_TOKEN or ":" not in BOT_TOKEN:
        errors.append("BOT_TOKEN seems invalid")
    
    if not MONGO_URL.startswith(("mongodb://", "mongodb+srv://")):
        errors.append("MONGO_URL seems invalid")
    
    # Enhanced validation warnings
    if not ENABLE_AI_CHAT:
        warnings.append("AI Chat is disabled - bot will use basic responses only")
    
    if not ENABLE_HINGLISH:
        warnings.append("Hinglish support is disabled - Indian users may prefer Hinglish")
        
    if not ENABLE_VOICE_MESSAGES:
        warnings.append("Voice messages are disabled - missing key girlfriend feature")
    
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   • {error}")
        sys.exit(1)
    
    if warnings:
        print("⚠️  Configuration warnings:")
        for warning in warnings:
            print(f"   • {warning}")
        print()

# ===============================================
# 🎯 CONFIGURATION SUMMARY
# ===============================================

def print_config_summary():
    """Print configuration summary"""
    if DEBUG:
        print("🚀 Ultimate AI Girlfriend ChatBot Configuration:")
        print("=" * 60)
        print(f"   🤖 Bot Identity: Indian Girlfriend (Ena)")
        print(f"   📍 Location: Mumbai, India")
        print(f"   🗣️  Language: Hinglish (Hindi + English)")
        print(f"   👨‍💻 Creator: {CREATOR_NAME} ({CREATOR_USERNAME})")
        print(f"   🏢 Team: {CREATOR_TITLE}")
        print("=" * 60)
        print(f"   🧠 AI System: lexica-api (FREE unlimited)")
        print(f"   🎭 Personality: {AI_PERSONALITY}")
        print(f"   🔊 Voice Messages: {'✅ Enabled' if ENABLE_VOICE_MESSAGES else '❌ Disabled'}")
        print(f"   📸 Anime Pictures: {'✅ Enabled' if ENABLE_ANIME_PICS else '❌ Disabled'}")
        print(f"   🎯 Smart Stickers: {'✅ Enabled' if ENABLE_SMART_STICKERS else '❌ Disabled'}")
        print(f"   💕 Relationship System: {'✅ Enabled' if ENABLE_RELATIONSHIP_SYSTEM else '❌ Disabled'}")
        print(f"   🎲 Random Interactions: {'✅ Enabled' if ENABLE_RANDOM_INTERACTIONS else '❌ Disabled'}")
        print(f"   🕐 Virtual Life: {'✅ Enabled' if ENABLE_VIRTUAL_LIFE else '❌ Disabled'}")
        print("=" * 60)
        print(f"   📊 Database: {'✅ Connected' if MONGO_URL else '❌ Not configured'}")
        print(f"   👤 Owner ID: {OWNER_ID}")
        print(f"   🌍 Timezone: {TIMEZONE}")
        print(f"   🔧 Debug Mode: {'✅ On' if DEBUG else '❌ Off'}")
        print("=" * 60)
        print("   🚀 System ready for world-class girlfriend experience!")
        print()

# Run validation and summary
validate_config()
print_config_summary()

# ===============================================
# 💡 USAGE TIPS
# ===============================================

if DEBUG:
    print("💡 Configuration Tips:")
    print("   • Set ENABLE_AI_CHAT=True for best experience")
    print("   • Use ENABLE_HINGLISH=True for Indian users")
    print("   • Enable voice messages for realistic girlfriend feel")
    print("   • Anime pictures make photo requests more engaging")
    print("   • Relationship system creates deeper user connections")
    print("   • Virtual life simulation makes conversations realistic")
    print()

LOGGER_CONFIG = {
    "level": LOG_LEVEL,
    "format": "[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    "datefmt": "%d-%b-%y %H:%M:%S"
}

# Export all configurations for easy import
__all__ = [
    # Basic config
    "API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "OWNER_ID", 
    "OWNER_USERNAME", "SUPPORT_GRP", "UPDATE_CHNL",
    
    # Enhanced AI config
    "ENABLE_AI_CHAT", "AI_PERSONALITY", "MAX_AI_TOKENS",
    "ENABLE_HINGLISH", "INDIAN_ACCENT", "MUMBAI_REFERENCES",
    
    # Features config
    "ENABLE_VOICE_MESSAGES", "ENABLE_ANIME_PICS", "ENABLE_SMART_STICKERS",
    "ENABLE_RELATIONSHIP_SYSTEM", "ENABLE_RANDOM_INTERACTIONS",
    "ENABLE_VIRTUAL_LIFE", "BOT_IDENTITY_DENIAL",
    
    # Creator config
    "CREATOR_NAME", "CREATOR_USERNAME", "CREATOR_TITLE",
    
    # Performance config
    "RATE_LIMIT_MESSAGES", "RATE_LIMIT_WINDOW", "DEBUG",
    
    # Personality config
    "PERSONALITY_TRAITS", "MOOD_SYSTEM", "VIRTUAL_LIFE_CONFIG"
]

# ===============================================
# 🎭 AI PERSONALITIES CONFIGURATION
# ===============================================

# AI Personality options for the Commands module
AI_PERSONALITIES = {
    "indian_girlfriend": {
        "name": "Ena",
        "description": "Sweet Indian girlfriend with Hinglish support",
        "traits": ["caring", "romantic", "flirty", "supportive"],
        "language": "hinglish"
    },
    "girlfriend": {
        "name": "Ena", 
        "description": "Caring girlfriend personality",
        "traits": ["loving", "supportive", "understanding"],
        "language": "english"
    },
    "cute": {
        "name": "Ena",
        "description": "Cute and playful personality", 
        "traits": ["playful", "cute", "fun", "energetic"],
        "language": "hinglish"
    },
    "romantic": {
        "name": "Ena",
        "description": "Extra romantic and loving",
        "traits": ["romantic", "passionate", "loving", "intimate"],
        "language": "hinglish"
    }
}

# Default personality for the bot
DEFAULT_AI_PERSONALITY = "indian_girlfriend"
