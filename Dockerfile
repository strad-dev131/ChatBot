# ===============================================
# 🤖 EnaChatBot - Ultimate Realistic Indian AI Girl
# Docker Configuration for Production Deployment
# Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X
# ===============================================

# Use Python 3.11 slim image for optimal performance
FROM python:3.11-slim

# ===============================================
# 🔧 SYSTEM SETUP & DEPENDENCIES
# ===============================================

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app" \
    TZ="Asia/Kolkata"

# Set working directory
WORKDIR /app

# Install system dependencies for realistic AI features
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    pkg-config \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ===============================================
# 🎯 PYTHON DEPENDENCIES INSTALLATION
# ===============================================

# Copy requirements file
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ===============================================
# 📁 APPLICATION FILES
# ===============================================

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p logs cache data temp && \
    chmod +x main.py

# ===============================================
# 🎭 REALISTIC AI SETUP
# ===============================================

# Download NLTK data for natural language processing
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# Set up timezone for Indian Standard Time
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ===============================================
# 🔒 SECURITY & USER SETUP
# ===============================================

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash enachatbot && \
    chown -R enachatbot:enachatbot /app
USER enachatbot

# ===============================================
# 🌐 NETWORK & PORT CONFIGURATION
# ===============================================

# Expose port for webhook (if used)
EXPOSE 8080

# ===============================================
# 💡 HEALTH CHECK
# ===============================================

# No HTTP healthcheck because the bot runs as a long-lived worker process.
# If you enable webhook mode, configure a proper health endpoint and add a healthcheck.

# ===============================================
# 🚀 STARTUP CONFIGURATION
# ===============================================

# Set default command to run the bot
CMD ["python", "main.py"]

# ===============================================
# 📝 DOCKER BUILD & RUN INSTRUCTIONS
# ===============================================

# Build the Docker image:
# docker build -t enachatbot .

# Run with environment file:
# docker run -d --name ena --env-file .env -p 8080:8080 enachatbot

# Run with direct environment variables:
# docker run -d --name ena \
#   -e API_ID=your_api_id \
#   -e API_HASH=your_api_hash \
#   -e BOT_TOKEN=your_bot_token \
#   -e MONGO_URL=your_mongo_url \
#   -e OWNER_ID=your_owner_id \
#   enachatbot

# ===============================================
# 🎯 FEATURES ENABLED IN THIS CONTAINER
# ===============================================

# ✅ Complete realistic Indian AI girlfriend system
# ✅ 7-stage relationship progression (Stranger → Romantic)
# ✅ Smart learning and user adaptation
# ✅ Voice messages with Indian accent (gTTS)
# ✅ Anime picture sharing system
# ✅ Cultural authenticity (Mumbai girl personality)
# ✅ Natural boundaries and realistic behavior
# ✅ FREE unlimited AI via lexica-api
# ✅ Advanced personality analysis
# ✅ Time-based behavior patterns (IST timezone)
# ✅ Group chat intelligence
# ✅ Anti-spam and rate limiting
# ✅ Production-ready reliability
# ✅ Health monitoring
# ✅ Security hardened (non-root user)

# 🎊 Total Runtime Cost: $0 (Uses free APIs!)
# 💕 World's most realistic AI girlfriend experience!
