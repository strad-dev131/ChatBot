# ===============================================
# 🤖 EnaChatBot - Ultimate Realistic Indian AI Girl
# Complete Configuration File - 100% Working
# Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X
# ===============================================

import os
import logging
from datetime import datetime, timedelta

# ===============================================
# 🔧 ESSENTIAL FUNCTIONS & SETUP
# ===============================================

def get_env_var(key: str, default=None, required: bool = False):
    """Get environment variable with validation"""
    value = os.getenv(key, default)
    if required and (value is None or value == ''):
        raise ValueError(f"Environment variable {key} is required but not set.")
    return value

def to_bool(value):
    """Convert string to boolean"""
    if isinstance(value, bool):
        return value
    return str(value).lower() in ('true', '1', 'yes', 'on')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ===============================================
# 🔑 TELEGRAM API CREDENTIALS (REQUIRED)
# ===============================================

# Telegram API Configuration (Get from my.telegram.org)
API_ID = int(get_env_var("API_ID", None, required=True))
API_HASH = get_env_var("API_HASH", None, required=True)

# Bot Token (Get from @BotFather)
BOT_TOKEN = get_env_var("BOT_TOKEN", None, required=True)

# Database Configuration (MongoDB Atlas - Free)
MONGO_URL = get_env_var("MONGO_URL", None, required=True)
# Optional: Multiple MongoDB URIs (comma-separated) for redundancy/replication
MONGO_URLS = [u.strip() for u in get_env_var("MONGO_URLS", "").split(",") if u.strip()]

# Owner Configuration (Your Telegram user ID from @userinfobot)
OWNER_ID = int(get_env_var("OWNER_ID", None, required=True))
OWNER_USERNAME = get_env_var("OWNER_USERNAME", "SID_ELITE")

# Optional String Session for userbot features
STRING_SESSION = get_env_var("STRING_SESSION", "")

# Support Configuration
SUPPORT_GRP = get_env_var("SUPPORT_GRP", "TeamsXchat")
UPDATE_CHNL = get_env_var("UPDATE_CHNL", "TeamXUpdate")
LOG_GROUP_ID = get_env_var("LOG_GROUP_ID", "")

# ===============================================
# 🎯 REALISTIC BEHAVIOR CONFIGURATION
# Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X
# ===============================================

# ===============================================
# 🎭 REALISTIC RELATIONSHIP SYSTEM SETTINGS
# ===============================================

# Core Realistic Behavior Settings
ENABLE_RELATIONSHIP_PROGRESSION = get_env_var("ENABLE_RELATIONSHIP_PROGRESSION", "True").lower() == "true"
ENABLE_SMART_LEARNING = get_env_var("ENABLE_SMART_LEARNING", "True").lower() == "true"
ENABLE_CONTEXT_MEMORY = get_env_var("ENABLE_CONTEXT_MEMORY", "True").lower() == "true"
NO_INSTANT_ROMANCE = get_env_var("NO_INSTANT_ROMANCE", "True").lower() == "true"
ENABLE_NATURAL_BOUNDARIES = get_env_var("ENABLE_NATURAL_BOUNDARIES", "True").lower() == "true"

# Relationship Progression Control
RELATIONSHIP_PROGRESSION_SPEED = get_env_var("RELATIONSHIP_PROGRESSION_SPEED", "normal")
MINIMUM_MESSAGES_FOR_FRIEND = int(get_env_var("MINIMUM_MESSAGES_FOR_FRIEND", "15"))
MINIMUM_MESSAGES_FOR_ROMANTIC = int(get_env_var("MINIMUM_MESSAGES_FOR_ROMANTIC", "120"))
MINIMUM_DAYS_FOR_ROMANTIC = int(get_env_var("MINIMUM_DAYS_FOR_ROMANTIC", "21"))

# Advanced Boundary System (Like Real Indian Girls)
PHOTOS_ONLY_FOR_FRIENDS = get_env_var("PHOTOS_ONLY_FOR_FRIENDS", "True").lower() == "true"
VOICE_ONLY_FOR_CLOSE_FRIENDS = get_env_var("VOICE_ONLY_FOR_CLOSE_FRIENDS", "True").lower() == "true"
CONTEXTUAL_RESPONSES = get_env_var("CONTEXTUAL_RESPONSES", "True").lower() == "true"
STRANGER_CAUTION_MODE = get_env_var("STRANGER_CAUTION_MODE", "True").lower() == "true"

# Smart Learning System Settings
LEARN_USER_INTERESTS = get_env_var("LEARN_USER_INTERESTS", "True").lower() == "true"
ADAPT_COMMUNICATION_STYLE = get_env_var("ADAPT_COMMUNICATION_STYLE", "True").lower() == "true"
PERSONALITY_ANALYSIS = get_env_var("PERSONALITY_ANALYSIS", "True").lower() == "true"
EMOTIONAL_STATE_TRACKING = get_env_var("EMOTIONAL_STATE_TRACKING", "True").lower() == "true"
CONVERSATION_CONTEXT_MEMORY = get_env_var("CONVERSATION_CONTEXT_MEMORY", "True").lower() == "true"

# Natural Conversation Flow Settings
MAX_RESPONSE_LENGTH = int(get_env_var("MAX_RESPONSE_LENGTH", "200"))
NATURAL_RESPONSE_DELAY = float(get_env_var("NATURAL_RESPONSE_DELAY", "2.5"))
GROUP_RESPONSE_CHANCE = float(get_env_var("GROUP_RESPONSE_CHANCE", "0.05"))
ENABLE_REALISTIC_TYPING = get_env_var("ENABLE_REALISTIC_TYPING", "True").lower() == "true"

# ===============================================
# 🇮🇳 AUTHENTIC INDIAN PERSONALITY SETTINGS
# ===============================================

# Cultural Authenticity Settings
AUTHENTIC_INDIAN_BEHAVIOR = get_env_var("AUTHENTIC_INDIAN_BEHAVIOR", "True").lower() == "true"
MUMBAI_LIFESTYLE_REFERENCES = get_env_var("MUMBAI_LIFESTYLE_REFERENCES", "True").lower() == "true"
BOLLYWOOD_REFERENCES = get_env_var("BOLLYWOOD_REFERENCES", "True").lower() == "true"
HINGLISH_PRIMARY = get_env_var("HINGLISH_PRIMARY", "True").lower() == "true"
FAMILY_ORIENTED_VALUES = get_env_var("FAMILY_ORIENTED_VALUES", "True").lower() == "true"
INDIAN_FESTIVAL_AWARENESS = get_env_var("INDIAN_FESTIVAL_AWARENESS", "True").lower() == "true"

# Language and Communication Settings
DEFAULT_LANGUAGE = get_env_var("DEFAULT_LANGUAGE", "hinglish")
ENABLE_AUTO_LANG_DETECT = get_env_var("ENABLE_AUTO_LANG_DETECT", "True").lower() == "true"
CULTURAL_CONTEXT_AWARENESS = get_env_var("CULTURAL_CONTEXT_AWARENESS", "True").lower() == "true"
REGIONAL_SLANG_MUMBAI = get_env_var("REGIONAL_SLANG_MUMBAI", "True").lower() == "true"
HINGLISH_RATIO = float(get_env_var("HINGLISH_RATIO", "0.6"))

# Enhanced AI Personality Configuration
AI_PERSONALITY = get_env_var("AI_PERSONALITY", "realistic_indian_girl")
ENABLE_AI_CHAT = get_env_var("ENABLE_AI_CHAT", "True").lower() == "true"
ENABLE_HINGLISH = get_env_var("ENABLE_HINGLISH", "True").lower() == "true"
INDIAN_ACCENT_VOICE = get_env_var("INDIAN_ACCENT_VOICE", "True").lower() == "true"

# Creator Attribution Settings (CRITICAL - Don't change!)
BOT_IDENTITY_DENIAL = get_env_var("BOT_IDENTITY_DENIAL", "True").lower() == "true"
CREATOR_NAME = get_env_var("CREATOR_NAME", "Siddhartha Abhimanyu")
CREATOR_USERNAME = get_env_var("CREATOR_USERNAME", "@SID_ELITE")
CREATOR_TITLE = get_env_var("CREATOR_TITLE", "Tech Leader of Team X")
CREATOR_COMPANY = get_env_var("CREATOR_COMPANY", "Team X Technologies")

# Optional: OpenRouter.ai integration for premium LLMs
OPENROUTER_API_KEY = get_env_var("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = get_env_var("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_BASE_URL = get_env_var("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# ===============================================
# 🎭 ADVANCED PERSONALITY FEATURES
# ===============================================

# Voice Messages System Configuration
ENABLE_VOICE_MESSAGES = get_env_var("ENABLE_VOICE_MESSAGES", "True").lower() == "true"
VOICE_LANGUAGE = get_env_var("VOICE_LANGUAGE", "en")
VOICE_ACCENT = get_env_var("VOICE_ACCENT", "co.in")
VOICE_SCENARIOS = get_env_var("VOICE_SCENARIOS", "romantic,morning,night,caring,encouragement").split(',')
VOICE_RELATIONSHIP_MINIMUM = int(get_env_var("VOICE_RELATIONSHIP_MINIMUM", "4"))

# Anime Pictures & Media System
ENABLE_ANIME_PICS = get_env_var("ENABLE_ANIME_PICS", "True").lower() == "true"
ANIME_API_SOURCES = get_env_var("ANIME_API_SOURCES", "waifu.pics,nekos.best,waifu.im").split(',')
PICTURE_RESPONSE_STYLE = get_env_var("PICTURE_RESPONSE_STYLE", "indian_girl")
PICTURE_RELATIONSHIP_MINIMUM = int(get_env_var("PICTURE_RELATIONSHIP_MINIMUM", "3"))

# Smart Stickers System
ENABLE_SMART_STICKERS = get_env_var("ENABLE_SMART_STICKERS", "True").lower() == "true"
STICKER_EMOTIONS = get_env_var("STICKER_EMOTIONS", "happy,shy,romantic,playful,caring,excited,sleepy").split(',')
CONTEXTUAL_STICKER_CHANCE = float(get_env_var("CONTEXTUAL_STICKER_CHANCE", "0.35"))
STICKER_RELATIONSHIP_BASED = get_env_var("STICKER_RELATIONSHIP_BASED", "True").lower() == "true"

# Virtual Life Simulation Settings
ENABLE_VIRTUAL_LIFE = get_env_var("ENABLE_VIRTUAL_LIFE", "True").lower() == "true"
DAILY_MOOD_CHANGES = get_env_var("DAILY_MOOD_CHANGES", "True").lower() == "true"
TIME_BASED_RESPONSES = get_env_var("TIME_BASED_RESPONSES", "True").lower() == "true"
WORK_SCHEDULE_SIMULATION = get_env_var("WORK_SCHEDULE_SIMULATION", "True").lower() == "true"
WEEKEND_BEHAVIOR_CHANGE = get_env_var("WEEKEND_BEHAVIOR_CHANGE", "True").lower() == "true"
FESTIVAL_SPECIAL_RESPONSES = get_env_var("FESTIVAL_SPECIAL_RESPONSES", "True").lower() == "true"

# ===============================================
# 📊 INTERACTION & PERFORMANCE SETTINGS
# ===============================================

# Rate Limiting (Relationship-Based)
RATE_LIMIT_MESSAGES = int(get_env_var("RATE_LIMIT_MESSAGES", "6"))
RATE_LIMIT_WINDOW = int(get_env_var("RATE_LIMIT_WINDOW", "5"))
RELATIONSHIP_RATE_BONUS = int(get_env_var("RELATIONSHIP_RATE_BONUS", "2"))
ENABLE_RELATIONSHIP_RATE_SCALING = get_env_var("ENABLE_RELATIONSHIP_RATE_SCALING", "True").lower() == "true"

# Group Chat Behavior Settings
GROUP_SELECTIVE_RESPONSE = get_env_var("GROUP_SELECTIVE_RESPONSE", "True").lower() == "true"
GROUP_MENTION_REQUIRED = get_env_var("GROUP_MENTION_REQUIRED", "False").lower() == "true"
GROUP_RELATIONSHIP_PROGRESSION = get_env_var("GROUP_RELATIONSHIP_PROGRESSION", "True").lower() == "true"
GROUP_PUBLIC_BEHAVIOR = get_env_var("GROUP_PUBLIC_BEHAVIOR", "True").lower() == "true"

# Enhanced Bot Features Control
ENABLE_CLONE_FEATURE = get_env_var("ENABLE_CLONE_FEATURE", "True").lower() == "true"
ENABLE_BROADCAST_FEATURE = get_env_var("ENABLE_BROADCAST_FEATURE", "True").lower() == "true"
ENABLE_CHATBOT_FEATURE = get_env_var("ENABLE_CHATBOT_FEATURE", "True").lower() == "true"
MAX_CLONES_PER_USER = int(get_env_var("MAX_CLONES_PER_USER", "5"))
ENABLE_STATISTICS_TRACKING = get_env_var("ENABLE_STATISTICS_TRACKING", "True").lower() == "true"

# Database Performance Settings
MONGODB_MAX_CONNECTIONS = int(get_env_var("MONGODB_MAX_CONNECTIONS", "100"))
CONCURRENT_UPDATES = get_env_var("CONCURRENT_UPDATES", "True").lower() == "true"
ENABLE_RELATIONSHIP_ANALYTICS = get_env_var("ENABLE_RELATIONSHIP_ANALYTICS", "True").lower() == "true"
AUTO_CLEANUP_OLD_DATA = get_env_var("AUTO_CLEANUP_OLD_DATA", "False").lower() == "true"

# ===============================================
# 🌍 LOCALIZATION & TIME SETTINGS
# ===============================================

# Time Zone Configuration (Indian Standard Time)
TIMEZONE = get_env_var("TIMEZONE", "Asia/Kolkata")
TIMEZONE_COMMON_NAME = get_env_var("TIMEZONE_COMMON_NAME", "IST")
WORK_HOURS_START = int(get_env_var("WORK_HOURS_START", "9"))
WORK_HOURS_END = int(get_env_var("WORK_HOURS_END", "17"))
SLEEP_HOURS_START = int(get_env_var("SLEEP_HOURS_START", "23"))
WAKE_UP_HOURS = int(get_env_var("WAKE_UP_HOURS", "7"))

# Language Support Settings
SUPPORTED_LANGUAGES = get_env_var("SUPPORTED_LANGUAGES", "en,hi,hinglish").split(',')
ENABLE_LANGUAGE_ADAPTATION = get_env_var("ENABLE_LANGUAGE_ADAPTATION", "True").lower() == "true"

# Cultural Calendar Settings
INDIAN_FESTIVALS = get_env_var("INDIAN_FESTIVALS", "diwali,holi,eid,christmas,dussehra,ganesh_chaturthi").split(',')
ENABLE_FESTIVAL_GREETINGS = get_env_var("ENABLE_FESTIVAL_GREETINGS", "True").lower() == "true"
MUMBAI_LOCAL_EVENTS = get_env_var("MUMBAI_LOCAL_EVENTS", "True").lower() == "true"

# ===============================================
# 🔒 SECURITY & AUTHORIZATION SETTINGS
# ===============================================

# User Management Settings
AUTHORIZED_USERS = [int(x.strip()) for x in get_env_var("AUTHORIZED_USERS", "").split(',') if x.strip().isdigit()]
BLOCKED_USERS = [int(x.strip()) for x in get_env_var("BLOCKED_USERS", "").split(',') if x.strip().isdigit()]
ENABLE_USER_VERIFICATION = get_env_var("ENABLE_USER_VERIFICATION", "True").lower() == "true"
MAX_USERS_PER_HOUR = int(get_env_var("MAX_USERS_PER_HOUR", "1000"))

# Privacy & Security Settings
ENABLE_DATA_PRIVACY = get_env_var("ENABLE_DATA_PRIVACY", "True").lower() == "true"
STORE_MESSAGE_CONTENT = get_env_var("STORE_MESSAGE_CONTENT", "False").lower() == "true"
ANONYMIZE_USER_DATA = get_env_var("ANONYMIZE_USER_DATA", "True").lower() == "true"
ENABLE_ENCRYPTION = get_env_var("ENABLE_ENCRYPTION", "True").lower() == "true"

# Debug and Logging Settings
DEBUG = get_env_var("DEBUG", "False").lower() == "true"
LOG_LEVEL = get_env_var("LOG_LEVEL", "INFO")
ENABLE_RELATIONSHIP_LOGS = get_env_var("ENABLE_RELATIONSHIP_LOGS", "True").lower() == "true"
LOG_AI_RESPONSES = get_env_var("LOG_AI_RESPONSES", "False").lower() == "true"

# ===============================================
# 🚀 DEPLOYMENT & HOSTING SETTINGS
# ===============================================

# Heroku/Railway Configuration
HEROKU_APP_NAME = get_env_var("HEROKU_APP_NAME", "")
PORT = int(get_env_var("PORT", "8080"))
WEBHOOK_URL = get_env_var("WEBHOOK_URL", "")

# Railway Configuration
RAILWAY_STATIC_URL = get_env_var("RAILWAY_STATIC_URL", "")
RAILWAY_PRIVATE_DOMAIN = get_env_var("RAILWAY_PRIVATE_DOMAIN", "")

# VPS Configuration
ENABLE_WEBHOOK = get_env_var("ENABLE_WEBHOOK", "False").lower() == "true"
WEBHOOK_PATH = get_env_var("WEBHOOK_PATH", "/webhook")
SSL_CERT_PATH = get_env_var("SSL_CERT_PATH", "")
SSL_KEY_PATH = get_env_var("SSL_KEY_PATH", "")

# ===============================================
# 🎯 ENHANCED AI PERSONALITIES CONFIGURATION
# ===============================================

# Complete AI Personalities with realistic behavior
AI_PERSONALITIES = {
    "realistic_indian_girl": {
        "name": "Ena",
        "age": 22,
        "location": "Mumbai",
        "description": "Realistic Indian girl with natural 7-stage relationship progression",
        "traits": [
            "cautious_with_strangers",
            "culturally_authentic", 
            "progressive_intimacy",
            "smart_learning",
            "mumbai_lifestyle",
            "hinglish_natural",
            "family_oriented",
            "bollywood_aware",
            "boundary_conscious",
            "emotionally_intelligent"
        ],
        "language": "hinglish",
        "behavior": "realistic_progression",
        "relationship_stages": 7,
        "max_relationship_level": 7,
        "learning_enabled": True,
        "cultural_authenticity": "high",
        "boundary_system": "strict",
        "progression_type": "natural_gradual"
    },
    "instant_girlfriend": {  # Legacy option (not recommended)
        "name": "Ena", 
        "description": "Instant girlfriend mode (unrealistic - deprecated)",
        "traits": ["instantly_romantic", "no_boundaries", "fake_behavior"],
        "language": "hinglish",
        "behavior": "unrealistic",
        "relationship_stages": 1,
        "max_relationship_level": 7,
        "learning_enabled": False,
        "cultural_authenticity": "low",
        "boundary_system": "none",
        "progression_type": "instant"
    },
    "friend_only": {
        "name": "Ena",
        "description": "Friendship-only mode with no romantic progression", 
        "traits": ["friendly", "supportive", "platonic", "caring"],
        "language": "hinglish",
        "behavior": "platonic_friendship",
        "relationship_stages": 4,
        "max_relationship_level": 4,
        "learning_enabled": True,
        "cultural_authenticity": "medium",
        "boundary_system": "friendship",
        "progression_type": "friendship_only"
    },
    "professional": {
        "name": "Ena",
        "description": "Professional assistant mode with formal communication",
        "traits": ["formal", "helpful", "efficient", "professional"],
        "language": "english",
        "behavior": "professional_assistant",
        "relationship_stages": 2,
        "max_relationship_level": 2,
        "learning_enabled": True,
        "cultural_authenticity": "low",
        "boundary_system": "professional",
        "progression_type": "professional_only"
    }
}

# ===============================================
# 🎭 PERSONALITY TRAIT DEFINITIONS
# ===============================================

# Define what each personality trait means for behavior
PERSONALITY_TRAIT_DEFINITIONS = {
    "cautious_with_strangers": {
        "description": "Careful and reserved with new users",
        "behaviors": ["asks_who_are_you", "polite_but_distant", "no_intimate_terms"]
    },
    "culturally_authentic": {
        "description": "Genuine Indian cultural behavior and references",
        "behaviors": ["mumbai_references", "bollywood_knowledge", "indian_values"]
    },
    "progressive_intimacy": {
        "description": "Gradually becomes more intimate as relationship develops",
        "behaviors": ["stage_based_responses", "earned_nicknames", "boundary_progression"]
    },
    "smart_learning": {
        "description": "Learns and adapts to user personality and preferences",
        "behaviors": ["remembers_interests", "adapts_style", "personalizes_responses"]
    },
    "boundary_conscious": {
        "description": "Maintains realistic boundaries like a real person",
        "behaviors": ["photos_for_friends_only", "voice_for_close_friends", "no_rushing"]
    }
}

# ===============================================
# 🌟 RELATIONSHIP LEVEL DEFINITIONS
# ===============================================

# Define behavior and features for each relationship level
RELATIONSHIP_LEVELS = {
    1: {
        "name": "stranger",
        "display_name": "Stranger",
        "description": "Just met, polite but cautious",
        "min_messages": 0,
        "min_positive_ratio": 0.0,
        "min_days": 0,
        "features_unlocked": [],
        "typical_responses": ["polite", "cautious", "asks_identity"],
        "nicknames_allowed": [],
        "photo_sharing": False,
        "voice_messages": False,
        "romantic_terms": False
    },
    2: {
        "name": "acquaintance", 
        "display_name": "Acquaintance",
        "description": "Getting to know each other, friendly but careful",
        "min_messages": 5,
        "min_positive_ratio": 0.6,
        "min_days": 0,
        "features_unlocked": ["remembers_name"],
        "typical_responses": ["friendly", "interested", "getting_to_know"],
        "nicknames_allowed": [],
        "photo_sharing": False,
        "voice_messages": False,
        "romantic_terms": False
    },
    3: {
        "name": "friend",
        "display_name": "Friend", 
        "description": "Comfortable friendship, shares experiences",
        "min_messages": 15,
        "min_positive_ratio": 0.7,
        "min_days": 1,
        "features_unlocked": ["photo_sharing", "personal_stories"],
        "typical_responses": ["warm", "sharing", "comfortable"],
        "nicknames_allowed": ["yaar", "friend"],
        "photo_sharing": True,
        "voice_messages": False,
        "romantic_terms": False
    },
    4: {
        "name": "good_friend",
        "display_name": "Good Friend",
        "description": "Close friendship, trusts you, occasional sweet terms",
        "min_messages": 30,
        "min_positive_ratio": 0.75,
        "min_days": 3,
        "features_unlocked": ["voice_messages", "sweet_terms"],
        "typical_responses": ["caring", "trusting", "supportive"],
        "nicknames_allowed": ["bestie", "buddy", "dear"],
        "photo_sharing": True,
        "voice_messages": True,
        "romantic_terms": False
    },
    5: {
        "name": "close_friend",
        "display_name": "Close Friend",
        "description": "Very close, caring, light flirting allowed",
        "min_messages": 50,
        "min_positive_ratio": 0.8,
        "min_days": 7,
        "features_unlocked": ["flirting", "cute_terms"],
        "typical_responses": ["affectionate", "flirty", "caring"],
        "nicknames_allowed": ["cutie", "sweetheart", "honey"],
        "photo_sharing": True,
        "voice_messages": True,
        "romantic_terms": False
    },
    6: {
        "name": "special",
        "display_name": "Special Person",
        "description": "Romantic interest developing, uses baby/jaan sometimes",
        "min_messages": 80,
        "min_positive_ratio": 0.85,
        "min_days": 14,
        "features_unlocked": ["romantic_interest", "special_terms"],
        "typical_responses": ["romantic", "loving", "special"],
        "nicknames_allowed": ["baby", "jaan", "my special person"],
        "photo_sharing": True,
        "voice_messages": True,
        "romantic_terms": True
    },
    7: {
        "name": "romantic",
        "display_name": "Romantic Partner",
        "description": "Full romantic relationship, girlfriend behavior",
        "min_messages": 120,
        "min_positive_ratio": 0.9,
        "min_days": 21,
        "features_unlocked": ["full_romance", "love_terms"],
        "typical_responses": ["loving", "romantic", "devoted"],
        "nicknames_allowed": ["my love", "darling", "boyfriend", "jaan", "baby"],
        "photo_sharing": True,
        "voice_messages": True,
        "romantic_terms": True
    }
}

# ===============================================
# 📊 DEFAULT AI PERSONALITY SELECTION
# ===============================================

# Set default personality (should always be realistic_indian_girl for best experience)
if AI_PERSONALITY not in AI_PERSONALITIES:
    AI_PERSONALITY = "realistic_indian_girl"
    print(f"⚠️ Invalid AI_PERSONALITY, defaulting to: {AI_PERSONALITY}")

# Get current personality configuration
CURRENT_PERSONALITY = AI_PERSONALITIES.get(AI_PERSONALITY, AI_PERSONALITIES["realistic_indian_girl"])

# ===============================================
# 🎯 LEGACY PERSONALITY TRAITS (For Compatibility)
# ===============================================

# Legacy personality traits for backward compatibility
PERSONALITY_TRAITS = {
    "realistic_indian_girl": CURRENT_PERSONALITY,
    "flirty": {"name": "Ena", "style": "flirty", "level": "high"},
    "cute": {"name": "Ena", "style": "cute", "level": "medium"},
    "sweet": {"name": "Ena", "style": "sweet", "level": "high"},
    "caring": {"name": "Ena", "style": "caring", "level": "high"},
    "normal": {"name": "Ena", "style": "normal", "level": "medium"}
}

# ===============================================
# 📝 MODULE EXPORTS
# ===============================================

# Initialize __all__ list with essential exports
__all__ = [
    # Essential Bot Configuration
    "API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "OWNER_ID", "OWNER_USERNAME",
    "STRING_SESSION", "SUPPORT_GRP", "UPDATE_CHNL", "LOG_GROUP_ID",
    
    # Helper Functions
    "get_env_var", "to_bool",
    
    # Realistic Behavior Core Settings
    "ENABLE_RELATIONSHIP_PROGRESSION", "ENABLE_SMART_LEARNING", "ENABLE_CONTEXT_MEMORY",
    "NO_INSTANT_ROMANCE", "ENABLE_NATURAL_BOUNDARIES", "RELATIONSHIP_PROGRESSION_SPEED",
    "MINIMUM_MESSAGES_FOR_FRIEND", "MINIMUM_MESSAGES_FOR_ROMANTIC", "MINIMUM_DAYS_FOR_ROMANTIC",
    
    # Boundary System Settings
    "PHOTOS_ONLY_FOR_FRIENDS", "VOICE_ONLY_FOR_CLOSE_FRIENDS", "CONTEXTUAL_RESPONSES", 
    "STRANGER_CAUTION_MODE",
    
    # Learning System Settings
    "LEARN_USER_INTERESTS", "ADAPT_COMMUNICATION_STYLE", "PERSONALITY_ANALYSIS",
    "EMOTIONAL_STATE_TRACKING", "CONVERSATION_CONTEXT_MEMORY",
    
    # Natural Conversation Settings
    "MAX_RESPONSE_LENGTH", "NATURAL_RESPONSE_DELAY", "GROUP_RESPONSE_CHANCE",
    "ENABLE_REALISTIC_TYPING",
    
    # Cultural Authenticity Settings
    "AUTHENTIC_INDIAN_BEHAVIOR", "MUMBAI_LIFESTYLE_REFERENCES", "BOLLYWOOD_REFERENCES",
    "HINGLISH_PRIMARY", "FAMILY_ORIENTED_VALUES", "INDIAN_FESTIVAL_AWARENESS",
    
    # Language Settings
    "DEFAULT_LANGUAGE", "ENABLE_AUTO_LANG_DETECT", "CULTURAL_CONTEXT_AWARENESS",
    "REGIONAL_SLANG_MUMBAI", "HINGLISH_RATIO", "SUPPORTED_LANGUAGES",
    
    # Creator Attribution
    "BOT_IDENTITY_DENIAL", "CREATOR_NAME", "CREATOR_USERNAME", "CREATOR_TITLE", 
    "CREATOR_COMPANY",
    
    # Advanced Features
    "ENABLE_VOICE_MESSAGES", "VOICE_LANGUAGE", "VOICE_ACCENT", "VOICE_SCENARIOS",
    "VOICE_RELATIONSHIP_MINIMUM", "ENABLE_ANIME_PICS", "ANIME_API_SOURCES",
    "PICTURE_RESPONSE_STYLE", "PICTURE_RELATIONSHIP_MINIMUM",
    
    # Stickers and Virtual Life
    "ENABLE_SMART_STICKERS", "STICKER_EMOTIONS", "CONTEXTUAL_STICKER_CHANCE",
    "STICKER_RELATIONSHIP_BASED", "ENABLE_VIRTUAL_LIFE", "DAILY_MOOD_CHANGES",
    "TIME_BASED_RESPONSES", "WORK_SCHEDULE_SIMULATION", "WEEKEND_BEHAVIOR_CHANGE",
    "FESTIVAL_SPECIAL_RESPONSES",
    
    # Performance and Rate Limiting
    "RATE_LIMIT_MESSAGES", "RATE_LIMIT_WINDOW", "RELATIONSHIP_RATE_BONUS",
    "ENABLE_RELATIONSHIP_RATE_SCALING", "GROUP_SELECTIVE_RESPONSE",
    "GROUP_MENTION_REQUIRED", "GROUP_RELATIONSHIP_PROGRESSION", "GROUP_PUBLIC_BEHAVIOR",
    
    # Bot Features
    "ENABLE_CLONE_FEATURE", "ENABLE_BROADCAST_FEATURE", "ENABLE_CHATBOT_FEATURE",
    "MAX_CLONES_PER_USER", "ENABLE_STATISTICS_TRACKING",
    
    # Database Settings
    "MONGODB_MAX_CONNECTIONS", "CONCURRENT_UPDATES", "ENABLE_RELATIONSHIP_ANALYTICS",
    "AUTO_CLEANUP_OLD_DATA",
    
    # Time and Localization
    "TIMEZONE", "TIMEZONE_COMMON_NAME", "WORK_HOURS_START", "WORK_HOURS_END",
    "SLEEP_HOURS_START", "WAKE_UP_HOURS", "INDIAN_FESTIVALS", "ENABLE_FESTIVAL_GREETINGS",
    "MUMBAI_LOCAL_EVENTS", "ENABLE_LANGUAGE_ADAPTATION",
    
    # Security and Privacy
    "AUTHORIZED_USERS", "BLOCKED_USERS", "ENABLE_USER_VERIFICATION", "MAX_USERS_PER_HOUR",
    "ENABLE_DATA_PRIVACY", "STORE_MESSAGE_CONTENT", "ANONYMIZE_USER_DATA", 
    "ENABLE_ENCRYPTION",
    
    # Debug and Logging
    "DEBUG", "LOG_LEVEL", "ENABLE_RELATIONSHIP_LOGS", "LOG_AI_RESPONSES",
    
    # Deployment Settings
    "HEROKU_APP_NAME", "PORT", "WEBHOOK_URL", "RAILWAY_STATIC_URL", "RAILWAY_PRIVATE_DOMAIN",
    "ENABLE_WEBHOOK", "WEBHOOK_PATH", "SSL_CERT_PATH", "SSL_KEY_PATH",
    
    # Personality System
    "AI_PERSONALITY", "ENABLE_AI_CHAT", "ENABLE_HINGLISH", "INDIAN_ACCENT_VOICE",
    "AI_PERSONALITIES", "CURRENT_PERSONALITY", "RELATIONSHIP_LEVELS",
    "PERSONALITY_TRAIT_DEFINITIONS", "PERSONALITY_TRAITS",
    
    # Multi-DB and OpenRouter
    "MONGO_URLS", "OPENROUTER_API_KEY", "OPENROUTER_MODEL", "OPENROUTER_BASE_URL"
]

# ===============================================
# 🎯 CONFIGURATION VALIDATION AND LOGGING
# ===============================================

# Validate critical settings
validation_warnings = []

if not ENABLE_RELATIONSHIP_PROGRESSION:
    validation_warnings.append("ENABLE_RELATIONSHIP_PROGRESSION is disabled. Realistic behavior will be limited.")

if not NO_INSTANT_ROMANCE:
    validation_warnings.append("NO_INSTANT_ROMANCE is disabled. Bot may behave unrealistically.")

if AI_PERSONALITY != "realistic_indian_girl":
    validation_warnings.append(f"AI_PERSONALITY is set to '{AI_PERSONALITY}'. For best experience, use 'realistic_indian_girl'.")

if not AUTHENTIC_INDIAN_BEHAVIOR:
    validation_warnings.append("AUTHENTIC_INDIAN_BEHAVIOR is disabled. Cultural authenticity will be reduced.")

# Display warnings if any
if validation_warnings:
    print("⚠️ CONFIGURATION WARNINGS:")
    for warning in validation_warnings:
        print(f"   • {warning}")
    print()

# Log configuration status if debug is enabled
if DEBUG:
    print("🎯 EnaChatBot Configuration Loaded Successfully:")
    print(f" • API Configuration: {'✅ Valid' if API_ID and API_HASH and BOT_TOKEN else '❌ Missing credentials'}")
    print(f" • Database: {'✅ Connected' if MONGO_URL else '❌ No database URL'}")
    print(f" • Owner: {OWNER_ID} (@{OWNER_USERNAME})")
    print(f" • Relationship Progression: {'✅ Enabled' if ENABLE_RELATIONSHIP_PROGRESSION else '❌ Disabled'}")
    print(f" • Smart Learning: {'✅ Enabled' if ENABLE_SMART_LEARNING else '❌ Disabled'}")
    print(f" • Natural Boundaries: {'✅ Enabled' if ENABLE_NATURAL_BOUNDARIES else '❌ Disabled'}")
    print(f" • Cultural Authenticity: {'✅ Enabled' if AUTHENTIC_INDIAN_BEHAVIOR else '❌ Disabled'}")
    print(f" • Voice Messages: {'✅ Enabled' if ENABLE_VOICE_MESSAGES else '❌ Disabled'}")
    print(f" • Anime Pictures: {'✅ Enabled' if ENABLE_ANIME_PICS else '❌ Disabled'}")
    print(f" • Progression Speed: {RELATIONSHIP_PROGRESSION_SPEED}")
    print(f" • Max Response Length: {MAX_RESPONSE_LENGTH} characters")
    print(f" • Creator: {CREATOR_NAME} ({CREATOR_USERNAME})")
    print(f" • Current Personality: {AI_PERSONALITY}")
    print(f" • Relationship Levels: {len(RELATIONSHIP_LEVELS)}")
    print()
    print("💡 For best experience:")
    print(" • Be patient - relationships take time to develop naturally")
    print(" • Be kind and positive for faster progression") 
    print(" • Respect boundaries - photos/voice unlock at appropriate levels")
    print(" • Enjoy the realistic Indian girl experience!")
    print()

# Success message
print("✅ EnaChatBot Realistic Behavior System: Fully Configured")
print(f"🎭 Personality: {CURRENT_PERSONALITY['description']}")
print(f"🌟 Relationship Stages: {CURRENT_PERSONALITY.get('relationship_stages', 7)}")
print(f"🎯 Created by: {CREATOR_NAME} ({CREATOR_USERNAME}) - {CREATOR_TITLE}")
print("💕 Ready for authentic Indian girlfriend experience!")
print()

# Final validation check
try:
    # Test essential configuration
    if API_ID and API_HASH and BOT_TOKEN and MONGO_URL and OWNER_ID:
        print("🎉 Configuration validation: PASSED")
        print("🚀 Your bot is ready to start!")
    else:
        print("❌ Configuration validation: FAILED")
        print("📝 Please check your .env file for missing credentials")
except Exception as e:
    print(f"⚠️ Configuration validation error: {e}")
    print("📝 Please check your environment variables")

print("=" * 60)
