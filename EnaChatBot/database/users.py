# EnaChatBot Database - Users Management
"""
Database operations for managing users
"""

from motor.motor_asyncio import AsyncIOMotorClient
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# Database collections
try:
    from EnaChatBot import db
    users_collection = db.users
except ImportError:
    users_collection = None
    logger.warning("Database connection not available")

async def add_served_user(user_id: int) -> bool:
    """
    Add a user to the served users database
    
    Args:
        user_id (int): User ID to add
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if users_collection is None:
            return False
            
        existing = await users_collection.find_one({"user_id": user_id})
        if not existing:
            await users_collection.insert_one({"user_id": user_id})
            logger.info(f"Added user {user_id} to served users")
        return True
    except Exception as e:
        logger.error(f"Error adding served user {user_id}: {e}")
        return False

async def remove_served_user(user_id: int) -> bool:
    """
    Remove a user from the served users database
    
    Args:
        user_id (int): User ID to remove
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if users_collection is None:
            return False
            
        await users_collection.delete_one({"user_id": user_id})
        logger.info(f"Removed user {user_id} from served users")
        return True
    except Exception as e:
        logger.error(f"Error removing served user {user_id}: {e}")
        return False

async def get_served_users() -> List[Dict]:
    """
    Get all served users from database
    
    Returns:
        List[Dict]: List of user documents
    """
    try:
        if users_collection is None:
            return []
            
        users = []
        async for user in users_collection.find():
            users.append(user)
        return users
    except Exception as e:
        logger.error(f"Error getting served users: {e}")
        return []

async def is_served_user(user_id: int) -> bool:
    """
    Check if a user is already served
    
    Args:
        user_id (int): User ID to check
        
    Returns:
        bool: True if user is served, False otherwise
    """
    try:
        if users_collection is None:
            return False
            
        user = await users_collection.find_one({"user_id": user_id})
        return user is not None
    except Exception as e:
        logger.error(f"Error checking served user {user_id}: {e}")
        return False

async def get_user_count() -> int:
    """
    Get the total number of served users
    
    Returns:
        int: Number of served users
    """
    try:
        if users_collection is None:
            return 0
            
        count = await users_collection.count_documents({})
        return count
    except Exception as e:
        logger.error(f"Error getting user count: {e}")
        return 0

async def update_user_info(user_id: int, user_data: dict) -> bool:
    """
    Update user information in database
    
    Args:
        user_id (int): User ID to update
        user_data (dict): Data to update
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if users_collection is None:
            return False
            
        await users_collection.update_one(
            {"user_id": user_id},
            {"$set": user_data},
            upsert=True
        )
        return True
    except Exception as e:
        logger.error(f"Error updating user info for {user_id}: {e}")
        return False

async def get_user_info(user_id: int) -> Dict:
    """
    Get user information from database
    
    Args:
        user_id (int): User ID to get info for
        
    Returns:
        Dict: User information or empty dict
    """
    try:
        if users_collection is None:
            return {}
            
        user = await users_collection.find_one({"user_id": user_id})
        return user or {}
    except Exception as e:
        logger.error(f"Error getting user info for {user_id}: {e}")
        return {}

async def ban_user(user_id: int, reason: str = "No reason provided") -> bool:
    """
    Ban a user from using the bot
    
    Args:
        user_id (int): User ID to ban
        reason (str): Reason for the ban
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if users_collection is None:
            return False
            
        await users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"banned": True, "ban_reason": reason}},
            upsert=True
        )
        logger.info(f"Banned user {user_id}: {reason}")
        return True
    except Exception as e:
        logger.error(f"Error banning user {user_id}: {e}")
        return False

async def unban_user(user_id: int) -> bool:
    """
    Unban a user
    
    Args:
        user_id (int): User ID to unban
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if users_collection is None:
            return False
            
        await users_collection.update_one(
            {"user_id": user_id},
            {"$unset": {"banned": "", "ban_reason": ""}},
        )
        logger.info(f"Unbanned user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error unbanning user {user_id}: {e}")
        return False

async def is_user_banned(user_id: int) -> bool:
    """
    Check if a user is banned
    
    Args:
        user_id (int): User ID to check
        
    Returns:
        bool: True if banned, False otherwise
    """
    try:
        if users_collection is None:
            return False
            
        user = await users_collection.find_one({"user_id": user_id})
        if user:
            return user.get("banned", False)
        return False
    except Exception as e:
        logger.error(f"Error checking ban status for {user_id}: {e}")
        return False

async def get_banned_users() -> List[Dict]:
    """
    Get all banned users
    
    Returns:
        List[Dict]: List of banned user documents
    """
    try:
        if users_collection is None:
            return []
            
        banned_users = []
        async for user in users_collection.find({"banned": True}):
            banned_users.append(user)
        return banned_users
    except Exception as e:
        logger.error(f"Error getting banned users: {e}")
        return []

async def clear_all_users() -> bool:
    """
    Clear all users from database (admin only)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if users_collection is None:
            return False
            
        await users_collection.delete_many({})
        logger.warning("Cleared all served users from database")
        return True
    except Exception as e:
        logger.error(f"Error clearing all users: {e}")
        return False
