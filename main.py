#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnaChatBot - Advanced AI Telegram ChatBot
Main entry point for the application

Author: strd-dev131
Repository: https://github.com/strd-dev131/ChatBot
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure basic logging
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

def main():
    """Main entry point for the ChatBot application"""
    try:
        print("🤖 Starting EnaChatBot...")
        print("📱 Advanced AI-Powered Telegram ChatBot")
        print("🔧 Initializing modules and dependencies...")
        
        # Import the main bot module
        from EnaChatBot.__main__ import anony_boot
        
        # Run the bot
        asyncio.get_event_loop().run_until_complete(anony_boot())
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user (Ctrl+C)")
        sys.exit(0)
        
    except Exception as e:
        print(f"💥 Critical Error: {e}")
        logging.exception("Critical error in main function")
        sys.exit(1)

if __name__ == "__main__":
    main()
