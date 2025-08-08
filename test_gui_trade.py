#!/usr/bin/env python3
"""
Test GUI Trade Script
This script will test trading through the web GUI interface.
"""

import requests
import json
import time
from datetime import datetime

def test_gui_trade():
    """Test trading through the GUI"""
    
    base_url = "http://localhost:5000"
    
    print("🌐 Testing GUI Trade Interface...")
    print("=" * 50)
    
    try:
        # Step 1: Check if GUI is running
        print("📡 Checking GUI availability...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ GUI is running")
        else:
            print("❌ GUI is not responding")
            return
        print()
        
        # Step 2: Get account balance through GUI
        print("💰 Getting balance through GUI...")
        balance_response = requests.get(f"{base_url}/api/balance")
        print(f"   Balance Response: {balance_response.json()}")
        print()
        
        # Step 3: Get current market data
        print("📈 Getting market data through GUI...")
        market_response = requests.get(f"{base_url}/api/market-data/BTC_USDT")
        print(f"   Market Response: {market_response.json()}")
        print()
        
        # Step 4: Test trade validation
        print("🔍 Testing trade validation...")
        validation_data = {
            "symbol": "BTC_USDT",
            "side": "BUY",
            "quantity": 0.0001,
            "order_type": "MARKET"
        }
        
        validation_response = requests.post(
            f"{base_url}/api/trade/validate",
            json=validation_data
        )
        print(f"   Validation Response: {validation_response.json()}")
        print()
        
        # Step 5: Execute a small trade
        print("🔄 Executing test trade through GUI...")
        trade_data = {
            "symbol": "BTC_USDT",
            "side": "BUY",
            "quantity": 0.0001,
            "order_type": "MARKET"
        }
        
        trade_response = requests.post(
            f"{base_url}/api/trade",
            json=trade_data
        )
        
        print(f"   Trade Response: {trade_response.json()}")
        
        if trade_response.json().get('success'):
            print("   ✅ Trade executed successfully through GUI!")
        else:
            print("   ❌ Trade failed through GUI")
            print(f"   Error: {trade_response.json().get('error')}")
        
        print()
        
        # Step 6: Check updated balance
        print("💰 Checking updated balance...")
        updated_balance = requests.get(f"{base_url}/api/balance")
        print(f"   Updated Balance: {updated_balance.json()}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to GUI. Make sure the GUI is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error during GUI test: {e}")

def test_auto_trading():
    """Test auto trading functionality"""
    
    base_url = "http://localhost:5000"
    
    print("🤖 Testing Auto Trading...")
    print("=" * 50)
    
    try:
        # Step 1: Check auto trading status
        print("📊 Checking auto trading status...")
        status_response = requests.get(f"{base_url}/api/auto-trading/status")
        print(f"   Status: {status_response.json()}")
        print()
        
        # Step 2: Enable auto trading
        print("🔄 Enabling auto trading...")
        enable_response = requests.post(f"{base_url}/api/auto-trading/enable")
        print(f"   Enable Response: {enable_response.json()}")
        print()
        
        # Step 3: Check status again
        print("📊 Checking updated status...")
        updated_status = requests.get(f"{base_url}/api/auto-trading/status")
        print(f"   Updated Status: {updated_status.json()}")
        print()
        
        # Step 4: Disable auto trading
        print("🛑 Disabling auto trading...")
        disable_response = requests.post(f"{base_url}/api/auto-trading/disable")
        print(f"   Disable Response: {disable_response.json()}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to GUI. Make sure the GUI is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error during auto trading test: {e}")

if __name__ == "__main__":
    print("🎯 Pionex Trading Bot - GUI Trade Test")
    print("=" * 50)
    print()
    
    print("Choose test type:")
    print("1. Manual trade test")
    print("2. Auto trading test")
    print("3. Both tests")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        test_gui_trade()
    elif choice == "2":
        test_auto_trading()
    elif choice == "3":
        test_gui_trade()
        print("\n" + "=" * 50 + "\n")
        test_auto_trading()
    else:
        print("Invalid choice. Running manual trade test...")
        test_gui_trade() 