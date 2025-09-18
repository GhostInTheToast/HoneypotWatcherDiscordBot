#!/usr/bin/env python3
"""
Setup script for HoneypotWatcher Discord Bot.
"""
import sys
from pathlib import Path


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here

# Bot Settings
BOT_PREFIX=!
BOT_DEBUG=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file. Please edit it with your Discord bot token.")
    else:
        print("ℹ️  .env file already exists.")


def create_directories():
    """Create necessary directories."""
    directories = ['logs', 'data']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✅ Python version {sys.version.split()[0]} is compatible.")


def main():
    """Main setup function."""
    print("🚀 Setting up HoneypotWatcher Discord Bot...")
    print()
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    print()
    print("🎉 Setup complete!")
    print()
    print("Next steps:")
    print("1. Edit .env file with your Discord bot token")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the bot: python run.py")
    print()
    print("For more information, see README.md")


if __name__ == "__main__":
    main()
