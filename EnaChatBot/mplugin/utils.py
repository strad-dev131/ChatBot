# EnaChatBot/mplugin/utils.py

import asyncio
from EnaChatBot.utils.logger import get_logger

LOGGER = get_logger(__name__)

def get_user_id(message) -> int:
    """
    Extract Telegram user ID from a message object.
    """
    return message.from_user.id if message.from_user else None

def get_chat_id(message) -> int:
    """
    Extract chat ID from message object.
    """
    return message.chat.id if message.chat else None

async def safe_reply(message, text: str):
    """
    Reply to a message object safely by catching exceptions.
    """
    try:
        await message.reply(text)
    except Exception as e:
        LOGGER.error(f"Failed to send reply: {e}")

async def safe_edit(message, text: str):
    """
    Edit a message safely by catching exceptions.
    """
    try:
        await message.edit(text)
    except Exception as e:
        LOGGER.error(f"Failed to edit message: {e}")

def extract_args(message) -> list:
    """Extract arguments from a command message"""
    if len(message.command) > 1:
        return message.command[1:]
    return []

async def delete_message_after_delay(message, delay: int = 5):
    """Delete a message after specified delay"""
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        LOGGER.error(f"Failed to delete message: {e}")