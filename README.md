# HoneypotWatcher Discord Bot

A Discord bot built with discord.py for monitoring honeypot activities. The bot is designed with a modular architecture for easy maintenance and extension.

## 🏗️ Project Structure

```
HoneypotWatcherDiscordBot/
├── bot.py                 # Main bot entry point
├── run.py                 # Simple script to run the bot
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
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
   git clone <repository-url>
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
   cp .env.example .env
   # Edit .env with your Discord bot token and other settings
   ```

5. **Run the bot:**
   ```bash
   python run.py
   # or
   python bot.py
   ```

## ⚙️ Configuration

### Environment Variables

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
6. Invite the bot to your server with the necessary permissions

## 📋 Features

### Commands

#### General Commands
- `/ping` - Check bot latency
- `/help` - Show help information
- `/status` - Show bot status

#### Honeypot Commands
- `/monitor_add <address> [description]` - Add address to monitoring
- `/monitor_remove <address>` - Remove address from monitoring
- `/monitor_list` - List all monitored addresses
- `/monitor_report <address> <activity>` - Report suspicious activity

#### Admin Commands
- `/admin_status` - Show detailed bot status
- `/admin_config` - Show bot configuration
- `/admin_reload <extension>` - Reload a bot extension
- `/admin_sync` - Sync slash commands

### Services

#### HoneypotService
- Monitors addresses for suspicious activities
- Tracks suspicious activity counts
- Triggers alerts when thresholds are exceeded

#### NotificationService
- Sends alerts and notifications to Discord channels
- Supports different severity levels
- Configurable notification channels and roles

## 🔧 Development

### Adding New Commands

1. Create a new file in the `commands/` directory
2. Follow the pattern in existing command files
3. Add the new command to the `initial_extensions` list in `bot.py`

### Adding New Services

1. Create a new service class in the `services/` directory
2. Inherit from `BaseService`
3. Implement the required abstract methods
4. Add the service to the bot's service manager

### Database

The bot uses SQLite for data persistence. The database is automatically created and initialized when the bot starts. Database operations are handled through the `DatabaseManager` class in `config/database.py`.

## 📝 Logging

The bot uses the `loguru` library for logging. Logs are written to both the console and a file (`logs/bot.log`). Log levels can be configured through the `LOG_LEVEL` environment variable.

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding to commands:**
   - Check that the bot has the necessary permissions
   - Verify that slash commands are synced using `/admin_sync`
   - Ensure the bot is online and connected

2. **Database errors:**
   - Check that the `data/` directory is writable
   - Verify database file permissions

3. **Import errors:**
   - Ensure all dependencies are installed
   - Check that you're running from the correct directory

### Debug Mode

Enable debug mode by setting `BOT_DEBUG=True` in your `.env` file. This will provide more detailed logging information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions, please:

1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information about your problem

## 🔄 Updates

To update the bot:

1. Pull the latest changes: `git pull origin main`
2. Update dependencies: `pip install -r requirements.txt`
3. Restart the bot

---

**Note:** This bot is designed for monitoring honeypot activities. Make sure to comply with all applicable laws and regulations when using this bot.
