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
from pathlib import Path
from EnaChatBot.utils.logger import get_logger

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

logger = get_logger(__name__)

def main():
    """Main entry point for the ChatBot application"""
    try:
        logger.info("Starting EnaChatBot...")
        logger.info("Advanced AI-Powered Telegram ChatBot")
        logger.info("Initializing modules and dependencies...")

        # Try to enable uvloop for better performance on small VPS
        try:
            import uvloop  # type: ignore
            uvloop.install()
            logger.info("uvloop installed for high-performance event loop")
        except Exception:
            logger.info("uvloop not available, using default asyncio loop")

        # Import the main bot module
        from EnaChatBot.__main__ import anony_boot

        # Run the bot
        asyncio.run(anony_boot())

    except ImportError as e:
        logger.error(f"Import Error: {e}")
        logger.info("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
