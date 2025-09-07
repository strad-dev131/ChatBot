# EnaChatBot/mplugin/helpers.py

from config import OWNER_ID

def is_owner(user_id: int) -> bool:
    """
    Check if the user ID matches the bot owner.
    """
    return user_id == OWNER_ID

def is_allowed_user(user_id: int, allowed_users: list) -> bool:
    """
    Return True if the user is in a list of allowed users.
    """
    return user_id in allowed_users

def format_message(text: str) -> str:
    """
    A placeholder for text formatting if needed.
    """
    return text.strip()

def get_user_mention(user):
    """Get user mention from user object"""
    if hasattr(user, 'mention'):
        return user.mention
    elif hasattr(user, 'first_name'):
        return f"[{user.first_name}](tg://user?id={user.id})"
    else:
        return f"User {user.id}"

def check_admin_rights(chat_member):
    """Check if user has admin rights"""
    admin_rights = ["creator", "administrator"]
    return hasattr(chat_member, 'status') and chat_member.status in admin_rights

def get_user_info(user):
    """Get formatted user information"""
    info = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': getattr(user, 'last_name', None),
        'username': getattr(user, 'username', None),
        'mention': get_user_mention(user)
    }
    return info

def is_command(message, command_name):
    """Check if message is a specific command"""
    if hasattr(message, 'command'):
        return message.command[0].lower() == command_name.lower()
    return False

def get_command_args(message):
    """Extract arguments from a command message"""
    if hasattr(message, 'command') and len(message.command) > 1:
        return message.command[1:]
    return []

def format_user_status(status):
    """Format user status for display"""
    status_map = {
        'creator': '👑 Creator',
        'administrator': '👨‍💼 Admin',
        'member': '👤 Member',
        'restricted': '🚫 Restricted',
        'left': '❌ Left',
        'kicked': '🦶 Kicked'
    }
    return status_map.get(status, status.title())

def check_bot_permissions(chat_member, required_permissions):
    """Check if bot has required permissions in a chat"""
    if not hasattr(chat_member, 'privileges'):
        return False
    
    privileges = chat_member.privileges
    for permission in required_permissions:
        if not getattr(privileges, permission, False):
            return False
    return True

def is_group_chat(chat):
    """Check if chat is a group or supergroup"""
    return chat.type in ['group', 'supergroup']

def is_private_chat(chat):
    """Check if chat is private"""
    return chat.type == 'private'

def is_channel_chat(chat):
    """Check if chat is a channel"""
    return chat.type == 'channel'

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def clean_text(text: str) -> str:
    """Clean and format text for display"""
    if not text:
        return ""
    
    # Remove extra whitespaces
    text = " ".join(text.split())
    
    # Remove markdown characters if needed
    # text = text.replace('*', '').replace('_', '').replace('`', '')
    
    return text.strip()

def validate_user_input(text: str, max_length: int = 1000) -> bool:
    """Validate user input"""
    if not text or not isinstance(text, str):
        return False
    
    if len(text) > max_length:
        return False
    
    # Add more validation rules as needed
    return True