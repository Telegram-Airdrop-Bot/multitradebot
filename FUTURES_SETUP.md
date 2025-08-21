# Bybit Futures Trading Setup Guide

## Overview
This bot now supports **hybrid trading**: Pionex for spot trading and Bybit for futures trading with leverage.

## Prerequisites
- Bybit account with API access
- API Key with trading permissions
- USDT balance in your futures wallet

## Step 1: Create Bybit API Keys

### 1.1 Login to Bybit
- Go to [Bybit.com](https://www.bybit.com)
- Login to your account

### 1.2 Generate API Keys
- Go to **Account & Security** → **API Management**
- Click **Create New Key**
- Set permissions:
  - ✅ **Read** (required)
  - ✅ **Trade** (required for futures trading)
  - ✅ **Transfer** (optional, for moving funds)
- Set IP restrictions (recommended for security)
- Click **Submit**
- **IMPORTANT**: Save your API Key and Secret Key securely

## Step 2: Configure the Bot

### 2.1 Update config.yaml
```yaml
# Bybit Futures Configuration
bybit:
  enabled: true
  api_key: 'YOUR_BYBIT_API_KEY'
  api_secret: 'YOUR_BYBIT_API_SECRET'
  testnet: false  # true for testing, false for live trading

# Trading Mode
trading_mode: 'HYBRID'  # SPOT_ONLY, FUTURES_ONLY, HYBRID
spot_exchange: 'PIONEX'
futures_exchange: 'BYBIT'

# Futures Settings
futures:
  enabled: true
  default_leverage: 10
  max_leverage: 125
  margin_type: 'ISOLATED'  # ISOLATED or CROSS
  risk_management:
    max_position_size: 0.1  # 10% of balance
    max_daily_loss: 5.0     # 5% of balance
    stop_loss_default: 2.0  # 2% default SL
    take_profit_default: 4.0 # 4% default TP
```

### 2.2 Or Use GUI Settings
1. Open the bot interface
2. Click **Settings** (gear icon)
3. Go to **Futures Trading (Bybit)** section
4. Enter your Bybit API Key and Secret
5. Configure leverage and risk management
6. Click **Save Settings**

## Step 3: Test Configuration

### 3.1 Check API Connection
- Restart the bot after saving settings
- Check console logs for "Bybit API initialized for futures trading"
- Verify no API errors in logs

### 3.2 Test Balance Loading
- Check if futures balance appears in the dashboard
- Verify Bybit futures wallet shows correct balance

## Step 4: Start Futures Trading

### 4.1 Basic Futures Trade
1. Click **Futures Trading** card
2. Click **Futures Trade** button
3. Select symbol (e.g., BTCUSDT)
4. Choose side (LONG/SHORT)
5. Set quantity in USDT
6. Choose leverage (1x to 125x)
7. Set stop loss and take profit
8. Click **Execute Futures Trade**

### 4.2 Risk Management
- **Stop Loss**: Automatically closes position if price moves against you
- **Take Profit**: Automatically closes position when profit target is reached
- **Leverage**: Higher leverage = higher risk and potential reward
- **Position Size**: Never risk more than you can afford to lose

## Trading Features

### Available Actions
- **Futures Trade**: Open new leveraged positions
- **Set Leverage**: Change leverage for specific symbols
- **Close Position**: Close open positions manually
- **Real-time Data**: Live price updates and market depth

### Supported Symbols
- BTCUSDT, ETHUSDT, DOTUSDT
- ADAUSDT, SOLUSDT
- And many more Bybit futures pairs

### Order Types
- **Market**: Execute immediately at current price
- **Limit**: Execute at specified price or better

## Safety Features

### Built-in Protections
- Maximum leverage limits (125x)
- Position size limits (% of balance)
- Daily loss limits
- Automatic stop loss and take profit

### Best Practices
1. **Start Small**: Begin with low leverage (1x-5x)
2. **Use Stop Loss**: Always set stop loss for every trade
3. **Risk Management**: Never risk more than 1-2% per trade
4. **Test First**: Use testnet for practice
5. **Monitor Positions**: Check positions regularly

## Troubleshooting

### Common Issues

#### API Key Errors
```
Error: Bybit API not initialized
```
**Solution**: Check API key/secret in config.yaml or GUI settings

#### Balance Not Loading
```
Failed to load futures balance
```
**Solution**: Verify API permissions include "Read" access

#### Trade Execution Failed
```
Failed to execute futures trade
```
**Solutions**:
- Check if you have sufficient USDT balance
- Verify symbol format (e.g., BTCUSDT not BTC_USDT)
- Ensure leverage is within allowed range

#### Position Not Opening
- Check if symbol is supported
- Verify leverage is set correctly
- Ensure sufficient margin

### Debug Steps
1. Check bot console logs for errors
2. Verify API key permissions
3. Test with small amounts first
4. Check Bybit account for any restrictions

## Advanced Configuration

### Custom Risk Parameters
```yaml
futures:
  risk_management:
    max_position_size: 0.05    # 5% max position
    max_daily_loss: 3.0        # 3% daily loss limit
    stop_loss_default: 1.5     # 1.5% default SL
    take_profit_default: 3.0   # 3% default TP
    trailing_stop_default: 0.5 # 0.5% trailing stop
```

### Margin Type
- **Isolated**: Risk only the amount allocated to position
- **Cross**: Use entire wallet balance as margin (higher risk)

### Leverage Settings
- **Conservative**: 1x-10x (lower risk)
- **Moderate**: 10x-50x (balanced)
- **Aggressive**: 50x-125x (high risk)

## Support

### Getting Help
- Check console logs for detailed error messages
- Verify API configuration
- Test with small amounts first
- Contact support if issues persist

### Resources
- [Bybit API Documentation](https://bybit-exchange.github.io/docs/v5/intro)
- [Futures Trading Guide](https://help.bybit.com/hc/en-us/categories/360000234652)
- [Risk Management](https://help.bybit.com/hc/en-us/articles/360039261154)

---

**⚠️ Risk Warning**: Futures trading involves substantial risk of loss. You can lose more than your initial investment. Only trade with funds you can afford to lose. 