# EnaChatBot OpenRouter AI Integration
"""
OpenRouter API integration for AI-powered feminine chatbot responses
Provides unlimited smart girl conversations with personality
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
        self.base_url = config.OPENROUTER_BASE_URL
        self.model = config.OPENROUTER_MODEL
        self.headers = config.OPENROUTER_HEADERS.copy() if config.OPENROUTER_HEADERS else {}
        self.session = None
        
        # Personality configurations
        self.personalities = config.AI_PERSONALITIES
        self.current_personality = config.AI_PERSONALITY
        
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
    
    async def generate_response(
        self, 
        user_message: str, 
        user_name: str = "babe",
        personality: str = None,
        chat_history: list = None
    ) -> Optional[str]:
        """
        Generate AI response using OpenRouter
        
        Args:
            user_message (str): User's message
            user_name (str): User's name or nickname
            personality (str): Personality type to use
            chat_history (list): Recent chat history for context
            
        Returns:
            str: AI generated response or None if failed
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
            
            # Add chat history if provided
            if chat_history:
                for msg in chat_history[-5:]:  # Last 5 messages for context
                    messages.append(msg)
            
            # Add current user message
            messages.append({
                "role": "user", 
                "content": user_message
            })
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": config.MAX_AI_TOKENS,
                "temperature": personality_config.get("temperature", 0.8),
                "top_p": 0.9,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.3
            }
            
            session = await self.get_session()
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    if "choices" in data and len(data["choices"]) > 0:
                        ai_response = data["choices"][0]["message"]["content"].strip()
                        
                        # Post-process response to ensure femininity
                        ai_response = self.enhance_feminine_response(ai_response, user_name)
                        
                        logger.info(f"AI response generated successfully for {user_name}")
                        return ai_response
                    else:
                        logger.error("No choices in AI response")
                        return None
                        
                else:
                    error_text = await response.text()
                    logger.error(f"OpenRouter API error {response.status}: {error_text}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error("OpenRouter API timeout")
            return None
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return None
    
    def enhance_feminine_response(self, response: str, user_name: str) -> str:
        """
        Enhance response to be more feminine and girl-like
        
        Args:
            response (str): Original AI response
            user_name (str): User's name
            
        Returns:
            str: Enhanced feminine response
        """
        # Add feminine touches if missing
        feminine_endings = ["💕", "😘", "🥰", "💖", "😊", "✨"]
        pet_names = ["babe", "honey", "sweetie", "cutie", "love"]
        
        # Ensure response isn't too long
        if len(response) > 200:
            response = response[:180] + "... 💕"
        
        # Add emoji if missing
        if not any(emoji in response for emoji in feminine_endings):
            response += f" {random.choice(feminine_endings)}"
        
        # Add pet name occasionally
        if user_name.lower() not in response.lower() and random.random() < 0.3:
            pet_name = random.choice(pet_names)
            if not any(name in response.lower() for name in pet_names):
                response = response.replace("you", f"you {pet_name}", 1)
        
        return response
    
    async def get_personality_response(self, message_type: str, user_name: str = "babe") -> str:
        """Generate response based on message type"""
        
        prompts_by_type = {
            "greeting": f"Generate a sweet, feminine greeting response for {user_name}",
            "compliment": f"Generate a flirty, blushing response to a compliment from {user_name}",
            "question": f"Generate a helpful but feminine response to {user_name}'s question",
            "sad": f"Generate a caring, supportive response for sad {user_name}",
            "funny": f"Generate a playful, giggly response to {user_name}'s joke",
            "love": f"Generate a romantic, loving response for {user_name}",
            "default": f"Generate a sweet, girl-like response for {user_name}"
        }
        
        prompt = prompts_by_type.get(message_type, prompts_by_type["default"])
        return await self.generate_response(prompt, user_name)

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
    return bool(config.OPENROUTER_API_KEY and config.ENABLE_AI_CHAT)

# Cleanup function
async def cleanup_ai():
    """Cleanup AI resources"""
    await ai_client.close_session()

import random  # Added for feminine enhancement function
