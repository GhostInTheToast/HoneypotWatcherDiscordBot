"""
Configuration settings for the Discord bot.
"""
import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BotConfig:
    """Bot configuration class."""
    
    # Discord settings
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    DISCORD_GUILD_ID: Optional[int] = int(os.getenv("DISCORD_GUILD_ID", "0")) or None
    
    # Bot settings
    BOT_PREFIX: str = os.getenv("BOT_PREFIX", "!")
    BOT_DEBUG: bool = os.getenv("BOT_DEBUG", "False").lower() == "true"
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/bot.log")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is required")
        return True


# Global config instance
config = BotConfig()
