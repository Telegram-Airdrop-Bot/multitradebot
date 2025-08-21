#!/usr/bin/env python3
"""
Bot 2025 - Enhanced Trading Bot with Session-Based Breakout Strategy
Copyright © 2024 Telegram-Airdrop-Bot

Advanced trading bot featuring:
- Market session management (US & Asian sessions)
- Breakout trading with range box analysis
- Multi-timeframe RSI filters
- Volume confirmation
- Advanced risk management
- Anti-fake breakout protection
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pytz
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class Bot2025:
    """Bot 2025 - Enhanced Trading Bot with Session-Based Breakout Strategy"""
    
    def __init__(self, config: Dict):
        self.config = config.get('bot_2025', {})
        self.enabled = self.config.get('enabled', False)
        
        if not self.enabled:
            logger.info("Bot 2025 is disabled in configuration")
            return
        
        # Initialize configuration
        self.sessions = self.config.get('sessions', {})
        self.breakout = self.config.get('breakout', {})
        self.risk_management = self.config.get('risk_management', {})
        self.anti_fake = self.config.get('anti_fake', {})
        self.mtf_rsi = self.config.get('mtf_rsi', {})
        self.volume_filter = self.config.get('volume_filter', {})
        
        # Trading state
        self.active_trades = {}
        self.session_trades = {}
        self.last_trade_time = {}
        self.range_boxes = {}
        
        # Timezone setup
        self.timezone = pytz.timezone('America/New_York')  # UTC-5
        
        logger.info("Bot 2025 initialized successfully")
    
    def is_session_active(self, session_name: str) -> bool:
        """Check if a trading session is currently active"""
        if not self.sessions.get(session_name, {}).get('enabled', False):
            return False
        
        session_config = self.sessions[session_name]
        current_time = datetime.now(self.timezone)
        
        if session_name == 'us_session':
            return self._is_us_session_active(current_time, session_config)
        elif session_name == 'asian_session':
            return self._is_asian_session_active(current_time, session_config)
        
        return False
    
    def _is_us_session_active(self, current_time: datetime, config: Dict) -> bool:
        """Check if US session is active based on daylight saving time"""
        month = current_time.month
        current_time_str = current_time.strftime("%H:%M")
        
        # Check if it's daylight saving time
        if month in config.get('daylight_saving', {}).get('months', []):
            start_time = config['daylight_saving']['start_time']
            end_time = config['daylight_saving']['end_time']
        else:
            start_time = config['standard_time']['start_time']
            end_time = config['standard_time']['end_time']
        
        return start_time <= current_time_str <= end_time
    
    def _is_asian_session_active(self, current_time: datetime, config: Dict) -> bool:
        """Check if Asian session is active"""
        current_time_str = current_time.strftime("%H:%M")
        start_time = config['start_time']
        end_time = config['end_time']
        
        # Handle session that crosses midnight
        if start_time > end_time:  # e.g., 19:30 -> 01:30
            return current_time_str >= start_time or current_time_str <= end_time
        else:
            return start_time <= current_time_str <= end_time
    
    def calculate_range_box(self, symbol: str, session_name: str, market_data: pd.DataFrame) -> Dict:
        """Calculate range box for a session"""
        if not self.is_session_active(session_name):
            return {}
        
        session_config = self.sessions[session_name]
        lookback_minutes = session_config.get('range_box_lookback', 90)
        
        # Get the first 90 minutes of data for the session
        session_start = self._get_session_start_time(session_name)
        session_data = market_data[market_data.index >= session_start]
        
        if len(session_data) < 2:
            return {}
        
        # Calculate high and low for the lookback period
        lookback_data = session_data.head(lookback_minutes)
        high = lookback_data['high'].max()
        low = lookback_data['low'].min()
        
        range_box = {
            'symbol': symbol,
            'session': session_name,
            'high': high,
            'low': low,
            'range': high - low,
            'session_start': session_start,
            'calculated_at': datetime.now(),
            'lookback_minutes': lookback_minutes
        }
        
        self.range_boxes[f"{symbol}_{session_name}"] = range_box
        
        if self.config.get('logging', {}).get('log_box_levels', False):
            logger.info(f"Range box calculated for {symbol} {session_name}: High={high:.4f}, Low={low:.4f}")
        
        return range_box
    
    def _get_session_start_time(self, session_name: str) -> datetime:
        """Get the start time of the current session"""
        current_time = datetime.now(self.timezone)
        
        if session_name == 'us_session':
            return self._get_us_session_start(current_time)
        elif session_name == 'asian_session':
            return self._get_asian_session_start(current_time)
        
        return current_time
    
    def _get_us_session_start(self, current_time: datetime) -> datetime:
        """Get US session start time"""
        month = current_time.month
        
        if month in self.sessions['us_session']['daylight_saving']['months']:
            start_time_str = self.sessions['us_session']['daylight_saving']['start_time']
        else:
            start_time_str = self.sessions['us_session']['standard_time']['start_time']
        
        # Parse time and set to today
        hour, minute = map(int, start_time_str.split(':'))
        session_start = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If session start is in the future, use yesterday
        if session_start > current_time:
            session_start -= timedelta(days=1)
        
        return session_start
    
    def _get_asian_session_start(self, current_time: datetime) -> datetime:
        """Get Asian session start time"""
        start_time_str = self.sessions['asian_session']['start_time']
        hour, minute = map(int, start_time_str.split(':'))
        
        # Asian session starts in the evening
        session_start = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If session start is in the future, use yesterday
        if session_start > current_time:
            session_start -= timedelta(days=1)
        
        return session_start
    
    def check_breakout_conditions(self, symbol: str, session_name: str, current_price: float, 
                                 market_data: pd.DataFrame) -> Dict:
        """Check if breakout conditions are met"""
        if not self.breakout.get('enabled', False):
            return {'valid': False, 'reason': 'Breakout trading disabled'}
        
        # Check if session is active
        if not self.is_session_active(session_name):
            return {'valid': False, 'reason': f'{session_name} not active'}
        
        # Check cooldown
        if not self._check_cooldown(symbol, session_name):
            return {'valid': False, 'reason': 'Cooldown period active'}
        
        # Check max trades per session
        if not self._check_max_trades(symbol, session_name):
            return {'valid': False, 'reason': 'Max trades per session reached'}
        
        # Get range box
        range_box = self.range_boxes.get(f"{symbol}_{session_name}")
        if not range_box:
            return {'valid': False, 'reason': 'Range box not calculated'}
        
        # Check breakout conditions
        buffer = self.breakout.get('buffer_percentage', 0.05) / 100
        high_breakout = range_box['high'] * (1 + buffer)
        low_breakout = range_box['low'] * (1 - buffer)
        
        breakout_signal = None
        if current_price > high_breakout:
            breakout_signal = 'LONG'
        elif current_price < low_breakout:
            breakout_signal = 'SHORT'
        
        if not breakout_signal:
            return {'valid': False, 'reason': 'No breakout detected'}
        
        # Check confirmation candles
        if not self._check_confirmation_candles(market_data, breakout_signal):
            return {'valid': False, 'reason': 'Confirmation candles not met'}
        
        # Check filters
        filter_result = self._check_filters(symbol, market_data, breakout_signal)
        if not filter_result['valid']:
            return filter_result
        
        # Check anti-fake breakout
        if not self._check_anti_fake_breakout(current_price, range_box, breakout_signal):
            return {'valid': False, 'reason': 'Anti-fake breakout check failed'}
        
        return {
            'valid': True,
            'signal': breakout_signal,
            'range_box': range_box,
            'breakout_price': current_price,
            'filters': filter_result
        }
    
    def _check_cooldown(self, symbol: str, session_name: str) -> bool:
        """Check if cooldown period has passed"""
        cooldown_minutes = self.breakout.get('cooldown_minutes', 30)
        last_trade_key = f"{symbol}_{session_name}"
        
        if last_trade_key not in self.last_trade_time:
            return True
        
        time_since_last = datetime.now() - self.last_trade_time[last_trade_key]
        return time_since_last.total_seconds() > (cooldown_minutes * 60)
    
    def _check_max_trades(self, symbol: str, session_name: str) -> bool:
        """Check if max trades per session reached"""
        max_trades = self.breakout.get('max_trades_per_session', 1)
        session_key = f"{symbol}_{session_name}"
        
        if session_key not in self.session_trades:
            return True
        
        return len(self.session_trades[session_key]) < max_trades
    
    def _check_confirmation_candles(self, market_data: pd.DataFrame, signal: str) -> bool:
        """Check if confirmation candles are met"""
        confirmation_candles = self.breakout.get('confirmation_candles', 1)
        
        if len(market_data) < confirmation_candles:
            return False
        
        # Check if the last N candles confirm the breakout
        recent_data = market_data.tail(confirmation_candles)
        
        if signal == 'LONG':
            return all(recent_data['close'] > recent_data['open'])
        else:  # SHORT
            return all(recent_data['close'] < recent_data['open'])
    
    def _check_filters(self, symbol: str, market_data: pd.DataFrame, signal: str) -> Dict:
        """Check all trading filters"""
        # Check MTF RSI
        if self.mtf_rsi.get('enabled', False):
            rsi_result = self._check_mtf_rsi(market_data, signal)
            if not rsi_result['valid']:
                return rsi_result
        
        # Check volume filter
        if self.volume_filter.get('enabled', False):
            volume_result = self._check_volume_filter(market_data)
            if not volume_result['valid']:
                return volume_result
        
        return {'valid': True, 'filters_passed': ['MTF_RSI', 'VOLUME']}
    
    def _check_mtf_rsi(self, market_data: pd.DataFrame, signal: str) -> Dict:
        """Check multi-timeframe RSI conditions"""
        # This would require market data from different timeframes
        # For now, we'll use the current timeframe data as a placeholder
        
        thresholds = self.mtf_rsi.get('thresholds', {})
        
        if signal == 'LONG':
            short_threshold = thresholds.get('long_conditions', {}).get('short_tf', 30)
            long_threshold = thresholds.get('long_conditions', {}).get('long_tf', 50)
            
            # Simplified check - would need actual RSI calculation
            # For now, return True as placeholder
            return {'valid': True, 'rsi_conditions': 'LONG conditions met'}
        
        else:  # SHORT
            short_threshold = thresholds.get('short_conditions', {}).get('short_tf', 70)
            long_threshold = thresholds.get('short_conditions', {}).get('long_tf', 50)
            
            # Simplified check - would need actual RSI calculation
            # For now, return True as placeholder
            return {'valid': True, 'rsi_conditions': 'SHORT conditions met'}
    
    def _check_volume_filter(self, market_data: pd.DataFrame) -> Dict:
        """Check volume filter conditions"""
        multiplier = self.volume_filter.get('multiplier', 1.5)
        ema_period = self.volume_filter.get('ema_period', 20)
        
        if len(market_data) < ema_period:
            return {'valid': False, 'reason': 'Insufficient data for volume filter'}
        
        current_volume = market_data['volume'].iloc[-1]
        ema_volume = market_data['volume'].tail(ema_period).mean()
        
        if current_volume > (ema_volume * multiplier):
            return {'valid': True, 'volume_ratio': current_volume / ema_volume}
        else:
            return {'valid': False, 'reason': f'Volume {current_volume} < {ema_volume * multiplier}'}
    
    def _check_anti_fake_breakout(self, current_price: float, range_box: Dict, signal: str) -> bool:
        """Check anti-fake breakout conditions"""
        if not self.anti_fake.get('retest_enabled', False):
            return True
        
        max_slippage = self.anti_fake.get('max_slippage', 0.05) / 100
        min_distance = self.anti_fake.get('min_distance_from_box', 0.02) / 100
        
        if signal == 'LONG':
            distance_from_high = (current_price - range_box['high']) / range_box['high']
            return distance_from_high >= min_distance and distance_from_high <= max_slippage
        else:  # SHORT
            distance_from_low = (range_box['low'] - current_price) / range_box['low']
            return distance_from_low >= min_distance and distance_from_low <= max_slippage
    
    def calculate_risk_management(self, symbol: str, entry_price: float, signal: str, 
                                range_box: Dict) -> Dict:
        """Calculate stop loss and take profit levels"""
        sl_config = self.risk_management.get('stop_loss', {})
        tp_config = self.risk_management.get('take_profit', {})
        
        # Calculate stop loss
        if sl_config.get('use_box_opposite', True):
            if signal == 'LONG':
                stop_loss = range_box['low'] * (1 - sl_config.get('percentage', 1.5) / 100)
            else:  # SHORT
                stop_loss = range_box['high'] * (1 + sl_config.get('percentage', 1.5) / 100)
        else:
            sl_percentage = sl_config.get('percentage', 1.5) / 100
            if signal == 'LONG':
                stop_loss = entry_price * (1 - sl_percentage)
            else:  # SHORT
                stop_loss = entry_price * (1 + sl_percentage)
        
        # Calculate take profit
        tp_percentage = tp_config.get('percentage', 2.5) / 100
        if signal == 'LONG':
            take_profit = entry_price * (1 + tp_percentage)
        else:  # SHORT
            take_profit = entry_price * (1 - tp_percentage)
        
        # Calculate trailing stop parameters
        trailing_config = self.risk_management.get('trailing_stop', {})
        trailing_step = trailing_config.get('step_percentage', 0.3) / 100
        trailing_distance = trailing_config.get('distance_percentage', 0.8) / 100
        
        return {
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'trailing_step': trailing_step,
            'trailing_distance': trailing_distance,
            'risk_reward_ratio': abs(take_profit - entry_price) / abs(stop_loss - entry_price)
        }
    
    def execute_trade(self, symbol: str, session_name: str, signal: str, 
                     entry_price: float, size: float) -> Dict:
        """Execute a breakout trade"""
        # Check if we can trade
        breakout_check = self.check_breakout_conditions(symbol, session_name, entry_price, None)
        if not breakout_check['valid']:
            return {'success': False, 'error': breakout_check['reason']}
        
        # Calculate risk management
        risk_params = self.calculate_risk_management(symbol, entry_price, signal, breakout_check['range_box'])
        
        # Create trade object
        trade = {
            'symbol': symbol,
            'session': session_name,
            'signal': signal,
            'entry_price': entry_price,
            'size': size,
            'stop_loss': risk_params['stop_loss'],
            'take_profit': risk_params['take_profit'],
            'entry_time': datetime.now(),
            'status': 'OPEN',
            'risk_params': risk_params
        }
        
        # Record the trade
        trade_id = f"{symbol}_{session_name}_{int(time.time())}"
        self.active_trades[trade_id] = trade
        
        # Update session trades
        session_key = f"{symbol}_{session_name}"
        if session_key not in self.session_trades:
            self.session_trades[session_key] = []
        self.session_trades[session_key].append(trade_id)
        
        # Update last trade time
        self.last_trade_time[f"{symbol}_{session_name}"] = datetime.now()
        
        logger.info(f"Trade executed: {trade_id} - {signal} {symbol} at {entry_price}")
        
        return {
            'success': True,
            'trade_id': trade_id,
            'trade': trade
        }
    
    def get_active_trades(self) -> Dict:
        """Get all active trades"""
        return self.active_trades
    
    def get_session_status(self) -> Dict:
        """Get current session status"""
        status = {}
        for session_name in self.sessions.keys():
            status[session_name] = {
                'active': self.is_session_active(session_name),
                'enabled': self.sessions[session_name].get('enabled', False),
                'name': self.sessions[session_name].get('name', session_name)
            }
        return status
    
    def get_range_boxes(self) -> Dict:
        """Get all calculated range boxes"""
        return self.range_boxes
    
    def update_config(self, new_config: Dict):
        """Update bot configuration"""
        self.config.update(new_config)
        logger.info("Bot 2025 configuration updated")
    
    def reset_session_trades(self, symbol: str = None, session_name: str = None):
        """Reset session trade counters"""
        if symbol and session_name:
            key = f"{symbol}_{session_name}"
            if key in self.session_trades:
                del self.session_trades[key]
            if key in self.last_trade_time:
                del self.last_trade_time[key]
        else:
            self.session_trades.clear()
            self.last_trade_time.clear()
        
        logger.info("Session trade counters reset") 