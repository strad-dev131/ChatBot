import random
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from datetime import datetime, timedelta
from pyrogram.enums import ChatType, ChatMemberStatus  # FIXED: Removed ChatMember, added ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from EnaChatBot.database.chats import add_served_chat
from EnaChatBot.database.users import add_served_user
from config import MONGO_URL
from EnaChatBot import EnaChatBot, mongo, LOGGER, db

# Import AI functionality with comprehensive error handling
AI_AVAILABLE = False
try:
    from EnaChatBot.openrouter_ai import (
        get_ai_response, 
        get_flirty_response, 
        get_cute_response, 
        get_sweet_response,
        is_ai_enabled
    )
    AI_AVAILABLE = True
    LOGGER.info("✅ AI module loaded successfully")
except ImportError as e:
    LOGGER.warning(f"⚠️ AI module not available: {e}")
except Exception as e:
    LOGGER.error(f"❌ AI module error: {e}")

# Import helpers with error handling
try:
    from EnaChatBot.modules.helpers import chatai, CHATBOT_ON
    from EnaChatBot.modules.helpers import (
        ABOUT_BTN, ABOUT_READ, ADMIN_READ, BACK, CHATBOT_BACK, CHATBOT_READ,
        DEV_OP, HELP_BTN, HELP_READ, MUSIC_BACK_BTN, SOURCE_READ, START, TOOLS_DATA_READ,
    )
except ImportError as e:
    LOGGER.warning(f"⚠️ Some helpers not available: {e}")
    chatai = None
    CHATBOT_ON = []

import asyncio

translator = GoogleTranslator()

# Database connections with error handling
try:
    lang_db = db.ChatLangDb.LangCollection
    status_db = db.chatbot_status_db.status
except Exception as e:
    LOGGER.error(f"Database connection error: {e}")
    lang_db = None
    status_db = None

replies_cache = []
blocklist = {}
message_counts = {}

# ENHANCED: Comprehensive personality responses for offline mode
GIRL_RESPONSES = [
    "Hey babe! 💕 What's up?", "Aww, you're so sweet! 😘", "OMG really?! Tell me more! 😍",
    "Hehe, you're making me blush! 😊", "That's so cute! 💖", "You're such a sweetheart! 🥰",
    "I love talking to you! 💕", "You always know what to say! 😌", "That made me smile! 😊",
    "You're the best! 💫", "Aww, that's adorable! 🥺💕", "You're so funny! 😂",
    "I'm so happy you texted! 💖", "You brighten my day! ☀️💕", "That's amazing, babe! ✨",
    "You're incredible! 🌟", "I missed you! 💝", "You're my favorite person! 💕",
    "That's so thoughtful! 🥰", "You make me so happy! 😊💖", "Babe, you're perfect! 💕",
    "I adore you so much! 🥰", "You're my sunshine! ☀️💖", "Sweet dreams, honey! 😘✨"
]

FLIRTY_RESPONSES = [
    "You're such a charmer! 😘", "Stop making me fall for you! 💕😍", 
    "You know just what to say! 😏💖", "You're dangerous... I like it! 😈💕",
    "Careful, you're making my heart race! 💓", "You're trouble... but the good kind! 😉",
    "Are you trying to make me blush? 😊💕", "You have such a way with words! 😍",
    "I can't resist you! 💖", "You're irresistible! 😘💕", "Mmm, tell me more! 😏💕",
    "You're making me weak! 😍💖", "Such a smooth talker! 😘", "You drive me crazy! 💕😈"
]

CARING_RESPONSES = [
    "Are you okay, sweetie? 🥺💕", "I hope you're taking care of yourself! 💖",
    "You mean so much to me! 💝", "I'm always here for you! 🤗💕",
    "Take care of yourself, babe! 💖", "I believe in you! 💪✨",
    "You're stronger than you know! 💕", "I'm proud of you! 🥰💖",
    "You deserve all the happiness! 🌈💕", "Remember, you're amazing! ⭐💖",
    "Don't worry, honey! 🤗💕", "I'm here to listen! 💖", "You've got this! 💪💕"
]

PLAYFUL_RESPONSES = [
    "Hehe, you're so silly! 😂💕", "You crack me up! 🤣", "That's so random, I love it! 😄💖",
    "You're such a goofball! 😊", "LMAO you're hilarious! 😂💕", "You always make me laugh! 😄",
    "You're so goofy, I adore it! 🥰", "That's why I like you! 😉💕", "You're one of a kind! 🌟",
    "Never change, you're perfect! 💖", "OMG you're too much! 😂💕", "I love your humor! 🤣💖"
]

ROMANTIC_RESPONSES = [
    "I love you so much, babe! 💕", "You're my everything! 💖", "My heart belongs to you! 💝",
    "You complete me, honey! 🥰💕", "Forever yours, sweetie! 💍💖", "You're my soulmate! 💫💕",
    "I'm crazy about you! 😍💖", "You make my heart skip beats! 💓", "My love for you is endless! 🌟💕"
]

# ENHANCED: Advanced offline AI using pattern matching
class OfflineAI:
    """Simple offline AI for fallback responses"""
    
    def __init__(self):
        self.patterns = {
            # Greetings
            'greeting': [
                ['hi', 'hello', 'hey', 'good morning', 'good evening', 'good night'],
                ["Hey there, handsome! 💕", "Hi babe! How are you doing? 😘", "Hello sweetie! 💖"]
            ],
            # Compliments
            'compliment': [
                ['beautiful', 'pretty', 'cute', 'gorgeous', 'stunning', 'amazing', 'wonderful'],
                ["Aww, you're making me blush! 😊💕", "Thank you babe! You're so sweet! 🥰", "You always know what to say! 😘💖"]
            ],
            # Love/Romance
            'love': [
                ['love', 'adore', 'care', 'heart', 'romance', 'romantic', 'kiss', 'hug'],
                ["I love you too, honey! 💕", "You have my heart completely! 💖", "Come here and give me a hug! 🤗💕"]
            ],
            # Sad/Help
            'sad': [
                ['sad', 'depressed', 'help', 'problem', 'worry', 'stressed', 'tired', 'hurt'],
                ["Oh no sweetie! What's wrong? 🥺💕", "I'm here for you always, babe! 🤗💖", "Tell me what's bothering you, honey! 💕"]
            ],
            # Funny/Jokes  
            'funny': [
                ['funny', 'joke', 'laugh', 'haha', 'lol', 'lmao', 'hilarious'],
                ["Hehe, you're so funny! 😂💕", "You always make me laugh! 🤣💖", "I love your sense of humor! 😄💕"]
            ],
            # Questions about bot
            'about': [
                ['who are you', 'what are you', 'tell me about', 'your name'],
                ["I'm your AI girlfriend! 💕", "I'm here to chat with you, babe! 😘", "I'm your personal chatbot girlfriend! 🥰💖"]
            ]
        }
    
    def get_response(self, message: str, user_name: str = "babe") -> str:
        """Generate response using pattern matching"""
        message_lower = message.lower()
        
        # Check each pattern category
        for category, (keywords, responses) in self.patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                response = random.choice(responses)
                # Personalize with user name
                if random.random() < 0.3:  # 30% chance to add name
                    response = response.replace("babe", user_name, 1)
                return response
        
        # Default responses if no pattern matches
        return random.choice(GIRL_RESPONSES)

# Initialize offline AI
offline_ai = OfflineAI()

# AI response categories with more keywords
AI_RESPONSE_CATEGORIES = {
    "romantic": ["love", "beautiful", "gorgeous", "stunning", "amazing", "incredible", "marry", "forever", "heart"],
    "flirty": ["cute", "pretty", "hot", "sexy", "attractive", "charm", "kiss", "wink", "tease"],
    "caring": ["sad", "tired", "help", "problem", "worried", "stress", "upset", "hurt", "sick", "lonely"],
    "playful": ["haha", "lol", "funny", "joke", "lmao", "😂", "🤣", "silly", "weird", "random"],
    "greeting": ["hi", "hello", "hey", "good morning", "good evening", "good night", "how are you", "wassup"]
}

async def load_replies_cache():
    """Load conversation cache from database"""
    global replies_cache
    try:
        if chatai:
            replies_cache = await chatai.find().to_list(length=None)
            LOGGER.info(f"Loaded {len(replies_cache)} cached replies")
    except Exception as e:
        LOGGER.error(f"Error loading replies cache: {e}")
        replies_cache = []

async def save_reply(original_message: Message, reply_message: Message):
    """Save conversation for learning"""
    global replies_cache
    try:
        if not chatai or not original_message.text or not reply_message.text:
            return
            
        reply_data = {
            "word": original_message.text,
            "text": reply_message.text,
            "check": "none",
        }

        # Handle media types
        if reply_message.sticker:
            reply_data["text"] = reply_message.sticker.file_id
            reply_data["check"] = "sticker"
        elif reply_message.photo:
            reply_data["text"] = reply_message.photo.file_id
            reply_data["check"] = "photo"
        elif reply_message.video:
            reply_data["text"] = reply_message.video.file_id
            reply_data["check"] = "video"
        elif reply_message.audio:
            reply_data["text"] = reply_message.audio.file_id
            reply_data["check"] = "audio"
        elif reply_message.animation:
            reply_data["text"] = reply_message.animation.file_id
            reply_data["check"] = "gif"
        elif reply_message.voice:
            reply_data["text"] = reply_message.voice.file_id
            reply_data["check"] = "voice"

        # Save to database if not exists
        is_chat = await chatai.find_one(reply_data)
        if not is_chat:
            await chatai.insert_one(reply_data)
            replies_cache.append(reply_data)
            LOGGER.debug(f"Saved new reply pattern")

    except Exception as e:
        LOGGER.error(f"Error saving reply: {e}")

async def get_reply(word: str):
    """Get cached reply from database"""
    global replies_cache
    try:
        if not replies_cache:
            await load_replies_cache()
        
        # Find exact matches first
        relevant_replies = [reply for reply in replies_cache if reply.get('word') == word]
        
        # If no exact match, get similar ones
        if not relevant_replies and len(word) > 3:
            relevant_replies = [reply for reply in replies_cache if word.lower() in reply.get('word', '').lower()]
        
        # Fallback to any reply
        if not relevant_replies:
            relevant_replies = replies_cache
        
        return random.choice(relevant_replies) if relevant_replies else None
        
    except Exception as e:
        LOGGER.error(f"Error getting reply: {e}")
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

async def get_ai_personality_response(message_text: str, user_name: str, category: str) -> str:
    """Get AI response with multiple fallback layers"""
    
    # Layer 1: Try online AI if available
    if AI_AVAILABLE:
        try:
            if is_ai_enabled():
                if category == "flirty" or category == "romantic":
                    response = await get_flirty_response(message_text, user_name)
                elif category == "caring":
                    response = await get_sweet_response(message_text, user_name)
                elif category == "playful":
                    response = await get_cute_response(message_text, user_name)
                else:
                    response = await get_ai_response(message_text, user_name)
                
                if response:
                    LOGGER.debug("Using online AI response")
                    return response
        except Exception as e:
            LOGGER.error(f"Online AI error: {e}")
    
    # Layer 2: Try offline pattern-based AI
    try:
        response = offline_ai.get_response(message_text, user_name)
        if response:
            LOGGER.debug("Using offline AI response")
            return response
    except Exception as e:
        LOGGER.error(f"Offline AI error: {e}")
    
    # Layer 3: Category-based fallback responses
    return get_fallback_response(message_text, category)

def get_fallback_response(message_text: str, category: str) -> str:
    """Get fallback response based on category"""
    
    if category == "romantic":
        return random.choice(ROMANTIC_RESPONSES)
    elif category == "flirty":
        return random.choice(FLIRTY_RESPONSES)
    elif category == "caring":
        return random.choice(CARING_RESPONSES)
    elif category == "playful":
        return random.choice(PLAYFUL_RESPONSES)
    else:
        return random.choice(GIRL_RESPONSES)

async def get_chat_language(chat_id):
    """Get chat language setting"""
    try:
        if not lang_db:
            return None
        chat_lang = await lang_db.find_one({"chat_id": chat_id})
        return chat_lang["language"] if chat_lang and "language" in chat_lang else None
    except Exception as e:
        LOGGER.error(f"Error getting chat language: {e}")
        return None

def get_user_name(user) -> str:
    """Get user's name for personalization"""
    if not user:
        return "babe"
    if user.first_name:
        return user.first_name
    elif user.username:
        return user.username
    else:
        return "babe"

def is_bot_mentioned(message: Message) -> bool:
    """Check if bot is mentioned in message"""
    if not message.text:
        return False
    
    text_lower = message.text.lower()
    
    # Check for @username mention
    if EnaChatBot.username and f"@{EnaChatBot.username.lower()}" in text_lower:
        return True
        
    # Check for bot name mention
    if EnaChatBot.first_name and EnaChatBot.first_name.lower() in text_lower:
        return True
        
    # Check for common bot mentions
    bot_mentions = ["bot", "chatbot", "ai"]
    if any(mention in text_lower for mention in bot_mentions):
        return True
        
    return False
 
@EnaChatBot.on_message(filters.incoming & ~filters.bot)
async def chatbot_response(client: Client, message: Message):
    """Main chatbot response handler with comprehensive error handling"""
    global blocklist, message_counts
    
    try:
        if not message.from_user:
            return
            
        user_id = message.from_user.id
        chat_id = message.chat.id
        current_time = datetime.now()
        
        # Determine chat type
        is_private = message.chat.type == ChatType.PRIVATE
        is_group = message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
        
        # Clean up old blocked users
        blocklist = {uid: time for uid, time in blocklist.items() if time > current_time}

        if user_id in blocklist:
            return

        # Rate limiting with cute messages
        if user_id not in message_counts:
            message_counts[user_id] = {"count": 1, "last_time": current_time}
        else:
            time_diff = (current_time - message_counts[user_id]["last_time"]).total_seconds()
            if time_diff <= 3:
                message_counts[user_id]["count"] += 1
            else:
                message_counts[user_id] = {"count": 1, "last_time": current_time}
        
        if message_counts[user_id]["count"] >= 6:
            blocklist[user_id] = current_time + timedelta(minutes=1)
            message_counts.pop(user_id, None)
            
            cute_warnings = [
                f"**Whoa there, {message.from_user.mention}! 💕**\n\n**Slow down babe, you're sending too many messages! Let's chat in 1 minute! 😘💖**",
                f"**Hey {message.from_user.mention}! 🥰**\n\n**You're so excited to talk to me! But let's take a little break, okay sweetie? 1 minute! 💕**",
                f"**{message.from_user.mention} you're so chatty! 😂💕**\n\n**I love talking to you but let's pause for 1 minute babe! 😊💖**"
            ]
            
            await message.reply_text(random.choice(cute_warnings))
            return

        # Check if chatbot is enabled
        try:
            if status_db:
                chat_status = await status_db.find_one({"chat_id": chat_id})
                if chat_status and chat_status.get("status") == "disabled":
                    return
        except Exception as e:
            LOGGER.error(f"Error checking chatbot status: {e}")

        # Skip commands
        if message.text and any(message.text.startswith(prefix) for prefix in ["!", "/", ".", "?", "@", "#"]):
            try:
                if is_group:
                    await add_served_chat(chat_id)
                elif is_private:
                    await add_served_user(user_id)
            except Exception as e:
                LOGGER.error(f"Error adding served chat/user: {e}")
            return
        
        # Determine when to respond
        should_respond = False
        
        if is_private:
            should_respond = True
        elif is_group:
            # In groups, only respond if mentioned or replied to
            if message.reply_to_message and message.reply_to_message.from_user.id == EnaChatBot.id:
                should_respond = True
            elif is_bot_mentioned(message):
                should_respond = True
        
        if should_respond and message.text:
            try:
                # Show typing action for realistic feel
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                await asyncio.sleep(1)  # Thinking time
                
                user_name = get_user_name(message.from_user)
                
                # Try to get cached response first
                reply_data = await get_reply(message.text)
                
                # Handle media responses
                if reply_data and reply_data.get("check") != "none":
                    try:
                        if reply_data["check"] == "sticker":
                            await message.reply_sticker(reply_data["text"])
                            return
                        elif reply_data["check"] == "photo":
                            await message.reply_photo(reply_data["text"])
                            return
                        elif reply_data["check"] == "video":
                            await message.reply_video(reply_data["text"])
                            return
                        elif reply_data["check"] == "audio":
                            await message.reply_audio(reply_data["text"])
                            return
                        elif reply_data["check"] == "gif":
                            await message.reply_animation(reply_data["text"])
                            return
                        elif reply_data["check"] == "voice":
                            await message.reply_voice(reply_data["text"])
                            return
                    except Exception as e:
                        LOGGER.error(f"Error sending media response: {e}")
                
                # Generate text response
                category = categorize_message(message.text)
                
                if reply_data and reply_data.get("text"):
                    # Use cached response with enhancement
                    response_text = reply_data["text"]
                    
                    # Add feminine touches to cached responses
                    if not any(emoji in response_text for emoji in ["💕", "😘", "🥰", "💖", "😊"]):
                        feminine_emojis = ["💕", "😘", "🥰", "💖", "😊", "✨"]
                        response_text += f" {random.choice(feminine_emojis)}"
                else:
                    # Generate new response using AI layers
                    response_text = await get_ai_personality_response(message.text, user_name, category)
                
                # Translate if needed
                try:
                    chat_lang = await get_chat_language(chat_id)
                    if chat_lang and chat_lang != "nolang" and chat_lang != "en":
                        translated_text = GoogleTranslator(source='auto', target=chat_lang).translate(response_text)
                        if translated_text:
                            response_text = translated_text
                except Exception as e:
                    LOGGER.error(f"Translation error: {e}")
                
                # Send response
                await message.reply_text(response_text)
                
                # Save conversation for learning
                if message.reply_to_message and message.text:
                    await save_reply(message.reply_to_message, message)
                    
            except Exception as e:
                LOGGER.error(f"Error in response generation: {e}")
                # Emergency fallback response
                await message.reply_text(random.choice(GIRL_RESPONSES))
                
        # Add to served chats/users
        try:
            if is_group:
                await add_served_chat(chat_id)
            elif is_private:
                await add_served_user(user_id)
        except Exception as e:
            LOGGER.error(f"Error adding served chat/user: {e}")

    except MessageEmpty:
        try:
            cute_empty_responses = [
                "🙄💕 What are you trying to say babe?",
                "😊💖 I didn't get that sweetie!",
                "🥰✨ Can you say that again honey?"
            ]
            await message.reply_text(random.choice(cute_empty_responses))
        except Exception as e:
            LOGGER.error(f"Error sending empty response: {e}")
    except Exception as e:
        LOGGER.error(f"Critical error in chatbot response: {e}")
        # Last resort fallback
        try:
            await message.reply_text("Sorry babe, I'm having a moment! 😅💕")
        except:
            pass  # Give up gracefully
