"""
Admin commands for the Discord bot.
"""
import discord
from discord import app_commands
from discord.ext import commands

from utils.logger import logger


class AdminCommands(commands.Cog):
    """Administrative commands."""
    
    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        """Check if user has admin permissions."""
        return ctx.author.guild_permissions.administrator
    
    @app_commands.command(name="admin_status", description="Show detailed bot status (Admin only)")
    async def admin_status(self, interaction: discord.Interaction):
        """Show detailed bot status."""
        embed = discord.Embed(
            title="🔧 Admin Status",
            color=discord.Color.orange()
        )
        
        # Bot info
        embed.add_field(
            name="Bot Information",
            value=f"**Name:** {self.bot.user.name}\n**ID:** {self.bot.user.id}\n**Version:** discord.py {discord.__version__}",
            inline=False
        )
        
        # System info
        import os

        import psutil
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        embed.add_field(
            name="System Information",
            value=f"**Memory Usage:** {memory_usage:.2f} MB\n**CPU Usage:** {process.cpu_percent():.1f}%",
            inline=False
        )
        
        # Guild info
        embed.add_field(
            name="Guild Information",
            value=f"**Total Guilds:** {len(self.bot.guilds)}\n**Total Users:** {len(self.bot.users)}",
            inline=False
        )
        
        # Services status
        services_status = "**Services:**\n"
        if hasattr(self.bot, 'services'):
            for service_name, service in self.bot.services.items():
                status = "🟢 Running" if service.running else "🔴 Stopped"
                services_status += f"• {service_name}: {status}\n"
        else:
            services_status += "No services loaded"
        
        embed.add_field(
            name="Services Status",
            value=services_status,
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="admin_config", description="Show bot configuration (Admin only)")
    async def admin_config(self, interaction: discord.Interaction):
        """Show bot configuration."""
        from config import config
        
        embed = discord.Embed(
            title="⚙️ Bot Configuration",
            color=discord.Color.blue()
        )
        
        # Discord config
        embed.add_field(
            name="Discord Configuration",
            value=f"**Guild ID:** {config.DISCORD_GUILD_ID or 'Global'}\n**Prefix:** {config.BOT_PREFIX}\n**Debug:** {config.BOT_DEBUG}",
            inline=False
        )
        
        # Logging config
        embed.add_field(
            name="Logging Configuration",
            value=f"**Level:** {config.LOG_LEVEL}\n**File:** {config.LOG_FILE}",
            inline=False
        )
        
        # Bot intents
        intents = self.bot.intents
        intents_list = []
        for intent_name in ['guilds', 'members', 'bans', 'emojis', 'integrations', 'webhooks', 'invites', 'voice_states', 'presences', 'messages', 'guild_messages', 'dm_messages', 'message_content', 'guild_scheduled_events', 'auto_moderation_configuration', 'auto_moderation_execution']:
            if getattr(intents, intent_name, False):
                intents_list.append(f"✅ {intent_name}")
            else:
                intents_list.append(f"❌ {intent_name}")
        
        embed.add_field(
            name="Bot Intents",
            value="\n".join(intents_list),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="admin_reload", description="Reload bot extensions (Admin only)")
    async def admin_reload(self, interaction: discord.Interaction, extension: str):
        """Reload a bot extension."""
        try:
            await self.bot.reload_extension(extension)
            embed = discord.Embed(
                title="✅ Extension Reloaded",
                description=f"Successfully reloaded `{extension}`",
                color=discord.Color.green()
            )
        except Exception as e:
            embed = discord.Embed(
                title="❌ Reload Failed",
                description=f"Failed to reload `{extension}`: {str(e)}",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="admin_sync", description="Sync slash commands (Admin only)")
    async def admin_sync(self, interaction: discord.Interaction):
        """Sync slash commands."""
        try:
            if config.DISCORD_GUILD_ID:
                guild = discord.Object(id=config.DISCORD_GUILD_ID)
                self.bot.tree.copy_global_to(guild=guild)
                await self.bot.tree.sync(guild=guild)
                message = f"Synced commands to guild {config.DISCORD_GUILD_ID}"
            else:
                await self.bot.tree.sync()
                message = "Synced global commands"
            
            embed = discord.Embed(
                title="✅ Commands Synced",
                description=message,
                color=discord.Color.green()
            )
        except Exception as e:
            embed = discord.Embed(
                title="❌ Sync Failed",
                description=f"Failed to sync commands: {str(e)}",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the bot is ready."""
        logger.info("Admin commands cog loaded")


async def setup(bot):
    """Setup function for the cog."""
    await bot.add_cog(AdminCommands(bot))
