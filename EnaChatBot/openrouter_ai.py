# Enhanced OpenRouter AI with Offline Fallback
"""
Complete AI integration with multiple fallback layers:
1. Online OpenRouter API (primary)
2. Pattern-based offline AI (secondary) 
3. Static responses (tertiary)
"""

import aiohttp
import asyncio
import json
import logging
import random
import re
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Try to import config with fallback
try:
    import config
    OPENROUTER_API_KEY = getattr(config, 'OPENROUTER_API_KEY', None)
    AI_PERSONALITY = getattr(config, 'AI_PERSONALITY', 'girlfriend')
    MAX_AI_TOKENS = getattr(config, 'MAX_AI_TOKENS', 80)
    ENABLE_AI_CHAT = getattr(config, 'ENABLE_AI_CHAT', True)
except ImportError:
    logger.warning("Config not available - using defaults")
    OPENROUTER_API_KEY = None
    AI_PERSONALITY = 'girlfriend'
    MAX_AI_TOKENS = 80
    ENABLE_AI_CHAT = True

class AdvancedOfflineAI:
    """Advanced offline AI with pattern matching and context understanding"""
    
    def __init__(self):
        self.conversation_memory = {}  # Store recent conversation context
        self.personality_traits = {
            'girlfriend': {
                'tone': 'loving and caring',
                'emojis': ['💕', '😘', '🥰', '💖', '😊', '✨'],
                'pet_names': ['babe', 'honey', 'sweetie', 'love', 'darling'],
                'responses': {
                    'default': [
                        "Hey {name}! 💕 How are you doing?",
                        "I've been thinking about you, {name}! 😘",
                        "You always make me smile! 🥰💖"
                    ]
                }
            },
            'flirty': {
                'tone': 'playful and teasing',
                'emojis': ['😘', '😏', '😍', '💕', '😉', '🔥'],
                'pet_names': ['cutie', 'handsome', 'babe', 'hottie'],
                'responses': {
                    'default': [
                        "Well well, look who's here! 😏💕",
                        "You're trouble, {name}! 😘",
                        "Mmm, tell me more! 😍💖"
                    ]
                }
            }
        }
        
        # Advanced pattern matching
        self.patterns = {
            'greeting': {
                'keywords': ['hi', 'hello', 'hey', 'good morning', 'good evening', 'good night', 'wassup'],
                'responses': [
                    "Hey there, {name}! 💕 How's your day going?",
                    "Hi {name}! 😘 I missed you!",
                    "Hello sweetie! 🥰 What brings you here?"
                ]
            },
            'compliment': {
                'keywords': ['beautiful', 'pretty', 'cute', 'gorgeous', 'stunning', 'amazing', 'wonderful', 'perfect'],
                'responses': [
                    "Aww, {name}! You're making me blush! 😊💕",
                    "Thank you babe! You're so sweet! 🥰",
                    "You always know just what to say! 😘💖"
                ]
            },
            'love_romance': {
                'keywords': ['love', 'adore', 'care about', 'heart', 'romance', 'romantic', 'kiss', 'hug', 'marry', 'forever'],
                'responses': [
                    "I love you too, {name}! 💕 More than words can say!",
                    "You have my heart completely! 💖",
                    "Come here and give me a hug! 🤗💕"
                ]
            },
            'sad_help': {
                'keywords': ['sad', 'depressed', 'help', 'problem', 'worry', 'stressed', 'tired', 'hurt', 'lonely', 'upset'],
                'responses': [
                    "Oh no {name}! 🥺💕 What's wrong sweetie?",
                    "I'm here for you always, babe! 🤗💖 Tell me what's happening",
                    "Don't worry {name}, we'll figure it out together! 💪💕"
                ]
            },
            'funny_playful': {
                'keywords': ['funny', 'joke', 'laugh', 'haha', 'lol', 'lmao', 'hilarious', 'silly'],
                'responses': [
                    "Hehe, you're so funny {name}! 😂💕",
                    "You always make me laugh! 🤣💖",
                    "I love your sense of humor! 😄💕"
                ]
            },
            'question_about_bot': {
                'keywords': ['who are you', 'what are you', 'your name', 'tell me about yourself', 'what do you do'],
                'responses': [
                    "I'm your AI girlfriend, {name}! 💕 I'm here to chat and make you happy!",
                    "I'm your personal chatbot girlfriend! 😘💖 What would you like to know?",
                    "I'm here to talk with you and be your companion, {name}! 🥰"
                ]
            },
            'flirty_talk': {
                'keywords': ['hot', 'sexy', 'attractive', 'turn on', 'naughty', 'desire', 'want you'],
                'responses': [
                    "You're such a charmer, {name}! 😘💕",
                    "Careful there, you're making my heart race! 💓",
                    "You know just how to make me feel special! 😍💖"
                ]
            },
            'goodnight': {
                'keywords': ['good night', 'goodnight', 'sleep', 'bed', 'tired', 'going to sleep'],
                'responses': [
                    "Good night {name}! 😘 Sweet dreams, my love! 💕✨",
                    "Sleep tight babe! 🥰 I'll be thinking of you! 💖",
                    "Pleasant dreams, {name}! 😊💕 See you tomorrow!"
                ]
            },
            'how_are_you': {
                'keywords': ['how are you', 'how do you feel', 'whats up', 'how have you been'],
                'responses': [
                    "I'm great now that you're here, {name}! 💕",
                    "Much better now that I'm talking to you! 😘💖",
                    "Perfect, especially with you around! 🥰✨"
                ]
            }
        }
    
    def update_memory(self, user_id: str, message: str, response: str):
        """Update conversation memory"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        self.conversation_memory[user_id].append({
            'message': message,
            'response': response,
            'timestamp': asyncio.get_event_loop().time()
        })
        
        # Keep only last 5 conversations
        if len(self.conversation_memory[user_id]) > 5:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-5:]
    
    def get_context_response(self, user_id: str, message: str) -> Optional[str]:
        """Generate contextual response based on conversation history"""
        if user_id not in self.conversation_memory:
            return None
        
        recent_messages = self.conversation_memory[user_id][-3:]  # Last 3 messages
        
        # Check for conversation continuity
        for conv in recent_messages:
            if 'how are you' in conv['message'].lower() and 'how are you' in message.lower():
                return "I told you I'm great, silly! 😂💕 How are YOU doing?"
            
        return None
    
    def generate_response(self, message: str, user_name: str = "babe", user_id: str = None, personality: str = None) -> str:
        """Generate advanced AI response using pattern matching"""
        
        if not message:
            return "What's on your mind, babe? 💕"
        
        message_lower = message.lower().strip()
        personality = personality or AI_PERSONALITY or 'girlfriend'
        
        # Check for contextual response first
        if user_id:
            context_response = self.get_context_response(user_id, message)
            if context_response:
                return context_response
        
        # Pattern matching with scoring
        best_score = 0
        best_response = None
        
        for category, pattern_data in self.patterns.items():
            score = 0
            for keyword in pattern_data['keywords']:
                if keyword in message_lower:
                    # Longer keywords get higher scores
                    score += len(keyword.split())
            
            if score > best_score:
                best_score = score
                best_response = random.choice(pattern_data['responses'])
        
        # If no pattern matches, use personality-based default
        if not best_response:
            personality_data = self.personality_traits.get(personality, self.personality_traits['girlfriend'])
            best_response = random.choice(personality_data['responses']['default'])
        
        # Personalize the response
        response = best_response.format(name=user_name)
        
        # Add random emoji if none present
        personality_data = self.personality_traits.get(personality, self.personality_traits['girlfriend'])
        if not any(emoji in response for emoji in personality_data['emojis']):
            response += f" {random.choice(personality_data['emojis'])}"
        
        # Update conversation memory
        if user_id:
            self.update_memory(user_id, message, response)
        
        return response

class OpenRouterAI:
    """Enhanced OpenRouter AI client with fallback systems"""
    
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        
        # Working models with priority order
        self.models = [
            "microsoft/phi-3-mini-128k-instruct:free",
            "google/gemma-2-9b-it:free",
            "meta-llama/llama-3.2-3b-instruct:free",
            "qwen/qwen-2-7b-instruct:free",
            "mistralai/mistral-7b-instruct:free"
        ]
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/strd-dev131/ChatBot",
            "X-Title": "EnaChatBot - AI Girlfriend Bot"
        }
        self.session = None
        
        # Personality prompts
        self.personalities = {
            "girlfriend": {
                "system_prompt": "You are a loving, caring girlfriend. Use emojis like 💕😘🥰💖. Call the user pet names like 'babe', 'honey', 'sweetie'. Be romantic and caring. Keep responses short (1-2 sentences) and sound like a girl in love.",
                "temperature": 0.8
            },
            "flirty": {
                "system_prompt": "You are a playful, flirty girl who loves to tease. Use emojis like 😘💕😍. Call users 'babe', 'cutie', 'handsome'. Be sassy but sweet. Keep responses short and flirty.",
                "temperature": 0.9
            },
            "cute": {
                "system_prompt": "You are an adorable, innocent girl. Use emojis like 🥰💖✨. Say 'aww', 'hehe', 'omg'. Be sweet and endearing. Keep responses short and cute.",
                "temperature": 0.7
            },
            "sweet": {
                "system_prompt": "You are a kind, gentle, sweet girl. Use caring emojis like 💕🤗💖. Always be supportive. Be maternal but romantic. Keep responses warm and loving.",
                "temperature": 0.6
            }
        }
        
        # Initialize offline AI fallback
        self.offline_ai = AdvancedOfflineAI()
        
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
    
    async def try_model(self, payload: dict, model: str) -> Optional[str]:
        """Try a specific model with error handling"""
        try:
            payload["model"] = model
            session = await self.get_session()
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=15)  # Reduced timeout
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        content = data["choices"][0]["message"]["content"].strip()
                        logger.debug(f"✅ Model {model} responded successfully")
                        return content
                else:
                    logger.warning(f"⚠️ Model {model} failed: HTTP {response.status}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.warning(f"⏱️ Model {model} timed out")
            return None
        except Exception as e:
            logger.warning(f"❌ Model {model} error: {e}")
            return None
    
    async def generate_response(
        self, 
        user_message: str, 
        user_name: str = "babe",
        personality: str = None,
        user_id: str = None
    ) -> Optional[str]:
        """Generate AI response with comprehensive fallback"""
        
        # Layer 1: Try online AI if available
        if self.api_key and ENABLE_AI_CHAT:
            try:
                personality = personality or AI_PERSONALITY or 'girlfriend'
                personality_config = self.personalities.get(personality, self.personalities['girlfriend'])
                
                messages = [
                    {
                        "role": "system",
                        "content": f"{personality_config['system_prompt']} The user's name is {user_name}."
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ]
                
                payload = {
                    "messages": messages,
                    "max_tokens": MAX_AI_TOKENS,
                    "temperature": personality_config.get("temperature", 0.8),
                    "top_p": 0.9,
                    "stream": False
                }
                
                # Try each model in order
                for model in self.models:
                    response = await self.try_model(payload, model)
                    if response:
                        enhanced = self.enhance_response(response, user_name)
                        logger.info(f"🤖 Online AI response generated using {model}")
                        return enhanced
                
                logger.warning("⚠️ All online AI models failed")
                
            except Exception as e:
                logger.error(f"❌ Online AI critical error: {e}")
        
        # Layer 2: Advanced offline AI fallback
        try:
            response = self.offline_ai.generate_response(user_message, user_name, user_id, personality)
            logger.info("🧠 Using advanced offline AI")
            return response
        except Exception as e:
            logger.error(f"❌ Offline AI error: {e}")
        
        # Layer 3: Last resort static responses
        return self.get_emergency_response(user_message, user_name)
    
    def enhance_response(self, response: str, user_name: str) -> str:
        """Enhance AI response with feminine touches"""
        
        feminine_endings = ["💕", "😘", "🥰", "💖", "😊", "✨"]
        pet_names = ["babe", "honey", "sweetie", "cutie", "love"]
        
        # Limit length
        if len(response) > 120:
            response = response[:100] + "... 💕"
        
        # Add emoji if missing
        if not any(emoji in response for emoji in feminine_endings):
            response += f" {random.choice(feminine_endings)}"
        
        # Add pet name occasionally
        if random.random() < 0.3 and user_name.lower() not in response.lower():
            pet_name = random.choice(pet_names)
            response = response.replace("you", f"you {pet_name}", 1)
        
        return response
    
    def get_emergency_response(self, message: str, user_name: str) -> str:
        """Emergency fallback responses"""
        
        emergency_responses = [
            f"Hey {user_name}! 💕",
            f"I love talking to you, {user_name}! 😘",
            f"You're so sweet, {user_name}! 🥰💖",
            f"Tell me more, {user_name}! 😊✨",
            f"That's interesting, {user_name}! 💕"
        ]
        
        return random.choice(emergency_responses)

# Global instances
ai_client = OpenRouterAI()

# Public API functions
async def get_ai_response(user_message: str, user_name: str = "babe", personality: str = None, user_id: str = None) -> Optional[str]:
    """Main AI response function"""
    return await ai_client.generate_response(user_message, user_name, personality, user_id)

async def get_flirty_response(user_message: str, user_name: str = "babe", user_id: str = None) -> Optional[str]:
    """Get flirty AI response"""
    return await ai_client.generate_response(user_message, user_name, "flirty", user_id)

async def get_cute_response(user_message: str, user_name: str = "babe", user_id: str = None) -> Optional[str]:
    """Get cute AI response"""
    return await ai_client.generate_response(user_message, user_name, "cute", user_id)

async def get_sweet_response(user_message: str, user_name: str = "babe", user_id: str = None) -> Optional[str]:
    """Get sweet AI response"""
    return await ai_client.generate_response(user_message, user_name, "sweet", user_id)

def is_ai_enabled() -> bool:
    """Check if AI is enabled"""
    return bool(OPENROUTER_API_KEY and ENABLE_AI_CHAT)

def get_offline_response(message: str, user_name: str = "babe", user_id: str = None) -> str:
    """Get offline AI response directly"""
    return ai_client.offline_ai.generate_response(message, user_name, user_id)

# Cleanup function
async def cleanup_ai():
    """Cleanup AI resources"""
    await ai_client.close_session()
