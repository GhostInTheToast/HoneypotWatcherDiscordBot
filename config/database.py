"""
Database configuration and models for the Discord bot.
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from utils.logger import logger


class DatabaseManager:
    """Manages database operations for the bot."""
    
    def __init__(self, db_path: str = "data/bot.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create monitored addresses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monitored_addresses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT UNIQUE NOT NULL,
                    description TEXT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    suspicious_count INTEGER DEFAULT 0,
                    last_checked TIMESTAMP,
                    metadata TEXT,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # Create notification channels table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notification_channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    channel_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # Create alert roles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alert_roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    role_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # Create activity logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    activity_data TEXT,
                    reported_by TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def add_monitored_address(self, address: str, description: str = None, metadata: Dict[str, Any] = None) -> bool:
        """Add a monitored address to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO monitored_addresses 
                    (address, description, metadata, added_at, suspicious_count, last_checked, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    address,
                    description,
                    json.dumps(metadata or {}),
                    datetime.now().isoformat(),
                    0,
                    datetime.now().isoformat(),
                    True
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to add monitored address: {e}")
            return False
    
    def remove_monitored_address(self, address: str) -> bool:
        """Remove a monitored address from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE monitored_addresses SET is_active = 0 WHERE address = ?", (address,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to remove monitored address: {e}")
            return False
    
    def get_monitored_addresses(self) -> List[Dict[str, Any]]:
        """Get all active monitored addresses."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM monitored_addresses 
                    WHERE is_active = 1 
                    ORDER BY added_at DESC
                """)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get monitored addresses: {e}")
            return []
    
    def update_suspicious_count(self, address: str, count: int) -> bool:
        """Update the suspicious count for an address."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE monitored_addresses 
                    SET suspicious_count = ?, last_checked = ?
                    WHERE address = ? AND is_active = 1
                """, (count, datetime.now().isoformat(), address))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to update suspicious count: {e}")
            return False
    
    def log_activity(self, address: str, activity_type: str, activity_data: Dict[str, Any], reported_by: str = None) -> bool:
        """Log an activity for an address."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO activity_logs 
                    (address, activity_type, activity_data, reported_by, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    address,
                    activity_type,
                    json.dumps(activity_data),
                    reported_by,
                    datetime.now().isoformat()
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to log activity: {e}")
            return False
    
    def get_activity_logs(self, address: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get activity logs, optionally filtered by address."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if address:
                    cursor.execute("""
                        SELECT * FROM activity_logs 
                        WHERE address = ? 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    """, (address, limit))
                else:
                    cursor.execute("""
                        SELECT * FROM activity_logs 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    """, (limit,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get activity logs: {e}")
            return []
