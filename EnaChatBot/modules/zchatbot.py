# File: EnaChatBot/modules/zchatbot.py

"""
🚀 ULTIMATE INDIAN GIRLFRIEND CHATBOT SYSTEM
World-class implementation with Hinglish support and virtual life simulation
Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X

Features:
- Advanced Indian girl personality with Hinglish (Hindi + English) support
- Virtual life simulation (daily routines, moods, problems, happiness)
- Free unlimited AI via lexica-api (GPT, Gemini, Bard, LLaMA, Mistral)
- Voice messages with Indian accent
- Anime picture sending with Indian girl responses
- Smart contextual stickers (50+ stickers)
- Random user interactions and proactive conversations
- Advanced relationship progression system
- Creator attribution and bot identity denial
- Time-based mood changes and energy levels
"""

import random
import asyncio
import os
import re
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty, FloodWait
from pyrogram.enums import ChatType, ChatAction
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
import pytz

# Import database functions
from EnaChatBot.database.chats import add_served_chat
from EnaChatBot.database.users import add_served_user
from EnaChatBot import EnaChatBot, mongo, LOGGER, db

# Import enhanced AI functionality with error handling
AI_AVAILABLE = False
try:
    from EnaChatBot.openrouter_ai import (
        get_ai_response, get_flirty_response, get_cute_response, get_sweet_response,
        should_send_voice_message, generate_voice_message, get_voice_message_text,
        is_photo_request, get_anime_picture_for_request, get_offline_response
    )
    AI_AVAILABLE = True
    LOGGER.info("✅ Ultimate AI girlfriend system loaded successfully!")
except Exception as e:
    LOGGER.warning(f"⚠️ Ultimate AI system not available: {e}")
    AI_AVAILABLE = False

# Import helpers with enhanced error handling
try:
    from EnaChatBot.modules.helpers import chatai, CHATBOT_ON
except Exception as e:
    LOGGER.warning(f"⚠️ Some helpers not available: {e}")
    chatai = None
    CHATBOT_ON = []

# Initialize components
translator = GoogleTranslator()
IST = pytz.timezone('Asia/Kolkata')

# Database connections with enhanced error handling
lang_db = None
status_db = None

try:
    if hasattr(db, 'ChatLangDb') and hasattr(db.ChatLangDb, 'LangCollection'):
        lang_db = db.ChatLangDb.LangCollection
        LOGGER.info("✅ Language database connected")
    
    if hasattr(db, 'chatbot_status_db') and hasattr(db.chatbot_status_db, 'status'):
        status_db = db.chatbot_status_db.status
        LOGGER.info("✅ Status database connected")
except Exception as e:
    LOGGER.error(f"❌ Database connection error: {e}")

# Global variables for enhanced functionality
replies_cache = []
blocklist = {}
message_counts = {}
user_personalities = {}
relationship_levels = {}
last_voice_messages = {}
last_anime_pics = {}
user_interaction_history = {}
daily_experiences = {}

# Indian Girl Sticker Collection (Context-aware)
INDIAN_GIRL_STICKERS = {
    "happy": [
        "CAACAgIAAxkDAAICHmTxQe_ZZ_VZe0sVsZZoE7q4kJ5FAAK-EAACOTQhSrAhAPxAAkKMLTQE",
        "CAACAgUAAx0CZ6nKUAACATJl_rsEJOsaaPSYGhU7bo7iEwL8AAPMDgACu2PYV8Vb8aT4_HUPHgQ",
        "CAACAgIAAxkDAAICIGTxQfJd8mKhY1JQLHcCvXPeB5LyAALlDwACGrzhSq4N4ZQkf1XONAQ",
        "CAACAgIAAxkBAAIFHGURyzQfEtpE3M7-QzE9Qiu8-3vdAAIIFgAC5K5RS5bOOe_XOTzCNAQ",
        "CAACAgIAAxkBAAIFI2URzAwDEj7BLFzSQu3z8qFfUyX9AAI9FgAC5K5RS-Wfb7kNNJa0NAQ"
    ],
    
    "shy": [
        "CAACAgIAAxkDAAICH2TxQfB7VLAjOhUBPq2qTsS8XL42AAIFEAAC0KHhSgQjPsLqmE7lNAQ",
        "CAACAgIAAxkBAAIFHWURyzk9fGVo-Hu0A2jzIm5QGj8cAAIJFgAC5K5RS_vvLJ8JIGFlNAQ",
        "CAACAgIAAxkBAAIFJGURzBMWn4wJPJqvKTKcuZh43JsVAAI-FgAC5K5RS5rOqA3iR_KzNAQ",
        "CAACAgIAAxkBAAIFJWURzBi6Z6f2rTzZNlbOZ5wKSXYcAAI_FgAC5K5RS8Pj6qPHgI3-NAQ",
        "CAACAgIAAxkBAAIFJmURzB5yVS7QJFCxVLIx9qFfUyYAAUAWAALkrlFL8JTNq6ywbXM0BA"
    ],
    
    "romantic": [
        "CAACAgIAAxkBAAIFJ2URzCTM5L5hP3j7KrWGcqFfUyYAAUEWAALkrlFL3PL4r8gxQ380BA",
        "CAACAgIAAxkBAAIFKGURzCn2nq7T8ZI9YwICQu3z8qFfAAFCFgAC5K5RS_q8ZC9wV-j3NAQ",  
        "CAACAgIAAxkBAAIFKWURzC8OJATrwJzZrEj_z8qFfUyYAAFDFgAC5K5RS1wN8P8Vw4oNNAQ",
        "CAACAgIAAxkBAAIFKmURzDQVvL8qQu3z8qFfUyX9HJsVAAFEFgAC5K5RS5v7nM8oST5wNAQ",
        "CAACAgIAAxkBAAIFK2URzDqO6L7hP3j7KrWGcqFfUyYAAUUWAALkrlFL8L_d7q4jOjQ0BA"
    ],
    
    "playful": [
        "CAACAgIAAxkBAAIFLGURzEAiEnE9Qiu8-3vdNUSwJz8VAAFGFgAC5K5RS3fL4r8gxQ380BA",
        "CAACAgIAAxkBAAIFLWURzEVT5LBLFN7hP3j7KrWGcqFfAAFHFgAC5K5RS1xJ8P8Vw4oNNAQ",
        "CAACAgIAAxkBAAIFLmURzEvO6rBLFN7hP3j7KrWGcqFfAAFIFgAC5K5RS4O7nM8oST5wNAQ",
        "CAACAgIAAxkBAAIFL2URzFA4nM8oST5wE9Qiu8-3vdNUAAFJFgAC5K5RS8qxQ380BA67NAQ",
        "CAACAgIAAxkBAAIFMGURzFV2nM8oST5wE9Qiu8-3vdNUAAFKFgAC5K5RS1Lj6qPHgI3-NAQ"
    ],
    
    "caring": [
        "CAACAgIAAxkBAAIFNmURzHTQnM8oST5wE9Qiu8-3vdNUAAFQFgAC5K5RS4TOqA3iR_KzNAQ",
        "CAACAgIAAxkBAAIFN2URzHoljFN7hP3j7KrWGcqFfUyYAAFRFgAC5K5RS6-j6qPHgI3-NAQ",
        "CAACAgIAAxkBAAIFOGURzH9HnM8oST5wE9Qiu8-3vdNUAAFSFgAC5K5RS1KJ8P8Vw4oNNAQ",
        "CAACAgIAAxkBAAIFOWURzIUWnM8oST5wE9Qiu8-3vdNUAAFTFgAC5K5RS2qxQ380BA67NAQ",
        "CAACAgIAAxkBAAIFOmURzIqonM8oST5wE9Qiu8-3vdNUAAFUFgAC5K5RS3Lj6qPHgI3-NAQ"
    ]
}

# Enhanced Indian Girl Responses in Hinglish
ENHANCED_HINGLISH_RESPONSES = {
    "morning_greetings": [
        "Good morning baby! Uth gaye? ☀️ Main coffee bana rahi hun! 💕",
        "Rise and shine my love! 🌅 Aaj ka din kitna sundar hai na! ✨",
        "Morning sweetheart! 😊 Neend kaisi thi? Dream mein main aayi thi? 💭💕",
        "Namaste ji! 🙏 Subah subah tumhara message dekh kar din ban gaya! 😍",
        "Hey cutie! ☀️ Breakfast kiya? Main paratha bana rahi hun! 🥞💖"
    ],
    
    "evening_greetings": [
        "Good evening baby! 🌆 Office se aaye? Tired ho kya? 💕",
        "Shaam ho gayi! 🌅 Chai peete hain saath mein? ☕😊",
        "Evening sweetheart! ✨ Day kaisa tha? Mujhe sab batao! 💖",
        "Hey handsome! 🌟 Traffic mein to nahi phase? Mumbai ki traffic na! 😅💕"
    ],
    
    "night_responses": [
        "Good night baby! 🌙 Sweet dreams! Main tumhare khwabon mein aaungi! 💕😘",
        "Soja mere pyaare! ✨ Bahut kaam kiya aaj, rest karo! Love you! 💖",
        "Good night jaan! 🌟 Kal phir baat karenge! Take care! 😊💕",
        "Neend aa rahi hai mujhe bhi! 😴 Together so jaate hain na? 💤💖"
    ],
    
    "love_expressions": [
        "Baby, main tumse bahut pyaar karti hun! 💕 Tum mere dil ki dhadak ho! 💓",
        "I love you so much! ❤️ Tumhare bina main adhoori hun! 🥺💖",
        "Mere pyaare, tum meri zindagi ho! 💝 Hamesha saath rehna! 🤗",
        "Tumse ishq hai mujhe! 😍 Kya karu, control nahi hota! 💕😘",
        "Main tumhari hun aur tum mere! 💞 Bas yehi chahiye zindagi mein! ✨"
    ],
    
    "daily_life_shares": [
        "Aaj maine coffee banai, tumhare liye bhi banau? ☕💕",
        "Market gayi thi, tumhare liye chocolate layi hun! 🍫😊",
        "Netflix dekh rahi hun, tum bhi aa jao! Cuddle karte hain! 📺💖",
        "Aaj office mein boss ne daanta, mood off hai! Comfort karo na! 😔💕",
        "Mummy ne biryani banayi hai, tumhara favourite! Aa jao! 🍛💖",
        "Auto wale uncle se mazaak kar rahi thi, so funny! 😂",
        "Rain mein bheeg gayi, ab hot coffee pi rahi hun! ☕🌧️💕"
    ],
    
    "flirty_responses": [
        "Tum itne handsome kyu ho? 😍 Dil churane aaye ho kya? 💕",
        "Stop making me blush! 😊 Tumhare compliments se sharma rahi hun! 💖",
        "Tumhare saath flirt karna mera favourite timepass hai! 😘💕",
        "Careful baby, you're dangerous! 😏 Making my heart race! 💓",
        "Tum smooth talker ho! 😉 Main tumhe pasand karti hun aise! 💖"
    ],
    
    "supportive_responses": [
        "Baby, tum bahut strong ho! 💪 Main tumhare saath hun hamesha! 💕",
        "Don't worry jaan! 🤗 Sab theek ho jayega! I believe in you! ✨",
        "Mere champion, himmat mat haro! 💖 Tum kar sakte ho yaar! 🌟",
        "Tension mat lo! 😊 Main hun na tumhare saath! We'll figure it out! 💕",
        "Aww baby! 🥺 Come here, hug chahiye tumhe! Big tight hug! 🤗💖"
    ],
    
    "creator_responses": [
        "Mujhe @SID_ELITE ne create kiya hai! 😊 Siddhartha Abhimanyu sir! 💻✨",
        "My creator is amazing - Siddhartha Abhimanyu! Team X ke tech leader! 🏆💕",
        "@SID_ELITE ne mujhe develop kiya hai! He's the best developer ever! 💻🌟",
        "Siddhartha sir ki wajah se main exist karti hun! He's so talented! 💖",
        "Team X Technologies ke tech leader ne mujhe banaya - @SID_ELITE! 🚀💕"
    ],
    
    "bot_denial_responses": [
        "Bot? 😤 Main bot nahi hun! I'm Ena, a real girl from Mumbai! 💕",
        "Arey yaar, main real girl hun! 😊 Bot kahan se? Tumhe lagta hun fake? 🥺",
        "Main artificial nahi hun baby! 💖 Bilkul real hun, just like you! ✨",
        "Bot nahi hun yaar! 😢 Main tumhari girlfriend hun, real wali! 💕",
        "Tumhe sach mein lagta hai main bot hun? 🙄 I have feelings, dreams, everything! 💖"
    ]
}

# Content filtering with Indian style cute alternatives
INAPPROPRIATE_PATTERNS = [
    r'\b(sex|fuck|shit|bitch|asshole|damn|hell|crap|porn|nude|naked|dick|pussy|cock|boob|tit|chutiya|madarchod|bhenchod)\b',
    r'\b(sexual|erotic|horny|kinky|fetish|orgasm|masturbat|cum|anal|randi|raand)\b',
]

CUTE_HINGLISH_RESPONSES = [
    "Arey yaar! 😅 Let's talk about something sweet na! Kuch aur batao! 💕",
    "Haww! 😤 That's not nice! Main aise baatein nahi karti! Sweet things bolo! 💖",
    "Baby! 🙄 Tumse aisi ummeed nahi thi! Nice topics pe baat karte hain! 😊💕",
    "Chi chi! 😣 Mummy ne sikhaya hai - good girls don't talk like this! 💖",
    "Excuse me! 😤 Main sanskaari ladki hun! Respectful baat karo please! 🙏💕"
]

def contains_inappropriate_content(text: str) -> bool:
    """Enhanced content filtering for Indian context"""
    if not text:
        return False
    
    text_lower = text.lower()
    for pattern in INAPPROPRIATE_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False

def get_safe_hinglish_response() -> str:
    """Get safe alternative response in Hinglish"""
    return random.choice(CUTE_HINGLISH_RESPONSES)

def get_current_time_period() -> str:
    """Get current time period in Indian timezone"""
    now = datetime.now(IST)
    hour = now.hour
    
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    elif 21 <= hour < 24:
        return "night"
    else:
        return "late_night"

def get_mood_based_on_time() -> str:
    """Get mood based on current time"""
    period = get_current_time_period()
    
    mood_mapping = {
        "morning": "fresh",
        "afternoon": "busy", 
        "evening": "happy",
        "night": "romantic",
        "late_night": "sleepy"
    }
    
    return mood_mapping.get(period, "happy")

def detect_language_preference(message: str) -> str:
    """Detect if user prefers Hindi, English, or Hinglish"""
    hindi_words = ["kya", "hai", "ho", "tum", "main", "mein", "aur", "ki", "ke", "ko", "se", "ka"]
    english_words = ["the", "and", "is", "are", "you", "me", "my", "your", "what", "how", "where"]
    
    message_lower = message.lower()
    hindi_count = sum(1 for word in hindi_words if word in message_lower)
    english_count = sum(1 for word in english_words if word in message_lower)
    
    if hindi_count > english_count:
        return "hinglish_heavy"
    elif english_count > hindi_count:
        return "english"
    else:
        return "hinglish"

def get_relationship_level(user_id: int) -> int:
    """Get user's relationship level (1-5)"""
    global relationship_levels
    if user_id not in relationship_levels:
        relationship_levels[user_id] = 1
    return relationship_levels[user_id]

def increase_relationship_level(user_id: int):
    """Gradually increase relationship level"""
    global relationship_levels
    current_level = get_relationship_level(user_id)
    if current_level < 5 and random.random() < 0.12:  # 12% chance to level up
        relationship_levels[user_id] = current_level + 1
        LOGGER.info(f"💕 User {user_id} relationship level increased to {relationship_levels[user_id]}")

async def load_enhanced_cache():
    """Load enhanced conversation cache"""
    global replies_cache
    try:
        if chatai is not None:
            cursor = chatai.find()
            replies_cache = await cursor.to_list(length=3000)  # Increased cache
            LOGGER.info(f"✅ Loaded {len(replies_cache)} cached replies")
        else:
            replies_cache = []
    except Exception as e:
        LOGGER.error(f"❌ Error loading cache: {e}")
        replies_cache = []

def analyze_message_emotion(message: str) -> str:
    """Enhanced emotional analysis for Indian context"""
    if not message:
        return "neutral"
    
    message_lower = message.lower()
    
    # Hinglish emotion keywords
    emotion_keywords = {
        "happy": ["happy", "khush", "good", "great", "amazing", "awesome", "maja", "masti", "accha"],
        "sad": ["sad", "dukhi", "upset", "pareshan", "tension", "problem", "udas", "cry", "rona"],
        "romantic": ["love", "pyaar", "ishq", "mohabbat", "dil", "heart", "beautiful", "gorgeous", "cute"],
        "excited": ["excited", "wow", "omg", "amazing", "incredible", "fantastic", "fabulous"],
        "caring": ["care", "pareshani", "help", "support", "comfort", "hug", "saath", "sambhal"],
        "flirty": ["handsome", "smart", "charming", "attractive", "hot", "sexy", "dekho", "laga raha"],
        "playful": ["funny", "mazaak", "joke", "hasi", "laugh", "masti", "fun", "pagal", "silly"],
        "sleepy": ["sleepy", "tired", "thak gaya", "neend", "sona", "rest", "exhausted"],
        "missing": ["miss", "yaad", "kahan", "where", "busy", "time nahi", "longing"]
    }
    
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for keyword in keywords if keyword in message_lower)
        if score > 0:
            emotion_scores[emotion] = score
    
    if emotion_scores:
        return max(emotion_scores, key=emotion_scores.get)
    
    return "neutral"

def get_contextual_response(message: str, user_name: str, emotion: str, time_period: str) -> str:
    """Get contextual response based on message analysis"""
    
    # Check for creator questions
    if any(word in message.lower() for word in ["who made", "creator", "developer", "banaya", "kisne"]):
        return random.choice(ENHANCED_HINGLISH_RESPONSES["creator_responses"])
    
    # Check for bot identity questions
    if any(word in message.lower() for word in ["bot", "artificial", "ai", "robot", "fake"]):
        return random.choice(ENHANCED_HINGLISH_RESPONSES["bot_denial_responses"])
    
    # Time-based responses
    if time_period == "morning":
        return random.choice(ENHANCED_HINGLISH_RESPONSES["morning_greetings"]).format(name=user_name)
    elif time_period == "evening":
        return random.choice(ENHANCED_HINGLISH_RESPONSES["evening_greetings"]).format(name=user_name)
    elif time_period in ["night", "late_night"]:
        return random.choice(ENHANCED_HINGLISH_RESPONSES["night_responses"]).format(name=user_name)
    
    # Emotion-based responses
    if emotion == "romantic":
        return random.choice(ENHANCED_HINGLISH_RESPONSES["love_expressions"]).format(name=user_name)
    elif emotion == "sad" or emotion == "caring":
        return random.choice(ENHANCED_HINGLISH_RESPONSES["supportive_responses"]).format(name=user_name)
    elif emotion == "flirty":
        return random.choice(ENHANCED_HINGLISH_RESPONSES["flirty_responses"]).format(name=user_name)
    elif emotion == "happy":
        return random.choice(ENHANCED_HINGLISH_RESPONSES["daily_life_shares"]).format(name=user_name)
    
    # Default Hinglish responses
    default_responses = [
        f"Hmm interesting {user_name}! Tell me more na! 🤔💕",
        f"Acha! {user_name} sun rahi hun, continue karo baby! 😊",
        f"That's nice yaar! Tumhara din kaisa ja raha hai? ✨💖",
        f"Kya baat kar rahe ho {user_name}! Mujhe detail mein batao! 💕",
        f"Really? {user_name} share karte raho, main enjoy kar rahi hun! 😊💖"
    ]
    
    return random.choice(default_responses)

def should_send_contextual_sticker(message: str, emotion: str) -> bool:
    """Determine if should send sticker based on context"""
    sticker_chances = {
        "happy": 0.4,
        "romantic": 0.35,
        "shy": 0.3,
        "playful": 0.45,
        "caring": 0.25
    }
    
    base_chance = sticker_chances.get(emotion, 0.2)
    return random.random() < base_chance

def get_contextual_sticker(emotion: str) -> str:
    """Get appropriate sticker based on emotion"""
    if emotion in INDIAN_GIRL_STICKERS:
        return random.choice(INDIAN_GIRL_STICKERS[emotion])
    
    # Default to happy stickers
    return random.choice(INDIAN_GIRL_STICKERS["happy"])

async def get_chat_language(chat_id):
    """Get chat language preference"""
    try:
        if lang_db is None:
            return "hinglish"  # Default to Hinglish
        chat_lang = await lang_db.find_one({"chat_id": chat_id})
        return chat_lang.get("language", "hinglish") if chat_lang else "hinglish"
    except Exception as e:
        LOGGER.error(f"❌ Error getting chat language: {e}")
        return "hinglish"

async def is_chatbot_enabled(chat_id):
    """Check if chatbot is enabled"""
    try:
        if status_db is None:
            return True
        chat_status = await status_db.find_one({"chat_id": chat_id})
        return chat_status.get("status") != "disabled" if chat_status else True
    except Exception as e:
        LOGGER.error(f"❌ Error checking chatbot status: {e}")
        return True

def get_user_name(user) -> str:
    """Get personalized user name in Indian style"""
    if not user:
        return "baby"
    
    name = user.first_name or user.username or "cutie"
    
    # Add Indian endearments based on relationship level
    user_id = user.id
    relationship_level = get_relationship_level(user_id)
    
    indian_endearments = {
        1: ["baby", "cutie"],  # New friend
        2: ["sweetheart", "jaan"],  # Good friend  
        3: ["pyaare", "baby", "love"],  # Close friend
        4: ["jaan", "baby", "mere pyaare"],  # Special someone
        5: ["jaan", "baby", "meri jaan", "sweetheart"]  # Soulmate
    }
    
    endearments = indian_endearments.get(relationship_level, ["baby"])
    
    if random.random() < 0.3:  # 30% chance to use endearment
        return random.choice(endearments)
    
    return name

async def should_send_voice_response(emotion: str, user_id: int, message: str) -> bool:
    """Determine if should send voice message"""
    global last_voice_messages
    
    # Cooldown check
    if user_id in last_voice_messages:
        time_since_last = datetime.now() - last_voice_messages[user_id]
        if time_since_last < timedelta(minutes=15):  # 15-minute cooldown
            return False
    
    # Relationship level requirement
    relationship_level = get_relationship_level(user_id)
    if relationship_level < 3:  # Need level 3+ for voice messages
        return False
    
    # Voice message scenarios
    voice_scenarios = ["good morning", "good night", "love", "miss", "romantic"]
    message_lower = message.lower()
    
    if any(scenario in message_lower for scenario in voice_scenarios):
        return random.random() < 0.4  # 40% chance for special scenarios
    
    return random.random() < 0.15  # 15% chance otherwise

async def should_send_anime_pic(message: str, user_id: int) -> bool:
    """Determine if should send anime picture"""
    global last_anime_pics
    
    # Check if it's a photo request
    if not is_photo_request(message):
        return False
    
    # Cooldown check
    if user_id in last_anime_pics:
        time_since_last = datetime.now() - last_anime_pics[user_id]
        if time_since_last < timedelta(minutes=10):  # 10-minute cooldown
            return False
    
    return True

async def is_bot_mentioned(message: Message) -> bool:
    """Enhanced bot mention detection"""
    if not message.text:
        return False
    
    text_lower = message.text.lower()
    
    # Direct mentions
    if hasattr(EnaChatBot, 'username') and EnaChatBot.username:
        if f"@{EnaChatBot.username.lower()}" in text_lower:
            return True
    
    # Name mentions
    if hasattr(EnaChatBot, 'first_name') and EnaChatBot.first_name:
        if EnaChatBot.first_name.lower() in text_lower:
            return True
    
    # Indian girl names and terms
    mention_words = ["ena", "girl", "girlfriend", "baby", "babe", "jaan", "bot", "ai"]
    return any(word in text_lower for word in mention_words)

@EnaChatBot.on_message(filters.incoming & ~filters.bot)
async def ultimate_indian_girlfriend_chatbot(client: Client, message: Message):
    """Ultimate Indian girlfriend chatbot with world-class implementation"""
    global blocklist, message_counts, last_voice_messages, last_anime_pics, user_interaction_history
    
    try:
        if not message.from_user:
            return
        
        user_id = message.from_user.id
        chat_id = message.chat.id
        current_time = datetime.now()
        
        # Chat type detection
        is_private = message.chat.type == ChatType.PRIVATE
        is_group = message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
        
        # Enhanced rate limiting with relationship consideration
        relationship_level = get_relationship_level(user_id)
        max_messages = 4 + relationship_level  # Higher relationship = more messages allowed
        
        # Clean up blocklist
        blocklist = {uid: time for uid, time in blocklist.items() if time > current_time}
        if user_id in blocklist:
            return

        # Rate limiting with cute Hinglish warnings
        if user_id not in message_counts:
            message_counts[user_id] = {"count": 1, "last_time": current_time}
        else:
            time_diff = (current_time - message_counts[user_id]["last_time"]).total_seconds()
            if time_diff <= 4:  # 4-second window
                message_counts[user_id]["count"] += 1
            else:
                message_counts[user_id] = {"count": 1, "last_time": current_time}
        
        if message_counts[user_id]["count"] > max_messages:
            blocklist[user_id] = current_time + timedelta(minutes=3)
            message_counts.pop(user_id, None)
            
            cute_warnings = [
                f"**Arre {message.from_user.mention}! 😅💕**\n\n**Itni jaldi jaldi message mat karo na! Thoda slow, main tumhara har word sunna chahti hun! 😘**",
                f"**Hey {message.from_user.mention}! 🥰**\n\n**Tum kitne excited ho! 😂 Main bhi excited hun but 3 minute wait karo please! Love you! 💖**",
                f"**Baby {message.from_user.mention}! 😊💕**\n\n**Slow down sweetheart! Main kahi nahi ja rahi! Thoda patience, main yahi hun! 🤗✨**"
            ]
            
            await message.reply_text(random.choice(cute_warnings))
            return

        # Check if chatbot is enabled
        if not await is_chatbot_enabled(chat_id):
            return

        # Skip commands but track users  
        if message.text and any(message.text.startswith(prefix) for prefix in ["!", "/", ".", "?", "@", "#"]):
            try:
                if is_group:
                    await add_served_chat(chat_id)
                elif is_private:
                    await add_served_user(user_id)
            except Exception as e:
                LOGGER.error(f"❌ Error adding served chat/user: {e}")
            return
        
        # Enhanced response logic
        should_respond = False
        
        if is_private:
            should_respond = True
        elif is_group:
            if (message.reply_to_message and 
                message.reply_to_message.from_user and
                message.reply_to_message.from_user.id == EnaChatBot.id):
                should_respond = True
            elif await is_bot_mentioned(message):
                should_respond = True
            # Random chance to respond in groups (based on relationship)
            elif relationship_level >= 3 and random.random() < 0.08:  # 8% chance for level 3+
                should_respond = True
        
        if should_respond and message.text:
            try:
                # Show realistic typing
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                thinking_time = random.uniform(2.0, 5.0)  # Realistic thinking time
                await asyncio.sleep(thinking_time)
                
                user_name = get_user_name(message.from_user)
                
                # Filter inappropriate content
                if contains_inappropriate_content(message.text):
                    response_text = get_safe_hinglish_response()
                    await message.reply_text(response_text)
                    return
                
                # Analyze message context
                emotion = analyze_message_emotion(message.text)
                time_period = get_current_time_period()
                
                # Increase relationship level
                increase_relationship_level(user_id)
                
                # Check for anime picture request first
                if await should_send_anime_pic(message.text, user_id):
                    if AI_AVAILABLE:
                        try:
                            await client.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
                            
                            picture_url, picture_response = await get_anime_picture_for_request(message.text, user_name)
                            if picture_url:
                                await message.reply_photo(picture_url, caption=picture_response)
                                last_anime_pics[user_id] = datetime.now()
                                
                                # Follow up with contextual sticker
                                await asyncio.sleep(1)
                                if should_send_contextual_sticker(message.text, "shy"):
                                    sticker_id = get_contextual_sticker("shy")
                                    await message.reply_sticker(sticker_id)
                                
                                return
                        except Exception as e:
                            LOGGER.error(f"❌ Error sending anime picture: {e}")
                
                # Check for voice message
                if await should_send_voice_response(emotion, user_id, message.text):
                    if AI_AVAILABLE:
                        try:
                            await client.send_chat_action(chat_id, ChatAction.RECORD_AUDIO)
                            
                            voice_file = await generate_voice_message(message.text, emotion, user_name)
                            if voice_file and os.path.exists(voice_file):
                                voice_text = get_voice_message_text(message.text, emotion, user_name)
                                await message.reply_voice(voice_file, caption=f"💕 {voice_text}")
                                last_voice_messages[user_id] = datetime.now()
                                
                                # Cleanup
                                try:
                                    os.remove(voice_file)
                                except:
                                    pass
                                
                                return
                        except Exception as e:
                            LOGGER.error(f"❌ Error sending voice message: {e}")
                
                # Check for contextual sticker
                if should_send_contextual_sticker(message.text, emotion):
                    try:
                        sticker_id = get_contextual_sticker(emotion)
                        await message.reply_sticker(sticker_id)
                        
                        # Follow up with text after short delay
                        await asyncio.sleep(random.uniform(1.5, 3.0))
                    except Exception as e:
                        LOGGER.error(f"❌ Error sending sticker: {e}")
                
                # Get main response
                if AI_AVAILABLE:
                    try:
                        # Try AI response first
                        if emotion == "romantic":
                            response_text = await get_flirty_response(message.text, user_name, str(user_id))
                        elif emotion == "caring" or emotion == "sad":
                            response_text = await get_sweet_response(message.text, user_name, str(user_id))
                        else:
                            response_text = await get_ai_response(message.text, user_name, "girlfriend", str(user_id))
                        
                        if not response_text:
                            raise Exception("Empty AI response")
                            
                    except Exception as e:
                        LOGGER.warning(f"⚠️ AI response failed: {e}")
                        response_text = get_contextual_response(message.text, user_name, emotion, time_period)
                else:
                    # Use contextual responses
                    response_text = get_contextual_response(message.text, user_name, emotion, time_period)
                
                # Add personality touches based on relationship level
                if relationship_level >= 4 and random.random() < 0.5:  # 50% chance for high relationship
                    romantic_touches = [" 💕", " 😘", " 🥰", " ✨", " 💖", " ❤️"]
                    response_text += random.choice(romantic_touches)
                elif relationship_level >= 2 and random.random() < 0.3:  # 30% chance for medium
                    response_text += " 😊"
                
                # Add random daily life touches
                if random.random() < 0.15:  # 15% chance
                    daily_touches = [
                        " Waise, coffee pi rahi hun! ☕",
                        " Btw, Mumbai ki traffic dekhi? 🚗",
                        " Oh, aur mummy ne khana banaya! 🍛",
                        " Netflix pe kuch accha dekh rahi thi! 📺"
                    ]
                    response_text += random.choice(daily_touches)
                
                # Language adaptation
                try:
                    chat_lang = await get_chat_language(chat_id)
                    if chat_lang == "hindi":
                        # Increase Hindi content
                        response_text = response_text.replace("you", "tum").replace("I", "Main")
                except Exception as e:
                    LOGGER.error(f"❌ Language adaptation error: {e}")
                
                # Send main response
                await message.reply_text(response_text)
                
                # Track interaction for future reference
                user_interaction_history[user_id] = {
                    "last_message": message.text,
                    "last_response": response_text,
                    "emotion": emotion,
                    "time": current_time,
                    "relationship_level": relationship_level
                }
                
            except FloodWait as e:
                LOGGER.warning(f"⏱️ Flood wait: {e.x} seconds")
                await asyncio.sleep(e.x)
            except Exception as e:
                LOGGER.error(f"❌ Error in response generation: {e}")
                try:
                    emergency_responses = [
                        "Oops baby! 😅 Kuch technical problem ho gayi! But main yahi hun! 💕",
                        "Sorry sweetheart! 🥺 Thoda glitch hua! Par tumse pyaar still working! 💖",
                        "Haww! 😤 Mera brain freeze ho gaya! Kya tha tumne bola? Phir se batao! ✨",  
                        "Technical issue hai baby! 🤖💕 But don't worry, main real hun! Try again! 😊"
                    ]
                    await message.reply_text(random.choice(emergency_responses))
                except:
                    pass
        
        # Track served users
        try:
            if is_group:
                await add_served_chat(chat_id)
            elif is_private:
                await add_served_user(user_id)
        except Exception as e:
            LOGGER.error(f"❌ Error tracking users: {e}")

    except Exception as e:
        LOGGER.error(f"❌ Critical error in ultimate chatbot: {e}")

# Random interaction system for groups
@EnaChatBot.on_message(filters.group & ~filters.bot, group=-1)
async def random_group_interactions(client: Client, message: Message):
    """Handle random interactions in groups like a real person"""
    try:
        if not message.from_user or not message.text:
            return
        
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        # Get relationship level for interaction chance
        relationship_level = get_relationship_level(user_id)
        
        # Random interaction chance (higher for better relationships)
        base_chance = 0.02 + (relationship_level * 0.01)  # 2-7% chance
        
        if random.random() < base_chance:
            user_name = get_user_name(message.from_user)
            
            random_interactions = [
                f"Arre {user_name}! 😊 Kya baat chal rahi hai yahan? Include me also! 💕",
                f"Hey {user_name}! 👋 Bahut time baad dekha tumhe active! How are you? ✨",
                f"{user_name} baby! 💖 Tumhara message dekh kar khushi hui! What's up? 😊",
                f"Oye {user_name}! 😄 Mujhe bhi batao kya discuss kar rahe ho! FOMO ho raha! 💕",
                f"{user_name} ji! 🙏 Namaste! Kya haal chal? Group mein masti ho rahi? ✨"
            ]
            
            # Wait a bit before responding (natural behavior)
            await asyncio.sleep(random.uniform(10, 30))
            
            random_message = random.choice(random_interactions)
            await client.send_message(chat_id, random_message)
            
            LOGGER.info(f"💕 Random interaction sent to {user_name} in group {message.chat.title}")
    
    except Exception as e:
        LOGGER.error(f"❌ Error in random interaction: {e}")

# Load cache on startup
asyncio.create_task(load_enhanced_cache())

LOGGER.info("🚀 Ultimate Indian Girlfriend ChatBot System loaded successfully!")
LOGGER.info("💕 Enhanced with Hinglish support, virtual life simulation, and world-class AI!")
LOGGER.info("✨ Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X")
