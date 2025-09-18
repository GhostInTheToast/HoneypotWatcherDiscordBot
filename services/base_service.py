"""
Base service class for all bot services.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict

from utils.logger import logger


class BaseService(ABC):
    """Base class for all bot services."""
    
    def __init__(self, bot):
        self.bot = bot
        self._initialized = False
        self._running = False
    
    @property
    def initialized(self) -> bool:
        """Check if the service is initialized."""
        return self._initialized
    
    @property
    def running(self) -> bool:
        """Check if the service is running."""
        return self._running
    
    async def initialize(self) -> bool:
        """Initialize the service."""
        try:
            await self._on_initialize()
            self._initialized = True
            logger.info(f"Service {self.__class__.__name__} initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize service {self.__class__.__name__}: {e}")
            return False
    
    async def start(self) -> bool:
        """Start the service."""
        if not self._initialized:
            if not await self.initialize():
                return False
        
        try:
            await self._on_start()
            self._running = True
            logger.info(f"Service {self.__class__.__name__} started")
            return True
        except Exception as e:
            logger.error(f"Failed to start service {self.__class__.__name__}: {e}")
            return False
    
    async def stop(self) -> bool:
        """Stop the service."""
        try:
            await self._on_stop()
            self._running = False
            logger.info(f"Service {self.__class__.__name__} stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop service {self.__class__.__name__}: {e}")
            return False
    
    @abstractmethod
    async def _on_initialize(self) -> None:
        """Called when the service is being initialized."""
        pass
    
    @abstractmethod
    async def _on_start(self) -> None:
        """Called when the service is being started."""
        pass
    
    @abstractmethod
    async def _on_stop(self) -> None:
        """Called when the service is being stopped."""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the service."""
        return {
            "name": self.__class__.__name__,
            "initialized": self._initialized,
            "running": self._running
        }
