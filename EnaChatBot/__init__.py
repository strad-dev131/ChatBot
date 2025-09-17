# ===============================================
# 🔧 CRITICAL FIX: Custom Decorators - CORRECTED
# ===============================================

import pyrogram.handlers
from pyrogram import filters

class CommandDecorator:
    def __init__(self, bot_instance):
        self.bot = bot_instance
    
    def __call__(self, commands, group=0):
        def decorator(func):
            # Create command filters
            if isinstance(commands, str):
                command_list = [commands]
            else:
                command_list = commands
                
            # Create the filter for commands
            cmd_filter = filters.command(command_list) & ~filters.bot
            
            # Register the handler
            self.bot.add_handler(
                pyrogram.handlers.MessageHandler(func, cmd_filter),
                group=group
            )
            return func
        return decorator

class MessageDecorator:
    def __init__(self, bot_instance):
        self.bot = bot_instance
    
    def __call__(self, filters_param=None, group=0):
        def decorator(func):
            self.bot.add_handler(
                pyrogram.handlers.MessageHandler(func, filters_param),
                group=group
            )
            return func
        return decorator

class CallbackDecorator:
    def __init__(self, bot_instance):
        self.bot = bot_instance
    
    def __call__(self, filters_param=None, group=0):
        def decorator(func):
            from pyrogram.handlers import CallbackQueryHandler
            self.bot.add_handler(
                CallbackQueryHandler(func, filters_param),
                group=group
            )
            return func
        return decorator

# Add decorators to EnaChatBot instance
EnaChatBot.on_cmd = CommandDecorator(EnaChatBot)
EnaChatBot.on_message = MessageDecorator(EnaChatBot)
EnaChatBot.on_callback_query = CallbackDecorator(EnaChatBot)
