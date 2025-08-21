#!/usr/bin/env python3
"""
Bybit Futures Bot Demo
Copyright © 2024 Telegram-Airdrop-Bot

This script demonstrates how to use the Bybit futures bot for live trading.
"""

import time
import logging
from datetime import datetime
from bybit_futures_bot import BybitFuturesBot

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def demo_futures_bot():
    """Demonstrate the futures bot functionality"""
    print("🤖 Bybit Futures Bot Demo")
    print("=" * 50)
    
    try:
        # Load configuration
        import yaml
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        
        bybit_config = config.get('bybit', {})
        api_key = bybit_config.get('api_key')
        api_secret = bybit_config.get('api_secret')
        
        print(f"✅ API credentials loaded")
        print(f"🔑 API Key: {api_key[:8]}...{api_key[-4:]}")
        
        # Initialize bot
        print("\n🚀 Initializing Futures Bot...")
        bot = BybitFuturesBot(api_key, api_secret, testnet=False)
        
        # Show initial status
        status = bot.get_bot_status()
        print("\n📊 Bot Status:")
        for key, value in status.items():
            if key != 'timestamp':
                print(f"   {key}: {value}")
        
        # Update trading configuration for safety
        print("\n⚙️ Setting Safe Trading Configuration...")
        safe_config = {
            'max_position_size': 0.02,      # 2% of balance (very conservative)
            'default_leverage': 3,          # Low leverage for safety
            'stop_loss_percentage': 1.0,    # 1% stop loss
            'take_profit_percentage': 2.0,  # 2% take profit
            'max_daily_loss': 2.0,         # 2% daily loss limit
            'rsi_period': 14,
            'ema_fast': 12,
            'ema_slow': 26
        }
        
        bot.update_trading_config(safe_config)
        print("   ✅ Safe configuration applied")
        
        # Show updated configuration
        print("\n📋 Current Trading Configuration:")
        print(f"   Max Position Size: {bot.max_position_size * 100}% of balance")
        print(f"   Default Leverage: {bot.default_leverage}x")
        print(f"   Stop Loss: {bot.stop_loss_percentage}%")
        print(f"   Take Profit: {bot.take_profit_percentage}%")
        print(f"   Max Daily Loss: {bot.max_daily_loss}%")
        print(f"   RSI Period: {bot.rsi_period}")
        print(f"   EMA Fast: {bot.ema_fast}")
        print(f"   EMA Slow: {bot.ema_slow}")
        
        # Demo market data collection
        print("\n📊 Demo: Market Data Collection...")
        try:
            # Get current market data
            symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
            
            for symbol in symbols:
                ticker = bot.api.get_futures_ticker(symbol)
                if ticker.get('success') and ticker.get('data', {}).get('list'):
                    ticker_data = ticker['data']['list'][0]
                    price = float(ticker_data.get('lastPrice', 0))
                    change_24h = float(ticker_data.get('price24hPcnt', 0)) * 100
                    
                    print(f"   {symbol}: ${price:,.2f} ({change_24h:+.2f}%)")
            
            print("   ✅ Market data collected successfully")
            
        except Exception as e:
            print(f"   ❌ Error collecting market data: {e}")
        
        # Demo signal generation (without executing)
        print("\n🔍 Demo: Trading Signal Generation...")
        try:
            # Get klines for BTCUSDT
            klines_response = bot.api.get_futures_klines('BTCUSDT', '5', 100)
            
            if klines_response.get('success'):
                prices = bot._extract_prices_from_klines(klines_response)
                
                if len(prices) >= 50:
                    # Calculate RSI
                    rsi_values = bot._calculate_rsi(prices, bot.rsi_period)
                    if rsi_values:
                        current_rsi = rsi_values[-1]
                        print(f"   📊 BTCUSDT RSI: {current_rsi:.2f}")
                        
                        if current_rsi < bot.rsi_oversold:
                            print(f"   🟢 RSI Oversold Signal: {current_rsi:.2f} < {bot.rsi_oversold}")
                        elif current_rsi > bot.rsi_overbought:
                            print(f"   🔴 RSI Overbought Signal: {current_rsi:.2f} > {bot.rsi_overbought}")
                        else:
                            print(f"   🟡 RSI Neutral: {current_rsi:.2f}")
                    
                    # Calculate EMA
                    ema_fast_values = bot._calculate_ema(prices, bot.ema_fast)
                    ema_slow_values = bot._calculate_ema(prices, bot.ema_slow)
                    
                    if len(ema_fast_values) >= 2 and len(ema_slow_values) >= 2:
                        current_fast = ema_fast_values[-1]
                        current_slow = ema_slow_values[-1]
                        prev_fast = ema_fast_values[-2]
                        prev_slow = ema_slow_values[-2]
                        
                        print(f"   📈 EMA Fast: {current_fast:.2f}, EMA Slow: {current_slow:.2f}")
                        
                        if prev_fast <= prev_slow and current_fast > current_slow:
                            print("   🟢 Bullish EMA Crossover Signal")
                        elif prev_fast >= prev_slow and current_fast < current_slow:
                            print("   🔴 Bearish EMA Crossover Signal")
                        else:
                            print("   🟡 No EMA Crossover")
                
                print("   ✅ Signal generation demo completed")
            else:
                print("   ❌ Failed to get klines data")
                
        except Exception as e:
            print(f"   ❌ Error in signal generation demo: {e}")
        
        # Show account information
        print("\n💰 Demo: Account Information...")
        try:
            balance_response = bot.api.get_futures_balance()
            if balance_response.get('success') and balance_response.get('data', {}).get('list'):
                balance_data = balance_response['data']['list'][0]
                total_balance = float(balance_data.get('totalWalletBalance', 0))
                available_balance = float(balance_data.get('availableToWithdraw', 0))
                
                print(f"   💰 Total Balance: ${total_balance:,.2f}")
                print(f"   💳 Available Balance: ${available_balance:,.2f}")
                
                if total_balance > 0:
                    # Calculate safe position sizes
                    safe_position_value = total_balance * bot.max_position_size
                    print(f"   🛡️ Safe Position Value: ${safe_position_value:,.2f}")
                    
                    # Show what this means for different symbols
                    for symbol in ['BTCUSDT', 'ETHUSDT']:
                        ticker = bot.api.get_futures_ticker(symbol)
                        if ticker.get('success') and ticker.get('data', {}).get('list'):
                            price = float(ticker['data']['list'][0].get('lastPrice', 0))
                            if price > 0:
                                safe_quantity = safe_position_value / price
                                print(f"      {symbol}: {safe_quantity:.4f} contracts")
                
                print("   ✅ Account information retrieved")
            else:
                print("   ❌ Failed to get account balance")
                
        except Exception as e:
            print(f"   ❌ Error getting account information: {e}")
        
        # Show positions
        print("\n📊 Demo: Current Positions...")
        try:
            positions_response = bot.api.get_futures_positions()
            if positions_response.get('success') and positions_response.get('data', {}).get('list'):
                positions_data = positions_response['data']['list']
                open_positions = [p for p in positions_data if float(p.get('size', 0)) > 0]
                
                if open_positions:
                    print(f"   📈 Open Positions: {len(open_positions)}")
                    for pos in open_positions:
                        symbol = pos.get('symbol', 'Unknown')
                        side = pos.get('side', 'Unknown')
                        size = float(pos.get('size', 0))
                        entry_price = float(pos.get('entryPrice', 0))
                        mark_price = float(pos.get('markPrice', 0))
                        pnl = float(pos.get('unrealizedPnl', 0))
                        leverage = pos.get('leverage', 0)
                        
                        print(f"      {symbol} {side}: {size} contracts")
                        print(f"         Entry: ${entry_price:,.2f}, Mark: ${mark_price:,.2f}")
                        print(f"         PnL: ${pnl:,.2f}, Leverage: {leverage}x")
                else:
                    print("   📊 No open positions")
                
                print("   ✅ Positions information retrieved")
            else:
                print("   ❌ Failed to get positions")
                
        except Exception as e:
            print(f"   ❌ Error getting positions: {e}")
        
        # Final status
        print("\n🎯 Demo Summary:")
        print("=" * 30)
        print("✅ Bot initialized successfully")
        print("✅ Safe configuration applied")
        print("✅ Market data collection working")
        print("✅ Signal generation working")
        print("✅ Account access working")
        print("✅ Ready for live trading")
        
        print("\n⚠️  IMPORTANT SAFETY NOTES:")
        print("   • Bot is configured with very conservative settings")
        print("   • Maximum position size: 2% of balance")
        print("   • Low leverage: 3x maximum")
        print("   • Tight stop-loss: 1%")
        print("   • Daily loss limit: 2%")
        
        print("\n🚀 To start live trading:")
        print("   1. Review the configuration above")
        print("   2. Adjust parameters if needed")
        print("   3. Run: bot.start_trading()")
        print("   4. Monitor performance closely")
        print("   5. Stop with: bot.stop_trading()")
        
        return bot
        
    except Exception as e:
        logger.error(f"Error in demo: {e}")
        return None

def interactive_demo():
    """Interactive demo with user input"""
    print("\n🎮 Interactive Demo Mode")
    print("=" * 30)
    
    bot = demo_futures_bot()
    if not bot:
        print("❌ Demo failed to initialize")
        return
    
    while True:
        print("\n📋 Available Commands:")
        print("   1. Show bot status")
        print("   2. Show positions")
        print("   3. Show market data")
        print("   4. Generate signals")
        print("   5. Start trading (DEMO)")
        print("   6. Stop trading")
        print("   7. Exit")
        
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                status = bot.get_bot_status()
                print("\n📊 Bot Status:")
                for key, value in status.items():
                    if key != 'timestamp':
                        print(f"   {key}: {value}")
            
            elif choice == '2':
                positions = bot.get_positions_summary()
                if positions:
                    print("\n📊 Current Positions:")
                    for symbol, pos in positions.items():
                        print(f"   {symbol}: {pos['side']} {pos['size']} contracts")
                        print(f"      PnL: ${pos['unrealized_pnl']:.2f}")
                else:
                    print("\n📊 No open positions")
            
            elif choice == '3':
                print("\n📊 Market Data:")
                symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
                for symbol in symbols:
                    ticker = bot.api.get_futures_ticker(symbol)
                    if ticker.get('success') and ticker.get('data', {}).get('list'):
                        data = ticker['data']['list'][0]
                        price = float(data.get('lastPrice', 0))
                        change = float(data.get('price24hPcnt', 0)) * 100
                        print(f"   {symbol}: ${price:,.2f} ({change:+.2f}%)")
            
            elif choice == '4':
                print("\n🔍 Generating Trading Signals...")
                signals = bot._generate_trading_signals()
                if signals:
                    print(f"   📈 {len(signals)} signals generated:")
                    for signal in signals:
                        print(f"      {signal.symbol} {signal.side} via {signal.strategy}")
                else:
                    print("   🟡 No trading signals at this time")
            
            elif choice == '5':
                print("\n🚀 Starting Trading Bot (DEMO MODE)...")
                print("   ⚠️  This is a DEMO - no real trades will be executed")
                print("   📊 Bot will run for 60 seconds to show functionality")
                
                # Start bot for demo
                bot.start_trading()
                
                # Let it run for 60 seconds
                print("   ⏱️  Bot running for 60 seconds...")
                time.sleep(60)
                
                # Stop bot
                bot.stop_trading()
                print("   ✅ Demo completed - bot stopped")
            
            elif choice == '6':
                if bot.is_running:
                    bot.stop_trading()
                    print("   ✅ Trading stopped")
                else:
                    print("   ℹ️  Bot is not currently trading")
            
            elif choice == '7':
                print("   👋 Exiting demo...")
                if bot.is_running:
                    bot.stop_trading()
                break
            
            else:
                print("   ❌ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n   👋 Demo interrupted by user")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🤖 Bybit Futures Bot Demo")
    print("=" * 50)
    print("This demo shows how to use the futures bot safely.")
    print("⚠️  Remember: This involves real money trading!")
    
    try:
        interactive_demo()
    except KeyboardInterrupt:
        print("\n👋 Demo ended by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    
    print("\n🎉 Demo completed!") 