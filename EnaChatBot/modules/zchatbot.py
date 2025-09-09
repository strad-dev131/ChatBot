import random
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from datetime import datetime, timedelta
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from EnaChatBot.database.chats import add_served_chat
from EnaChatBot.database.users import add_served_user
from config import MONGO_URL
from EnaChatBot import EnaChatBot, mongo, LOGGER, db

# FIXED: Import helpers
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

# Enhanced chatbot responses with more personality
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
        print(f"Error in save_reply: {e}")

async def get_reply(word: str):
    global replies_cache
    if not replies_cache:
        await load_replies_cache()
    
    # Try to find exact match first
    relevant_replies = [reply for reply in replies_cache if reply['word'] == word]
    
    # If no exact match, use any random reply
    if not relevant_replies:
        relevant_replies = replies_cache
    
    if relevant_replies:
        return random.choice(relevant_replies)
    
    # If no replies in database, use built-in girl responses
    return None

def get_personality_response(message_text: str) -> str:
    """Get a personality-based response"""
    text_lower = message_text.lower()
    
    # Flirty keywords
    if any(word in text_lower for word in ['beautiful', 'cute', 'pretty', 'love', 'like you', 'gorgeous', 'stunning']):
        return random.choice(FLIRTY_RESPONSES)
    
    # Caring/emotional keywords
    elif any(word in text_lower for word in ['sad', 'tired', 'help', 'problem', 'worried', 'stress']):
        return random.choice(CARING_RESPONSES)
    
    # Playful/funny keywords
    elif any(word in text_lower for word in ['haha', 'lol', 'funny', 'joke', 'lmao', '😂', '🤣']):
        return random.choice(PLAYFUL_RESPONSES)
    
    # Default girl responses
    else:
        return random.choice(GIRL_RESPONSES)

async def get_chat_language(chat_id):
    try:
        chat_lang = await lang_db.find_one({"chat_id": chat_id})
        return chat_lang["language"] if chat_lang and "language" in chat_lang else None
    except:
        return None
 
@EnaChatBot.on_message(filters.incoming)
async def chatbot_response(client: Client, message: Message):
    global blocklist, message_counts
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        current_time = datetime.now()
        
        # Clean up old blocked users
        blocklist = {uid: time for uid, time in blocklist.items() if time > current_time}

        if user_id in blocklist:
            return

        # Rate limiting
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
            await message.reply_text(f"**Hey, {message.from_user.mention}** 💕\n\n**You're sending too many messages! Take a break for 1 minute babe! 😘**")
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
            if message.chat.type in ["group", "supergroup"]:
                return await add_served_chat(chat_id)
            else:
                return await add_served_user(chat_id)
        
        # Only respond if replied to bot or direct message
        if (message.reply_to_message and message.reply_to_message.from_user.id == EnaChatBot.id) or not message.reply_to_message:
            
            # First try to get response from database
            reply_data = await get_reply(message.text)
            
            response_text = None
            
            if reply_data:
                response_text = reply_data["text"]
                
                # Handle different media types
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
            
            # If no database response, use personality responses
            if not response_text:
                response_text = get_personality_response(message.text or "")
            
            # Translate if needed
            try:
                chat_lang = await get_chat_language(chat_id)
                if chat_lang and chat_lang != "nolang" and chat_lang != "en":
                    translated_text = GoogleTranslator(source='auto', target=chat_lang).translate(response_text)
                    if translated_text:
                        response_text = translated_text
            except Exception as e:
                # If translation fails, use original text
                pass
            
            # Send the response
            await message.reply_text(response_text)

        # Save user replies for learning
        if message.reply_to_message:
            await save_reply(message.reply_to_message, message)

    except MessageEmpty:
        await message.reply_text("🙄🙄")
    except Exception as e:
        LOGGER.error(f"Error in chatbot response: {e}")
        return
