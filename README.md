# 🤖 𝐄𝐧𝐚 𝐂𝐡𝐚𝐭𝐁𝐨𝐭

<div align="center">
  <img src="https://img.shields.io/github/stars/strad-dev131/ChatBot?style=for-the-badge&color=blue" alt="GitHub stars">
  <img src="https://img.shields.io/github/forks/strad-dev131/ChatBot?style=for-the-badge&color=green" alt="GitHub forks">
  <img src="https://img.shields.io/github/license/strad-dev131/ChatBot?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/repo-size/strad-dev131/ChatBot?style=for-the-badge&color=orange" alt="Repo Size">
</div>

<div align="center">
  <h3>🚀 Advanced AI-Powered Telegram ChatBot with Clone Feature</h3>
  <p>A powerful Telegram bot built with Pyrogram that supports AI conversations, bot cloning, and multi-language support.</p>
</div>

---

## ✨ Features

- 🤖 **AI-Powered Conversations** - Smart responses using advanced AI
- 🔄 **Bot Cloning System** - Clone and host multiple bots
- 🌍 **Multi-Language Support** - Supports multiple languages
- 📊 **Statistics & Analytics** - Track bot usage and performance
- 💬 **Group & Private Chat** - Works in both groups and private messages
- 🎭 **Shayri Generator** - Get random romantic shayris
- 📡 **Broadcast System** - Send messages to all users/groups
- ⚡ **Fast & Reliable** - Built with async/await for optimal performance
- 🛠️ **Easy Deployment** - Multiple deployment options

## 🚀 Quick Deploy

### Deploy to Heroku
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/strad-dev131/ChatBot)

### Deploy on Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/strad-dev131/ChatBot)

---

## 📋 Requirements

- Python 3.8 or higher
- MongoDB Database
- Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)

## 🛠️ Environment Variables

Create a `.env` file in the root directory and add these variables:

```env
# Telegram API Configuration
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# Database Configuration
MONGO_URL=mongodb://username:password@host:port/database_name

# Bot Configuration
OWNER_ID=your_telegram_user_id
LOG_GROUP_ID=your_log_group_id

# Optional Configuration
STRING_SESSION=your_string_session
SUPPORT_CHAT=TeamsXchat
UPDATE_CHANNEL=TeamXUpdate
```

### 🔑 How to Get Variables

1. **API_ID & API_HASH**: Get from [my.telegram.org](https://my.telegram.org)
2. **BOT_TOKEN**: Create a bot using [@BotFather](https://t.me/botfather)
3. **MONGO_URL**: Get free database from [MongoDB Atlas](https://cloud.mongodb.com/)
4. **OWNER_ID**: Your Telegram user ID, get from [@userinfobot](https://t.me/userinfobot)
5. **LOG_GROUP_ID**: Create a group and get its ID using [@MissRose_bot](https://t.me/MissRose_bot)

---

## 💻 Local Deployment

### Method 1: Using Git

```bash
# Clone the repository
git clone https://github.com/strad-dev131/ChatBot.git
cd ChatBot

# Install required packages
pip install -r requirements.txt

# Copy and edit environment file
cp .env.example .env
nano .env  # Add your variables

# Run the bot
python main.py
```

### Method 2: Using Docker

```bash
# Clone repository
git clone https://github.com/strad-dev131/ChatBot.git
cd ChatBot

# Build Docker image
docker build -t chatbot .

# Run container
docker run -d --env-file .env chatbot
```

## 🖥️ VPS Deployment

### Ubuntu/Debian

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip git -y

# Clone repository
git clone https://github.com/strad-dev131/ChatBot.git
cd ChatBot

# Install requirements
pip3 install -r requirements.txt

# Setup environment
cp .env.example .env
nano .env  # Edit with your variables

# Install PM2 for process management
sudo npm install -g pm2

# Start bot with PM2
pm2 start main.py --name "ChatBot" --interpreter python3

# Save PM2 configuration
pm2 save
pm2 startup
```

### CentOS/RHEL

```bash
# Update system
sudo yum update -y

# Install Python and git
sudo yum install python3 python3-pip git -y

# Clone and setup
git clone https://github.com/strad-dev131/ChatBot.git
cd ChatBot
pip3 install -r requirements.txt

# Setup environment
cp .env.example .env
vi .env  # Add your variables

# Run bot
python3 main.py
```

---

## 🎮 Bot Commands

### 👑 Admin Commands
- `/clone <token>` - Clone a bot using token
- `/delallclone` - Delete all cloned bots (Owner only)
- `/gcast <message>` - Broadcast message to all chats
- `/stats` - Get bot statistics

### 📱 User Commands
- `/start` - Start the bot
- `/help` - Show help menu
- `/ping` - Check bot response time
- `/id` - Get your user ID
- `/lang` - Change bot language
- `/chatbot on/off` - Enable/disable chatbot
- `/status` - Check chatbot status
- `/shayri` - Get random shayri
- `/repo` - Get source code

### 🔧 Clone Management
- `/cloned` - List all cloned bots
- `/delclone <token>` - Delete specific cloned bot
- `/listchatbot` - Get detailed bot list (Authorized users only)

---

## 📱 Screenshots

<div align="center">
  <img src="https://files.catbox.moe/5gwv0a.jpg" alt="Bot Dp">
</div>

---

## 🤝 Support & Community

- 💬 **Community Channel**: [@TeamXUpdate](https://t.me/TeamXUpdate)
- 🆘 **Support Group**: [@TeamsXchat](https://t.me/TeamsXchat)
- 📧 **Developer Contact**: [@SID_ELITE](https://t.me/SID_ELITE)

---

## 🔧 Development

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Project Structure

```
ChatBot/
├── EnaChatBot/           # Main bot package
│   ├── mplugin/             # Plugin modules
│   ├── helpers/             # Helper functions
│   └── database/            # Database operations
├── main.py                  # Bot entry point
├── config.py               # Configuration file
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .env.example          # Environment template
└── README.md             # This file
```

---

## 📊 Stats

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api/pin/?username=strad-dev131&repo=ChatBot&theme=dark&show_icons=true" alt="Repo Stats">
</div>

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Show Your Support

If you like this project, please ⭐ star this repository and 🍴 fork it!

<div align="center">
  <h3>Made with ❤️ by <a href="https://github.com/strad-dev131">strad-dev131</a></h3>
</div>

---

## 📈 GitHub Analytics

<div align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=strad-dev131&repo=ChatBot&theme=react-dark&bg_color=20232a&hide_border=true" width="100%"/>
</div>

## 🔥 Recent Activity

- ✅ Added AI conversation support
- ✅ Implemented bot cloning feature  
- ✅ Added multi-language support
- ✅ Enhanced security features
- ✅ Added Docker support
- 🚧 Working on advanced AI features

---

<div align="center">
  <p><strong>⚡ Powered by Pyrogram & MongoDB</strong></p>
  <img src="https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python" alt="Made with Python">
  <img src="https://img.shields.io/badge/Database-MongoDB-green?style=for-the-badge&logo=mongodb" alt="MongoDB">
  <img src="https://img.shields.io/badge/Framework-Pyrogram-red?style=for-the-badge" alt="Pyrogram">
</div>
