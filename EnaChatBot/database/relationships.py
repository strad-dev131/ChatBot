# EnaChatBot/database/relationships.py
"""
Persistent relationship and personality memory stored in MongoDB.
Also supports writing to multiple MongoDB clusters if configured.
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

from motor.motor_asyncio import AsyncIOMotorClient
import config

logger = logging.getLogger(__name__)

# Primary DB from package init
try:
    from EnaChatBot import db as primary_db
    REL_COLLECTION = primary_db.relationships
except Exception as e:
    REL_COLLECTION = None
    logger.warning(f"Primary DB not available in relationships module: {e}")

# Optional additional MongoDB URIs for redundancy
_extra_clients: List[AsyncIOMotorClient] = []
_extra_cols = []

def _init_extra_clients():
    global _extra_clients, _extra_cols
    if _extra_clients or not getattr(config, "MONGO_URLS", []):
        return
    for uri in config.MONGO_URLS:
        try:
            if not uri or (hasattr(config, "MONGO_URL") and uri == config.MONGO_URL):
                continue
            cli = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=3000)
            _extra_clients.append(cli)
            _extra_cols.append(cli.Anonymous.relationships)
        except Exception as e:
            logger.warning(f"Failed to init extra Mongo client: {e}")

_init_extra_clients()

def _default_state(user_id: str) -> Dict[str, Any]:
    now = datetime.utcnow()
    return {
        "user_id": user_id,
        "relationship_level": 1,
        "total_messages": 0,
        "positive_interactions": 0,
        "negative_interactions": 0,
        "first_interaction": now,
        "last_interaction": now,
        "topics_discussed": [],
        "personality_traits": {},
        "relationship_history": [],
        "special_moments": [],
        "analysis": {
            "interests": [],
            "communication_style": "neutral",
            "preferred_language": "hinglish",
            "personality_type": "friendly",
            "topics_of_interest": [],
            "emotional_state_history": [],
            "cultural_background": "unknown",
            "age_group": "unknown",
            "relationship_goals": "unknown",
        },
    }

async def get_user_state(user_id: str) -> Dict[str, Any]:
    """Fetch existing state or create default one."""
    if REL_COLLECTION is None:
        return _default_state(user_id)
    try:
        doc = await REL_COLLECTION.find_one({"user_id": user_id})
        return doc or _default_state(user_id)
    except Exception as e:
        logger.error(f"get_user_state failed for {user_id}: {e}")
        return _default_state(user_id)

async def save_user_state(user_id: str, state: Dict[str, Any]) -> bool:
    """Upsert state into primary DB and best-effort to additional DBs."""
    if not state:
        return False
    state = dict(state)
    state["user_id"] = user_id
    state["last_interaction"] = state.get("last_interaction") or datetime.utcnow()
    ok = True

    # Primary write
    if REL_COLLECTION is not None:
        try:
            await REL_COLLECTION.update_one({"user_id": user_id}, {"$set": state}, upsert=True)
        except Exception as e:
            logger.error(f"Primary save_user_state failed for {user_id}: {e}")
            ok = False

    # Replicate writes to extra clusters
    for col in _extra_cols:
        try:
            await col.update_one({"user_id": user_id}, {"$set": state}, upsert=True)
        except Exception as e:
            logger.warning(f"Replica save_user_state failed for {user_id}: {e}")

    return ok