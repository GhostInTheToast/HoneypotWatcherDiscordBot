"""
Service for sending notifications to Discord channels.
"""
from datetime import datetime
from typing import Dict

from discord import Color, Embed

from services.base_service import BaseService
from utils.logger import logger


class NotificationService(BaseService):
    """Service for sending notifications to Discord channels."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.notification_channels: Dict[str, int] = {}  # channel_name -> channel_id
        self.alert_roles: Dict[str, int] = {}  # role_name -> role_id
    
    async def _on_initialize(self) -> None:
        """Initialize the notification service."""
        logger.info("Initializing NotificationService...")
        # Load notification channels and roles from config
        # This is where you'd load persistent configuration
        pass
    
    async def _on_start(self) -> None:
        """Start the notification service."""
        logger.info("Starting notification service...")
        # Initialize any required resources
        pass
    
    async def _on_stop(self) -> None:
        """Stop the notification service."""
        logger.info("Stopping notification service...")
        # Clean up resources
        pass
    
    async def send_alert(self, title: str, description: str, severity: str = "warning", 
                        channel_name: str = "alerts", **kwargs) -> bool:
        """Send an alert notification."""
        try:
            channel_id = self.notification_channels.get(channel_name)
            if not channel_id:
                logger.error(f"Notification channel '{channel_name}' not configured")
                return False
            
            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.error(f"Could not find channel with ID {channel_id}")
                return False
            
            # Create embed
            embed = self._create_alert_embed(title, description, severity, **kwargs)
            
            # Add role mention if specified
            content = ""
            if "role" in kwargs:
                role_id = self.alert_roles.get(kwargs["role"])
                if role_id:
                    content = f"<@&{role_id}>"
            
            await channel.send(content=content, embed=embed)
            logger.info(f"Sent alert notification to {channel_name}: {title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send alert notification: {e}")
            return False
    
    async def send_info(self, title: str, description: str, channel_name: str = "general", **kwargs) -> bool:
        """Send an info notification."""
        try:
            channel_id = self.notification_channels.get(channel_name)
            if not channel_id:
                logger.error(f"Notification channel '{channel_name}' not configured")
                return False
            
            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.error(f"Could not find channel with ID {channel_id}")
                return False
            
            # Create embed
            embed = self._create_info_embed(title, description, **kwargs)
            
            await channel.send(embed=embed)
            logger.info(f"Sent info notification to {channel_name}: {title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send info notification: {e}")
            return False
    
    def _create_alert_embed(self, title: str, description: str, severity: str = "warning", **kwargs) -> Embed:
        """Create an alert embed."""
        color_map = {
            "info": Color.blue(),
            "warning": Color.yellow(),
            "error": Color.red(),
            "critical": Color.dark_red()
        }
        
        embed = Embed(
            title=f"🚨 {title}",
            description=description,
            color=color_map.get(severity, Color.yellow()),
            timestamp=datetime.utcnow()
        )
        
        # Add fields if provided
        if "fields" in kwargs:
            for field in kwargs["fields"]:
                embed.add_field(
                    name=field.get("name", ""),
                    value=field.get("value", ""),
                    inline=field.get("inline", False)
                )
        
        # Add footer
        embed.set_footer(text="HoneypotWatcher Bot")
        
        return embed
    
    def _create_info_embed(self, title: str, description: str, **kwargs) -> Embed:
        """Create an info embed."""
        embed = Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Add fields if provided
        if "fields" in kwargs:
            for field in kwargs["fields"]:
                embed.add_field(
                    name=field.get("name", ""),
                    value=field.get("value", ""),
                    inline=field.get("inline", False)
                )
        
        # Add footer
        embed.set_footer(text="HoneypotWatcher Bot")
        
        return embed
    
    async def add_notification_channel(self, name: str, channel_id: int) -> bool:
        """Add a notification channel."""
        try:
            self.notification_channels[name] = channel_id
            logger.info(f"Added notification channel: {name} -> {channel_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add notification channel: {e}")
            return False
    
    async def add_alert_role(self, name: str, role_id: int) -> bool:
        """Add an alert role."""
        try:
            self.alert_roles[name] = role_id
            logger.info(f"Added alert role: {name} -> {role_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add alert role: {e}")
            return False
    
    async def get_notification_channels(self) -> Dict[str, int]:
        """Get all notification channels."""
        return self.notification_channels.copy()
    
    async def get_alert_roles(self) -> Dict[str, int]:
        """Get all alert roles."""
        return self.alert_roles.copy()
