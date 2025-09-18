"""
Main Discord bot entry point.
"""
import asyncio
import sys

import discord
from discord.ext import commands

from config import config
from services import HoneypotService, NotificationService
from utils.logger import logger


class HoneypotWatcherBot(commands.Bot):
    """Main bot class for HoneypotWatcher Discord Bot."""
    
    def __init__(self):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix=config.BOT_PREFIX,
            intents=intents,
            help_command=None,  # We'll implement custom help
            case_insensitive=True
        )
        
        self.initial_extensions = [
            "commands.general",
            "commands.admin",
            "commands.honeypot",
        ]
        
        # Initialize services
        self.services = {}
        self._init_services()
    
    def _init_services(self):
        """Initialize bot services."""
        self.services['honeypot'] = HoneypotService(self)
        self.services['notification'] = NotificationService(self)
    
    async def setup_hook(self):
        """Called when the bot is starting up."""
        logger.info("Setting up bot...")
        
        # Load extensions
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                logger.info(f"Loaded extension: {extension}")
            except Exception as e:
                logger.error(f"Failed to load extension {extension}: {e}")
        
        # Start services
        for service_name, service in self.services.items():
            try:
                await service.start()
                logger.info(f"Started service: {service_name}")
            except Exception as e:
                logger.error(f"Failed to start service {service_name}: {e}")
        
        # Sync commands
        if config.DISCORD_GUILD_ID:
            guild = discord.Object(id=config.DISCORD_GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info(f"Synced commands to guild {config.DISCORD_GUILD_ID}")
        else:
            await self.tree.sync()
            logger.info("Synced global commands")
    
    async def on_ready(self):
        """Called when the bot is ready."""
        logger.info(f"Bot is ready! Logged in as {self.user}")
        logger.info(f"Bot ID: {self.user.id}")
        logger.info(f"Connected to {len(self.guilds)} guilds")
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="for honeypot activities"
        )
        await self.change_presence(activity=activity)
    
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
            return
        
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the necessary permissions to execute this command.")
            return
        
        logger.error(f"Command error in {ctx.command}: {error}")
        await ctx.send("❌ An error occurred while executing the command.")
    
    async def close(self):
        """Called when the bot is shutting down."""
        logger.info("Bot is shutting down...")
        
        # Stop services
        for service_name, service in self.services.items():
            try:
                await service.stop()
                logger.info(f"Stopped service: {service_name}")
            except Exception as e:
                logger.error(f"Failed to stop service {service_name}: {e}")
        
        await super().close()


async def main():
    """Main function to run the bot."""
    try:
        # Validate configuration
        config.validate()
        
        # Create bot instance
        bot = HoneypotWatcherBot()
        
        # Start the bot
        await bot.start(config.DISCORD_TOKEN)
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
