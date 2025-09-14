# EnaChatBot Database - Chats Management
"""
Database operations for managing chats
"""

from motor.motor_asyncio import AsyncIOMotorClient
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# Database collections
try:
    from EnaChatBot import db
    chats_collection = db.chats
except ImportError:
    chats_collection = None
    logger.warning("Database connection not available")

async def add_served_chat(chat_id: int) -> bool:
    """
    Add a chat to the served chats database
    
    Args:
        chat_id (int): Chat ID to add
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if chats_collection is None:
            return False
            
        existing = await chats_collection.find_one({"chat_id": chat_id})
        if not existing:
            await chats_collection.insert_one({"chat_id": chat_id})
            logger.info(f"Added chat {chat_id} to served chats")
        return True
    except Exception as e:
        logger.error(f"Error adding served chat {chat_id}: {e}")
        return False

async def remove_served_chat(chat_id: int) -> bool:
    """
    Remove a chat from the served chats database
    
    Args:
        chat_id (int): Chat ID to remove
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if chats_collection is None:
            return False
            
        await chats_collection.delete_one({"chat_id": chat_id})
        logger.info(f"Removed chat {chat_id} from served chats")
        return True
    except Exception as e:
        logger.error(f"Error removing served chat {chat_id}: {e}")
        return False

async def get_served_chats() -> List[Dict]:
    """
    Get all served chats from database
    
    Returns:
        List[Dict]: List of chat documents
    """
    try:
        if chats_collection is None:
            return []
            
        chats = []
        async for chat in chats_collection.find():
            chats.append(chat)
        return chats
    except Exception as e:
        logger.error(f"Error getting served chats: {e}")
        return []

async def is_served_chat(chat_id: int) -> bool:
    """
    Check if a chat is already served
    
    Args:
        chat_id (int): Chat ID to check
        
    Returns:
        bool: True if chat is served, False otherwise
    """
    try:
        if chats_collection is None:
            return False
            
        chat = await chats_collection.find_one({"chat_id": chat_id})
        return chat is not None
    except Exception as e:
        logger.error(f"Error checking served chat {chat_id}: {e}")
        return False

async def get_chat_count() -> int:
    """
    Get the total number of served chats
    
    Returns:
        int: Number of served chats
    """
    try:
        if chats_collection is None:
            return 0
            
        count = await chats_collection.count_documents({})
        return count
    except Exception as e:
        logger.error(f"Error getting chat count: {e}")
        return 0

async def update_chat_info(chat_id: int, chat_data: dict) -> bool:
    """
    Update chat information in database
    
    Args:
        chat_id (int): Chat ID to update
        chat_data (dict): Data to update
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if chats_collection is None:
            return False
            
        await chats_collection.update_one(
            {"chat_id": chat_id},
            {"$set": chat_data},
            upsert=True
        )
        return True
    except Exception as e:
        logger.error(f"Error updating chat info for {chat_id}: {e}")
        return False

async def get_chat_info(chat_id: int) -> Dict:
    """
    Get chat information from database
    
    Args:
        chat_id (int): Chat ID to get info for
        
    Returns:
        Dict: Chat information or empty dict
    """
    try:
        if chats_collection is None:
            return {}
            
        chat = await chats_collection.find_one({"chat_id": chat_id})
        return chat or {}
    except Exception as e:
        logger.error(f"Error getting chat info for {chat_id}: {e}")
        return {}

async def clear_all_chats() -> bool:
    """
    Clear all chats from database (admin only)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if chats_collection is None:
            return False
            
        await chats_collection.delete_many({})
        logger.warning("Cleared all served chats from database")
        return True
    except Exception as e:
        logger.error(f"Error clearing all chats: {e}")
        return False
