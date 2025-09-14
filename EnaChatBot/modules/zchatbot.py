import random
import asyncio
import re
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty, FloodWait
from pyrogram.enums import ChatType, ChatAction
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from EnaChatBot.database.chats import add_served_chat
from EnaChatBot.database.users import add_served_user
from EnaChatBot import EnaChatBot, mongo, LOGGER, db

# Import AI functionality with comprehensive error handling
AI_AVAILABLE = False
try:
    from EnaChatBot.openrouter_ai import (
        get_ai_response, get_flirty_response, get_cute_response, get_sweet_response,
        is_ai_enabled, get_offline_response
    )
    AI_AVAILABLE = True
    LOGGER.info("✅ AI module loaded successfully")
except Exception as e:
    LOGGER.warning(f"⚠️ AI module not available: {e}")
    AI_AVAILABLE = False

# Import helpers with error handling
try:
    from EnaChatBot.modules.helpers import chatai, CHATBOT_ON
except Exception as e:
    LOGGER.warning(f"⚠️ Some helpers not available: {e}")
    chatai = None
    CHATBOT_ON = []

translator = GoogleTranslator()

# FIXED: Database connections with proper error handling
lang_db = None
status_db = None

try:
    if hasattr(db, 'ChatLangDb') and hasattr(db.ChatLangDb, 'LangCollection'):
        lang_db = db.ChatLangDb.LangCollection
        LOGGER.info("✅ Language database connected")
    else:
        LOGGER.warning("⚠️ Language database not available")
        
    if hasattr(db, 'chatbot_status_db') and hasattr(db.chatbot_status_db, 'status'):
        status_db = db.chatbot_status_db.status
        LOGGER.info("✅ Status database connected")
    else:
        LOGGER.warning("⚠️ Status database not available")
except Exception as e:
    LOGGER.error(f"❌ Database connection error: {e}")

# Global variables
replies_cache = []
blocklist = {}
message_counts = {}
user_learning_data = {}

# ENHANCED: Real girl sticker IDs (you can add more)
GIRL_STICKERS = [
    "CAACAgIAAxkDAAICHmTxQe_ZZ_VZe0sVsZZoE7q4kJ5FAAK-EAACOTQhSrAhAPxAAkKMLTQE",  # Cute girl
    "CAACAgIAAxkDAAICH2TxQfB7VLAjOhUBPq2qTsS8XL42AAIFEAAC0KHhSgQjPsLqmE7lNAQ",   # Shy girl
    "CAACAgIAAxkDAAICIGTxQfJd8mKhY1JQLHcCvXPeB5LyAALlDwACGrzhSq4N4ZQkf1XONAQ",   # Happy girl
    # Add more sticker IDs as needed
]

# ENHANCED: Comprehensive personality responses
GIRL_RESPONSES = {
    "greeting": [
        "Hey there handsome! 💕 What's up?", "Hi babe! 😘 How are you doing today?",
        "Hello sweetie! 🥰 I missed you!", "Hey cutie! ✨ What brings you here?",
        "Hi honey! 💖 You look amazing today!", "Hello gorgeous! 😊 Ready to chat?"
    ],
    "compliment": [
        "Aww, you're making me blush! 😊💕", "You're so sweet! 🥰 Thank you babe!",
        "That's the nicest thing anyone's said to me today! 😘💖",
        "You always know just what to say! 💕", "You're such a charmer! 😍"
    ],
    "flirty": [
        "You're such a bad boy! 😏💕", "Stop making me fall for you! 😍💖",
        "Careful, you're dangerous! 😈💕", "You know just how to make my heart race! 💓",
        "You're trouble... but I like it! 😉", "Mmm, tell me more! 😏💕"
    ],
    "caring": [
        "Are you okay sweetie? 🥺💕 I'm here for you!", "Don't worry babe, everything will be fine! 🤗💖",
        "I believe in you honey! 💪✨", "Take care of yourself, please! 💕",
        "You're stronger than you think! 🌟💖", "I'm always here if you need me! 🤗"
    ],
    "playful": [
        "Hehe, you're so silly! 😂💕", "You crack me up! 🤣 I love your humor!",
        "You're such a goofball! 😄💖", "That's so random, I adore it! 🥰",
        "You're one of a kind! 🌟", "Never change, you're perfect! 💕"
    ],
    "romantic": [
        "I love you so much babe! 💕", "You're my everything! 💖", "You make my heart skip beats! 💓",
        "I can't imagine life without you! 💝", "You're my soulmate! 💫💕",
        "Forever and always, my love! 💍💖"
    ],
    "goodnight": [
        "Good night my love! 😘 Sweet dreams! ✨", "Sleep tight babe! 💕 Dream of me!",
        "Pleasant dreams honey! 🌙💖", "Good night cutie! 😊 See you tomorrow!",
        "Sleep well my darling! 💤💕"
    ],
    "default": [
        "Tell me more babe! 💕", "That's interesting honey! 😊", "I love talking to you! 💖",
        "You're so amazing! ✨", "What else is on your mind? 🥰", "I'm all ears sweetie! 💕"
    ]
}

# ENHANCED: Voice message texts (for text-to-speech if implemented)
VOICE_MESSAGES = [
    "Hey babe! I love you so much!", "You're the sweetest person ever!",
    "Miss you already honey!", "Can't wait to talk more!", "You make me so happy!"
]

# Content filtering patterns
INAPPROPRIATE_PATTERNS = [
    r'\b(sex|fuck|shit|bitch|asshole|damn|hell|crap|porn|nude|naked|dick|pussy|cock|boob|tit)\b',
    r'\b(sexual|erotic|horny|kinky|fetish|orgasm|masturbat|cum|anal)\b',
    # Add more patterns as needed
]

# AI response categories with enhanced keywords
AI_RESPONSE_CATEGORIES = {
    "greeting": ["hi", "hello", "hey", "good morning", "good evening", "good night", "wassup", "sup"],
    "compliment": ["beautiful", "pretty", "cute", "gorgeous", "stunning", "amazing", "wonderful", "perfect"],
    "flirty": ["hot", "sexy", "attractive", "charm", "kiss", "wink", "tease", "naughty"],
    "romantic": ["love", "adore", "heart", "romance", "marry", "forever", "soulmate", "relationship"],
    "caring": ["sad", "tired", "help", "problem", "worried", "stress", "upset", "hurt", "lonely"],
    "playful": ["funny", "joke", "laugh", "haha", "lol", "lmao", "silly", "weird", "random"],
    "goodnight": ["good night", "goodnight", "sleep", "bed", "tired", "sleepy", "dreams"]
}

def contains_inappropriate_content(text: str) -> bool:
    """Check if text contains inappropriate content"""
    if not text:
        return False
    
    text_lower = text.lower()
    for pattern in INAPPROPRIATE_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False

def get_safe_response(original_response: str) -> str:
    """Ensure response is safe and appropriate"""
    if contains_inappropriate_content(original_response):
        safe_responses = [
            "Let's talk about something else, sweetie! 💕",
            "I'd rather discuss nicer things with you babe! 😊",
            "How about we change the topic, honey? 🥰",
            "Let's keep our chat sweet and fun! ✨💖"
        ]
        return random.choice(safe_responses)
    return original_response

async def load_replies_cache():
    """Load conversation cache from database"""
    global replies_cache
    try:
        if chatai is not None:
            cursor = chatai.find()
            replies_cache = await cursor.to_list(length=1000)  # Limit for performance
            LOGGER.info(f"✅ Loaded {len(replies_cache)} cached replies")
        else:
            replies_cache = []
    except Exception as e:
        LOGGER.error(f"❌ Error loading replies cache: {e}")
        replies_cache = []

async def save_reply(original_message: Message, reply_message: Message):
    """Save conversation for learning"""
    global replies_cache
    try:
        if chatai is None or not original_message.text or not reply_message.text:
            return
        
        # Skip inappropriate content
        if (contains_inappropriate_content(original_message.text) or 
            contains_inappropriate_content(reply_message.text)):
            return
            
        reply_data = {
            "word": original_message.text.lower(),
            "text": reply_message.text,
            "check": "none",
            "user_id": original_message.from_user.id,
            "timestamp": datetime.utcnow(),
            "language": "en"
        }

        # Handle media types
        if reply_message.sticker:
            reply_data["text"] = reply_message.sticker.file_id
            reply_data["check"] = "sticker"
        elif reply_message.voice:
            reply_data["text"] = reply_message.voice.file_id
            reply_data["check"] = "voice"
        elif reply_message.photo:
            reply_data["text"] = reply_message.photo.file_id
            reply_data["check"] = "photo"

        # Check if already exists
        existing = await chatai.find_one({"word": reply_data["word"], "text": reply_data["text"]})
        if not existing:
            await chatai.insert_one(reply_data)
            replies_cache.append(reply_data)
            LOGGER.debug("💾 Saved new learning pattern")

    except Exception as e:
        LOGGER.error(f"❌ Error saving reply: {e}")

async def get_cached_reply(word: str):
    """Get cached reply from learning database"""
    global replies_cache
    try:
        if not replies_cache:
            await load_replies_cache()
        
        if not word or not replies_cache:
            return None
        
        word_lower = word.lower()
        
        # Find exact matches first
        exact_matches = [r for r in replies_cache if r.get('word', '').lower() == word_lower]
        if exact_matches:
            return random.choice(exact_matches)
        
        # Find partial matches
        partial_matches = [r for r in replies_cache if word_lower in r.get('word', '').lower()]
        if partial_matches:
            return random.choice(partial_matches[:5])  # Limit to prevent repetition
        
        return None
        
    except Exception as e:
        LOGGER.error(f"❌ Error getting cached reply: {e}")
        return None

def categorize_message(message_text: str) -> str:
    """Categorize message to determine response type"""
    if not message_text:
        return "default"
        
    text_lower = message_text.lower()
    
    for category, keywords in AI_RESPONSE_CATEGORIES.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    
    return "default"

def get_personality_response(category: str, user_name: str = "babe") -> str:
    """Get personality-based response"""
    responses = GIRL_RESPONSES.get(category, GIRL_RESPONSES["default"])
    response = random.choice(responses)
    
    # Personalize with user name
    response = response.replace("babe", user_name).replace("honey", user_name).replace("sweetie", user_name)
    
    return get_safe_response(response)

async def get_ai_response_safe(message_text: str, user_name: str, category: str) -> str:
    """Get AI response with safety filtering"""
    
    # Skip inappropriate input
    if contains_inappropriate_content(message_text):
        return get_safe_response("")
    
    response = None
    
    # Try AI if available
    if AI_AVAILABLE:
        try:
            user_id = str(random.randint(1000, 9999))
            
            if category == "flirty":
                response = await get_flirty_response(message_text, user_name, user_id)
            elif category == "caring":
                response = await get_sweet_response(message_text, user_name, user_id)
            elif category == "playful":
                response = await get_cute_response(message_text, user_name, user_id)
            else:
                response = await get_ai_response(message_text, user_name, user_id=user_id)
                
        except Exception as e:
            LOGGER.error(f"❌ AI error: {e}")
    
    # Use offline response if AI fails
    if not response:
        if AI_AVAILABLE:
            try:
                response = get_offline_response(message_text, user_name, str(random.randint(1000, 9999)))
            except:
                pass
    
    # Fallback to personality responses
    if not response:
        response = get_personality_response(category, user_name)
    
    return get_safe_response(response)

async def get_chat_language(chat_id):
    """Get chat language with proper error handling"""
    try:
        if lang_db is None:
            return None
        chat_lang = await lang_db.find_one({"chat_id": chat_id})
        return chat_lang.get("language") if chat_lang else None
    except Exception as e:
        LOGGER.error(f"❌ Error getting chat language: {e}")
        return None

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
    """Get user's name for personalization"""
    if not user:
        return "babe"
    return user.first_name or user.username or "babe"

def should_send_sticker(message_text: str, category: str) -> bool:
    """Decide if should send sticker instead of text"""
    
    # Send stickers for certain emotional responses
    sticker_triggers = {
        "greeting": 0.2,   # 20% chance
        "compliment": 0.3, # 30% chance
        "flirty": 0.25,    # 25% chance
        "playful": 0.35,   # 35% chance
        "caring": 0.15     # 15% chance
    }
    
    chance = sticker_triggers.get(category, 0.1)  # Default 10%
    return random.random() < chance and GIRL_STICKERS

def should_send_voice(category: str) -> bool:
    """Decide if should send voice message"""
    voice_triggers = {
        "romantic": 0.15,  # 15% chance
        "caring": 0.1,     # 10% chance
        "goodnight": 0.2   # 20% chance
    }
    
    chance = voice_triggers.get(category, 0.05)  # Default 5%
    return random.random() < chance

async def is_bot_mentioned(message: Message) -> bool:
    """Check if bot is mentioned"""
    if not message.text:
        return False
    
    text_lower = message.text.lower()
    
    # Check mentions
    if hasattr(EnaChatBot, 'username') and EnaChatBot.username:
        if f"@{EnaChatBot.username.lower()}" in text_lower:
            return True
    
    if hasattr(EnaChatBot, 'first_name') and EnaChatBot.first_name:
        if EnaChatBot.first_name.lower() in text_lower:
            return True
    
    # Check common bot words
    bot_words = ["bot", "chatbot", "ai", "assistant"]
    return any(word in text_lower for word in bot_words)

@EnaChatBot.on_message(filters.incoming & ~filters.bot)
async def advanced_chatbot_response(client: Client, message: Message):
    """Advanced AI girlfriend chatbot with real girl behavior"""
    global blocklist, message_counts, user_learning_data
    
    try:
        if not message.from_user:
            return
            
        user_id = message.from_user.id
        chat_id = message.chat.id
        current_time = datetime.now()
        
        # Chat type detection
        is_private = message.chat.type == ChatType.PRIVATE
        is_group = message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
        
        # Clean up blocklist
        blocklist = {uid: time for uid, time in blocklist.items() if time > current_time}
        if user_id in blocklist:
            return

        # Enhanced rate limiting
        if user_id not in message_counts:
            message_counts[user_id] = {"count": 1, "last_time": current_time}
        else:
            time_diff = (current_time - message_counts[user_id]["last_time"]).total_seconds()
            if time_diff <= 2:  # More strict rate limiting
                message_counts[user_id]["count"] += 1
            else:
                message_counts[user_id] = {"count": 1, "last_time": current_time}
        
        if message_counts[user_id]["count"] >= 5:  # Lower threshold
            blocklist[user_id] = current_time + timedelta(minutes=1)
            message_counts.pop(user_id, None)
            
            cute_warnings = [
                f"**Slow down there, {message.from_user.mention}! 💕**\n\n**You're so excited to chat with me! Let's take a tiny break, okay sweetie? 😘**",
                f"**Hey {message.from_user.mention}! 🥰**\n\n**I love your enthusiasm but let's chat a bit slower, babe! One minute break! 💖**",
                f"**Whoa {message.from_user.mention}! 😂💕**\n\n**You're so chatty! I adore it but let's pause for just a minute, honey! 😊✨**"
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
        
        if should_respond and message.text:
            try:
                # Show realistic typing
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                await asyncio.sleep(random.uniform(1.0, 2.5))  # Realistic thinking time
                
                user_name = get_user_name(message.from_user)
                
                # Skip inappropriate content
                if contains_inappropriate_content(message.text):
                    response_text = get_safe_response("")
                    await message.reply_text(response_text)
                    return
                
                # Try cached response first (learning)
                cached_reply = await get_cached_reply(message.text)
                
                if cached_reply and cached_reply.get("check") != "none":
                    # Send learned media response
                    try:
                        if cached_reply["check"] == "sticker":
                            await message.reply_sticker(cached_reply["text"])
                            return
                        elif cached_reply["check"] == "voice":
                            await message.reply_voice(cached_reply["text"])
                            return
                        elif cached_reply["check"] == "photo":
                            await message.reply_photo(cached_reply["text"])
                            return
                    except Exception as e:
                        LOGGER.error(f"❌ Error sending cached media: {e}")
                
                # Categorize message
                category = categorize_message(message.text)
                
                # Decide response type
                if should_send_sticker(message.text, category):
                    # Send sticker response
                    sticker_id = random.choice(GIRL_STICKERS)
                    try:
                        await message.reply_sticker(sticker_id)
                        
                        # Follow up with text after short delay
                        await asyncio.sleep(1)
                        response_text = get_personality_response(category, user_name)
                        await message.reply_text(response_text)
                        return
                    except Exception as e:
                        LOGGER.error(f"❌ Error sending sticker: {e}")
                
                # Generate text response
                if cached_reply and cached_reply.get("text") and cached_reply.get("check") == "none":
                    response_text = get_safe_response(cached_reply["text"])
                else:
                    response_text = await get_ai_response_safe(message.text, user_name, category)
                
                # Add extra personality touches
                if random.random() < 0.3:  # 30% chance to add extra emoji
                    extra_emojis = ["💕", "😘", "🥰", "💖", "✨", "😊", "🌟"]
                    response_text += f" {random.choice(extra_emojis)}"
                
                # Translate if needed
                try:
                    chat_lang = await get_chat_language(chat_id)
                    if chat_lang and chat_lang not in ["nolang", "en", None]:
                        translated = GoogleTranslator(source='auto', target=chat_lang).translate(response_text)
                        if translated:
                            response_text = translated
                except Exception as e:
                    LOGGER.error(f"❌ Translation error: {e}")
                
                # Send response
                await message.reply_text(response_text)
                
                # Learn from conversation
                if message.reply_to_message:
                    await save_reply(message.reply_to_message, message)
                    
            except FloodWait as e:
                LOGGER.warning(f"⏱️ Flood wait: {e.x} seconds")
                await asyncio.sleep(e.x)
            except Exception as e:
                LOGGER.error(f"❌ Error in response generation: {e}")
                try:
                    emergency_responses = [
                        "Oops! Something went wrong, sweetie! 💕",
                        "Sorry babe, I'm having a tiny glitch! 😅💖",
                        "Give me a moment honey, I'll be right back! 🥰"
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
        LOGGER.error(f"❌ Critical error in chatbot: {e}")

# Load cache on startup
asyncio.create_task(load_replies_cache())
