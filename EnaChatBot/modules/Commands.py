# AI Command Module for EnaChatBot
"""
Commands to control AI personality and responses
"""

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from EnaChatBot import EnaChatBot, LOGGER
from EnaChatBot.openrouter_ai import ai_client, is_ai_enabled
from config import OWNER_ID, AI_PERSONALITIES
import config

# AI Personality selection keyboard
def get_personality_keyboard():
    """Generate personality selection keyboard"""
    buttons = []
    personalities = {
        "girlfriend": "💕 Girlfriend (Loving & Caring)",
        "flirty": "😘 Flirty (Playful & Teasing)", 
        "cute": "🥰 Cute (Sweet & Innocent)",
        "sweet": "💖 Sweet (Kind & Gentle)"
    }
    
    for key, name in personalities.items():
        buttons.append([InlineKeyboardButton(name, callback_data=f"setpersonality_{key}")])
    
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close_personality")])
    return InlineKeyboardMarkup(buttons)

@EnaChatBot.on_message(filters.command(["aipersonality", "personality"]) & filters.user(int(OWNER_ID)))
async def set_ai_personality(client: Client, message: Message):
    """Set AI personality (Owner only)"""
    
    if not is_ai_enabled():
        await message.reply_text(
            "**🚫 AI is not enabled!**\n\n"
            "**💡 Please set OPENROUTER_API_KEY in your environment variables.**\n"
            "**🔗 Get free API key from: https://openrouter.ai/**"
        )
        return
    
    current_personality = config.AI_PERSONALITY
    await message.reply_text(
        f"**🤖 AI Personality Settings**\n\n"
        f"**Current Personality:** `{current_personality.title()}`\n\n"
        f"**Choose a new personality for your AI girlfriend:**",
        reply_markup=get_personality_keyboard()
    )

@EnaChatBot.on_callback_query(filters.regex(r"^setpersonality_"))
async def handle_personality_change(client: Client, query):
    """Handle personality change callback"""
    
    if query.from_user.id != int(OWNER_ID):
        await query.answer("❌ Only owner can change AI personality!", show_alert=True)
        return
    
    personality = query.data.split("_")[1]
    
    if personality in AI_PERSONALITIES:
        # Update config (this would need to be saved to a config file in production)
        config.AI_PERSONALITY = personality
        ai_client.current_personality = personality
        
        personality_names = {
            "girlfriend": "💕 Girlfriend (Loving & Caring)",
            "flirty": "😘 Flirty (Playful & Teasing)",
            "cute": "🥰 Cute (Sweet & Innocent)", 
            "sweet": "💖 Sweet (Kind & Gentle)"
        }
        
        await query.edit_message_text(
            f"**✅ AI Personality Updated!**\n\n"
            f"**New Personality:** {personality_names[personality]}\n\n"
            f"**🤖 Your bot will now respond with {personality} personality!**\n"
            f"**💕 Try sending a message to see the new personality in action!**"
        )
        
        LOGGER.info(f"AI personality changed to: {personality}")
    else:
        await query.answer("❌ Invalid personality selected!", show_alert=True)

@EnaChatBot.on_callback_query(filters.regex(r"^close_personality$"))
async def close_personality_menu(client: Client, query):
    """Close personality selection menu"""
    if query.from_user.id != int(OWNER_ID):
        await query.answer("❌ Access denied!", show_alert=True)
        return
    
    await query.message.delete()

@EnaChatBot.on_message(filters.command(["aitest", "testai"]) & filters.user(int(OWNER_ID)))
async def test_ai_response(client: Client, message: Message):
    """Test AI response (Owner only)"""
    
    if not is_ai_enabled():
        await message.reply_text("**🚫 AI is not enabled! Please set OPENROUTER_API_KEY.**")
        return
    
    if len(message.command) < 2:
        await message.reply_text(
            "**🧪 AI Response Test**\n\n"
            "**Usage:** `/aitest your message here`\n\n"
            "**Example:** `/aitest Hello beautiful!`"
        )
        return
    
    test_message = " ".join(message.command[1:])
    
    status_msg = await message.reply_text("**🤖 Generating AI response...**")
    
    try:
        from EnaChatBot.openrouter_ai import get_ai_response
        
        response = await get_ai_response(test_message, "Owner")
        
        if response:
            await status_msg.edit_text(
                f"**🧪 AI Test Results**\n\n"
                f"**Input:** `{test_message}`\n\n"
                f"**AI Response:** {response}\n\n"
                f"**Personality:** `{config.AI_PERSONALITY}`\n"
                f"**Model:** `{config.OPENROUTER_MODEL}`"
            )
        else:
            await status_msg.edit_text(
                "**❌ AI Test Failed**\n\n"
                "**Could not generate response. Check:**\n"
                "• OpenRouter API key validity\n"
                "• Internet connection\n" 
                "• API rate limits"
            )
            
    except Exception as e:
        await status_msg.edit_text(f"**❌ AI Test Error:** `{str(e)}`")
        LOGGER.error(f"AI test error: {e}")

@EnaChatBot.on_message(filters.command(["aistatus", "ainfo"]))
async def ai_status(client: Client, message: Message):
    """Show AI status information"""
    
    ai_enabled = is_ai_enabled()
    
    status_text = f"**🤖 AI Status Information**\n\n"
    status_text += f"**AI Enabled:** {'✅ Yes' if ai_enabled else '❌ No'}\n"
    
    if ai_enabled:
        status_text += f"**Personality:** `{config.AI_PERSONALITY.title()}`\n"
        status_text += f"**Model:** `{config.OPENROUTER_MODEL}`\n"
        status_text += f"**Max Tokens:** `256`\n"
        status_text += f"**API Provider:** OpenRouter\n\n"
        status_text += "**💕 AI girlfriend responses are active!**"
    else:
        status_text += "\n**💡 To enable AI:**\n"
        status_text += "1. Get free API key from https://openrouter.ai/\n"
        status_text += "2. Set OPENROUTER_API_KEY in environment\n"
        status_text += "3. Restart the bot"
    
    await message.reply_text(status_text)

@EnaChatBot.on_message(filters.command(["aihelp"]))
async def ai_help(client: Client, message: Message):
    """Show AI commands help"""
    
    help_text = """**🤖 AI Commands Help**

**For Everyone:**
• `/aistatus` - Check AI status
• `/aihelp` - Show this help

**For Owner Only:**
• `/personality` - Change AI personality
• `/aitest <message>` - Test AI response
• `/aistatus` - Detailed AI information

**💕 Available Personalities:**
• **Girlfriend** - Loving, caring responses
• **Flirty** - Playful, teasing responses  
• **Cute** - Sweet, innocent responses
• **Sweet** - Kind, gentle responses

**🔧 Setup Instructions:**
1. Get free API key: https://openrouter.ai/
2. Set OPENROUTER_API_KEY environment variable
3. Choose your favorite personality
4. Enjoy unlimited AI girlfriend chats! 💖"""

    await message.reply_text(help_text)

# Add new command to existing start.py or commands.py for easy access
@EnaChatBot.on_message(filters.command(["ai"]))
async def ai_quick_info(client: Client, message: Message):
    """Quick AI information"""
    
    if is_ai_enabled():
        await message.reply_text(
            f"**🤖 AI Active: {config.AI_PERSONALITY.title()} Personality 💕**\n\n"
            f"**💬 Send me any message and I'll respond with my {config.AI_PERSONALITY} personality!**\n\n"
            f"**🔧 Use /aihelp for more commands**"
        )
    else:
        await message.reply_text(
            "**🤖 AI Girlfriend Mode 💕**\n\n"
            "**❌ AI is currently disabled**\n\n"
            "**💡 Owner can enable AI by setting OPENROUTER_API_KEY**\n"
            "**🔗 Get free key: https://openrouter.ai/**"
        )
