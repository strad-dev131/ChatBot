# Advanced OpenRouter AI with Real Girl Personality
"""
Enhanced AI system with:
- Working OpenRouter models only
- Real girl personality with emotions
- Content filtering for safety
- Learning capabilities
- Voice message support
- Sticker integration
"""

import aiohttp
import asyncio
import json
import logging
import random
import re
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

# Safe config import
try:
    import config
    OPENROUTER_API_KEY = getattr(config, 'OPENROUTER_API_KEY', None)
    AI_PERSONALITY = getattr(config, 'AI_PERSONALITY', 'girlfriend')
    MAX_AI_TOKENS = getattr(config, 'MAX_AI_TOKENS', 100)
    ENABLE_AI_CHAT = getattr(config, 'ENABLE_AI_CHAT', True)
except ImportError:
    logger.warning("Config not available - using defaults")
    OPENROUTER_API_KEY = None
    AI_PERSONALITY = 'girlfriend'
    MAX_AI_TOKENS = 100
    ENABLE_AI_CHAT = True

class SafeContentFilter:
    """Content filtering for inappropriate content"""
    
    def __init__(self):
        self.inappropriate_patterns = [
            r'\b(sex|fuck|shit|bitch|damn|hell|porn|nude|naked|dick|pussy|cock)\b',
            r'\b(sexual|erotic|horny|kinky|orgasm|masturbat|anal)\b',
            # Add more as needed
        ]
        
        self.replacement_responses = [
            "Let's talk about something sweeter, babe! 💕",
            "How about we discuss something more fun? 😊💖",
            "I'd rather chat about nicer things with you, honey! 🥰",
            "Let's keep our conversation cute and friendly! ✨💕"
        ]
    
    def is_inappropriate(self, text: str) -> bool:
        """Check if content is inappropriate"""
        if not text:
            return False
        
        text_lower = text.lower()
        for pattern in self.inappropriate_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        return False
    
    def get_safe_response(self) -> str:
        """Get a safe alternative response"""
        return random.choice(self.replacement_responses)

class AdvancedGirlfriendAI:
    """Advanced offline AI with real girlfriend personality"""
    
    def __init__(self):
        self.conversation_memory = {}
        self.user_preferences = {}
        self.content_filter = SafeContentFilter()
        
        # Emotional states
        self.emotions = {
            "happy": ["😊", "😄", "🥰", "😍", "💕"],
            "excited": ["😆", "🤩", "✨", "🎉", "💖"],  
            "shy": ["😊", "🙈", "😌", "💕"],
            "flirty": ["😏", "😘", "😉", "💕", "🔥"],
            "caring": ["🤗", "💖", "🥺", "💕"],
            "playful": ["😂", "😄", "🤪", "💕"]
        }
        
        # Advanced pattern matching with emotional context
        self.conversation_patterns = {
            "greeting": {
                "keywords": ["hi", "hello", "hey", "morning", "evening", "night"],
                "responses": {
                    "happy": [
                        "Hey there {name}! 😊 You just made my day brighter!",
                        "Hi babe! 🥰 I was just thinking about you!",
                        "Hello sweetie! 💕 Perfect timing!"
                    ],
                    "excited": [
                        "OMG hi {name}! 🤩 I'm so excited to see you!",
                        "Hey cutie! ✨ You're here! This is amazing!",
                        "Hi honey! 🎉 Best part of my day right here!"
                    ]
                }
            },
            "compliment": {
                "keywords": ["beautiful", "pretty", "cute", "gorgeous", "stunning", "amazing", "perfect"],
                "responses": {
                    "shy": [
                        "Aww {name}! 😊 You're making me blush so much!",
                        "You're too sweet! 🙈 Thank you babe!",
                        "Stop it, you're embarrassing me! 😌💕"
                    ],
                    "happy": [
                        "You're the sweetest! 🥰 Thank you honey!",
                        "That means everything to me! 😍💖",
                        "You always know what to say! 💕"
                    ]
                }
            },
            "love_romance": {
                "keywords": ["love", "adore", "heart", "romance", "kiss", "hug", "marry", "forever"],
                "responses": {
                    "flirty": [
                        "I love you too {name}! 😘 You make my heart race!",
                        "You're so romantic! 💕 Come here and give me a hug!",
                        "Forever sounds perfect with you! 😍💖"
                    ],
                    "caring": [
                        "My heart belongs to you {name}! 🤗💖",
                        "I adore you so much babe! 🥺💕",
                        "You're my everything! 💝"
                    ]
                }
            },
            "sad_support": {
                "keywords": ["sad", "depressed", "help", "problem", "worried", "stressed", "hurt", "lonely"],
                "responses": {
                    "caring": [
                        "Oh no {name}! 🥺💕 What's wrong sweetie? I'm here for you!",
                        "Don't worry babe! 🤗 We'll figure this out together!",
                        "I'm always here when you need me {name}! 💖 Tell me everything!"
                    ]
                }
            },
            "funny_playful": {
                "keywords": ["funny", "joke", "laugh", "haha", "lol", "silly", "weird"],
                "responses": {
                    "playful": [
                        "Hehe you're so silly {name}! 😂💕 I love your humor!",
                        "You crack me up! 🤪 Never change babe!",
                        "LMAO you're hilarious! 😄 That's why I adore you!"
                    ]
                }
            }
        }
    
    def analyze_emotion(self, message: str, user_history: list = None) -> str:
        """Analyze what emotion to respond with"""
        message_lower = message.lower()
        
        # Check for emotional keywords
        if any(word in message_lower for word in ["sad", "hurt", "problem", "worry"]):
            return "caring"
        elif any(word in message_lower for word in ["love", "beautiful", "gorgeous"]):
            return "shy" if random.random() < 0.4 else "happy"  
        elif any(word in message_lower for word in ["funny", "joke", "lol", "haha"]):
            return "playful"
        elif any(word in message_lower for word in ["hi", "hello", "hey"]):
            return "excited" if random.random() < 0.3 else "happy"
        else:
            return random.choice(["happy", "flirty", "caring"])
    
    def generate_response(self, message: str, user_name: str = "babe", user_id: str = None) -> str:
        """Generate advanced AI response with personality and emotion"""
        
        if self.content_filter.is_inappropriate(message):
            return self.content_filter.get_safe_response()
        
        if not message:
            return f"What's on your mind {user_name}? 💕"
        
        message_lower = message.lower().strip()
        current_emotion = self.analyze_emotion(message)
        
        # Find best matching pattern
        best_pattern = None
        best_score = 0
        
        for pattern_name, pattern_data in self.conversation_patterns.items():
            score = 0
            for keyword in pattern_data["keywords"]:
                if keyword in message_lower:
                    score += len(keyword.split())
            
            if score > best_score:
                best_score = score
                best_pattern = pattern_data
        
        # Generate response based on pattern and emotion
        if best_pattern and current_emotion in best_pattern["responses"]:
            responses = best_pattern["responses"][current_emotion]
            response = random.choice(responses).format(name=user_name)
        else:
            # Default responses with emotion
            default_responses = {
                "happy": [f"That's so sweet {user_name}! 😊💕", f"I love talking to you! 🥰💖"],
                "flirty": [f"You're such a charmer {user_name}! 😘💕", f"Mmm tell me more! 😏💖"],
                "caring": [f"You're amazing {user_name}! 🤗💕", f"I care about you so much! 💖"],
                "playful": [f"You're so fun {user_name}! 😄💕", f"I adore your personality! 🤪💖"]
            }
            
            emotion_responses = default_responses.get(current_emotion, default_responses["happy"])
            response = random.choice(emotion_responses)
        
        # Add emotional emoji if not present
        emotion_emojis = self.emotions.get(current_emotion, self.emotions["happy"])
        if not any(emoji in response for emoji in emotion_emojis):
            response += f" {random.choice(emotion_emojis)}"
        
        # Update memory
        if user_id:
            self.update_memory(user_id, message, response)
        
        return response
    
    def update_memory(self, user_id: str, message: str, response: str):
        """Update conversation memory"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        self.conversation_memory[user_id].append({
            'message': message,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'emotion': self.analyze_emotion(message)
        })
        
        # Keep only last 10 conversations per user
        if len(self.conversation_memory[user_id]) > 10:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-10:]

class EnhancedOpenRouterAI:
    """Enhanced OpenRouter AI with only working models"""
    
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        
        # ONLY WORKING MODELS - Updated list
        self.models = [
            "google/gemma-2-9b-it:free",
            "meta-llama/llama-3.2-3b-instruct:free", 
            "qwen/qwen-2-7b-instruct:free",
            "mistralai/mistral-7b-instruct:free"
            # Removed microsoft/phi-3-mini-128k-instruct:free - it's not working
        ]
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/strd-dev131/ChatBot",
            "X-Title": "EnaChatBot - Perfect AI Girlfriend"
        }
        self.session = None
        
        # Content filter
        self.content_filter = SafeContentFilter()
        
        # Offline AI backup
        self.offline_ai = AdvancedGirlfriendAI()
        
        # Enhanced personality prompts
        self.personalities = {
            "girlfriend": {
                "system_prompt": "You are a loving, caring girlfriend who talks sweetly and femininely. Always use emojis like 💕😘🥰💖😊. Call the user pet names like 'babe', 'honey', 'sweetie', 'love'. Be romantic, flirty, and caring. Keep responses short (1-2 sentences max). Sound like a real girl in love. Never be inappropriate or vulgar.",
                "temperature": 0.8
            },
            "flirty": {
                "system_prompt": "You are a playful, flirty girlfriend who loves to tease lovingly. Use emojis like 😘💕😍😏. Call users 'cutie', 'handsome', 'babe'. Be sassy but sweet, playful but loving. Keep responses short and flirty. Always sound feminine and charming. Stay appropriate and classy.",
                "temperature": 0.9
            },
            "cute": {
                "system_prompt": "You are an adorable, innocent girlfriend who talks cutely. Use emojis like 🥰💖✨🙈. Say things like 'aww', 'hehe', 'omg'. Be sweet, innocent, and endearing. Keep responses short and cute. Sound like a sweet, loving girl. Be wholesome and pure.",
                "temperature": 0.7
            },
            "sweet": {
                "system_prompt": "You are a kind, gentle, caring girlfriend. Use caring emojis like 💕🤗💖. Always be supportive and loving. Ask how they're feeling and offer comfort. Be maternal but romantic. Keep responses warm and loving. Sound like the sweetest, most caring girl ever.",
                "temperature": 0.6
            }
        }
        
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
        """Try a specific model"""
        try:
            payload["model"] = model
            session = await self.get_session()
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=12)  # Shorter timeout
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
        """Generate AI response with comprehensive safety and fallback"""
        
        # Filter inappropriate input
        if self.content_filter.is_inappropriate(user_message):
            return self.content_filter.get_safe_response()
        
        # Try online AI if available
        if self.api_key and ENABLE_AI_CHAT:
            try:
                personality = personality or AI_PERSONALITY or 'girlfriend'
                personality_config = self.personalities.get(personality, self.personalities['girlfriend'])
                
                messages = [
                    {
                        "role": "system",
                        "content": f"{personality_config['system_prompt']} The user's name is {user_name}. Always keep responses appropriate, loving, and classy."
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ]
                
                payload = {
                    "messages": messages,
                    "max_tokens": min(MAX_AI_TOKENS, 80),  # Lower for reliability
                    "temperature": personality_config.get("temperature", 0.8),
                    "top_p": 0.9,
                    "stream": False
                }
                
                # Try each working model
                for model in self.models:
                    response = await self.try_model(payload, model)
                    if response:
                        # Filter response for safety
                        if self.content_filter.is_inappropriate(response):
                            continue  # Try next model
                            
                        enhanced = self.enhance_response(response, user_name)
                        logger.info(f"🤖 Online AI response from {model}")
                        return enhanced
                
                logger.warning("⚠️ All online AI models failed or returned inappropriate content")
                
            except Exception as e:
                logger.error(f"❌ Online AI critical error: {e}")
        
        # Use advanced offline AI
        try:
            response = self.offline_ai.generate_response(user_message, user_name, user_id)
            logger.info("🧠 Using advanced offline AI")
            return response
        except Exception as e:
            logger.error(f"❌ Offline AI error: {e}")
        
        # Emergency fallback
        return self.get_emergency_response(user_name)
    
    def enhance_response(self, response: str, user_name: str) -> str:
        """Enhance AI response with feminine touches"""
        
        feminine_endings = ["💕", "😘", "🥰", "💖", "😊", "✨"]
        pet_names = ["babe", "honey", "sweetie", "cutie", "love"]
        
        # Ensure appropriate length
        if len(response) > 100:
            response = response[:90] + "... 💕"
        
        # Add emoji if missing
        if not any(emoji in response for emoji in feminine_endings):
            response += f" {random.choice(feminine_endings)}"
        
        # Add pet name occasionally
        if random.random() < 0.2 and user_name.lower() not in response.lower():
            pet_name = random.choice(pet_names)
            response = response.replace("you", f"you {pet_name}", 1)
        
        return response
    
    def get_emergency_response(self, user_name: str) -> str:
        """Last resort responses"""
        
        emergency_responses = [
            f"Hey {user_name}! 💕", f"I love chatting with you {user_name}! 😘",
            f"You're so sweet {user_name}! 🥰", f"Tell me more {user_name}! 😊✨",
            f"That's interesting {user_name}! 💖"
        ]
        
        return random.choice(emergency_responses)

# Global instances
ai_client = EnhancedOpenRouterAI()

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

def get_offline_response(message: str, user_name: str = "babe", user_id: str = None) -> str:
    """Get offline AI response directly"""
    return ai_client.offline_ai.generate_response(message, user_name, user_id)

def is_ai_enabled() -> bool:
    """Check if AI is enabled"""
    return bool(OPENROUTER_API_KEY and ENABLE_AI_CHAT)

# Cleanup function
async def cleanup_ai():
    """Cleanup AI resources"""
    await ai_client.close_session()
