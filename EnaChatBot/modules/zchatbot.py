import random
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from datetime import datetime, timedelta
from pyrogram.enums import ChatMember, ChatType
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from EnaChatBot.database.chats import add_served_chat
from EnaChatBot.database.users import add_served_user
from config import MONGO_URL
from EnaChatBot import EnaChatBot, mongo, LOGGER, db

# Import AI functionality with error handling
try:
    from EnaChatBot.openrouter_ai import (
        get_ai_response, 
        get_flirty_response, 
        get_cute_response, 
        get_sweet_response,
        is_ai_enabled
    )
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    LOGGER.warning("AI module not available - using fallback responses")

# Import helpers
from EnaChatBot.modules.helpers import chatai, CHATBOT_ON
from EnaChatBot.modules.helpers import (
    ABOUT_BTN,
    ABOUT_READ,
    ADMIN_READ,
    BACK,
    CHATBOT_BACK,
    CHATBOT_READ,
    DEV_OP,
    HELP_BTN,
    HELP_READ,
    MUSIC_BACK_BTN,
    SOURCE_READ,
    START,
    TOOLS_DATA_READ,
)
import asyncio

translator = GoogleTranslator()

lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status

replies_cache = []
blocklist = {}
message_counts = {}

# Enhanced personality responses
GIRL_RESPONSES = [
    "Hey babe! 💕 What's up?",
    "Aww, you're so sweet! 😘",
    "OMG really?! Tell me more! 😍",
    "Hehe, you're making me blush! 😊",
    "That's so cute! 💖",
    "You're such a sweetheart! 🥰",
    "I love talking to you! 💕",
    "You always know what to say! 😌",
    "That made me smile! 😊",
    "You're the best! 💫",
    "Aww, that's adorable! 🥺💕",
    "You're so funny! 😂",
    "I'm so happy you texted! 💖",
    "You brighten my day! ☀️💕",
    "That's amazing, babe! ✨",
    "You're incredible! 🌟",
    "I missed you! 💝",
    "You're my favorite person! 💕",
    "That's so thoughtful! 🥰",
    "You make me so happy! 😊💖"
]

FLIRTY_RESPONSES = [
    "You're such a charmer! 😘",
    "Stop making me fall for you! 💕😍",
    "You know just what to say! 😏💖",
    "You're dangerous... I like it! 😈💕",
    "Careful, you're making my heart race! 💓",
    "You're trouble... but the good kind! 😉",
    "Are you trying to make me blush? 😊💕",
    "You have such a way with words! 😍",
    "I can't resist you! 💖",
    "You're irresistible! 😘💕"
]

CARING_RESPONSES = [
    "Are you okay, sweetie? 🥺💕",
    "I hope you're taking care of yourself! 💖",
    "You mean so much to me! 💝",
    "I'm always here for you! 🤗💕",
    "Take care of yourself, babe! 💖",
    "I believe in you! 💪✨",
    "You're stronger than you know! 💕",
    "I'm proud of you! 🥰💖",
    "You deserve all the happiness! 🌈💕",
    "Remember, you're amazing! ⭐💖"
]

PLAYFUL_RESPONSES = [
    "Hehe, you're so silly! 😂💕",
    "You crack me up! 🤣",
    "That's so random, I love it! 😄💖",
    "You're such a goofball! 😊",
    "LMAO you're hilarious! 😂💕",
    "You always make me laugh! 😄",
    "You're so goofy, I adore it! 🥰",
    "That's why I like you! 😉💕",
    "You're one of a kind! 🌟",
    "Never change, you're perfect! 💖"
]

# AI response categories
AI_RESPONSE_CATEGORIES = {
    "romantic": ["love", "beautiful", "gorgeous", "stunning", "amazing", "incredible"],
    "flirty": ["cute", "pretty", "hot", "sexy", "attractive", "charm"],
    "caring": ["sad", "tired", "help", "problem", "worried", "stress", "upset", "hurt"],
    "playful": ["haha", "lol", "funny", "joke", "lmao", "😂", "🤣", "silly"],
    "greeting": ["hi", "hello", "hey", "good morning", "good night", "how are you"]
}

async def load_replies_cache():
    global replies_cache
    try:
        if chatai:
            replies_cache = await chatai.find().to_list(length=None)
    except:
        replies_cache = []

async def save_reply(original_message: Message, reply_message: Message):
    global replies_cache
    try:
        reply_data = {
            "word": original_message.text,
            "text": None,
            "check": "none",
        }

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
        elif reply_message.text:
            reply_data["text"] = reply_message.text
            reply_data["check"] = "none"

        if chatai:
            is_chat = await chatai.find_one(reply_data)
            if not is_chat:
                await chatai.insert_one(reply_data)
                replies_cache.append(reply_data)

    except Exception as e:
        LOGGER.error(f"Error in save_reply: {e}")

async def get_reply(word: str):
    global replies_cache
    if not replies_cache:
        await load_replies_cache()
    
    relevant_replies = [reply for reply in replies_cache if reply['word'] == word]
    if not relevant_replies:
        relevant_replies = replies_cache
    
    if relevant_replies:
        return random.choice(relevant_replies)
    
    return None

def categorize_message(message_text: str) -> str:
    """Categorize message to determine response type"""
    text_lower = message_text.lower()
    
    for category, keywords in AI_RESPONSE_CATEGORIES.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    
    return "default"

async def get_ai_personality_response(message_text: str, user_name: str, category: str) -> str:
    """Get AI response based on message category"""
    
    if not AI_AVAILABLE or not is_ai_enabled():
        return get_fallback_response(message_text, category)
    
    try:
        # Use different AI personalities based on category
        if category == "flirty" or category == "romantic":
            response = await get_flirty_response(message_text, user_name)
        elif category == "caring":
            response = await get_sweet_response(message_text, user_name)
        elif category == "playful":
            response = await get_cute_response(message_text, user_name)
        else:
            response = await get_ai_response(message_text, user_name)
        
        return response if response else get_fallback_response(message_text, category)
        
    except Exception as e:
        LOGGER.error(f"AI response error: {e}")
        return get_fallback_response(message_text, category)

def get_fallback_response(message_text: str, category: str) -> str:
    """Get fallback response when AI is not available"""
    
    if category == "romantic" or category == "flirty":
        return random.choice(FLIRTY_RESPONSES)
    elif category == "caring":
        return random.choice(CARING_RESPONSES)
    elif category == "playful":
        return random.choice(PLAYFUL_RESPONSES)
    else:
        return random.choice(GIRL_RESPONSES)

async def get_chat_language(chat_id):
    try:
        chat_lang = await lang_db.find_one({"chat_id": chat_id})
        return chat_lang["language"] if chat_lang and "language" in chat_lang else None
    except:
        return None

def get_user_name(user) -> str:
    """Get user's name for personalization"""
    if user.first_name:
        return user.first_name
    elif user.username:
        return user.username
    else:
        return "babe"
 
@EnaChatBot.on_message(filters.incoming & ~filters.bot)
async def chatbot_response(client: Client, message: Message):
    global blocklist, message_counts
    try:
        if not message.from_user:
            return
            
        user_id = message.from_user.id
        chat_id = message.chat.id
        current_time = datetime.now()
        
        # FIXED: Properly distinguish between group chats and private chats
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
            chat_status = await status_db.find_one({"chat_id": chat_id})
            if chat_status and chat_status.get("status") == "disabled":
                return
        except:
            pass

        # Skip commands
        if message.text and any(message.text.startswith(prefix) for prefix in ["!", "/", ".", "?", "@", "#"]):
            # FIXED: Properly add served chats/users
            if is_group:
                await add_served_chat(chat_id)
            elif is_private:
                await add_served_user(user_id)  # Use user_id not chat_id for private chats
            return
        
        # FIXED: Determine when to respond in groups vs private
        should_respond = False
        
        if is_private:
            should_respond = True
        elif is_group:
            # In groups, only respond if:
            # 1. Reply to bot message
            # 2. Bot is mentioned
            # 3. Message contains bot username
            if message.reply_to_message and message.reply_to_message.from_user.id == EnaChatBot.id:
                should_respond = True
            elif EnaChatBot.username and f"@{EnaChatBot.username}" in (message.text or ""):
                should_respond = True
            elif EnaChatBot.first_name and EnaChatBot.first_name.lower() in (message.text or "").lower():
                should_respond = True
        
        if should_respond and message.text:
            # Show typing action for more realistic feel
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            await asyncio.sleep(1)  # Simulate thinking time
            
            user_name = get_user_name(message.from_user)
            
            # First try database responses for consistency
            reply_data = await get_reply(message.text)
            
            if reply_data and reply_data["check"] != "none":
                # Handle media responses
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
            
            # Get AI or fallback response
            category = categorize_message(message.text)
            
            if reply_data and reply_data["text"]:
                # Use database text response but enhance it
                response_text = reply_data["text"]
                
                # Add some feminine touches to database responses
                if not any(emoji in response_text for emoji in ["💕", "😘", "🥰", "💖", "😊"]):
                    feminine_emojis = ["💕", "😘", "🥰", "💖", "😊", "✨"]
                    response_text += f" {random.choice(feminine_emojis)}"
                    
            else:
                # Get fresh AI response
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
            
            # Send the response
            await message.reply_text(response_text)

        # Save user replies for learning (only text responses)
        if message.reply_to_message and message.text:
            await save_reply(message.reply_to_message, message)
            
        # FIXED: Properly add served chats/users
        if is_group:
            await add_served_chat(chat_id)
        elif is_private:
            await add_served_user(user_id)  # Use user_id not chat_id

    except MessageEmpty:
        cute_empty_responses = [
            "🙄💕 What are you trying to say babe?",
            "😊💖 I didn't get that sweetie!",
            "🥰✨ Can you say that again honey?"
        ]
        await message.reply_text(random.choice(cute_empty_responses))
    except Exception as e:
        LOGGER.error(f"Error in chatbot response: {e}")
        return
