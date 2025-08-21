# 🚀 Bybit V5 Futures API - Auto Trading Bot Implementation Guide

## 📋 Overview

This guide provides a complete implementation for Bybit V5 Futures API auto trading bot with proper parameters and trading flow based on the [official Bybit V5 API documentation](https://bybit-exchange.github.io/docs/v5/intro).

## 🔧 **V5 API Endpoints with Correct Parameters**

### **1. Place Futures Order**
```python
POST /v5/order/create

# Required Parameters
{
  "category": "linear",           # Market type: "linear" (USDT Perpetual)
  "symbol": "BTCUSDT",           # Trading pair
  "side": "Buy",                 # "Buy" or "Sell" (V5 uses title case)
  "orderType": "Limit",          # "Limit" or "Market"
  "qty": "0.01",                # Order size (contracts)
  "price": "60000",             # Required for Limit orders
  "timeInForce": "GTC",         # "GTC", "IOC", "FOK"
  "reduceOnly": false,          # true/false (closing positions)
  "closeOnTrigger": false       # true/false (stop-loss/TP orders)
}
```

### **2. Cancel Order**
```python
POST /v5/order/cancel

# Parameters
{
  "category": "linear",
  "symbol": "BTCUSDT",
  "orderId": "f8a1a8d7-xxxx-xxxx"
}
```

### **3. Get Position Info**
```python
GET /v5/position/list

# Parameters
category: "linear"
symbol: "BTCUSDT"

# URL Example
GET https://api.bybit.com/v5/position/list?category=linear&symbol=BTCUSDT
```

### **4. Market Data - Klines**
```python
GET /v5/market/kline

# Parameters
category: "linear"
symbol: "BTCUSDT"
interval: "1" (1min), "5", "15", "60", "D" (day)
start: 1670601600000 (ms timestamp)
end: 1670688000000 (optional)
limit: 200 (max rows)

# URL Example
GET https://api.bybit.com/v5/market/kline?category=linear&symbol=BTCUSDT&interval=5&limit=100
```

### **5. WebSocket Real-time Orders**
```python
# Connect to
wss://stream.bybit.com/v5/private

# Send subscription
{
  "op": "subscribe",
  "args": ["order", "position"]
}
```

## 🚀 **Auto Trading Bot Flow**

### **Step 1: Market Data Collection**
```python
def collect_market_data(symbols: List[str]):
    """Collect real-time market data for trading decisions"""
    market_data = {}
    
    for symbol in symbols:
        # Get ticker data
        ticker = api.get_futures_ticker(symbol)
        
        # Get klines for technical analysis
        klines = api.get_futures_klines(symbol, '5', 100)
        
        # Get order book
        orderbook = api.get_futures_orderbook(symbol, 25)
        
        market_data[symbol] = {
            'ticker': ticker,
            'klines': klines,
            'orderbook': orderbook
        }
    
    return market_data
```

### **Step 2: Trading Signal Generation**
```python
def generate_trading_signals(market_data: Dict) -> List[TradingSignal]:
    """Generate trading signals based on technical analysis"""
    signals = []
    
    for symbol, data in market_data.items():
        # RSI Strategy
        if rsi_oversold(data['klines']):
            signals.append(TradingSignal(
                symbol=symbol,
                side="Buy",
                order_type="Market",
                quantity=calculate_position_size(symbol),
                stop_loss=calculate_stop_loss(symbol, "Buy"),
                take_profit=calculate_take_profit(symbol, "Buy"),
                leverage=10,
                strategy="RSI_OVERSOLD"
            ))
        
        # EMA Crossover Strategy
        if ema_bullish_crossover(data['klines']):
            signals.append(TradingSignal(
                symbol=symbol,
                side="Buy",
                order_type="Market",
                quantity=calculate_position_size(symbol),
                stop_loss=calculate_stop_loss(symbol, "Buy"),
                take_profit=calculate_take_profit(symbol, "Buy"),
                leverage=10,
                strategy="EMA_CROSSOVER"
            ))
    
    return signals
```

### **Step 3: Order Execution**
```python
def execute_trading_signal(signal: TradingSignal):
    """Execute a trading signal with proper V5 API parameters"""
    
    # Set leverage first
    leverage_result = api.set_futures_leverage(
        symbol=signal.symbol,
        leverage=signal.leverage
    )
    
    if not leverage_result.get('success'):
        logger.error(f"Failed to set leverage: {leverage_result}")
        return
    
    # Place the order
    order_params = {
        'category': 'linear',
        'symbol': signal.symbol,
        'side': signal.side,           # "Buy" or "Sell"
        'orderType': signal.order_type, # "Limit" or "Market"
        'qty': str(signal.quantity),
        'timeInForce': 'GTC',
        'reduceOnly': False,
        'closeOnTrigger': False
    }
    
    # Add price for limit orders
    if signal.order_type == "Limit" and signal.price:
        order_params['price'] = str(signal.price)
    
    # Add stop loss and take profit
    if signal.stop_loss:
        order_params['stopLoss'] = str(signal.stop_loss)
    
    if signal.take_profit:
        order_params['takeProfit'] = str(signal.take_profit)
    
    # Execute order
    order_result = api.place_futures_order(**order_params)
    
    if order_result.get('success'):
        logger.info(f"Order placed successfully: {order_result}")
        return order_result
    else:
        logger.error(f"Failed to place order: {order_result}")
        return None
```

### **Step 4: Position Management**
```python
def manage_positions():
    """Manage existing positions with stop-loss and take-profit"""
    
    # Get current positions
    positions = api.get_futures_positions()
    
    if not positions.get('success'):
        return
    
    for position in positions['data']['list']:
        symbol = position['symbol']
        size = float(position['size'])
        
        if size > 0:  # Open position
            # Check stop loss
            if check_stop_loss_triggered(position):
                close_position(symbol, position['side'], size)
            
            # Check take profit
            elif check_take_profit_triggered(position):
                close_position(symbol, position['side'], size)
            
            # Check trailing stop
            elif check_trailing_stop(position):
                update_trailing_stop(position)

def close_position(symbol: str, side: str, size: float):
    """Close a futures position"""
    
    close_params = {
        'category': 'linear',
        'symbol': symbol,
        'side': 'Sell' if side == 'Buy' else 'Buy',
        'orderType': 'Market',
        'qty': str(size),
        'reduceOnly': True,      # Important: This closes the position
        'timeInForce': 'GTC'
    }
    
    result = api.place_futures_order(**close_params)
    
    if result.get('success'):
        logger.info(f"Position closed: {symbol}")
    else:
        logger.error(f"Failed to close position: {result}")
```

### **Step 5: Real-time Monitoring (WebSocket)**
```python
import websocket
import json

class BybitWebSocket:
    def __init__(self, api_key: str, api_secret: str):
        self.ws = None
        self.api_key = api_key
        self.api_secret = api_secret
        
    def connect_private_stream(self):
        """Connect to private WebSocket stream"""
        self.ws = websocket.WebSocketApp(
            "wss://stream.bybit.com/v5/private",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        self.ws.run_forever()
    
    def on_open(self, ws):
        """WebSocket connection opened"""
        logger.info("WebSocket connected")
        
        # Subscribe to order and position updates
        subscribe_message = {
            "op": "subscribe",
            "args": ["order", "position"]
        }
        
        ws.send(json.dumps(subscribe_message))
    
    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            if 'topic' in data:
                topic = data['topic']
                
                if topic == 'order':
                    self.handle_order_update(data['data'])
                elif topic == 'position':
                    self.handle_position_update(data['data'])
                    
        except Exception as e:
            logger.error(f"Error processing WebSocket message: {e}")
    
    def handle_order_update(self, order_data):
        """Handle order updates (filled, cancelled, etc.)"""
        order_id = order_data.get('orderId')
        status = order_data.get('orderStatus')
        symbol = order_data.get('symbol')
        
        logger.info(f"Order {order_id} ({symbol}) status: {status}")
        
        if status == 'Filled':
            # Order executed successfully
            self.on_order_filled(order_data)
        elif status == 'Cancelled':
            # Order was cancelled
            self.on_order_cancelled(order_data)
    
    def handle_position_update(self, position_data):
        """Handle position updates"""
        symbol = position_data.get('symbol')
        size = float(position_data.get('size', 0))
        unrealized_pnl = float(position_data.get('unrealizedPnl', 0))
        
        logger.info(f"Position update {symbol}: size={size}, PnL={unrealized_pnl}")
        
        # Update local position tracking
        self.update_local_position(position_data)
```

## 📊 **Technical Analysis Implementation**

### **RSI Strategy**
```python
def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Calculate RSI indicator"""
    if len(prices) < period + 1:
        return 50.0
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def rsi_oversold(klines_data: List, period: int = 14, threshold: int = 30) -> bool:
    """Check if RSI indicates oversold condition"""
    prices = extract_close_prices(klines_data)
    rsi = calculate_rsi(prices, period)
    return rsi < threshold

def rsi_overbought(klines_data: List, period: int = 14, threshold: int = 70) -> bool:
    """Check if RSI indicates overbought condition"""
    prices = extract_close_prices(klines_data)
    rsi = calculate_rsi(prices, period)
    return rsi > threshold
```

### **EMA Crossover Strategy**
```python
def calculate_ema(prices: List[float], period: int) -> List[float]:
    """Calculate Exponential Moving Average"""
    if len(prices) < period:
        return []
    
    ema_values = []
    multiplier = 2 / (period + 1)
    
    # First EMA is SMA
    sma = sum(prices[:period]) / period
    ema_values.append(sma)
    
    # Calculate subsequent EMAs
    for i in range(period, len(prices)):
        ema = (prices[i] * multiplier) + (ema_values[-1] * (1 - multiplier))
        ema_values.append(ema)
    
    return ema_values

def ema_bullish_crossover(klines_data: List, fast_period: int = 12, slow_period: int = 26) -> bool:
    """Check for bullish EMA crossover"""
    prices = extract_close_prices(klines_data)
    
    if len(prices) < slow_period + 1:
        return False
    
    ema_fast = calculate_ema(prices, fast_period)
    ema_slow = calculate_ema(prices, slow_period)
    
    if len(ema_fast) < 2 or len(ema_slow) < 2:
        return False
    
    # Check for crossover
    current_fast = ema_fast[-1]
    current_slow = ema_slow[-1]
    prev_fast = ema_fast[-2]
    prev_slow = ema_slow[-2]
    
    # Bullish crossover: fast EMA crosses above slow EMA
    return prev_fast <= prev_slow and current_fast > current_slow

def ema_bearish_crossover(klines_data: List, fast_period: int = 12, slow_period: int = 26) -> bool:
    """Check for bearish EMA crossover"""
    prices = extract_close_prices(klines_data)
    
    if len(prices) < slow_period + 1:
        return False
    
    ema_fast = calculate_ema(prices, fast_period)
    ema_slow = calculate_ema(prices, slow_period)
    
    if len(ema_fast) < 2 or len(ema_slow) < 2:
        return False
    
    # Check for crossover
    current_fast = ema_fast[-1]
    current_slow = ema_slow[-1]
    prev_fast = ema_fast[-2]
    prev_slow = ema_slow[-2]
    
    # Bearish crossover: fast EMA crosses below slow EMA
    return prev_fast >= prev_slow and current_fast < current_slow
```

## 🛡️ **Risk Management**

### **Position Sizing**
```python
def calculate_position_size(symbol: str, risk_percentage: float = 2.0) -> float:
    """Calculate position size based on risk management"""
    
    # Get account balance
    balance = api.get_futures_balance()
    if not balance.get('success'):
        return 0.01  # Minimum size
    
    total_balance = float(balance['data']['list'][0]['totalWalletBalance'])
    
    # Calculate risk amount
    risk_amount = total_balance * (risk_percentage / 100)
    
    # Get current price
    ticker = api.get_futures_ticker(symbol)
    if not ticker.get('success'):
        return 0.01
    
    current_price = float(ticker['data']['list'][0]['lastPrice'])
    
    # Calculate position size
    position_size = risk_amount / current_price
    
    # Round to appropriate precision
    if symbol == 'BTCUSDT':
        return round(position_size, 3)
    elif symbol == 'ETHUSDT':
        return round(position_size, 2)
    else:
        return round(position_size, 1)
```

### **Stop Loss & Take Profit**
```python
def calculate_stop_loss(symbol: str, side: str, entry_price: float, 
                        stop_loss_percentage: float = 2.0) -> float:
    """Calculate stop loss price"""
    
    if side == "Buy":
        stop_loss = entry_price * (1 - stop_loss_percentage / 100)
    else:  # Sell
        stop_loss = entry_price * (1 + stop_loss_percentage / 100)
    
    # Round to appropriate precision
    if symbol == 'BTCUSDT':
        return round(stop_loss, 1)
    elif symbol == 'ETHUSDT':
        return round(stop_loss, 2)
    else:
        return round(stop_loss, 3)

def calculate_take_profit(symbol: str, side: str, entry_price: float, 
                         take_profit_percentage: float = 4.0) -> float:
    """Calculate take profit price"""
    
    if side == "Buy":
        take_profit = entry_price * (1 + take_profit_percentage / 100)
    else:  # Sell
        take_profit = entry_price * (1 - take_profit_percentage / 100)
    
    # Round to appropriate precision
    if symbol == 'BTCUSDT':
        return round(take_profit, 1)
    elif symbol == 'ETHUSDT':
        return round(take_profit, 2)
    else:
        return round(take_profit, 3)
```

## 🔄 **Complete Auto Trading Flow**

### **Main Trading Loop**
```python
def main_trading_loop():
    """Main auto trading loop"""
    
    while True:
        try:
            # 1. Collect market data
            symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
            market_data = collect_market_data(symbols)
            
            # 2. Generate trading signals
            signals = generate_trading_signals(market_data)
            
            # 3. Execute signals
            for signal in signals:
                if should_execute_signal(signal):
                    execute_trading_signal(signal)
            
            # 4. Manage existing positions
            manage_positions()
            
            # 5. Risk management checks
            perform_risk_checks()
            
            # 6. Wait before next iteration
            time.sleep(30)  # 30 second intervals
            
        except Exception as e:
            logger.error(f"Error in main trading loop: {e}")
            time.sleep(60)  # Wait longer on error

def should_execute_signal(signal: TradingSignal) -> bool:
    """Check if signal should be executed"""
    
    # Check if trading is enabled
    if not trading_enabled:
        return False
    
    # Check daily loss limit
    if daily_pnl < -max_daily_loss_percentage:
        return False
    
    # Check if we already have a position
    if has_open_position(signal.symbol):
        return False
    
    # Check balance
    if not has_sufficient_balance(signal):
        return False
    
    return True
```

## 📈 **Performance Monitoring**

### **Trade Tracking**
```python
class TradeTracker:
    def __init__(self):
        self.trades = []
        self.daily_pnl = 0.0
        self.total_trades = 0
        
    def add_trade(self, trade_data: Dict):
        """Add a new trade to tracking"""
        self.trades.append(trade_data)
        self.total_trades += 1
        
        # Update daily PnL
        if 'realized_pnl' in trade_data:
            self.daily_pnl += trade_data['realized_pnl']
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        if not self.trades:
            return {}
        
        winning_trades = [t for t in self.trades if t.get('realized_pnl', 0) > 0]
        losing_trades = [t for t in self.trades if t.get('realized_pnl', 0) < 0]
        
        win_rate = len(winning_trades) / len(self.trades) * 100
        
        total_profit = sum(t.get('realized_pnl', 0) for t in winning_trades)
        total_loss = sum(t.get('realized_pnl', 0) for t in losing_trades)
        
        return {
            'total_trades': self.total_trades,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'total_loss': total_loss,
            'net_pnl': total_profit + total_loss,
            'daily_pnl': self.daily_pnl
        }
```

## 🚀 **Getting Started**

### **1. Setup API Keys**
```python
# config.yaml
bybit:
  enabled: true
  api_key: 'your_api_key'
  api_secret: 'your_api_secret'
  testnet: true  # Use testnet for testing
```

### **2. Initialize Bot**
```python
from bybit_futures_bot import BybitFuturesBot

bot = BybitFuturesBot(
    api_key="your_api_key",
    api_secret="your_api_secret",
    testnet=True
)
```

### **3. Start Trading**
```python
# Start the bot
bot.start_trading()

# Monitor status
while True:
    status = bot.get_bot_status()
    print(f"Bot Status: {status}")
    time.sleep(60)
```

## ⚠️ **Important Notes**

### **V5 API Specific Requirements:**
- **All endpoints require `category: "linear"`** for futures
- **Account endpoints require `accountType: "UNIFIED"`**
- **Use title case for side**: "Buy" not "BUY", "Sell" not "SELL"
- **Order types**: "Limit" not "LIMIT", "Market" not "MARKET"

### **Rate Limits:**
- **10 requests per second**
- **600 requests per minute**
- **36,000 requests per hour**

### **Risk Management:**
- Always set stop-loss and take-profit
- Use proper position sizing
- Monitor daily loss limits
- Implement trailing stops

### **Testing:**
- Use testnet for development
- Test with small amounts
- Validate all strategies
- Monitor WebSocket connections

## 🎯 **Next Steps**

1. **Implement the complete bot class**
2. **Add more trading strategies**
3. **Implement advanced risk management**
4. **Add performance analytics**
5. **Create user interface**
6. **Deploy to production**

---

**🚀 Ready to implement Bybit V5 Futures Auto Trading Bot!**

*All endpoints and parameters follow the official Bybit V5 API documentation.*

---

**Copyright © 2024 Telegram-Airdrop-Bot. All rights reserved.** 