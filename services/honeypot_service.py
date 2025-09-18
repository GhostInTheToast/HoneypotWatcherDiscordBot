"""
Service for monitoring honeypot activities.
"""
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from services.base_service import BaseService
from utils.logger import logger


class HoneypotService(BaseService):
    """Service for monitoring and managing honeypot activities."""
    
    def __init__(self, bot):
        super().__init__(bot)
        self.monitored_addresses: Dict[str, Dict[str, Any]] = {}
        self.alert_threshold = 5  # Number of suspicious activities before alert
        self.monitoring_task: Optional[asyncio.Task] = None
    
    async def _on_initialize(self) -> None:
        """Initialize the honeypot service."""
        logger.info("Initializing HoneypotService...")
        # Load monitored addresses from database or config
        # This is where you'd load persistent data
        pass
    
    async def _on_start(self) -> None:
        """Start monitoring honeypot activities."""
        logger.info("Starting honeypot monitoring...")
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
    
    async def _on_stop(self) -> None:
        """Stop monitoring honeypot activities."""
        logger.info("Stopping honeypot monitoring...")
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while True:
            try:
                await self._check_honeypot_activities()
                await asyncio.sleep(30)  # Check every 30 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _check_honeypot_activities(self) -> None:
        """Check for honeypot activities."""
        # This is where you'd implement the actual honeypot monitoring logic
        # For now, this is a placeholder
        logger.debug("Checking honeypot activities...")
        
        # Example: Check each monitored address
        for address, data in self.monitored_addresses.items():
            # Simulate checking for suspicious activity
            suspicious_count = data.get("suspicious_count", 0)
            if suspicious_count >= self.alert_threshold:
                await self._trigger_alert(address, data)
    
    async def _trigger_alert(self, address: str, data: Dict[str, Any]) -> None:
        """Trigger an alert for suspicious activity."""
        logger.warning(f"Alert triggered for address {address}: {data}")
        
        # Reset the suspicious count after alert
        self.monitored_addresses[address]["suspicious_count"] = 0
        self.monitored_addresses[address]["last_alert"] = datetime.now()
    
    async def add_monitored_address(self, address: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add an address to monitor."""
        try:
            self.monitored_addresses[address] = {
                "added_at": datetime.now(),
                "suspicious_count": 0,
                "last_checked": datetime.now(),
                "metadata": metadata or {}
            }
            logger.info(f"Added address to monitoring: {address}")
            return True
        except Exception as e:
            logger.error(f"Failed to add monitored address {address}: {e}")
            return False
    
    async def remove_monitored_address(self, address: str) -> bool:
        """Remove an address from monitoring."""
        try:
            if address in self.monitored_addresses:
                del self.monitored_addresses[address]
                logger.info(f"Removed address from monitoring: {address}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove monitored address {address}: {e}")
            return False
    
    async def get_monitored_addresses(self) -> List[Dict[str, Any]]:
        """Get all monitored addresses."""
        return [
            {
                "address": address,
                **data
            }
            for address, data in self.monitored_addresses.items()
        ]
    
    async def report_suspicious_activity(self, address: str, activity_data: Dict[str, Any]) -> bool:
        """Report suspicious activity for an address."""
        try:
            if address in self.monitored_addresses:
                self.monitored_addresses[address]["suspicious_count"] += 1
                self.monitored_addresses[address]["last_checked"] = datetime.now()
                logger.info(f"Reported suspicious activity for {address}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to report suspicious activity for {address}: {e}")
            return False
