# EnaChatBot/database/settings.py
"""
Simple settings storage backed by MongoDB collections.

Provides helpers for:
- Chat language per chat
- Chatbot enabled/disabled per chat
"""

import logging
from typing import Optional

from EnaChatBot import db

logger = logging.getLogger(__name__)

# Collections
_lang_collection = db.chat_lang
_status_collection = db.chatbot_status


# Language helpers
async def set_chat_language(chat_id: int, lang_code: str) -> None:
    try:
        await _lang_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"language": lang_code}},
            upsert=True,
        )
    except Exception as e:
        logger.error(f"Failed to set chat language for {chat_id}: {e}")


async def reset_chat_language(chat_id: int) -> None:
    try:
        await _lang_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"language": "nolang"}},
            upsert=True,
        )
    except Exception as e:
        logger.error(f"Failed to reset chat language for {chat_id}: {e}")


async def get_chat_language(chat_id: int) -> Optional[str]:
    try:
        doc = await _lang_collection.find_one({"chat_id": chat_id})
        return doc.get("language") if doc else None
    except Exception as e:
        logger.error(f"Failed to get chat language for {chat_id}: {e}")
        return None


# Chatbot status helpers
async def enable_chatbot(chat_id: int) -> None:
    try:
        await _status_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"enabled": True}},
            upsert=True,
        )
    except Exception as e:
        logger.error(f"Failed to enable chatbot for {chat_id}: {e}")


async def disable_chatbot(chat_id: int) -> None:
    try:
        await _status_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"enabled": False}},
            upsert=True,
        )
    except Exception as e:
        logger.error(f"Failed to disable chatbot for {chat_id}: {e}")


async def is_chatbot_enabled(chat_id: int) -> bool:
    try:
        doc = await _status_collection.find_one({"chat_id": chat_id})
        # Default to enabled if not set
        return bool(doc.get("enabled", True)) if doc else True
    except Exception as e:
        logger.error(f"Failed to read chatbot status for {chat_id}: {e}")
        return True