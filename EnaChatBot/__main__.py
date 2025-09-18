# ===============================================
# 🤖 EnaChatBot - Ultimate Realistic Indian AI Girl
# Main Entry Point - Production Ready
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
    banner = """
🤖 Starting EnaChatBot...
📱 Advanced AI-Powered Telegram ChatBot
🔧 Initializing modules and dependencies...
    """
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
# 🔧 MAIN FUNCTION
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
        
        # Import and start the main bot
        try:
            from EnaChatBot.__main__ import anony_boot
            LOGGER.info("✅ EnaChatBot modules imported successfully")
            
            # Start the realistic Indian AI girlfriend system
            await anony_boot()
            
        except ImportError as e:
            LOGGER.error(f"❌ Failed to import EnaChatBot modules: {e}")
            LOGGER.error("💡 Make sure EnaChatBot package is properly installed")
            sys.exit(1)
        except Exception as e:
            LOGGER.error(f"❌ Error starting EnaChatBot: {e}")
            raise
        
        # Display success banner
        display_success_banner()
        
    except KeyboardInterrupt:
        LOGGER.info("🛑 EnaChatBot stopped by user (Ctrl+C)")
        print("\n🛑 EnaChatBot stopped gracefully. Goodbye! 👋")
        
    except Exception as e:
        LOGGER.error(f"💥 Critical error in main function: {e}")
        print(f"\n💥 Critical Error: {e}")
        print("📞 Please contact @SID_ELITE for support")
        sys.exit(1)
    
    finally:
        # Cleanup if needed
        LOGGER.info("🔄 EnaChatBot shutdown completed")

# ===============================================
# 🚀 ENTRY POINT
# ===============================================

if __name__ == "__main__":
    try:
        # Set event loop policy for Windows compatibility
        if sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        # Run the main function
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye from EnaChatBot!")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        print("📞 Contact @SID_ELITE for support")
        sys.exit(1)
