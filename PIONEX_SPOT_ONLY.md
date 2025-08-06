# Pionex API - Spot Trading Only

## Overview

**Pionex only supports spot trading, not futures trading.** This is an important distinction that affects how the trading bot works and what features are available.

## What This Means

### ✅ **Available Features (Spot Trading)**
- **Spot Market Orders**: Buy and sell actual cryptocurrencies
- **Market Orders**: Immediate execution at current market price
- **Limit Orders**: Orders executed at a specific price or better
- **Stop Loss Orders**: Automatic sell orders when price drops
- **Take Profit Orders**: Automatic sell orders when price rises
- **Spot Holdings**: Your actual cryptocurrency balances
- **Real-time Prices**: Live market data for spot trading pairs

### ❌ **Not Available (No Futures)**
- **Futures Trading**: No leverage or margin trading
- **Perpetual Contracts**: No perpetual futures contracts
- **Leverage Trading**: No leveraged positions
- **Short Selling**: No short positions (except through spot selling)
- **Futures Positions**: No futures position management
- **Margin Trading**: No margin accounts

## Spot Trading vs Futures Trading

### **Spot Trading (Pionex)**
- You buy and sell **actual cryptocurrencies**
- You own the coins you buy
- No leverage or margin
- Lower risk, more straightforward
- Good for long-term holding and simple trading

### **Futures Trading (Not Available)**
- Trading contracts based on cryptocurrency prices
- Can use leverage (borrowed money)
- Can go short (bet on price drops)
- Higher risk, more complex
- Good for advanced trading strategies

## How This Affects the Trading Bot

### **Balance Display**
- Shows your **actual cryptocurrency holdings**
- Displays coins you own (BTC, ETH, USDT, etc.)
- No leverage or margin positions

### **Order Types**
- **Market Orders**: Buy/sell at current price
- **Limit Orders**: Buy/sell at specific price
- **Stop Orders**: Automatic orders based on price triggers
- **No Futures Orders**: No leverage or margin orders

### **Position Management**
- **Spot Holdings**: Your actual coin balances
- **No Futures Positions**: No leveraged positions to manage
- **Simple Portfolio**: Just the coins you own

## API Endpoints

### **Working Endpoints (Spot Trading)**
- `/api/v1/account/balances` - Your spot holdings
- `/api/v1/trade/order` - Place spot orders
- `/api/v1/market/tickers` - Spot market prices
- `/api/v1/market/klines` - Spot market data

### **Not Available (Futures)**
- No futures account endpoints
- No leverage management
- No margin account endpoints
- No futures position endpoints

## Trading Strategy Implications

### **Suitable Strategies**
- **Buy and Hold**: Purchase coins and hold long-term
- **Spot Trading**: Buy low, sell high with actual coins
- **DCA (Dollar Cost Averaging)**: Regular purchases
- **Portfolio Diversification**: Hold multiple cryptocurrencies

### **Not Suitable**
- **Leverage Trading**: No margin or leverage
- **Short Selling**: Can't bet on price drops
- **High-Frequency Trading**: Limited by spot trading constraints
- **Futures Arbitrage**: No futures markets

## Getting Started with Spot Trading

### **1. Fund Your Account**
- Deposit USDT or other supported cryptocurrencies
- No margin or leverage needed

### **2. Place Spot Orders**
```python
# Buy BTC with USDT
api.place_market_order('BTC_USDT', 'BUY', 0.001)

# Sell BTC for USDT
api.place_market_order('BTC_USDT', 'SELL', 0.001)
```

### **3. Check Your Holdings**
```python
# Get your spot holdings
balances = api.get_balances()
positions = api.get_positions()
```

### **4. Monitor Prices**
```python
# Get real-time prices
price = api.get_real_time_price('BTC_USDT')
```

## Benefits of Spot Trading

### **Advantages**
- **Lower Risk**: No leverage means no margin calls
- **Simpler**: Easier to understand and manage
- **Actual Ownership**: You own the coins you buy
- **No Liquidation**: Can't get liquidated like in futures
- **Tax Benefits**: Often simpler for tax purposes

### **Limitations**
- **No Leverage**: Can't amplify gains (or losses)
- **No Shorting**: Can't easily bet on price drops
- **Limited Strategies**: Fewer advanced trading options
- **Capital Intensive**: Need full amount for purchases

## Conclusion

Pionex is designed for **spot trading only**, making it ideal for:
- **Beginners**: Simple, straightforward trading
- **Long-term Investors**: Buy and hold strategies
- **Conservative Traders**: Lower risk approach
- **Portfolio Builders**: Diversify with actual coins

The trading bot is optimized for spot trading and will show your actual cryptocurrency holdings rather than leveraged positions. 