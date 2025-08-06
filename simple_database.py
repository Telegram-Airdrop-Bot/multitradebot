#!/usr/bin/env python3
"""
Simple Database for Pionex Trading Bot
Copyright © 2024 Telegram-Airdrop-Bot
https://github.com/Telegram-Airdrop-Bot/autotradebot

A lightweight, file-based database that doesn't require SQLite.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class SimpleDatabase:
    """Simple file-based database using JSON files"""
    
    def __init__(self, data_dir='data'):
        """Initialize database"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize data files
        self.files = {
            'trades': self.data_dir / 'trades.json',
            'settings': self.data_dir / 'settings.json',
            'portfolio': self.data_dir / 'portfolio.json',
            'logs': self.data_dir / 'logs.json',
            'users': self.data_dir / 'users.json'
        }
        
        # Initialize files
        self._init_files()
        logger.info(f"SimpleDatabase initialized in {self.data_dir}")
    
    def _init_files(self):
        """Initialize all database files"""
        default_data = {
            'trades': [],
            'settings': {},
            'portfolio': {},
            'logs': [],
            'users': {}
        }
        
        for name, file_path in self.files.items():
            if not file_path.exists():
                self._write_json(file_path, default_data[name])
                logger.info(f"Created {file_path}")
    
    def _read_json(self, file_path: Path) -> Any:
        """Read JSON data from file"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None
    
    def _write_json(self, file_path: Path, data: Any) -> bool:
        """Write JSON data to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Error writing {file_path}: {e}")
            return False
    
    # Trade operations
    def add_trade(self, trade_data: Dict[str, Any]) -> bool:
        """Add a new trade"""
        try:
            trades = self._read_json(self.files['trades']) or []
            
            # Add timestamp if not present
            if 'timestamp' not in trade_data:
                trade_data['timestamp'] = datetime.now().isoformat()
            
            trades.append(trade_data)
            
            # Keep only last 1000 trades
            if len(trades) > 1000:
                trades = trades[-1000:]
            
            return self._write_json(self.files['trades'], trades)
        except Exception as e:
            logger.error(f"Error adding trade: {e}")
            return False
    
    def get_recent_trades(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent trades"""
        try:
            trades = self._read_json(self.files['trades']) or []
            return trades[-limit:] if trades else []
        except Exception as e:
            logger.error(f"Error getting recent trades: {e}")
            return []
    
    def get_trades_by_symbol(self, symbol: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get trades for a specific symbol"""
        try:
            trades = self._read_json(self.files['trades']) or []
            symbol_trades = [trade for trade in trades if trade.get('symbol') == symbol]
            return symbol_trades[-limit:] if symbol_trades else []
        except Exception as e:
            logger.error(f"Error getting trades for {symbol}: {e}")
            return []
    
    # User settings operations
    def save_user_setting(self, user_id: str, key: str, value: Any) -> bool:
        """Save user setting"""
        try:
            settings = self._read_json(self.files['settings']) or {}
            
            if user_id not in settings:
                settings[user_id] = {}
            
            settings[user_id][key] = value
            
            return self._write_json(self.files['settings'], settings)
        except Exception as e:
            logger.error(f"Error saving user setting: {e}")
            return False
    
    def get_user_settings(self, user_id: str) -> Dict[str, Any]:
        """Get all settings for a user"""
        try:
            settings = self._read_json(self.files['settings']) or {}
            return settings.get(user_id, {})
        except Exception as e:
            logger.error(f"Error getting user settings: {e}")
            return {}
    
    def update_user_setting(self, user_id: str, key: str, value: Any) -> bool:
        """Update user setting"""
        return self.save_user_setting(user_id, key, value)
    
    # Portfolio operations
    def save_portfolio_snapshot(self, portfolio_data: Dict[str, Any]) -> bool:
        """Save portfolio snapshot"""
        try:
            portfolio = self._read_json(self.files['portfolio']) or {}
            
            # Add timestamp
            portfolio_data['timestamp'] = datetime.now().isoformat()
            
            # Keep only last 100 snapshots
            snapshots = portfolio.get('snapshots', [])
            snapshots.append(portfolio_data)
            
            if len(snapshots) > 100:
                snapshots = snapshots[-100:]
            
            portfolio['snapshots'] = snapshots
            portfolio['last_updated'] = datetime.now().isoformat()
            
            return self._write_json(self.files['portfolio'], portfolio)
        except Exception as e:
            logger.error(f"Error saving portfolio snapshot: {e}")
            return False
    
    def get_portfolio_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get portfolio history"""
        try:
            portfolio = self._read_json(self.files['portfolio']) or {}
            snapshots = portfolio.get('snapshots', [])
            return snapshots[-limit:] if snapshots else []
        except Exception as e:
            logger.error(f"Error getting portfolio history: {e}")
            return []
    
    # Log operations
    def add_log(self, log_data: Dict[str, Any]) -> bool:
        """Add log entry"""
        try:
            logs = self._read_json(self.files['logs']) or []
            
            # Add timestamp if not present
            if 'timestamp' not in log_data:
                log_data['timestamp'] = datetime.now().isoformat()
            
            logs.append(log_data)
            
            # Keep only last 1000 logs
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            return self._write_json(self.files['logs'], logs)
        except Exception as e:
            logger.error(f"Error adding log: {e}")
            return False
    
    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent logs"""
        try:
            logs = self._read_json(self.files['logs']) or []
            return logs[-limit:] if logs else []
        except Exception as e:
            logger.error(f"Error getting recent logs: {e}")
            return []
    
    # User operations
    def create_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """Create a new user"""
        try:
            users = self._read_json(self.files['users']) or {}
            
            user_data['created_at'] = datetime.now().isoformat()
            user_data['updated_at'] = datetime.now().isoformat()
            
            users[user_id] = user_data
            
            return self._write_json(self.files['users'], users)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data"""
        try:
            users = self._read_json(self.files['users']) or {}
            return users.get(user_id)
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """Update user data"""
        try:
            users = self._read_json(self.files['users']) or {}
            
            if user_id in users:
                users[user_id].update(user_data)
                users[user_id]['updated_at'] = datetime.now().isoformat()
                
                return self._write_json(self.files['users'], users)
            return False
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False
    
    # Utility operations
    def clear_old_data(self, days: int = 30) -> bool:
        """Clear old data"""
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            # Clear old trades
            trades = self._read_json(self.files['trades']) or []
            trades = [trade for trade in trades if self._parse_timestamp(trade.get('timestamp', 0)) > cutoff_date]
            self._write_json(self.files['trades'], trades)
            
            # Clear old logs
            logs = self._read_json(self.files['logs']) or []
            logs = [log for log in logs if self._parse_timestamp(log.get('timestamp', 0)) > cutoff_date]
            self._write_json(self.files['logs'], logs)
            
            logger.info(f"Cleared data older than {days} days")
            return True
        except Exception as e:
            logger.error(f"Error clearing old data: {e}")
            return False
    
    def _parse_timestamp(self, timestamp: Any) -> float:
        """Parse timestamp to unix timestamp"""
        try:
            if isinstance(timestamp, (int, float)):
                return timestamp
            elif isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                return dt.timestamp()
            else:
                return 0
        except Exception:
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {
                'trades_count': len(self._read_json(self.files['trades']) or []),
                'settings_count': len(self._read_json(self.files['settings']) or {}),
                'portfolio_snapshots': len(self._read_json(self.files['portfolio']) or {}),
                'logs_count': len(self._read_json(self.files['logs']) or []),
                'users_count': len(self._read_json(self.files['users']) or {}),
                'data_directory': str(self.data_dir),
                'last_updated': datetime.now().isoformat()
            }
            return stats
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
    
    def backup(self, backup_dir: str = 'backup') -> bool:
        """Create backup of database files"""
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            for name, file_path in self.files.items():
                if file_path.exists():
                    backup_file = backup_path / f"{name}_{timestamp}.json"
                    with open(file_path, 'r', encoding='utf-8') as src:
                        with open(backup_file, 'w', encoding='utf-8') as dst:
                            dst.write(src.read())
            
            logger.info(f"Backup created in {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False 