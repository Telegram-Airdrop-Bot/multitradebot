# 🚀 MultiTradeBot - Advanced Cryptocurrency Trading Bot

<div align="center">

![MultiTradeBot](https://img.shields.io/badge/MultiTradeBot-Advanced%20Trading%20Bot-blue?style=for-the-badge&logo=bitcoin)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-red?style=for-the-badge&logo=flask)
![Bybit](https://img.shields.io/badge/Bybit-API%20V5-orange?style=for-the-badge&logo=bitcoin)
![Pionex](https://img.shields.io/badge/Pionex-Spot%20Trading-yellow?style=for-the-badge&logo=bitcoin)

**Professional Dual-Exchange Cryptocurrency Trading Bot with Advanced Risk Management**

[![GitHub stars](https://img.shields.io/github/stars/Telegram-Airdrop-Bot/multitradebot?style=social)](https://github.com/Telegram-Airdrop-Bot/multitradebot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Telegram-Airdrop-Bot/multitradebot?style=social)](https://github.com/Telegram-Airdrop-Bot/multitradebot/network)
[![GitHub issues](https://img.shields.io/github/issues/Telegram-Airdrop-Bot/multitradebot)](https://github.com/Telegram-Airdrop-Bot/multitradebot/issues)
[![GitHub license](https://img.shields.io/github/license/Telegram-Airdrop-Bot/multitradebot)](https://github.com/Telegram-Airdrop-Bot/multitradebot/blob/main/LICENSE)

</div>

---

## 📋 Table of Contents

- [🌟 Features](#-features)
- [🛠️ Technology Stack](#️-technology-stack)
- [🚀 Quick Start](#-quick-start)
- [📱 Dual Exchange Support](#-dual-exchange-support)
- [🤖 Advanced Trading System](#-advanced-trading-system)
- [📊 Risk Management](#-risk-management)
- [🔔 Telegram Notifications](#-telegram-notifications)
- [⚙️ Configuration](#️-configuration)
- [📈 API Endpoints](#-api-endpoints)
- [🔧 Installation](#-installation)
- [📖 Usage](#-usage)
- [⚠️ Disclaimer](#️-disclaimer)
- [📞 Contact & Support](#-contact--support)
- [💝 Donate](#-donate)
- [📄 License](#-license)

---

## 🌟 Features

### 🎯 **Core Trading Features**
- **Dual Exchange Support** - Pionex (Spot) + Bybit (Futures)
- **Real-time Market Data** - Live price feeds and market analysis
- **Advanced Order Types** - Market, Limit, Stop-Loss, Take-Profit
- **Position Management** - Open, close, and modify positions
- **Leverage Control** - Configurable leverage from 1x to 125x

### 🤖 **Advanced Trading System (Bot 2025)**
- **Session Management** - US & Asian trading sessions with DST support
- **Range Box Calculation** - First 90 minutes high/low analysis
- **Breakout Detection** - Automated breakout strategy execution
- **Technical Filters** - Multi-Timeframe RSI & Volume analysis
- **Anti-Fake Breakout** - Slippage and distance protection

### 🛡️ **Risk Management**
- **Stop Loss Management** - Automatic stop-loss placement
- **Take Profit Strategy** - TP1/TP2 with trailing stops
- **Auto-Breakeven** - Automatic breakeven level management
- **Position Sizing** - Risk-based position calculation
- **Daily Loss Limits** - Configurable daily risk limits

### 📱 **User Interface**
- **Professional Web GUI** - Modern, responsive interface
- **Real-time Monitoring** - Live P&L, positions, and balance
- **Mobile Responsive** - Works on all devices
- **Dark Theme** - Professional trading interface
- **Real-time Logs** - Comprehensive system monitoring

---

## 🛠️ Technology Stack

### **Backend**
- **Python 3.8+** - Core programming language
- **Flask 3.0+** - Web framework for API and GUI
- **PyBit 5.7+** - Official Bybit API integration
- **Requests** - HTTP library for API calls
- **PyYAML** - Configuration management

### **Frontend**
- **HTML5 + CSS3** - Modern web standards
- **Bootstrap 5** - Responsive UI framework
- **JavaScript ES6+** - Dynamic functionality
- **Font Awesome** - Professional icons
- **Chart.js** - Data visualization

### **APIs & Integrations**
- **Bybit V5 API** - Futures trading
- **Pionex API** - Spot trading
- **Telegram Bot API** - Notifications
- **WebSocket** - Real-time data

---

## 🚀 Quick Start

### **1. Clone Repository**
```bash
git clone https://github.com/Telegram-Airdrop-Bot/multitradebot.git
cd multitradebot
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Configure API Keys**
```yaml
# config.yaml
bybit:
  api_key: "YOUR_BYBIT_API_KEY"
  api_secret: "YOUR_BYBIT_API_SECRET"
  
pionex:
  api_key: "YOUR_PIONEX_API_KEY"
  api_secret: "YOUR_PIONEX_API_SECRET"
```

### **4. Run the Bot**
```bash
python gui_app.py
```

### **5. Access Web Interface**
Open your browser and navigate to: `http://localhost:5000`

---

## 📱 Dual Exchange Support

### **🟠 Pionex (Spot Trading)**
- **Spot Market Trading** - Buy/sell actual cryptocurrencies
- **Real-time Price Feeds** - Live market data
- **Portfolio Management** - Track holdings and P&L
- **Order History** - Complete trade history
- **Risk Management** - Stop-loss and take-profit

### **🟡 Bybit (Futures Trading)**
- **Futures Trading** - Long/Short with leverage
- **Advanced Order Types** - Market, Limit, Stop orders
- **Position Management** - Real-time position tracking
- **Risk Control** - Leverage and margin management
- **Professional Interface** - Advanced trading dashboard

---

## 🤖 Advanced Trading System

### **⏰ Session Management**
- **US Session** - 8:30 AM - 3:00 PM EST (with DST support)
- **Asian Session** - 7:30 PM - 1:30 AM UTC-5
- **Automatic Detection** - Real-time session status
- **Session-based Limits** - Trade limits per session

### **📊 Range Box Strategy**
- **90-Minute Analysis** - Calculate high/low ranges
- **Breakout Detection** - Price breakout monitoring
- **Buffer Zones** - Configurable breakout thresholds
- **Confirmation Candles** - Wait for confirmation

### **🔍 Technical Filters**
- **Multi-Timeframe RSI** - 5-minute and 1-hour analysis
- **Volume Analysis** - Volume vs EMA20 comparison
- **Reduced/Normal Mode** - Configurable filter intensity
- **Real-time Monitoring** - Live filter status

---

## 📊 Risk Management

### **🛑 Stop Loss Management**
- **Automatic Placement** - Set SL on order entry
- **Box Opposite Logic** - Use session range for SL
- **Trailing Stops** - Dynamic stop-loss adjustment
- **Breakeven Protection** - Move SL to entry at profit

### **💰 Take Profit Strategy**
- **TP1/TP2 Levels** - Multiple profit targets
- **Trailing Stops** - Lock in profits automatically
- **Risk-Reward Ratios** - Configurable R:R ratios
- **Partial Close** - Close portions at targets

### **⚖️ Position Sizing**
- **Risk-based Calculation** - Percentage of account
- **Daily Limits** - Maximum trades per day
- **Session Limits** - Maximum trades per session
- **Cooldown Periods** - Time between trades

---

## 🔔 Telegram Notifications

### **📱 Real-time Alerts**
- **Trade Executions** - Order placement confirmations
- **Breakout Detections** - Strategy signal alerts
- **Risk Alerts** - Stop-loss and margin warnings
- **Session Updates** - Trading session status
- **System Status** - Bot health and performance

### **⚙️ Easy Setup**
1. **Message @BotFather** on Telegram
2. **Create new bot** with `/newbot`
3. **Get bot token** and **chat ID**
4. **Enter in interface** and test connection
5. **Save settings** to enable notifications

---

## ⚙️ Configuration

### **📁 Configuration Files**
```yaml
# config.yaml - Main configuration
# .env - Environment variables
# requirements.txt - Python dependencies
```

### **🔧 Key Settings**
- **API Credentials** - Exchange API keys
- **Risk Parameters** - Stop-loss, take-profit percentages
- **Session Times** - Trading session configurations
- **Technical Filters** - RSI thresholds, volume settings
- **Notification Settings** - Telegram bot configuration

---

## 📈 API Endpoints

### **🔄 Core Trading APIs**
```
POST /api/bybit/place-order          # Place futures order
POST /api/bybit/close-position       # Close position
GET  /api/bybit/positions            # Get open positions
GET  /api/bybit/balance              # Get account balance
```

### **🤖 Auto Trading APIs**
```
POST /api/bybit/auto-trading/start   # Start auto trading
POST /api/bybit/auto-trading/stop    # Stop auto trading
POST /api/bybit/auto-trading/settings # Update settings
GET  /api/bybit/auto-trading/status  # Get status
```

### **📱 Notification APIs**
```
POST /api/telegram/test-connection   # Test bot connection
POST /api/telegram/save-settings     # Save notification settings
POST /api/telegram/send-notification # Send custom notification
```

---

## 🔧 Installation

### **System Requirements**
- **Python 3.8+** - Modern Python version
- **8GB RAM** - Recommended for smooth operation
- **Stable Internet** - Required for API connections
- **Windows/Linux/Mac** - Cross-platform support

### **Dependencies Installation**
```bash
# Install Python packages
pip install -r requirements.txt

# Install system dependencies (Linux)
sudo apt-get update
sudo apt-get install python3-dev python3-pip

# Install system dependencies (Windows)
# Python installer handles dependencies automatically
```

### **Environment Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📖 Usage

### **🔄 Starting the Bot**
1. **Configure API keys** in `config.yaml`
2. **Set risk parameters** in the interface
3. **Choose trading pairs** for auto trading
4. **Start auto trading** with START button
5. **Monitor performance** in real-time

### **📊 Monitoring Dashboard**
- **Real-time P&L** - Live profit/loss tracking
- **Position Status** - Current open positions
- **Market Data** - Live price feeds
- **System Logs** - Comprehensive activity logs
- **Performance Metrics** - Trading statistics

### **⚙️ Configuration Management**
- **Settings Persistence** - All settings automatically saved
- **Real-time Updates** - Changes applied immediately
- **Backup & Restore** - Configuration backup support
- **Profile Management** - Multiple trading profiles

---

## ⚠️ Disclaimer

### **🚨 Risk Warning**
- **Cryptocurrency trading involves substantial risk**
- **Past performance does not guarantee future results**
- **Only trade with funds you can afford to lose**
- **This software is for educational purposes**

### **🔒 Security Notice**
- **Never share your API keys**
- **Use testnet for learning**
- **Enable 2FA on exchange accounts**
- **Regular security updates required**

---

## 📞 Contact & Support

### **👨‍💻 Author Information**
- **Name:** Md Mushfiqur Rahman
- **Email:** [moonbd01717@gmail.com](mailto:moonbd01717@gmail.com)
- **Website:** [https://i-am-mushfiqur.netlify.app/](https://i-am-mushfiqur.netlify.app/)
- **WhatsApp:** [+8801701259687](https://wa.me/8801701259687)

### **💬 Support Channels**
- **GitHub Issues** - [Report bugs and feature requests](https://github.com/Telegram-Airdrop-Bot/multitradebot/issues)
- **Email Support** - Technical assistance and questions
- **WhatsApp Support** - Quick help and guidance
- **Documentation** - Comprehensive usage guides

---

## 💝 Donate

### **🌟 Support Development**
If you find this project helpful, please consider donating to support continued development and maintenance.

### **💳 Donation Wallets**

#### **Ethereum (ETH)**
```
0xeca8Be238726121258425b808F240971778Ac18c
```

#### **Solana (SOL)**
```
BdYEZDM5weQKHqweDdts6bNVMpEGwWbfRjccoHz2tXtu
```

### **🎁 What Your Donation Supports**
- **Feature Development** - New trading strategies
- **Bug Fixes** - Performance improvements
- **Documentation** - Better user guides
- **Server Costs** - Hosting and maintenance
- **Community Support** - User assistance

---

## 📄 License

### **🔒 Copyright Protection**
```
Copyright (c) 2025 Md Mushfiqur Rahman
All Rights Reserved

This software is protected by copyright law and international treaties.
Unauthorized reproduction or distribution of this software, or any portion of it,
may result in severe civil and criminal penalties, and will be prosecuted
to the maximum extent possible under the law.

This software is provided "AS IS" without warranty of any kind, either
express or implied, including but not limited to the implied warranties
of merchantability and fitness for a particular purpose.
```

### **📋 License Terms**
- **All Rights Reserved** - Full copyright protection
- **No Redistribution** - Without explicit permission
- **No Modification** - Code integrity protection
- **Commercial Use** - Requires written permission
- **Educational Use** - Allowed with attribution

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Telegram-Airdrop-Bot/multitradebot&type=Date)](https://star-history.com/#Telegram-Airdrop-Bot/multitradebot&Date)

---

<div align="center">

**Made with ❤️ by [Md Mushfiqur Rahman](https://i-am-mushfiqur.netlify.app/)**

**⭐ Star this repository if you find it helpful! ⭐**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Telegram-Airdrop-Bot/multitradebot)
[![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://i-am-mushfiqur.netlify.app/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:moonbd01717@gmail.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/8801701259687)

</div>
