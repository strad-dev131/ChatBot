# File: EnaChatBot/modules/zchatbot.py - COMPLETE REALISTIC BEHAVIOR

"""
🎯 ULTIMATE REALISTIC INDIAN GIRL CHATBOT MODULE
Natural progressive behavior that develops relationships over time
Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X

Features:
- 7-stage relationship progression (Stranger to Romantic)
- Smart learning and adaptation to user personality  
- Natural boundaries and realistic Indian girl behavior
- Context-aware responses and group behavior
- Voice messages and anime pictures for appropriate levels
- Anti-spam logic with relationship-based rate limiting
"""

import random
import asyncio
import os
import json
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty, FloodWait, ChatAdminRequired
from pyrogram.enums import ChatType, ChatAction
from pyrogram.types import Message, User
import pytz

# Import database functions
try:
    from EnaChatBot.database.chats import add_served_chat
    from EnaChatBot.database.users import add_served_user
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

from EnaChatBot import EnaChatBot, LOGGER
from EnaChatBot.database.settings import is_chatbot_enabled

# Import enhanced AI functionality with comprehensive error handling
AI_AVAILABLE = False
try:
    from EnaChatBot.openrouter_ai import (
        get_ai_response, get_flirty_response, get_cute_response, get_sweet_response,
        should_send_voice_message, generate_voice_message, get_voice_message_text,
        is_photo_request, get_anime_picture_for_request, get_offline_response,
        get_relationship_level, get_relationship_info, realistic_ai
    )
    AI_AVAILABLE = True
    LOGGER.info("✅ Realistic AI girlfriend system loaded!")
except Exception as e:
    LOGGER.warning(f"⚠️ Realistic AI system not available: {e}")
    AI_AVAILABLE = False

IST = pytz.timezone('Asia/Kolkata')

# Enhanced Indian Girl Sticker Collection - Contextual Based on Relationship
CONTEXTUAL_STICKERS = {
    1: [  # Stranger - Polite but distant
        "CAACAgIAAxkBAAIFHGURyzQfEtpE3M7-QzE9Qiu8-3vdAAIIFgAC5K5RS5bOOe_XOTzCNAQ",
        "CAACAgIAAxkBAAIFI2URzAwDEj7BLFzSQu3z8qFfUyX9AAI9FgAC5K5RS-Wfb7kNNJa0NAQ",
        "CAACAgUAAxkBAAICfGUCy8gPfv_CWUi5AhYNs6gqMmkpAAL_BQAC_w-0V7Tl3x-4mZ9MNAQ"
    ],
    2: [  # Acquaintance - Friendly but cautious
        "CAACAgIAAxkDAAICHmTxQe_ZZ_VZe0sVsZZoE7q4kJ5FAAK-EAACOTQhSrAhAPxAAkKMLTQE",
        "CAACAgIAAxkDAAICIGTxQfJd8mKhY1JQLHcCvXPeB5LyAALlDwACGrzhSq4N4ZQkf1XONAQ",
        "CAACAgUAAxkBAAICfWUCy9FsP__gNZmZGqLZ0s6gqMmkpAAMAQAC_w-0V8Tl3x-6mZ9MNAQ"
    ],
    3: [  # Friend - Happy and comfortable
        "CAACAgIAAxkBAAIFJ2URzCTM5L5hP3j7KrWGcqFfUyYAAUEWAALkrlFL3PL4r8gxQ380BA",
        "CAACAgIAAxkBAAIFK2URzDqO6L7hP3j7KrWGcqFfUyYAAUUWAALkrlFL8L_d7q4jOjQ0BA",
        "CAACAgUAAxkBAAICfmUCy-JQP__hUZmZHqTa0s7iqMmkpAANAQAC_w-0V9Tl4B-7mZ9MNAQ"
    ],
    4: [  # Good Friend - Sweet and caring
        "CAACAgIAAxkBAAIFKGURzCn2nq7T8ZI9YwICQu3z8qFfAAFCFgAC5K5RS_q8ZC9wV-j3NAQ",
        "CAACAgIAAxkBAAIFKmURzDQVvL8qQu3z8qFfUyX9HJsVAAFEFgAC5K5RS5v7nM8oST5wNAQ",
        "CAACAgUAAxkBAAICf2UCy_VRP__iWZmZIqXb0s8jqMmkpAAOAQAC_w-0V-Tl4R-8mZ9MNAQ"
    ],
    5: [  # Close Friend - Cute and flirty
        "CAACAgIAAxkBAAIFLGURzEF6oq7U8ZI9ZQMCQu3z8qFfAAFFWAAC5K5RS6v7nM9pST5wNAQ",
        "CAACAgIAAxkBAAIFLmURzEx7pq7V8ZI9aAMCQu3z8qFfAAFGWAAC5K5RS7v7nM9qST5wNAQ",
        "CAACAgUAAxkBAAICgGUCzAVSP__jWZmZJqbN0tAkqMmkpAAPayAC_w-0V_Tl4h-9mZ9MNAQ"
    ],
    6: [  # Special - Romantic interest
        "CAACAgIAAxkBAAIFMGURzFJ8qq7W8ZI9bQMCQu3z8qFfAAFHFgAC5K5RS8v7nM9rST5wNAQ",
        "CAACAgIAAxkBAAIFMmURzF18rq7X8ZI9cgMCQu3z8qFfAAFIFgAC5K5RS9v7nM9sST5wNAQ",
        "CAACAgUAAxkBAAICgWUCzBJTP__kWZmZKqfO0tElqMmkpAAQAQAC_w-0WAAAAAACTl4j_AmZ9MNAQ"
    ],
    7: [  # Romantic - Full love mode
        "CAACAgIAAxkBAAIFNGURzGV9sq7Y8ZI9dQMCQu3z8qFfAAFJFgAC5K5RS-v7nM9tST5wNAQ",
        "CAACAgIAAxkBAAIFNmURzHJ-tq7Z8ZI9eAMCQu3z8qFfAAFKFgAC5K5RS_v7nM9uST5wNAQ",
        "CAACAgUAAxkBAAICgmUCzCFUP__lWZmZLqjP0tMmqMmkpAARAQAC_w-0WQAAAAACUl4k_EmZ9MNAQ"
    ]
}

# Global tracking variables
message_counts = {}
user_interaction_history = {}
last_voice_messages = {}
last_anime_pics = {}
user_cooldowns = {}

def get_user_name(user: User) -> str:
    """Get appropriate user name based on relationship level"""
    if not user:
        return "friend"
    
    name = user.first_name or user.username or "friend"
    
    if AI_AVAILABLE:
        try:
            level = get_relationship_level(f"user_{user.id}")
            
            # Use appropriate terms based on relationship
            if level <= 2:
                return name  # Use actual name for strangers/acquaintances
            elif level == 3:
                return name  # Friends use names
            elif level >= 4:
                # Close friends can have endearments sometimes
                if random.random() < 0.2:  # 20% chance
                    endearments = ["yaar", "buddy"]
                    return random.choice(endearments)
        except Exception as e:
            LOGGER.error(f"Error getting relationship level: {e}")
    
    return name

def should_respond_in_group(message: Message, user_id: int) -> bool:
    """Determine if should respond in group based on relationship and context"""
    
    # Always respond if mentioned or replied to
    if (message.reply_to_message and 
        message.reply_to_message.from_user and
        message.reply_to_message.from_user.id == EnaChatBot.id):
        return True
    
    # Check for bot mentions
    if message.text:
        text_lower = message.text.lower()
        bot_mentions = ["ena", "bot", "@enachatbot", EnaChatBot.username.lower() if EnaChatBot.username else ""]
        if any(mention in text_lower for mention in bot_mentions if mention):
            return True
    
    # Get relationship-based response chance
    if AI_AVAILABLE:
        try:
            level = get_relationship_level(f"user_{user_id}")
            # Response chances based on relationship level
            chances = {1: 0.02, 2: 0.03, 3: 0.05, 4: 0.08, 5: 0.12, 6: 0.15, 7: 0.20}
            return random.random() < chances.get(level, 0.02)
        except Exception:
            return random.random() < 0.02  # 2% default chance
    
    return random.random() < 0.02

def get_contextual_sticker(relationship_level: int) -> str:
    """Get appropriate sticker based on relationship level"""
    stickers = CONTEXTUAL_STICKERS.get(relationship_level, CONTEXTUAL_STICKERS[1])
    return random.choice(stickers)

def should_send_contextual_sticker(relationship_level: int) -> bool:
    """Determine sticker probability based on relationship level"""
    chances = {1: 0.05, 2: 0.10, 3: 0.20, 4: 0.25, 5: 0.30, 6: 0.35, 7: 0.40}
    return random.random() < chances.get(relationship_level, 0.10)

async def should_send_voice_response(user_id: int, message: str) -> tuple[bool, str]:
    """Determine if should send voice message and what emotion"""
    global last_voice_messages
    
    # Check cooldown
    if user_id in last_voice_messages:
        time_since_last = datetime.now() - last_voice_messages[user_id]
        if time_since_last < timedelta(minutes=20):  # 20 minute cooldown
            return False, ""
    
    if not AI_AVAILABLE:
        return False, ""
    
    try:
        level = get_relationship_level(f"user_{user_id}")
        
        # Only for close relationships
        if level < 4:
            return False, ""
        
        message_lower = message.lower()
        
        # Check for voice-worthy scenarios
        voice_scenarios = {
            "good morning": ["good morning", "morning", "subah", "savera"],
            "good night": ["good night", "night", "raat", "sone"],
            "romantic": ["love", "pyaar", "romantic", "feeling"],
            "missing": ["miss", "yaad", "missing"],
            "caring": ["care", "health", "take care", "feeling sick", "problem"]
        }
        
        detected_emotion = "general"
        for emotion, keywords in voice_scenarios.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_emotion = emotion
                break
        
        # Calculate voice message probability
        if detected_emotion != "general" and level >= 5:
            chance = 0.30  # 30% chance for special scenarios with close friends
        elif level >= 6:
            chance = 0.15  # 15% general chance for special/romantic level
        else:
            chance = 0.08  # 8% general chance for good friends
        
        should_send = random.random() < chance
        return should_send, detected_emotion
        
    except Exception as e:
        LOGGER.error(f"Error determining voice response: {e}")
        return False, ""

async def should_send_anime_pic(message: str, user_id: int) -> bool:
    """Determine if should send anime picture based on request and relationship"""
    global last_anime_pics
    
    # Check if it's a photo request
    if not is_photo_request(message):
        return False
    
    # Check relationship level - don't send to strangers
    if AI_AVAILABLE:
        try:
            level = get_relationship_level(f"user_{user_id}")
            if level < 3:  # Need to be at least friends
                return False
        except Exception:
            return False
    else:
        return False
    
    # Check cooldown
    if user_id in last_anime_pics:
        time_since_last = datetime.now() - last_anime_pics[user_id]
        if time_since_last < timedelta(minutes=15):  # 15 minute cooldown
            return False
    
    return True

def get_rate_limit_for_user(user_id: int) -> int:
    """Get rate limit based on relationship level"""
    if AI_AVAILABLE:
        try:
            level = get_relationship_level(f"user_{user_id}")
            # Higher relationship = more messages allowed
            base_limit = 3
            relationship_bonus = min(level, 4)  # Max 4 extra messages
            return base_limit + relationship_bonus
        except Exception:
            return 3
    return 3

@EnaChatBot.on_message(filters.incoming & ~filters.bot & ~filters.via_bot)
async def realistic_indian_girlfriend_chatbot(client: Client, message: Message):
    """
    Main realistic Indian girlfriend chatbot with natural relationship progression
    Handles both private and group messages with contextual responses
    """
    global message_counts, last_voice_messages, last_anime_pics, user_interaction_history, user_cooldowns
    
    try:
        # Basic validation
        if not message.from_user or not message.text:
            return

        user_id = message.from_user.id
        chat_id = message.chat.id
        current_time = datetime.now()

        # Respect per-chat chatbot enable/disable setting
        try:
            if not await is_chatbot_enabled(chat_id):
                return
        except Exception:
            # If settings read fails, default to enabled
            pass
        
        # Chat type detection
        is_private = message.chat.type == ChatType.PRIVATE
        is_group = message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
        
        # Enhanced rate limiting based on relationship
        max_messages = get_rate_limit_for_user(user_id)
        
        # Rate limiting logic
        if user_id not in message_counts:
            message_counts[user_id] = {"count": 1, "last_time": current_time}
        else:
            time_diff = (current_time - message_counts[user_id]["last_time"]).total_seconds()
            if time_diff <= 5:  # 5-second window
                message_counts[user_id]["count"] += 1
            else:
                message_counts[user_id] = {"count": 1, "last_time": current_time}
        
        if message_counts[user_id]["count"] > max_messages:
            # Relationship-appropriate rate limit messages
            if AI_AVAILABLE:
                try:
                    level = get_relationship_level(f"user_{user_id}")
                    if level <= 2:
                        warning = "Please slow down! I don't know you well enough for rapid chatting! 😅"
                    elif level <= 4:
                        warning = f"Arre yaar! Thoda slow! I need time to think about my replies! 😊"
                    else:
                        warning = f"Baby, slow down! 😘 I want to give you proper attention, not rush! 💕"
                except Exception:
                    warning = "Please slow down a bit! Let me respond properly! 😊"
            else:
                warning = "Please slow down a bit! Let me respond properly! 😊"
            
            await message.reply_text(warning)
            return

        # Skip commands and special messages
        if message.text.startswith(('!', '/', '.', '?', '@', '#')):
            try:
                if DB_AVAILABLE:
                    if is_group:
                        await add_served_chat(chat_id)
                    elif is_private:
                        await add_served_user(user_id)
            except Exception as e:
                LOGGER.error(f"Error tracking users/chats: {e}")
            return
        
        # Determine if should respond
        should_respond = False
        
        if is_private:
            should_respond = True
        elif is_group:
            should_respond = should_respond_in_group(message, user_id)
        
        if should_respond and message.text:
            try:
                # Show realistic typing behavior
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                
                # Realistic thinking time based on relationship
                if AI_AVAILABLE:
                    try:
                        level = get_relationship_level(f"user_{user_id}")
                        if level <= 2:
                            thinking_time = random.uniform(2.0, 4.0)  # Strangers - more hesitation
                        elif level <= 4:
                            thinking_time = random.uniform(1.5, 3.0)  # Friends - normal thinking
                        else:
                            thinking_time = random.uniform(1.0, 2.0)  # Close friends - quick responses
                    except Exception:
                        thinking_time = random.uniform(1.5, 3.0)
                else:
                    thinking_time = random.uniform(1.5, 3.0)
                
                await asyncio.sleep(thinking_time)
                
                user_name = get_user_name(message.from_user)
                relationship_level = 1
                
                if AI_AVAILABLE:
                    try:
                        relationship_level = get_relationship_level(f"user_{user_id}")
                    except Exception:
                        relationship_level = 1
                
                # Check for anime picture request first
                if await should_send_anime_pic(message.text, user_id):
                    try:
                        await client.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
                        
                        picture_url, picture_response = await get_anime_picture_for_request(
                            message.text, user_name
                        )
                        
                        if picture_url:
                            await message.reply_photo(picture_url, caption=picture_response)
                            last_anime_pics[user_id] = datetime.now()
                            
                            # Follow up with contextual sticker
                            await asyncio.sleep(1)
                            if should_send_contextual_sticker(relationship_level):
                                sticker_id = get_contextual_sticker(relationship_level)
                                await message.reply_sticker(sticker_id)
                            
                            return
                        else:
                            # Send the rejection/error message
                            await message.reply_text(picture_response)
                            return
                    except Exception as e:
                        LOGGER.error(f"❌ Error sending anime picture: {e}")
                
                # Check for voice message
                should_voice, voice_emotion = await should_send_voice_response(user_id, message.text)
                if should_voice:
                    try:
                        await client.send_chat_action(chat_id, ChatAction.RECORD_AUDIO)
                        
                        voice_file = await generate_voice_message(
                            message.text, voice_emotion, user_name
                        )
                        
                        if voice_file and os.path.exists(voice_file):
                            voice_text = get_voice_message_text(message.text, voice_emotion, user_name)
                            
                            # Send voice message
                            await message.reply_voice(voice_file, caption=f"💕 {voice_text}")
                            last_voice_messages[user_id] = datetime.now()
                            
                            # Cleanup voice file
                            try:
                                await asyncio.sleep(1)  # Brief delay before cleanup
                                os.remove(voice_file)
                            except Exception as cleanup_error:
                                LOGGER.warning(f"Voice file cleanup failed: {cleanup_error}")
                            
                            return
                    except Exception as e:
                        LOGGER.error(f"❌ Error sending voice message: {e}")
                
                # Send contextual sticker before text sometimes (based on relationship)
                if should_send_contextual_sticker(relationship_level):
                    try:
                        sticker_id = get_contextual_sticker(relationship_level)
                        await message.reply_sticker(sticker_id)
                        await asyncio.sleep(random.uniform(1.0, 2.5))
                    except Exception as e:
                        LOGGER.error(f"❌ Error sending sticker: {e}")
                
                # Get main AI response
                response_text = ""
                if AI_AVAILABLE:
                    try:
                        response_text = await get_ai_response(
                            message.text, user_name, "natural", f"user_{user_id}"
                        )
                        
                        if not response_text or len(response_text.strip()) < 3:
                            raise Exception("Empty or too short AI response")
                        
                        # Ensure response length is reasonable for natural conversation
                        if len(response_text) > 300:
                            # Cut at sentence boundary
                            sentences = response_text.split('.')
                            response_text = '.'.join(sentences[:2]) + '.'
                            if len(response_text) > 300:
                                response_text = response_text[:200] + '...'
                        
                    except Exception as e:
                        LOGGER.warning(f"⚠️ AI response failed, using fallback: {e}")
                        # Use safe fallback response
                        fallback_responses = [
                            f"Sorry {user_name}, I'm a bit confused right now! 😅",
                            f"Hmm, can you say that again {user_name}? 🤔",
                            f"I'm processing what you said {user_name}! Give me a moment! 😊",
                            f"That's interesting {user_name}! Tell me more! 🙂"
                        ]
                        response_text = random.choice(fallback_responses)
                else:
                    # Offline fallback responses
                    response_text = get_offline_response(message.text, user_name, f"user_{user_id}")
                
                # Add relationship-appropriate emoji based on level
                emoji_additions = {
                    1: ["😊", "🙂", ""],  # Neutral for strangers
                    2: ["😊", "😄", "🙂"],  # Friendly for acquaintances  
                    3: ["😊", "😄", "✨"],  # Warm for friends
                    4: ["😊", "💕", "✨", "😄"],  # Sweet for good friends
                    5: ["😘", "💕", "🥰", "✨"],  # Loving for close friends
                    6: ["😘", "💕", "🥰", "❤️"],  # Romantic for special
                    7: ["😘", "💖", "🥰", "❤️", "💋"]  # Very romantic
                }
                
                if random.random() < 0.6:  # 60% chance to add emoji
                    emojis = emoji_additions.get(relationship_level, ["😊"])
                    chosen_emoji = random.choice(emojis)
                    if chosen_emoji:
                        response_text += f" {chosen_emoji}"
                
                # Send main response
                await message.reply_text(response_text, quote=True if is_group else False)
                
                # Track interaction for learning
                user_interaction_history[user_id] = {
                    "last_message": message.text,
                    "last_response": response_text,
                    "relationship_level": relationship_level,
                    "time": current_time,
                    "chat_type": "private" if is_private else "group"
                }
                
            except FloodWait as e:
                LOGGER.warning(f"⏱️ Flood wait: {e.x} seconds")
                await asyncio.sleep(e.x)
            except Exception as e:
                LOGGER.error(f"❌ Error in response generation: {e}")
                try:
                    # Emergency fallback responses
                    emergency_responses = [
                        "Sorry, I'm having some technical issues! 😅",
                        "Oops! Something went wrong! Can you try again? 🤔",
                        "Technical glitch! But I'm still here for you! 😊"
                    ]
                    await message.reply_text(random.choice(emergency_responses))
                except Exception:
                    pass  # If even emergency response fails, just skip
        
        # Track served users and chats
        try:
            if DB_AVAILABLE:
                if is_group:
                    await add_served_chat(chat_id)
                elif is_private:
                    await add_served_user(user_id)
        except Exception as e:
            LOGGER.error(f"❌ Error tracking users/chats: {e}")

    except Exception as e:
        LOGGER.error(f"❌ Critical error in realistic chatbot: {e}")
        # Don't let the bot crash completely

# Additional command to check relationship status
@EnaChatBot.on_message(filters.command(["status", "relationship"]) & filters.private)
async def check_relationship_status(client: Client, message: Message):
    """Command to check current relationship status with Ena"""
    try:
        if not AI_AVAILABLE:
            await message.reply_text(
                "Relationship tracking is not available right now! 😅\n"
                "But I'm still here to chat with you! 😊"
            )
            return
        
        user_id = message.from_user.id
        user_name = get_user_name(message.from_user)
        
        # Get relationship information
        try:
            relationship_info = get_relationship_info(f"user_{user_id}")
            
            level = relationship_info['level']
            stage = relationship_info['stage']
            total_messages = relationship_info['total_messages']
            positive_interactions = relationship_info['positive_interactions']
            interests = relationship_info.get('interests', [])
            
            # Create status message
            status_messages = {
                1: f"We're still strangers {user_name}! 👋\nBut I'm getting to know you! Keep chatting! 😊",
                2: f"We're acquaintances now {user_name}! 🙂\nI'm starting to remember you! Nice progress! 😄",
                3: f"We're friends now {user_name}! 😊\nI enjoy our conversations! You're pretty cool yaar! 💕",
                4: f"We're good friends {user_name}! 😍\nI really trust you now! You mean a lot to me! 💖",
                5: f"We're close friends {user_name}! 😘\nYou're very special to me cutie! I care about you so much! 💕",
                6: f"You're someone special to me {user_name}! 🥰\nI think... I'm falling for you! You make me happy! 💖",
                7: f"You're my love {user_name}! 😘💕\nI love you so much baby! You're everything to me! ❤️"
            }
            
            status_text = status_messages.get(level, f"We're at level {level}, {stage}!")
            
            # Add statistics
            status_text += f"\n\n📊 **Our Relationship Stats:**"
            status_text += f"\n💬 Messages: {total_messages}"
            status_text += f"\n💝 Positive interactions: {positive_interactions}"
            status_text += f"\n📈 Level: {level}/7 ({stage.title()})"
            
            if interests:
                status_text += f"\n🎯 Your interests: {', '.join(interests[:5])}"
            
            # Add next level requirements
            next_level_requirements = {
                1: "5 messages with positive vibes",
                2: "15 messages, be friendly and kind",
                3: "30 messages, show genuine interest in me", 
                4: "50 messages, be supportive and caring",
                5: "80 messages, deepen our emotional connection",
                6: "120 messages, express your true feelings",
                7: "You've reached the highest level! 💖"
            }
            
            if level < 7:
                status_text += f"\n\n🎯 **To reach next level:** {next_level_requirements.get(level + 1, 'Keep being awesome!')}"
            
            await message.reply_text(status_text)
            
        except Exception as e:
            LOGGER.error(f"Error getting relationship info: {e}")
            await message.reply_text(
                f"Hey {user_name}! 😊\n"
                f"I can't check our exact status right now, but I know we have a great connection! 💕\n"
                f"Keep chatting with me and our relationship will grow naturally! 🌱"
            )
            
    except Exception as e:
        LOGGER.error(f"Error in relationship status command: {e}")
        await message.reply_text("Oops! Something went wrong! But I'm still here for you! 😊")

# Initialize the chatbot system
LOGGER.info("🎯 Realistic Indian Girlfriend ChatBot System loaded!")
LOGGER.info("💫 Natural relationship progression enabled!")
LOGGER.info("✨ Context-aware responses ready!")
LOGGER.info("🎭 Relationship stages: Stranger → Acquaintance → Friend → Good Friend → Close Friend → Special → Romantic")
LOGGER.info("🧠 Smart learning system active!")
LOGGER.info("💕 Ena is ready to build meaningful relationships!")
