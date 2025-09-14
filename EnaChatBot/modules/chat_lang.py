from pyrogram import Client, filters
from pyrogram.types import Message
from EnaChatBot import EnaChatBot as app, mongo, db
import asyncio

# FIXED: Import languages from helpers
from EnaChatBot.modules.helpers import chatai, CHATBOT_ON, languages
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

lang_db = db.ChatLangDb.LangCollection
message_cache = {}

async def get_chat_language(chat_id):
    chat_lang = await lang_db.find_one({"chat_id": chat_id})
    return chat_lang["language"] if chat_lang and "language" in chat_lang else None

# FIXED: Commented out the problematic auto language detection temporarily
# This was causing issues with the MukeshAPI
@app.on_message(filters.text, group=2)
async def store_messages(client, message: Message):
    """
    Store messages for language detection
    Note: MukeshAPI dependency commented out until proper API setup
    """
    global message_cache

    chat_id = message.chat.id
    chat_lang = await get_chat_language(chat_id)

    if not chat_lang or chat_lang == "nolang":
        if message.from_user and message.from_user.is_bot:
            return

        if chat_id not in message_cache:
            message_cache[chat_id] = []

        message_cache[chat_id].append(message)

        # FIXED: Temporarily disabled auto language detection
        # Need to set up proper API key for MukeshAPI
        if len(message_cache[chat_id]) >= 30:
            # Clear cache to prevent memory issues
            message_cache[chat_id].clear()
            
            # For now, just notify about language setting
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("sᴇʟᴇᴄᴛ ʟᴀɴɢᴜᴀɢᴇ", callback_data="choose_lang")]]) 
            await message.reply_text(
                "**💬 I've noticed you're chatting in this group!**\n\n"
                "**🌍 Please set your preferred language for better responses.**\n\n"
                "**Use /lang to set the chat language.**", 
                reply_markup=reply_markup
            )

@app.on_message(filters.command("chatlang"))
async def fetch_chat_lang(client, message):
    chat_id = message.chat.id
    chat_lang = await get_chat_language(chat_id)
    if chat_lang:
        await message.reply_text(f"The language code using for this chat is: **{chat_lang}**")
    else:
        await message.reply_text("No specific language set for this chat. Using default (English).")
