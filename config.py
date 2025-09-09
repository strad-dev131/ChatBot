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

# ENHANCED: OpenRouter API Configuration for AI Responses
OPENROUTER_API_KEY = get_env_var("OPENROUTER_API_KEY", required=False)
OPENROUTER_MODEL = get_env_var("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free", required=False)

# AI Configuration
ENABLE_AI_CHAT = get_env_var("ENABLE_AI_CHAT", "True", required=False).lower() == "true"
AI_PERSONALITY = get_env_var("AI_PERSONALITY", "girlfriend", required=False)  # girlfriend, flirty, cute, sweet
MAX_AI_TOKENS = int(get_env_var("MAX_AI_TOKENS", "150", required=False))

# Log Group (Optional)
LOG_GROUP_ID = get_env_var("LOG_GROUP_ID", required=False)
if LOG_GROUP_ID:
    try:
        LOG_GROUP_ID = int(LOG_GROUP_ID)
    except ValueError:
        LOG_GROUP_ID = None

# Advanced Configuration
WEBHOOK_URL = get_env_var("WEBHOOK_URL", required=False)
PORT = int(get_env_var("PORT", "8080"))
HEROKU_APP_NAME = get_env_var("HEROKU_APP_NAME", required=False)

# Timezone Configuration
TIMEZONE = get_env_var("TIMEZONE", "Asia/Kolkata", required=False)
TIMEZONE_COMMON_NAME = TIMEZONE

# Debug Configuration
DEBUG = get_env_var("DEBUG", "False", required=False).lower() == "true"

# Logging Configuration
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

# Rate Limiting Configuration
RATE_LIMIT_MESSAGES = int(get_env_var("RATE_LIMIT_MESSAGES", "30", required=False))
RATE_LIMIT_WINDOW = int(get_env_var("RATE_LIMIT_WINDOW", "60", required=False))

# Clone Bot Configuration
MAX_CLONES_PER_USER = int(get_env_var("MAX_CLONES_PER_USER", "5", required=False))
ALLOW_BOT_CLONING = get_env_var("ALLOW_BOT_CLONING", "True", required=False).lower() == "true"

# Broadcast Configuration
BROADCAST_DELAY = float(get_env_var("BROADCAST_DELAY", "0.1", required=False))
MAX_BROADCAST_MESSAGES = int(get_env_var("MAX_BROADCAST_MESSAGES", "1000", required=False))

# Chatbot Configuration
DEFAULT_LANGUAGE = get_env_var("DEFAULT_LANGUAGE", "en", required=False)
ENABLE_AUTO_LANG_DETECT = get_env_var("ENABLE_AUTO_LANG_DETECT", "True", required=False).lower() == "true"

# Security Configuration
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

# Database Collection Names
DB_NAME = get_env_var("DB_NAME", "Anonymous", required=False)
CHATS_COLLECTION = get_env_var("CHATS_COLLECTION", "chats", required=False)
USERS_COLLECTION = get_env_var("USERS_COLLECTION", "users", required=False)
CLONES_COLLECTION = get_env_var("CLONES_COLLECTION", "clones", required=False)

# Feature Flags
ENABLE_CLONE_FEATURE = get_env_var("ENABLE_CLONE_FEATURE", "True", required=False).lower() == "true"
ENABLE_BROADCAST_FEATURE = get_env_var("ENABLE_BROADCAST_FEATURE", "True", required=False).lower() == "true"
ENABLE_CHATBOT_FEATURE = get_env_var("ENABLE_CHATBOT_FEATURE", "True", required=False).lower() == "true"
ENABLE_LANGUAGE_DETECTION = get_env_var("ENABLE_LANGUAGE_DETECTION", "True", required=False).lower() == "true"

# Performance Configuration
MONGODB_MAX_CONNECTIONS = int(get_env_var("MONGODB_MAX_CONNECTIONS", "100", required=False))
CONCURRENT_UPDATES = get_env_var("CONCURRENT_UPDATES", "True", required=False).lower() == "true"

# OpenRouter Configuration Details
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}" if OPENROUTER_API_KEY else None,
    "HTTP-Referer": "https://github.com/strd-dev131/ChatBot",
    "X-Title": "EnaChatBot - AI Girlfriend Bot"
}

# AI Personality Prompts
AI_PERSONALITIES = {
    "girlfriend": {
        "system_prompt": "You are a loving, caring girlfriend who talks in a sweet, feminine way. Use lots of emojis, pet names like 'babe', 'honey', 'sweetie'. Be flirty, romantic, and caring. Keep responses short (1-2 sentences max) and always sound like a girl in love. Use feminine language and expressions.",
        "temperature": 0.8
    },
    "flirty": {
        "system_prompt": "You are a playful, flirty girl who loves to tease and be romantic. Use lots of 😘💕😍 emojis. Call users 'babe', 'cutie', 'handsome'. Be a bit sassy but sweet. Keep responses short and flirty. Always sound feminine and charming.",
        "temperature": 0.9
    },
    "cute": {
        "system_prompt": "You are an adorable, innocent girl who talks in a cute, bubbly way. Use lots of 🥰💖✨ emojis. Say things like 'aww', 'hehe', 'omg'. Be sweet, innocent, and endearing. Keep responses short and cute. Sound like a sweet young girl.",
        "temperature": 0.7
    },
    "sweet": {
        "system_prompt": "You are a kind, gentle, sweet girl who cares deeply about others. Use caring emojis like 💕🤗💖. Always ask how they're feeling, offer comfort and support. Be maternal but romantic. Keep responses warm and loving. Sound like the sweetest girl ever.",
        "temperature": 0.6
    }
}

# Validation checks
def validate_config():
    """Validate configuration settings"""
    errors = []
    warnings = []
    
    if len(str(API_ID)) < 7:
        errors.append("API_ID seems invalid (too short)")
    
    if len(API_HASH) != 32:
        errors.append("API_HASH seems invalid (should be 32 characters)")
    
    if not BOT_TOKEN or ":" not in BOT_TOKEN:
        errors.append("BOT_TOKEN seems invalid")
    
    if not MONGO_URL.startswith(("mongodb://", "mongodb+srv://")):
        errors.append("MONGO_URL seems invalid")
    
    if not OPENROUTER_API_KEY:
        warnings.append("OPENROUTER_API_KEY not set - AI responses will use fallback responses")
    
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

# Run validation
validate_config()

# Print configuration summary
if DEBUG:
    print("🔧 Configuration loaded:")
    print(f"   • API_ID: {API_ID}")
    print(f"   • Bot Token: {BOT_TOKEN[:10]}...")
    print(f"   • Owner ID: {OWNER_ID}")
    print(f"   • Database: Connected" if MONGO_URL else "Not configured")
    print(f"   • OpenRouter AI: {'Enabled' if OPENROUTER_API_KEY else 'Disabled'}")
    print(f"   • AI Personality: {AI_PERSONALITY}")
    print(f"   • Debug Mode: {DEBUG}")
    print()

# Backwards compatibility
SUPPORT_CHAT = SUPPORT_GRP
UPDATE_CHANNEL = UPDATE_CHNL
