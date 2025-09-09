# EnaChatBot Plugin System
"""
This directory contains plugin modules for the EnaChatBot clone system.
These plugins are loaded when cloned bots are created.
"""

from pyrogram import Client, filters
from pyrogram.types import Message
import logging

# Plugin logger
logger = logging.getLogger(__name__)

# Plugin initialization
def init_plugins():
    """Initialize plugin system"""
    logger.info("🔌 Initializing plugin system...")
    return True

# Helper functions for plugins
def is_owner(user_id: int) -> bool:
    """Check if user is owner of a cloned bot"""
    from config import OWNER_ID
    from EnaChatBot import CLONE_OWNERS, get_clone_owner
    
    # Check if user is main owner
    if user_id == int(OWNER_ID):
        return True
    
    # Check if user is clone owner
    for bot_id, owner_id in CLONE_OWNERS.items():
        if owner_id == user_id:
            return True
    
    return False

def get_bot_owner(bot_id: int):
    """Get owner of a cloned bot"""
    from EnaChatBot import CLONE_OWNERS
    return CLONE_OWNERS.get(bot_id)

# Default plugin handlers for cloned bots
@Client.on_message(filters.command("start"))
async def clone_start_handler(client: Client, message: Message):
    """Start command for cloned bots"""
    await message.reply_text(
        f"**👋 Hello {message.from_user.mention}!**\n\n"
        f"**I'm {client.me.first_name}, a cloned chatbot!**\n\n"
        f"**Type /help to see available commands.**"
    )

@Client.on_message(filters.command("help"))
async def clone_help_handler(client: Client, message: Message):
    """Help command for cloned bots"""
    help_text = """**🤖 Help Menu**

**Available Commands:**
• /start - Start the bot
• /help - Show this help menu
• /ping - Check bot status
• /id - Get your user ID
• /chatbot - Enable/disable chatbot
• /lang - Set language
• /shayri - Get random shayri

**This is a cloned bot powered by EnaChatBot.**"""
    
    await message.reply_text(help_text)

@Client.on_message(filters.command("ping"))
async def clone_ping_handler(client: Client, message: Message):
    """Ping command for cloned bots"""
    await message.reply_text(
        f"**🏓 Pong!**\n\n"
        f"**{client.me.first_name} is alive and working!**"
    )
