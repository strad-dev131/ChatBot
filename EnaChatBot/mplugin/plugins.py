# EnaChatBot/mplugin/plugins.py

import importlib
import os
from config import ENABLE_CLONE_FEATURE, ENABLE_CHATBOT_FEATURE  # feature flags
from EnaChatBot.utils.logger import get_logger

LOGGER = get_logger(__name__)

def load_plugins(plugin_directory="EnaChatBot/modules"):
    """
    Dynamically imports all Python modules in the plugin directory.
    Ignores __init__.py and non-.py files.
    Respects feature flags to optionally skip certain plugins.
    """
    plugins = []
    if not os.path.exists(plugin_directory):
        LOGGER.warning(f"Plugin directory {plugin_directory} not found")
        return plugins

    # Build skip list based on flags
    skip_modules = set()
    if not ENABLE_CLONE_FEATURE:
        skip_modules.update({"Clone", "Id_Clone"})

    if not ENABLE_CHATBOT_FEATURE:
        skip_modules.update({"zchatbot"})

    for file in os.listdir(plugin_directory):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            if module_name in skip_modules:
                LOGGER.info(f"Skipping plugin due to feature flag: {module_name}")
                continue
            try:
                module = importlib.import_module(f"EnaChatBot.modules.{module_name}")
                plugins.append(module)
                LOGGER.info(f"Loaded plugin: {module_name}")
            except Exception as e:
                LOGGER.error(f"Failed to load plugin {module_name}: {e}")
    return plugins

def reload_plugin(plugin_name):
    """Reload a specific plugin"""
    try:
        module = importlib.import_module(f"EnaChatBot.modules.{plugin_name}")
        importlib.reload(module)
        return True
    except Exception as e:
        LOGGER.error(f"Failed to reload plugin {plugin_name}: {e}")
        return False