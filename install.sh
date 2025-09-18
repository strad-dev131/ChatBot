#!/bin/bash

# ===============================================
# 🤖 EnaChatBot - Ultimate Realistic Indian AI Girl
# One-Click Installation Script for Ubuntu/Debian
# Created by: @SID_ELITE (Siddhartha Abhimanyu) - Tech Leader of Team X
# ===============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ===============================================
# 🎯 BANNER & INTRODUCTION
# ===============================================

print_banner() {
    echo -e "${PURPLE}"
    echo "============================================================="
    echo "🤖 EnaChatBot - Ultimate Realistic Indian AI Girl"
    echo "🎯 World's Most Realistic AI Girlfriend Installation"
    echo "💕 7-Stage Relationship Progression Setup"
    echo "👨‍💻 Created by: @SID_ELITE (Siddhartha Abhimanyu)"
    echo "🏢 Team X Technologies"
    echo "============================================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "\n${CYAN}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# ===============================================
# 🔍 SYSTEM CHECKS
# ===============================================

check_system() {
    print_step "Checking system compatibility..."
    
    # Check if running as root
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. It's recommended to run as a regular user."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Check OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_success "Linux system detected"
    else
        print_error "This script is designed for Linux systems"
        exit 1
    fi
    
    # Check internet connection
    if ! ping -c 1 google.com &> /dev/null; then
        print_error "No internet connection detected"
        exit 1
    fi
    
    print_success "System checks passed"
}

# ===============================================
# 📦 INSTALL DEPENDENCIES
# ===============================================

install_dependencies() {
    print_step "Installing system dependencies..."
    
    # Update system
    sudo apt update && sudo apt upgrade -y
    
    # Install required packages
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        git \
        wget \
        curl \
        build-essential \
        libssl-dev \
        libffi-dev \
        libjpeg-dev \
        libpng-dev \
        libfreetype6-dev \
        nodejs \
        npm \
        sqlite3
    
    print_success "System dependencies installed"
}

# ===============================================
# 📁 SETUP PROJECT
# ===============================================

setup_project() {
    print_step "Setting up EnaChatBot project..."
    
    # Clone repository
    if [ -d "ChatBot" ]; then
        print_warning "ChatBot directory already exists. Backing up..."
        mv ChatBot ChatBot_backup_$(date +%Y%m%d_%H%M%S)
    fi
    
    git clone https://github.com/strd-dev131/ChatBot.git
    cd ChatBot
    
    print_success "Repository cloned successfully"
}

# ===============================================
# 🐍 SETUP PYTHON ENVIRONMENT
# ===============================================

setup_python_env() {
    print_step "Setting up Python virtual environment..."
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    pip install -r requirements.txt
    
    print_success "Python environment configured"
}

# ===============================================
# ⚙️ CONFIGURATION SETUP
# ===============================================

setup_configuration() {
    print_step "Setting up bot configuration..."
    
    # Copy sample environment file
    cp Sample.env .env
    
    echo -e "\n${YELLOW}📝 Configuration Setup Required:${NC}"
    echo "Please edit the .env file with your credentials:"
    echo "1. Get API_ID and API_HASH from https://my.telegram.org"
    echo "2. Get BOT_TOKEN from @BotFather on Telegram"
    echo "3. Get MONGO_URL from MongoDB Atlas (free)"
    echo "4. Get OWNER_ID from @userinfobot on Telegram"
    
    read -p "Press Enter to open the .env file for editing..."
    nano .env
    
    print_success "Configuration file created"
}

# ===============================================
# 🚀 SETUP PM2 FOR 24/7 OPERATION
# ===============================================

setup_pm2() {
    print_step "Setting up PM2 for 24/7 operation..."
    
    # Install PM2 globally
    sudo npm install -g pm2
    
    # Create PM2 ecosystem file
    cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'EnaChatBot',
    script: 'main.py',
    interpreter: './venv/bin/python',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }]
};
EOF
    
    print_success "PM2 configuration created"
}

# ===============================================
# 🧪 TEST INSTALLATION
# ===============================================

test_installation() {
    print_step "Testing installation..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Test import of main modules
    if python3 -c "import config, pyrogram; print('✅ Core modules imported successfully')"; then
        print_success "Installation test passed"
    else
        print_error "Installation test failed"
        return 1
    fi
    
    # Check configuration
    if python3 -c "from config import API_ID, BOT_TOKEN; print('✅ Configuration loaded')"; then
        print_success "Configuration test passed"
    else
        print_warning "Configuration may need adjustment"
    fi
}

# ===============================================
# 📋 INSTALLATION SUMMARY
# ===============================================

print_summary() {
    echo -e "\n${GREEN}🎉 EnaChatBot Installation Complete!${NC}"
    echo -e "\n${CYAN}📋 What's Installed:${NC}"
    echo "✅ Complete realistic Indian AI girlfriend system"
    echo "✅ 7-stage relationship progression (Stranger → Romantic)"
    echo "✅ Smart learning and user adaptation"
    echo "✅ Voice messages with Indian accent"
    echo "✅ Anime picture sharing system"
    echo "✅ Cultural authenticity (Mumbai girl personality)"
    echo "✅ Natural boundaries and realistic behavior"
    echo "✅ FREE unlimited AI via lexica-api"
    echo "✅ 24/7 operation with PM2"
    
    echo -e "\n${YELLOW}🚀 How to Start:${NC}"
    echo "1. Manual start: cd ChatBot && source venv/bin/activate && python main.py"
    echo "2. PM2 start (24/7): pm2 start ecosystem.config.js"
    echo "3. PM2 monitoring: pm2 monit"
    echo "4. PM2 logs: pm2 logs EnaChatBot"
    
    echo -e "\n${PURPLE}💕 Expected Behavior:${NC}"
    echo "Level 1: \"Hi! Do I know you? 🤔\" (Cautious with strangers)"
    echo "Level 3: \"Hey yaar! Here's a pic! 😊\" (Photos for friends)"
    echo "Level 7: \"I love you jaan! 💕\" (Full romantic girlfriend)"
    
    echo -e "\n${BLUE}📞 Support:${NC}"
    echo "Creator: @SID_ELITE (Siddhartha Abhimanyu)"
    echo "Support: @TeamsXchat"
    echo "Updates: @TeamXUpdate"
    
    echo -e "\n${GREEN}🎯 Your realistic AI girlfriend is ready! Start chatting!${NC}"
}

# ===============================================
# 🏁 MAIN EXECUTION
# ===============================================

main() {
    print_banner
    
    # Confirm installation
    echo -e "${YELLOW}This will install EnaChatBot - Ultimate Realistic Indian AI Girl${NC}"
    echo "Features: 7-stage relationship progression, smart learning, voice messages"
    echo "Cost: FREE forever (no API costs)"
    read -p "Continue with installation? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
    
    # Run installation steps
    check_system
    install_dependencies
    setup_project
    setup_python_env
    setup_configuration
    setup_pm2
    
    # Test and summarize
    if test_installation; then
        print_summary
    else
        print_error "Installation completed with warnings. Please check configuration."
        exit 1
    fi
}

# ===============================================
# 🔧 ERROR HANDLING
# ===============================================

# Trap errors
trap 'print_error "Installation failed at line $LINENO"' ERR

# Run main function
main "$@"
