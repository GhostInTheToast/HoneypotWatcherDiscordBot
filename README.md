# HoneypotWatcher Discord Bot

A Discord bot built with discord.py for monitoring and managing Discord channels with advanced features like message deletion, role-based whitelisting, and automated responses.

## 🏗️ Project Structure

```
HoneypotWatcherDiscordBot/
├── bot.py                 # Main bot entry point
├── run.py                 # Simple script to run the bot
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── config/               # Configuration files
│   ├── __init__.py
│   ├── settings.py       # Bot configuration
│   └── database.py       # Database management
├── commands/             # Bot commands
│   ├── __init__.py
│   ├── general.py        # General commands
│   ├── admin.py          # Admin commands
│   └── honeypot.py       # Honeypot monitoring commands
├── services/             # Bot services
│   ├── __init__.py
│   ├── base_service.py   # Base service class
│   ├── honeypot_service.py    # Honeypot monitoring service
│   └── notification_service.py # Notification service
├── utils/                # Utility functions
│   ├── __init__.py
│   └── logger.py         # Logging configuration
└── logs/                 # Log files (created automatically)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Discord application and bot token
- Git (for cloning the repository)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GhostInTheToast/HoneypotWatcherDiscordBot.git
   cd HoneypotWatcherDiscordBot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   python setup.py  # Creates .env file
   # Edit .env with your Discord bot token and other settings
   ```

5. **Run the bot:**
   ```bash
   python run.py
   # or
   python bot.py
   ```

## ⚙️ Configuration

### Environment Variables (.env file)

Create a `.env` file in the project root with the following variables:

```env
# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here

# Bot Settings
BOT_PREFIX=!
BOT_DEBUG=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

### Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. Enable the following intents in the bot settings:
   - Server Members Intent
   - Message Content Intent
6. Invite the bot to your server with the necessary permissions:
   - Send Messages
   - Manage Messages (for message deletion)
   - Use Slash Commands
   - Read Message History

## 🎯 Bot Features

### Channel Management

#### Target Channel
- **Purpose:** The channel the bot monitors for messages
- **Current ID:** `1418079817256931350` (configurable in `bot.py`)
- **Behavior:** 
  - Deletes user messages immediately
  - No bot responses sent here
  - Clean channel with only deletions

#### Log Channel
- **Purpose:** Where bot sends all responses and logs
- **Current ID:** `385510724912283648` (configurable in `bot.py`)
- **Content:**
  - Elimination messages
  - Itachi Sharingan GIFs
  - Detailed activity logs
  - Bot responses

### Whitelist System

The bot has a whitelist system that completely ignores users with specific roles:

```python
# In bot.py, whitelist_roles array
whitelist_roles = [
    # 462663247934390275,  # Ghost role
    # 213335817823715328,  # mods
    # 359424853285142539,  # Knowledgeable
    # 890067789832929280,  # Helpful
    # 213334124767739904,  # Daunzo
]
```

**To add roles to whitelist:**
1. Get the role ID (right-click role → Copy Role ID with Developer Mode on)
2. Uncomment and add the role ID to the `whitelist_roles` array
3. Restart the bot

**Whitelisted users:**
- ✅ Can post freely in target channel
- ✅ No message deletion
- ✅ No bot responses
- ✅ Complete bypass of all bot features

### Message Processing

When a non-whitelisted user posts in the target channel:

1. **Message Deletion** - User's message is immediately deleted
2. **Log Channel Response** - Bot sends elimination message to log channel
3. **GIF Response** - Itachi Sharingan GIF is sent to log channel
4. **Activity Logging** - Detailed log entry with user info and message content

### Special Role Handling

- **Ghost Role Users** - Get special "You have the ghost role also" message
- **Regular Users** - Get standard elimination message

## 📋 Commands

### General Commands
- `/ping` - Check bot latency
- `/help` - Show help information
- `/status` - Show bot status

### Admin Commands
- `/admin_status` - Show detailed bot status
- `/admin_config` - Show bot configuration
- `/admin_reload <extension>` - Reload a bot extension
- `/admin_sync` - Sync slash commands

### Special Commands
- `!message` - Post warning message (restricted to specific user ID)

## 🔧 Customization

### Changing Channel IDs

To change the target or log channels, edit these values in `bot.py`:

```python
# Target channel (monitored channel)
target_channel_id = 1418079817256931350

# Log channel (where responses are sent)
log_channel_id = 385510724912283648
```

### Changing Authorized Users

To change who can use the `!message` command, edit this in `commands/general.py`:

```python
authorized_user_id = 150009383592525826
```

### Changing GIFs

To change the elimination GIF, edit this in `bot.py`:

```python
gif_url = "https://tenor.com/view/itachi-sharingan-mangekyou-tsukuyomi-tsukyomi-gif-2677620834910513053"
```

## 🛡️ Security

### What's Safe to Push to GitHub
- ✅ Source code
- ✅ Channel/User/Role IDs (not sensitive)
- ✅ Configuration structure
- ✅ Documentation

### What's Protected
- ❌ `.env` file (contains Discord token)
- ❌ `logs/` directory (contains log files)
- ❌ `data/` directory (contains database files)

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding:**
   - Check Discord token in `.env` file
   - Verify bot has necessary permissions
   - Check if bot is online

2. **Messages not being deleted:**
   - Ensure bot has "Manage Messages" permission
   - Check if user has whitelisted role

3. **Commands not working:**
   - Use `/admin_sync` to sync slash commands
   - Check bot permissions

4. **Import errors:**
   - Activate virtual environment: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

### Debug Mode

Enable debug mode by setting `BOT_DEBUG=True` in your `.env` file for more detailed logging.

## 📝 Logging

The bot uses the `loguru` library for logging:
- **Console output** - Real-time logging
- **File logging** - Saved to `logs/bot.log`
- **Rotation** - Logs rotate at 10MB
- **Retention** - Keeps logs for 7 days

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Check bot logs in `logs/bot.log`
3. Create an issue on GitHub

---

**Note:** This bot is designed for Discord server management. Make sure to comply with Discord's Terms of Service and your server's rules when using this bot.
