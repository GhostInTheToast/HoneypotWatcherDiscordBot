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
            name="for traitors..."
        )
        await self.change_presence(activity=activity)
        
        # Send "Pathetic." message to specific channel
        target_channel_id = 1418079817256931350
        log_channel_id = 385510724912283648
        try:
            channel = self.get_channel(target_channel_id)
            if channel:
                await channel.send("Pathetic.")
                logger.info(f"Sent 'Pathetic.' message to channel {target_channel_id}")
            else:
                logger.warning(f"Could not find channel with ID {target_channel_id}")
        except Exception as e:
            logger.error(f"Failed to send message to channel {target_channel_id}: {e}")
    
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
    
    async def on_message(self, message):
        """Handle incoming messages."""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        # Whitelist of role IDs that should be ignored
        whitelist_roles = [
            462663247934390275,  # Ghost role
            213335817823715328,  # mods
            359424853285142539,  # Knowledgeable
            890067789832929280,  # Helpful
            213334124767739904,  # Daunzo
        ]
        
        # Check if user has any whitelisted roles
        user_role_ids = [role.id for role in message.author.roles]
        if any(role_id in whitelist_roles for role_id in user_role_ids):
            # User has a whitelisted role, ignore completely
            return
        
        # Check if message is in the target channel
        target_channel_id = 1418079817256931350
        log_channel_id = 385510724912283648
        if message.channel.id == target_channel_id:
            try:
                # Check if user has the ghost role
                ghost_role_id = 462663247934390275
                has_ghost_role = any(role.id == ghost_role_id for role in message.author.roles)
                
                # Delete the user's message first
                try:
                    await message.delete()
                    logger.info(f"Deleted message from {message.author.name}")
                except Exception as delete_error:
                    logger.error(f"Failed to delete message from {message.author.name}: {delete_error}")
                
                # BAN THE USER AND DELETE THEIR MESSAGES FROM PAST 24 HOURS
                try:
                    # Ban the user
                    await message.author.ban(reason="Posted in restricted channel - auto-ban")
                    logger.warning(f"BANNED user {message.author.name} ({message.author.id}) for posting in restricted channel")
                    
                    # Delete all messages from this user in the past 24 hours
                    from datetime import datetime, timedelta
                    cutoff_time = datetime.utcnow() - timedelta(hours=24)
                    
                    deleted_count = 0
                    async for msg in message.channel.history(limit=None, after=cutoff_time):
                        if msg.author.id == message.author.id:
                            try:
                                await msg.delete()
                                deleted_count += 1
                            except Exception as msg_delete_error:
                                logger.error(f"Failed to delete message {msg.id}: {msg_delete_error}")
                    
                    logger.info(f"Deleted {deleted_count} messages from banned user {message.author.name}")
                    
                except Exception as ban_error:
                    logger.error(f"Failed to ban user {message.author.name}: {ban_error}")
                
                # Send elimination messages to log channel instead
                log_channel = self.get_channel(log_channel_id)
                if log_channel:
                    if has_ghost_role:
                        # Special message for ghost role users
                        await log_channel.send(f"***{message.author.name} eliminated.***")
                        
                        # Send the GIF
                        gif_url = "https://tenor.com/view/itachi-sharingan-mangekyou-tsukuyomi-tsukyomi-gif-2677620834910513053"
                        await log_channel.send(gif_url)
                    else:
                        # Regular elimination message
                        await log_channel.send(f"***{message.author.name} eliminated.***")
                        
                        # Send the GIF
                        gif_url = "https://tenor.com/view/itachi-sharingan-mangekyou-tsukuyomi-tsukyomi-gif-2677620834910513053"
                        await log_channel.send(gif_url)
                
                # Log activity to the log channel
                try:
                    log_channel = self.get_channel(log_channel_id)
                    if log_channel:
                        log_message = f"🚨 **USER BANNED**\n**User:** {message.author.name} ({message.author.id})\n**Channel:** {message.channel.name} ({message.channel.id})\n**Ghost Role:** {'Yes' if has_ghost_role else 'No'}\n**Message:** {message.content[:100]}{'...' if len(message.content) > 100 else ''}\n**Action:** BANNED + Messages deleted from past 24h"
                        await log_channel.send(log_message)
                    else:
                        logger.warning(f"Could not find log channel with ID {log_channel_id}")
                except Exception as log_error:
                    logger.error(f"Failed to log activity to channel {log_channel_id}: {log_error}")
 
                logger.info(f"Responded to message from {message.author.name} in channel {target_channel_id} (ghost role: {has_ghost_role})")
            except Exception as e:
                logger.error(f"Failed to respond to message in channel {target_channel_id}: {e}")
        
        # Process commands (important for command handling)
        await self.process_commands(message)
    
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
