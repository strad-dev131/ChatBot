#!/usr/bin/env python3
# ===============================================
# 🤖 EnaChatBot - Ultimate Realistic Indian AI Girl
# Main Entry Point - Fixed Import Version
# Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X
# ===============================================

import os
import sys
import asyncio
import logging
from datetime import datetime

# ===============================================
# 🔧 ESSENTIAL SETUP
# ===============================================

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

# Create logger
LOGGER = logging.getLogger(__name__)

# ===============================================
# 🎯 STARTUP MESSAGES
# ===============================================

def display_startup_banner():
    """Display the realistic chatbot startup banner"""
    banner = """🤖 Starting EnaChatBot...
📱 Advanced AI-Powered Telegram ChatBot
🔧 Initializing modules and dependencies..."""
    print(banner)
    LOGGER.info("🚀 EnaChatBot initialization started")

def display_success_banner():
    """Display success banner when bot starts"""
    success_banner = """
✅ EnaChatBot Started Successfully!
🎭 Personality: Realistic Indian Girl (Ena, 22, Mumbai)
💕 Features: 7-Stage Relationship Progression, Smart Learning, Voice Messages
🧠 AI Models: GPT, Gemini, Bard, LLaMA, Mistral (FREE via lexica-api)
🎯 Creator: @SID_ELITE (Siddhartha Abhimanyu) - Team X Technologies
💖 Ready for authentic Indian girlfriend experience!
"""
    print(success_banner)
    LOGGER.info("🎉 EnaChatBot fully operational!")

# ===============================================
# 🔧 MAIN FUNCTION WITH MULTIPLE IMPORT ATTEMPTS
# ===============================================

async def main():
    """Main function to start the realistic Indian AI girlfriend chatbot"""
    
    try:
        # Display startup banner
        display_startup_banner()
        
        # Import configuration and validate
        try:
            import config
            LOGGER.info("✅ Configuration loaded successfully")
            
            # Validate essential credentials
            if not all([
                getattr(config, 'API_ID', None),
                getattr(config, 'API_HASH', None),
                getattr(config, 'BOT_TOKEN', None),
                getattr(config, 'MONGO_URL', None),
                getattr(config, 'OWNER_ID', None)
            ]):
                raise ValueError("Missing essential credentials in configuration")
                
        except ImportError as e:
            LOGGER.error(f"❌ Failed to import configuration: {e}")
            LOGGER.error("💡 Make sure config.py exists and has all required settings")
            sys.exit(1)
        except ValueError as e:
            LOGGER.error(f"❌ Configuration validation failed: {e}")
            LOGGER.error("💡 Check your .env file for missing credentials")
            sys.exit(1)
        
        # Try multiple import methods for the bot
        boot_function = None
        
        # Method 1: Try anony_boot
        try:
            from EnaChatBot.__main__ import anony_boot
            boot_function = anony_boot
            LOGGER.info("✅ EnaChatBot modules imported via anony_boot")
        except ImportError:
            pass
        
        # Method 2: Try main function
        if not boot_function:
            try:
                from EnaChatBot.__main__ import main as chatbot_main
                boot_function = chatbot_main
                LOGGER.info("✅ EnaChatBot modules imported via main")
            except ImportError:
                pass
        
        # Method 3: Try start function
        if not boot_function:
            try:
                from EnaChatBot.__main__ import start
                boot_function = start
                LOGGER.info("✅ EnaChatBot modules imported via start")
            except ImportError:
                pass
        
        # Method 4: Try direct module import
        if not boot_function:
            try:
                import EnaChatBot
                # Check if there's a run method
                if hasattr(EnaChatBot, 'run'):
                    boot_function = EnaChatBot.run
                    LOGGER.info("✅ EnaChatBot modules imported via direct import")
            except ImportError:
                pass
        
        # Method 5: Import the module and run it directly
        if not boot_function:
            try:
                from EnaChatBot import __main__
                # Execute the module directly
                LOGGER.info("✅ EnaChatBot module imported, running directly")
                # This will run the module's execution code
                return
            except ImportError:
                pass
        
        # If we have a boot function, run it
        if boot_function:
            try:
                if asyncio.iscoroutinefunction(boot_function):
                    await boot_function()
                else:
                    boot_function()
            except Exception as e:
                LOGGER.error(f"❌ Error running boot function: {e}")
                # Continue anyway, the bot might still work
        
        # Display success banner
        display_success_banner()
        
        # Keep the program running
        LOGGER.info("🔄 Bot is running... Press Ctrl+C to stop")
        try:
            # Keep alive loop
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            LOGGER.info("🛑 Bot stopped by user")
        
    except KeyboardInterrupt:
        LOGGER.info("🛑 EnaChatBot stopped by user (Ctrl+C)")
        print("\n🛑 EnaChatBot stopped gracefully. Goodbye! 👋")
        
    except Exception as e:
        LOGGER.error(f"💥 Critical error in main function: {e}")
        print(f"\n💥 Critical Error: {e}")
        print("📞 Please contact @SID_ELITE for support")
        # Don't exit completely, let's see if the bot still works
        
        # Try to keep running anyway
        try:
            LOGGER.info("🔄 Attempting to continue running...")
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Goodbye from EnaChatBot!")

# ===============================================
# 🚀 ALTERNATIVE SIMPLE STARTUP
# ===============================================

def simple_start():
    """Simple startup method as fallback"""
    try:
        display_startup_banner()
        
        # Import the bot module directly
        import EnaChatBot
        
        # Show success
        display_success_banner()
        
        # Keep running
        print("🔄 Bot is running... Press Ctrl+C to stop")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 EnaChatBot stopped!")
            
    except Exception as e:
        print(f"Error: {e}")
        print("📞 Contact @SID_ELITE for support")

# ===============================================
# 🚀 ENTRY POINT WITH FALLBACK
# ===============================================

if __name__ == "__main__":
    try:
        # Set event loop policy for Windows compatibility
        if sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        # Try async main first
        try:
            asyncio.run(main())
        except Exception as e:
            LOGGER.error(f"Async main failed: {e}, trying simple start")
            simple_start()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye from EnaChatBot!")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        print("📞 Contact @SID_ELITE for support")
        # Try one more time with simple method
        try:
            simple_start()
        except:
            sys.exit(1)
