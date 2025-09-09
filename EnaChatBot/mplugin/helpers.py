# EnaChatBot mplugin helpers
"""
Helper functions for the mplugin system used by cloned bots
"""

from pyrogram import Client, filters
from pyrogram.types import Message
import logging

logger = logging.getLogger(__name__)

def is_owner(user_id: int) -> bool:
    """
    Check if user is owner of the bot or a cloned bot
    
    Args:
        user_id (int): User ID to check
        
    Returns:
        bool: True if user is owner, False otherwise
    """
    try:
        from config import OWNER_ID
        from EnaChatBot import CLONE_OWNERS
        
        # Check if user is main owner
        if user_id == int(OWNER_ID):
            return True
        
        # Check if user is clone owner
        for bot_id, owner_id in CLONE_OWNERS.items():
            if owner_id == user_id:
                return True
        
        return False
    except Exception as e:
        logger.error(f"Error checking owner status: {e}")
        return False

def get_clone_owner(bot_id: int):
    """
    Get the owner of a specific cloned bot
    
    Args:
        bot_id (int): Bot ID to check
        
    Returns:
        int: Owner user ID or None
    """
    try:
        from EnaChatBot import CLONE_OWNERS
        return CLONE_OWNERS.get(bot_id)
    except Exception as e:
        logger.error(f"Error getting clone owner: {e}")
        return None

def is_clone_owner(user_id: int, bot_id: int) -> bool:
    """
    Check if user is owner of a specific cloned bot
    
    Args:
        user_id (int): User ID to check
        bot_id (int): Bot ID to check against
        
    Returns:
        bool: True if user is owner of the bot
    """
    try:
        clone_owner = get_clone_owner(bot_id)
        return clone_owner == user_id
    except Exception as e:
        logger.error(f"Error checking clone owner: {e}")
        return False

def get_bot_info(client: Client):
    """
    Get basic information about the bot
    
    Args:
        client (Client): Pyrogram client instance
        
    Returns:
        dict: Bot information
    """
    try:
        me = client.me
        return {
            "id": me.id,
            "name": me.first_name,
            "username": me.username,
            "mention": me.mention
        }
    except Exception as e:
        logger.error(f"Error getting bot info: {e}")
        return {}

async def send_clone_message(client: Client, chat_id: int, text: str):
    """
    Send a message from cloned bot with error handling
    
    Args:
        client (Client): Pyrogram client instance
        chat_id (int): Chat ID to send message to
        text (str): Message text
    """
    try:
        await client.send_message(chat_id, text)
    except Exception as e:
        logger.error(f"Error sending clone message: {e}")

# Command filters for cloned bots
owner_filter = filters.create(lambda _, __, message: is_owner(message.from_user.id))
clone_owner_filter = filters.create(
    lambda _, __, message: is_clone_owner(message.from_user.id, message._client.me.id) 
    if hasattr(message._client, 'me') else False
)

# Utility functions for plugin management
def load_plugin(plugin_name: str):
    """Load a specific plugin"""
    try:
        logger.info(f"Loading plugin: {plugin_name}")
        return True
    except Exception as e:
        logger.error(f"Error loading plugin {plugin_name}: {e}")
        return False

def unload_plugin(plugin_name: str):
    """Unload a specific plugin"""
    try:
        logger.info(f"Unloading plugin: {plugin_name}")
        return True
    except Exception as e:
        logger.error(f"Error unloading plugin {plugin_name}: {e}")
        return False

# Plugin registration system
registered_plugins = {}

def register_plugin(name: str, plugin_obj):
    """Register a plugin in the system"""
    try:
        registered_plugins[name] = plugin_obj
        logger.info(f"Registered plugin: {name}")
        return True
    except Exception as e:
        logger.error(f"Error registering plugin {name}: {e}")
        return False

def get_registered_plugins():
    """Get all registered plugins"""
    return registered_plugins.copy()

# Error handling decorator for plugin functions
def plugin_error_handler(func):
    """Decorator to handle plugin errors gracefully"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Plugin error in {func.__name__}: {e}")
            return None
    return wrapper
