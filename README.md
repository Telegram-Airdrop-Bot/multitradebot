# 🤖 Auto Trade Bot - Pionex Trading Bot

A comprehensive automated trading bot for the Pionex cryptocurrency exchange with advanced features, real-time market data, and a modern web interface.

## 📄 Copyright Notice

**Copyright © 2024 Telegram-Airdrop-Bot**

All rights reserved. This software and associated documentation files (the "Software") are the property of Telegram-Airdrop-Bot.

### **License Terms**
- **Commercial Use**: Allowed with attribution
- **Modification**: Allowed for personal use
- **Distribution**: Allowed with source code
- **Attribution**: Required - must include copyright notice

### **Attribution Requirements**
When using this software, you must include:
```
Copyright © 2024 Telegram-Airdrop-Bot
https://github.com/Telegram-Airdrop-Bot/autotradebot
```

### **Restrictions**
- **No Warranty**: Software provided "as is" without warranty
- **Risk Disclaimer**: Trading involves significant financial risk
- **No Liability**: Authors not liable for trading losses
- **Educational Use**: Intended for educational purposes

---

## 🚀 Features

### **Core Trading Features**
- ✅ **Automated Trading**: Multiple trading strategies
- ✅ **Real-time Market Data**: Live price feeds and charts
- ✅ **Technical Analysis**: RSI, MACD, Bollinger Bands
- ✅ **Risk Management**: Stop-loss, take-profit, trailing stops
- ✅ **Portfolio Management**: Position tracking and P&L
- ✅ **Trading History**: Complete trade history and analytics

### **Advanced Features**
- ✅ **Web GUI**: Modern, responsive web interface
- ✅ **Real-time Updates**: WebSocket-based live updates
- ✅ **Multiple Strategies**: RSI, Volume Filter, Advanced, Grid, DCA
- ✅ **Notifications**: Email and Telegram alerts
- ✅ **Chart Analysis**: Interactive price charts with indicators
- ✅ **Market Depth**: Order book visualization
- ✅ **Live Trades**: Real-time trade feed

### **Configuration & Control**
- ✅ **Trading Hours**: Configurable trading time windows
- ✅ **Amount Control**: Set trading amounts per trade
- ✅ **Strategy Selection**: Choose from multiple strategies
- ✅ **Risk Settings**: Customizable risk parameters
- ✅ **API Management**: Secure API key management

## 📋 Requirements

### **System Requirements**
- **Python**: 3.7+ (3.8+ recommended)
- **Memory**: 100MB+ available RAM
- **Storage**: 50MB+ free space
- **Network**: Internet connection for API calls

### **Dependencies**
```bash
# Core Dependencies
Flask==2.3.3
Flask-SocketIO==5.3.6
requests==2.31.0
pandas>=2.1.0
numpy>=1.25.2
matplotlib==3.7.2
ta==0.10.2

# Optional Dependencies
scikit-learn
plotly
seaborn
scipy
```

## 🛠️ Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/Telegram-Airdrop-Bot/autotradebot.git
cd autotradebot
```

### **2. Install Dependencies**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install Flask Flask-SocketIO requests pandas numpy matplotlib ta
```

### **3. Configure API Keys**
```bash
# Copy the example config
cp config.yaml.example config.yaml

# Edit config.yaml with your Pionex API keys
nano config.yaml
```

### **4. Run the Application**
```bash
python gui_app.py
```

### **5. Access Web Interface**
Open your browser and go to: `http://localhost:5000`

## ⚙️ Configuration

### **API Configuration**
```yaml
# config.yaml
api:
  api_key: "your_pionex_api_key"
  secret_key: "your_pionex_secret_key"
  testnet: false  # Set to true for testing
```

### **Trading Settings**
```yaml
trading:
  trading_pair: "BTC_USDT"
  position_size: 0.5
  leverage: 10
  trading_amount: 100  # USDT per trade
  max_daily_loss: 500  # USDT
  stop_loss_percentage: 1.5
  take_profit_percentage: 2.5
  trailing_stop_percentage: 1.0
```

### **Strategy Configuration**
```yaml
strategies:
  default_strategy: "ADVANCED_STRATEGY"
  rsi:
    period: 7
    overbought: 70
    oversold: 30
```

## 🎯 Usage

### **Starting the Bot**
1. **Configure API Keys**: Edit `config.yaml` with your Pionex credentials
2. **Set Trading Parameters**: Configure amount, risk settings, strategy
3. **Launch Application**: Run `python gui_app.py`
4. **Access Web Interface**: Open `http://localhost:5000`
5. **Enable Auto Trading**: Click "Enable Auto Trading" in the web interface

### **Web Interface Features**
- **Dashboard**: Overview of account balance, positions, and performance
- **Charts**: Interactive price charts with technical indicators
- **Trading**: Manual trade execution interface
- **Settings**: Configure trading parameters and strategies
- **History**: View trading history and performance analytics
- **Market Data**: Real-time market depth and live trades

### **Trading Strategies**
1. **RSI Strategy**: Based on Relative Strength Index
2. **Volume Filter**: Volume-based entry/exit signals
3. **Advanced Strategy**: Multi-indicator approach
4. **Grid Trading**: Automated grid trading system
5. **DCA Strategy**: Dollar Cost Averaging approach

## 📊 Monitoring & Analytics

### **Real-time Monitoring**
- Live account balance updates
- Real-time position tracking
- P&L monitoring
- Trade execution alerts

### **Performance Analytics**
- Win/loss ratio
- Average profit per trade
- Maximum drawdown
- Sharpe ratio
- Total return

### **Risk Management**
- Daily loss limits
- Position size limits
- Stop-loss protection
- Trailing stop orders

## 🔧 Maintenance

### **Dependency Management**
```bash
# Check dependencies
python quick_dependency_check.py

# Comprehensive check
python check_dependencies.py --save

# Fix dependency issues
python fix_dependencies.py
```

### **Logs & Debugging**
- Application logs: `logs/app.log`
- Trading logs: `logs/trading.log`
- Error logs: `logs/error.log`

### **Backup & Recovery**
- Database backup: `backup/database.db`
- Configuration backup: `backup/config.yaml`
- Trading history: `backup/history.json`

## ⚠️ Important Notes

### **Risk Disclaimer**
- This is automated trading software
- Cryptocurrency trading involves significant risk
- Past performance does not guarantee future results
- Only trade with funds you can afford to lose

### **Security**
- Keep your API keys secure
- Use testnet for initial testing
- Monitor the bot regularly
- Set appropriate risk limits

### **Best Practices**
- Start with small amounts
- Test thoroughly on testnet
- Monitor performance regularly
- Keep backups of configurations
- Update dependencies regularly

## 🤝 Contributing

### **How to Contribute**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### **Development Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python -m pytest tests/
```

## 📞 Support

### **Documentation**
- [API Documentation](https://pionex-doc.gitbook.io/apidocs/)
- [Trading Strategies Guide](docs/strategies.md)
- [Configuration Guide](docs/configuration.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

### **Community**
- **Issues**: [GitHub Issues](https://github.com/Telegram-Airdrop-Bot/autotradebot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Telegram-Airdrop-Bot/autotradebot/discussions)
- **Wiki**: [Project Wiki](https://github.com/Telegram-Airdrop-Bot/autotradebot/wiki)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pionex API**: For providing the trading API
- **Technical Analysis Library**: For TA indicators
- **Flask Community**: For the web framework
- **Open Source Contributors**: For various libraries used

---

**🎉 Happy Trading!**

*Remember: Trade responsibly and never invest more than you can afford to lose.*

---

**Copyright © 2024 Telegram-Airdrop-Bot. All rights reserved.**