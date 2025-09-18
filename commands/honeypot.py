"""
Honeypot monitoring commands for the Discord bot.
"""
import discord
from discord import app_commands
from discord.ext import commands

from utils.logger import logger


class HoneypotCommands(commands.Cog):
    """Honeypot monitoring commands."""
    
    def __init__(self, bot):
        self.bot = bot
        self.honeypot_service = None
    
    async def cog_load(self):
        """Called when the cog is loaded."""
        # Get the honeypot service from the bot
        if hasattr(self.bot, 'services') and 'honeypot' in self.bot.services:
            self.honeypot_service = self.bot.services['honeypot']
    
    @app_commands.command(name="monitor_add", description="Add an address to honeypot monitoring")
    @app_commands.describe(address="The address to monitor")
    @app_commands.describe(description="Optional description for the address")
    async def monitor_add(self, interaction: discord.Interaction, address: str, description: str = None):
        """Add an address to monitoring."""
        if not self.honeypot_service:
            await interaction.response.send_message("❌ Honeypot service is not available.", ephemeral=True)
            return
        
        metadata = {"description": description} if description else {}
        success = await self.honeypot_service.add_monitored_address(address, metadata)
        
        if success:
            embed = discord.Embed(
                title="✅ Address Added",
                description=f"Successfully added `{address}` to monitoring.",
                color=discord.Color.green()
            )
            if description:
                embed.add_field(name="Description", value=description, inline=False)
        else:
            embed = discord.Embed(
                title="❌ Add Failed",
                description=f"Failed to add `{address}` to monitoring.",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="monitor_remove", description="Remove an address from honeypot monitoring")
    @app_commands.describe(address="The address to remove from monitoring")
    async def monitor_remove(self, interaction: discord.Interaction, address: str):
        """Remove an address from monitoring."""
        if not self.honeypot_service:
            await interaction.response.send_message("❌ Honeypot service is not available.", ephemeral=True)
            return
        
        success = await self.honeypot_service.remove_monitored_address(address)
        
        if success:
            embed = discord.Embed(
                title="✅ Address Removed",
                description=f"Successfully removed `{address}` from monitoring.",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ Remove Failed",
                description=f"Failed to remove `{address}` from monitoring. Address may not exist.",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="monitor_list", description="List all monitored addresses")
    async def monitor_list(self, interaction: discord.Interaction):
        """List all monitored addresses."""
        if not self.honeypot_service:
            await interaction.response.send_message("❌ Honeypot service is not available.", ephemeral=True)
            return
        
        addresses = await self.honeypot_service.get_monitored_addresses()
        
        if not addresses:
            embed = discord.Embed(
                title="📋 Monitored Addresses",
                description="No addresses are currently being monitored.",
                color=discord.Color.blue()
            )
        else:
            embed = discord.Embed(
                title="📋 Monitored Addresses",
                description=f"Currently monitoring {len(addresses)} address(es):",
                color=discord.Color.blue()
            )
            
            for i, addr_data in enumerate(addresses[:10], 1):  # Limit to 10 addresses
                address = addr_data["address"]
                added_at = addr_data["added_at"].strftime("%Y-%m-%d %H:%M")
                suspicious_count = addr_data["suspicious_count"]
                description = addr_data.get("metadata", {}).get("description", "No description")
                
                embed.add_field(
                    name=f"{i}. {address}",
                    value=f"**Added:** {added_at}\n**Suspicious:** {suspicious_count}\n**Description:** {description}",
                    inline=False
                )
            
            if len(addresses) > 10:
                embed.set_footer(text=f"... and {len(addresses) - 10} more addresses")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="monitor_report", description="Report suspicious activity for an address")
    @app_commands.describe(address="The address to report activity for")
    @app_commands.describe(activity="Description of the suspicious activity")
    async def monitor_report(self, interaction: discord.Interaction, address: str, activity: str):
        """Report suspicious activity for an address."""
        if not self.honeypot_service:
            await interaction.response.send_message("❌ Honeypot service is not available.", ephemeral=True)
            return
        
        activity_data = {
            "reported_by": interaction.user.name,
            "activity": activity,
            "timestamp": discord.utils.utcnow().isoformat()
        }
        
        success = await self.honeypot_service.report_suspicious_activity(address, activity_data)
        
        if success:
            embed = discord.Embed(
                title="✅ Activity Reported",
                description=f"Successfully reported suspicious activity for `{address}`.",
                color=discord.Color.green()
            )
            embed.add_field(name="Activity", value=activity, inline=False)
            embed.add_field(name="Reported by", value=interaction.user.name, inline=True)
        else:
            embed = discord.Embed(
                title="❌ Report Failed",
                description=f"Failed to report activity for `{address}`. Address may not be monitored.",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the bot is ready."""
        logger.info("Honeypot commands cog loaded")


async def setup(bot):
    """Setup function for the cog."""
    await bot.add_cog(HoneypotCommands(bot))
