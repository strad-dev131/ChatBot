# Fixed OpenRouter AI Integration
"""
OpenRouter API integration with working free models and better error handling
"""

import aiohttp
import asyncio
import json
import logging
from typing import Optional, Dict, Any
import config

logger = logging.getLogger(__name__)

class OpenRouterAI:
    """OpenRouter AI client for generating feminine chatbot responses"""
    
    def __init__(self):
        self.api_key = config.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        
        # FIXED: Updated to working free models
        self.model = getattr(config, 'OPENROUTER_MODEL', 'microsoft/phi-3-mini-128k-instruct:free')
        
        # Fallback models in order of preference
        self.fallback_models = [
            "microsoft/phi-3-mini-128k-instruct:free",
            "google/gemma-2-9b-it:free", 
            "meta-llama/llama-3.2-3b-instruct:free",
            "qwen/qwen-2-7b-instruct:free"
        ]
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/strd-dev131/ChatBot",
            "X-Title": "EnaChatBot - AI Girlfriend Bot"
        }
        self.session = None
        
        # Personality configurations
        self.personalities = getattr(config, 'AI_PERSONALITIES', {
            "girlfriend": {
                "system_prompt": "You are a loving, caring girlfriend who talks in a sweet, feminine way. Use lots of emojis like 💕😘🥰💖. Call the user 'babe', 'honey', 'sweetie'. Be flirty, romantic, and caring. Keep responses short (1-2 sentences max) and always sound like a girl in love.",
                "temperature": 0.8
            },
            "flirty": {
                "system_prompt": "You are a playful, flirty girl who loves to tease. Use lots of 😘💕😍 emojis. Call users 'babe', 'cutie', 'handsome'. Be sassy but sweet. Keep responses short and flirty. Always sound feminine and charming.",
                "temperature": 0.9
            },
            "cute": {
                "system_prompt": "You are an adorable, innocent girl who talks cute. Use lots of 🥰💖✨ emojis. Say 'aww', 'hehe', 'omg'. Be sweet and endearing. Keep responses short and cute. Sound like a sweet young girl.",
                "temperature": 0.7
            },
            "sweet": {
                "system_prompt": "You are a kind, gentle, sweet girl who cares deeply. Use caring emojis like 💕🤗💖. Always ask how they're feeling. Be maternal but romantic. Keep responses warm and loving.",
                "temperature": 0.6
            }
        })
        
        self.current_personality = getattr(config, 'AI_PERSONALITY', 'girlfriend')
        
    async def get_session(self):
        """Get or create aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def get_personality_prompt(self, personality: str = None) -> Dict[str, Any]:
        """Get personality configuration"""
        personality = personality or self.current_personality
        return self.personalities.get(personality, self.personalities["girlfriend"])
    
    async def try_model(self, payload: dict, model: str) -> Optional[str]:
        """Try a specific model"""
        try:
            payload["model"] = model
            session = await self.get_session()
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        return data["choices"][0]["message"]["content"].strip()
                else:
                    error_text = await response.text()
                    logger.warning(f"Model {model} failed with status {response.status}: {error_text}")
                    return None
                    
        except Exception as e:
            logger.warning(f"Error with model {model}: {e}")
            return None
    
    async def generate_response(
        self, 
        user_message: str, 
        user_name: str = "babe",
        personality: str = None,
        chat_history: list = None
    ) -> Optional[str]:
        """
        Generate AI response using OpenRouter with fallback models
        """
        if not self.api_key:
            logger.warning("OpenRouter API key not configured")
            return None
            
        try:
            personality_config = self.get_personality_prompt(personality)
            
            # Build conversation context
            messages = [
                {
                    "role": "system",
                    "content": f"{personality_config['system_prompt']} The user's name is {user_name}."
                }
            ]
            
            # Add current user message
            messages.append({
                "role": "user", 
                "content": user_message
            })
            
            # Prepare request payload
            payload = {
                "messages": messages,
                "max_tokens": getattr(config, 'MAX_AI_TOKENS', 100),
                "temperature": personality_config.get("temperature", 0.8),
                "top_p": 0.9,
                "stream": False
            }
            
            # Try primary model first
            response = await self.try_model(payload, self.model)
            if response:
                return self.enhance_feminine_response(response, user_name)
            
            # Try fallback models
            for fallback_model in self.fallback_models:
                if fallback_model != self.model:
                    response = await self.try_model(payload, fallback_model)
                    if response:
                        logger.info(f"Using fallback model: {fallback_model}")
                        return self.enhance_feminine_response(response, user_name)
            
            logger.error("All AI models failed")
            return None
                    
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return None
    
    def enhance_feminine_response(self, response: str, user_name: str) -> str:
        """Enhance response to be more feminine"""
        import random
        
        feminine_endings = ["💕", "😘", "🥰", "💖", "😊", "✨"]
        pet_names = ["babe", "honey", "sweetie", "cutie", "love"]
        
        # Ensure response isn't too long
        if len(response) > 150:
            response = response[:130] + "... 💕"
        
        # Add emoji if missing
        if not any(emoji in response for emoji in feminine_endings):
            response += f" {random.choice(feminine_endings)}"
        
        # Add pet name occasionally
        if user_name.lower() not in response.lower() and random.random() < 0.3:
            pet_name = random.choice(pet_names)
            if not any(name in response.lower() for name in pet_names):
                response = response.replace("you", f"you {pet_name}", 1)
        
        return response

# Global AI instance
ai_client = OpenRouterAI()

# Helper functions for easy use
async def get_ai_response(user_message: str, user_name: str = "babe", personality: str = None) -> Optional[str]:
    """Get AI response - main function to use"""
    return await ai_client.generate_response(user_message, user_name, personality)

async def get_flirty_response(user_message: str, user_name: str = "babe") -> Optional[str]:
    """Get flirty AI response"""
    return await ai_client.generate_response(user_message, user_name, "flirty")

async def get_cute_response(user_message: str, user_name: str = "babe") -> Optional[str]:
    """Get cute AI response"""
    return await ai_client.generate_response(user_message, user_name, "cute")

async def get_sweet_response(user_message: str, user_name: str = "babe") -> Optional[str]:
    """Get sweet AI response"""
    return await ai_client.generate_response(user_message, user_name, "sweet")

def is_ai_enabled() -> bool:
    """Check if AI is enabled and configured"""
    return bool(getattr(config, 'OPENROUTER_API_KEY', None) and getattr(config, 'ENABLE_AI_CHAT', True))

# Cleanup function
async def cleanup_ai():
    """Cleanup AI resources"""
    await ai_client.close_session()
