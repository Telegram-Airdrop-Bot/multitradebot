#!/usr/bin/env python3
"""
Simple Trade Test
Test the exact API response and error details
"""

import requests
import time
import json

def test_simple_trade():
    """Test a simple trade with detailed error analysis"""
    
    base_url = "https://api.pionex.com"
    
    print("🔍 Simple Trade Test with Error Analysis")
    print("=" * 50)
    
    # Step 1: Get server timestamp
    print("📡 Getting server timestamp...")
    try:
        response = requests.get(f"{base_url}/api/v1/market/tickers", timeout=5)
        if response.status_code == 200:
            data = response.json()
            server_timestamp = data.get('timestamp', 0)
            print(f"   Server timestamp: {server_timestamp}")
            print(f"   Server time: {time.ctime(server_timestamp/1000)}")
        else:
            print(f"   Error getting timestamp: {response.status_code}")
            return
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    print()
    
    # Step 2: Test a simple API call without timestamp
    print("🔍 Testing API without timestamp...")
    try:
        response = requests.get(f"{base_url}/api/v1/market/tickers?symbol=BTC_USDT", timeout=5)
        print(f"   Response status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Step 3: Test with different timestamp formats
    print("⏰ Testing different timestamp formats...")
    
    current_time = int(time.time() * 1000)
    server_time = server_timestamp
    
    timestamps = [
        ("Current local time", current_time),
        ("Server time", server_time),
        ("Server time + 1", server_time + 1),
        ("Server time - 1", server_time - 1),
        ("Server time + 1000", server_time + 1000),
        ("Server time - 1000", server_time - 1000)
    ]
    
    for name, ts in timestamps:
        print(f"   {name}: {ts} ({time.ctime(ts/1000)})")
    
    print()
    
    # Step 4: Test if the issue is with the API endpoint itself
    print("🌐 Testing if the issue is with the trading endpoint...")
    
    # Try to get account info first
    print("   Testing account endpoint...")
    try:
        # This would normally require authentication, but let's see what error we get
        response = requests.get(f"{base_url}/api/v1/account/balances", timeout=5)
        print(f"   Account endpoint status: {response.status_code}")
        print(f"   Account endpoint response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Account endpoint error: {e}")
    
    print()
    
    # Step 5: Check if there are any API documentation or examples
    print("📚 Checking for API documentation...")
    print("   The issue might be:")
    print("   1. Wrong endpoint URL")
    print("   2. Wrong authentication method")
    print("   3. Wrong timestamp format")
    print("   4. API key permissions")
    print("   5. Rate limiting")
    print("   6. Server maintenance")

if __name__ == "__main__":
    test_simple_trade() 