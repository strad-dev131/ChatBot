import os

# Set minimal environment variables so modules can import during tests
os.environ.setdefault("API_ID", "12345")
os.environ.setdefault("API_HASH", "testhash")
os.environ.setdefault("BOT_TOKEN", "123456:TEST")
os.environ.setdefault("MONGO_URL", "mongodb://127.0.0.1:27017/test")
os.environ.setdefault("OWNER_ID", "1")