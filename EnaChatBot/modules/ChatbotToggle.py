from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from EnaChatBot import EnaChatBot, LOGGER
from EnaChatBot.database.settings import enable_chatbot, disable_chatbot, is_chatbot_enabled, get_chat_language

USAGE_TEXT = (
    "**🤖 Chatbot Control**\n\n"
    "**Usage:** `/chatbot on` or `/chatbot off`\n"
    "• Enable or disable AI chatbot responses in this chat.\n\n"
    "**Other commands:**\n"
    "• `/status` - Show chatbot status for this chat\n"
    "• `/chatlang` - Show current chat language\n"
)

@EnaChatBot.on_message(filters.command(["chatbot"]))
async def chatbot_toggle(client: Client, message: Message):
    chat_id = message.chat.id
    args = message.command[1:] if len(message.command) > 1 else []

    if not args:
        return await message.reply_text(USAGE_TEXT)

    action = args[0].lower()

    if action in ("on", "enable", "start"):
        try:
            await enable_chatbot(chat_id)
            await message.reply_text("✅ Chatbot enabled for this chat.")
        except Exception as e:
            LOGGER.error(f"Error enabling chatbot for {chat_id}: {e}")
            await message.reply_text("❌ Failed to enable chatbot. Try again later.")
    elif action in ("off", "disable", "stop"):
        try:
            await disable_chatbot(chat_id)
            await message.reply_text("✅ Chatbot disabled for this chat.")
        except Exception as e:
            LOGGER.error(f"Error disabling chatbot for {chat_id}: {e}")
            await message.reply_text("❌ Failed to disable chatbot. Try again later.")
    else:
        await message.reply_text(USAGE_TEXT)

@EnaChatBot.on_message(filters.command(["status"]))
async def chatbot_status(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        enabled = await is_chatbot_enabled(chat_id)
        lang = await get_chat_language(chat_id) or "default"
        status = "✅ Enabled" if enabled else "❌ Disabled"
        await message.reply_text(f"**Chatbot Status:** {status}\n**Language:** `{lang}`")
    except Exception as e:
        LOGGER.error(f"Error reading chatbot status for {chat_id}: {e}")
        await message.reply_text("❌ Failed to read chatbot status.")