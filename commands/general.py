"""
General commands for the Discord bot.
"""
import discord
from discord import app_commands
from discord.ext import commands

from utils.logger import logger


class GeneralCommands(commands.Cog):
    """General purpose commands."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        """Check bot latency."""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: {latency}ms",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="help", description="Show bot help information")
    async def help_command(self, interaction: discord.Interaction):
        """Show bot help information."""
        embed = discord.Embed(
            title="🤖 HoneypotWatcher Bot Help",
            description="A Discord bot for monitoring honeypot activities.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="General Commands",
            value="• `/ping` - Check bot latency\n• `/help` - Show this help message",
            inline=False
        )
        
        embed.add_field(
            name="Honeypot Commands",
            value="• `/monitor add <address>` - Add address to monitoring\n• `/monitor remove <address>` - Remove address from monitoring\n• `/monitor list` - List monitored addresses",
            inline=False
        )
        
        embed.add_field(
            name="Admin Commands",
            value="• `/admin status` - Show bot status\n• `/admin config` - Show bot configuration",
            inline=False
        )
        
        embed.set_footer(text="Use / before commands to use slash commands")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="status", description="Show bot status")
    async def status(self, interaction: discord.Interaction):
        """Show bot status."""
        embed = discord.Embed(
            title="📊 Bot Status",
            color=discord.Color.green()
        )
        
        # Bot info
        embed.add_field(
            name="Bot Info",
            value=f"**Name:** {self.bot.user.name}\n**ID:** {self.bot.user.id}\n**Latency:** {round(self.bot.latency * 1000)}ms",
            inline=False
        )
        
        # Guild info
        embed.add_field(
            name="Guild Info",
            value=f"**Guilds:** {len(self.bot.guilds)}\n**Users:** {len(self.bot.users)}",
            inline=False
        )
        
        # Uptime
        uptime = discord.utils.utcnow() - self.bot.start_time if hasattr(self.bot, 'start_time') else "Unknown"
        embed.add_field(
            name="Uptime",
            value=str(uptime),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name="message")
    async def warning_message(self, ctx):
        """Post the warning message about the channel."""
        # Check if user is authorized
        authorized_user_id = 150009383592525826
        target_channel_id = 1418079817256931350
        
        if ctx.author.id != authorized_user_id:
            await ctx.send("❌ You don't have permission to use this command.")
            return
        
        # Get the target channel
        target_channel = self.bot.get_channel(target_channel_id)
        if not target_channel:
            await ctx.send(f"❌ Could not find channel with ID {target_channel_id}")
            return
        
        # Post the warning message in the target channel
        warning_text = "**Do NOT post here. This channel is for finding chatbots only. Post here and you will be __immediately banned__. This is not a joke.**"
        await target_channel.send(warning_text)
        
        # Confirm to the user who ran the command
        await ctx.send(f"✅ Warning message posted in {target_channel.name}")
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the bot is ready."""
        logger.info("General commands cog loaded")


async def setup(bot):
    """Setup function for the cog."""
    await bot.add_cog(GeneralCommands(bot))
