#!/usr/bin/env python3
"""
Test Timestamp Format
Check the exact timestamp format required by Pionex API
"""

import requests
import time
import json

def test_timestamp_formats():
    """Test different timestamp formats"""
    
    base_url = "https://api.pionex.com"
    
    print("🔍 Testing Timestamp Formats")
    print("=" * 50)
    
    # Test 1: Get server time
    print("📡 Testing server time endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/time", timeout=5)
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Get ticker with timestamp
    print("📈 Testing ticker endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/market/tickers", timeout=5)
        data = response.json()
        print(f"   Response: {data}")
        
        if 'data' in data and 'timestamp' in data['data']:
            server_timestamp = data['data']['timestamp']
            print(f"   Server timestamp: {server_timestamp}")
            print(f"   Server time: {time.ctime(server_timestamp/1000)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Test different timestamp formats
    print("⏰ Testing different timestamp formats...")
    
    current_time = time.time()
    formats = [
        ("Unix timestamp (seconds)", int(current_time)),
        ("Unix timestamp (milliseconds)", int(current_time * 1000)),
        ("Unix timestamp (microseconds)", int(current_time * 1000000)),
        ("ISO format", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(current_time))),
        ("RFC format", time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(current_time)))
    ]
    
    for name, timestamp in formats:
        print(f"   {name}: {timestamp}")
    
    print()
    
    # Test 4: Check if we can get server time from different endpoints
    print("🌐 Testing different endpoints for server time...")
    
    endpoints = [
        "/api/v1/time",
        "/api/v1/market/tickers",
        "/api/v1/common/symbols"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   {endpoint}: Status {response.status_code}")
                if 'timestamp' in data:
                    print(f"     Timestamp: {data['timestamp']}")
                elif 'data' in data and 'timestamp' in data['data']:
                    print(f"     Timestamp: {data['data']['timestamp']}")
                else:
                    print(f"     No timestamp found")
            else:
                print(f"   {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"   {endpoint}: Error {e}")

if __name__ == "__main__":
    test_timestamp_formats() 