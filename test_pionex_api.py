#!/usr/bin/env python3
"""
Test script for Pionex API connection and endpoints
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pionex_api import PionexAPI

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_pionex_api():
    """Test Pionex API connection and basic endpoints"""
    
    # Initialize API client
    api = PionexAPI()
    
    print("🔧 Testing Pionex API Connection...")
    print("=" * 50)
    
    # Test 1: Market Data (No Authentication Required)
    print("\n📊 Testing Market Data Endpoints...")
    
    try:
        # Test ticker endpoint
        print("Testing ticker endpoint...")
        ticker_response = api.get_ticker('BTC_USDT')
        print(f"Ticker Response: {ticker_response}")
        
        if 'error' not in ticker_response:
            print("✅ Ticker endpoint working")
        else:
            print(f"❌ Ticker endpoint failed: {ticker_response['error']}")
            
    except Exception as e:
        print(f"❌ Ticker test failed: {e}")
    
    try:
        # Test klines endpoint
        print("Testing klines endpoint...")
        klines_response = api.get_klines('BTC_USDT', '1H', 10)
        print(f"Klines Response: {klines_response}")
        
        if 'error' not in klines_response:
            print("✅ Klines endpoint working")
        else:
            print(f"❌ Klines endpoint failed: {klines_response['error']}")
            
    except Exception as e:
        print(f"❌ Klines test failed: {e}")
    
    # Test 2: Account Endpoints (Authentication Required)
    print("\n💰 Testing Account Endpoints...")
    
    # Check if API credentials are set
    if not api.api_key or not api.secret_key:
        print("⚠️  API credentials not found. Set PIONEX_API_KEY and PIONEX_SECRET_KEY environment variables.")
        print("Skipping authenticated endpoints...")
        return
    
    try:
        # Test balance endpoint
        print("Testing balance endpoint...")
        balance_response = api.get_balances()
        print(f"Balance Response: {balance_response}")
        
        if 'error' not in balance_response:
            print("✅ Balance endpoint working")
        else:
            print(f"❌ Balance endpoint failed: {balance_response['error']}")
            
    except Exception as e:
        print(f"❌ Balance test failed: {e}")
    
    try:
        # Test positions endpoint
        print("Testing positions endpoint...")
        positions_response = api.get_positions()
        print(f"Positions Response: {positions_response}")
        
        if 'error' not in positions_response:
            print("✅ Positions endpoint working")
        else:
            print(f"❌ Positions endpoint failed: {positions_response['error']}")
            
    except Exception as e:
        print(f"❌ Positions test failed: {e}")
    
    # Test 3: Order Endpoints (Authentication Required)
    print("\n📋 Testing Order Endpoints...")
    
    try:
        # Test open orders endpoint
        print("Testing open orders endpoint...")
        open_orders_response = api.get_open_orders()
        print(f"Open Orders Response: {open_orders_response}")
        
        if 'error' not in open_orders_response:
            print("✅ Open orders endpoint working")
        else:
            print(f"❌ Open orders endpoint failed: {open_orders_response['error']}")
            
    except Exception as e:
        print(f"❌ Open orders test failed: {e}")
    
    # Test 4: Symbol Format Conversion
    print("\n🔤 Testing Symbol Format Conversion...")
    
    test_symbols = ['BTC_USDT', 'BTCUSDT', 'btc_usdt', 'ETH_USDT']
    
    for symbol in test_symbols:
        formatted = api._convert_symbol_format(symbol)
        print(f"Original: {symbol} -> Formatted: {formatted}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing Complete!")
    
    # Summary
    print("\n📋 Summary:")
    print("- Market data endpoints should work without authentication")
    print("- Account and order endpoints require valid API credentials")
    print("- Check the logs above for detailed error messages")
    print("- If you see 'INVALID_SIGNATURE' errors, check your API credentials")
    print("- If you see '404 Route Not Found' errors, the endpoint may be incorrect")

if __name__ == "__main__":
    test_pionex_api() 