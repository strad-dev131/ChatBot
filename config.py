import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API
API_ID = int(os.getenv("API_ID", 25387587))  
API_HASH = os.getenv("API_HASH", "7b8e2e5bb84c617a474656ad7439ea6a")

# Bot Token / String Session
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING1 = os.getenv("STRING_SESSION", None)

# Database
MONGO_URL = os.getenv("MONGO_URL", None)

# Owner / Admin
OWNER_ID = int(os.getenv("OWNER_ID", 7784241637))
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "SID_ELITE")

# Support / Updates
SUPPORT_GRP = os.getenv("SUPPORT_GRP", "TeamsXchat")
UPDATE_CHNL = os.getenv("UPDATE_CHNL", "TeamXUpdate")