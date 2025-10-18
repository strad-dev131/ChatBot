"""
EnaChatBot - Pyrogram Boot Entrypoint
Unified launcher for the realistic Indian girlfriend system.

This replaces the legacy python-telegram-bot bootstrap and aligns the
runtime with the Pyrogram-based modules in EnaChatBot/modules.
"""

import asyncio
import logging
from typing import List

from EnaChatBot import EnaChatBot as BotClient, LOGGER, load_clone_owners, userbot
from EnaChatBot.mplugin.plugins import load_plugins

logger = logging.getLogger(__name__)

_loaded_plugins: List[str] = []


async def _start_userbot_if_available():
    try:
        if userbot is not None:
            await userbot.start()
            LOGGER.info("✅ Userbot started")
    except Exception as e:
        LOGGER.warning(f"⚠️ Failed to start userbot: {e}")


async def _stop_userbot_if_running():
    try:
        if userbot is not None:
            await userbot.stop()
            LOGGER.info("🛑 Userbot stopped")
    except Exception as e:
        LOGGER.warning(f"⚠️ Failed to stop userbot: {e}")


async def anony_boot():
    """
    Start the Pyrogram bot client, load all modules, and idle.

    This coroutine is imported and executed by main.py.
    """
    # Load plugin modules (Pyrogram handlers)
    try:
        plugins = load_plugins("EnaChatBot/modules")
        global _loaded_plugins
        _loaded_plugins = [p.__name__ for p in plugins]
        LOGGER.info(f"✅ Loaded {len(_loaded_plugins)} modules")
    except Exception as e:
        LOGGER.error(f"❌ Failed loading modules: {e}")

    # Optional: load clone owners from DB if collection exists
    try:
        await load_clone_owners()
    except Exception as e:
        LOGGER.warning(f"⚠️ Could not load clone owners: {e}")

    # Start bot
    await BotClient.start()
    me = await BotClient.get_me()
    LOGGER.info(f"🤖 Bot started as @{me.username} ({me.id})")

    # Start userbot if configured
    await _start_userbot_if_available()

    # Idle until cancelled
    LOGGER.info("🚀 EnaChatBot is up. Press Ctrl+C to stop.")
    stop_event = asyncio.Event()

    try:
        await stop_event.wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await _stop_userbot_if_running()
        await BotClient.stop()
        LOGGER.info("🛑 EnaChatBot stopped")


# Allow `python -m EnaChatBot` to work as well
if __name__ == "__main__":
    asyncio.run(anony_boot())
