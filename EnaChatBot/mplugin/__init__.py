# EnaChatBot/mplugin/__init__.py
# Plugin package initialization file

"""
mplugin - Module Plugin Package for EnaChatBot

This package contains helper functions and utilities for the chatbot.
"""

# Import main helper functions to make them easily accessible
from .helpers import (
    is_owner,
    is_allowed_user,
    format_message,
    get_user_mention,
    check_admin_rights,
    get_user_info,
    is_command,
    get_command_args,
    format_user_status,
    check_bot_permissions,
    is_group_chat,
    is_private_chat,
    is_channel_chat,
    format_file_size,
    clean_text,
    validate_user_input
)

from .utils import (
    get_user_id,
    get_chat_id,
    safe_reply,
    safe_edit,
    extract_args,
    delete_message_after_delay
)

from .plugins import (
    load_plugins,
    reload_plugin
)

__version__ = "1.0.0"
__author__ = "strad-dev131"