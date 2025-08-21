#!/usr/bin/env python3
"""
Debug Bybit API Issues
"""

import requests
import hashlib
import hmac
import time
import json

def debug_api_issue():
    """Debug the API issue step by step"""
    api_key = "hqtW8Wu0LIKkkXl7zW"
    api_secret = "tkjQxgMREM810JYEJ9ndhkOC3MS64yCtxaRb"
    base_url = "https://api.bybit.com"
    
    print("🔍 Debugging Bybit API Issue")
    print("=" * 60)
    
    # Test 1: Check if API key exists
    print("\n📊 Test 1: API Key Validation")
    try:
        response = requests.get(f"{base_url}/v5/market/time")
        if response.status_code == 200:
            print("   ✅ Bybit API is accessible")
        else:
            print(f"   ❌ Bybit API error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return False
    
    # Test 2: Test with minimal parameters
    print("\n🔐 Test 2: Minimal Private Request")
    try:
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        
        # No parameters - just basic request
        params = {}
        param_str = ""
        
        signature_input = timestamp + api_key + recv_window + param_str
        signature = hmac.new(
            api_secret.encode('utf-8'),
            signature_input.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'Content-Type': 'application/json',
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-SIGNATURE': signature,
            'X-BAPI-SIGNATURE-TYPE': '2',
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': recv_window
        }
        
        print(f"   Timestamp: {timestamp}")
        print(f"   Signature Input: {signature_input}")
        print(f"   Signature: {signature}")
        print(f"   Headers: {json.dumps(headers, indent=2)}")
        
        # Try different endpoints
        endpoints = [
            "/v5/account/wallet-balance",
            "/v5/position/list",
            "/v5/order/realtime"
        ]
        
        for endpoint in endpoints:
            print(f"\n   Testing: {endpoint}")
            try:
                response = requests.get(
                    f"{base_url}{endpoint}",
                    headers=headers
                )
                
                print(f"      Status: {response.status_code}")
                print(f"      Response: {response.text[:200]}...")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('retCode') == 0:
                        print(f"      ✅ SUCCESS: {endpoint}")
                        return True
                    else:
                        print(f"      ❌ API Error: {data.get('retMsg', 'Unknown')}")
                else:
                    print(f"      ❌ HTTP Error: {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ Exception: {e}")
        
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    return False

def test_ip_restriction():
    """Test if IP restriction is the issue"""
    print("\n🌐 Test 3: IP Restriction Check")
    
    try:
        # Get current IP
        response = requests.get("https://api.ipify.org?format=json", timeout=10)
        if response.status_code == 200:
            ip_data = response.json()
            current_ip = ip_data.get('ip', 'Unknown')
            print(f"   Your Current IP: {current_ip}")
            
            # Test with different user agent
            print(f"   Testing with different user agent...")
            
            api_key = "hqtW8Wu0LIKkkXl7zW"
            api_secret = "tkjQxgMREM810JYEJ9ndhkOC3MS64yCtxaRb"
            base_url = "https://api.bybit.com"
            
            timestamp = str(int(time.time() * 1000))
            recv_window = "5000"
            params = {"accountType": "UNIFIED"}
            
            param_str = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
            signature_input = timestamp + api_key + recv_window + param_str
            signature = hmac.new(
                api_secret.encode('utf-8'),
                signature_input.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'X-BAPI-API-KEY': api_key,
                'X-BAPI-SIGNATURE': signature,
                'X-BAPI-SIGNATURE-TYPE': '2',
                'X-BAPI-TIMESTAMP': timestamp,
                'X-BAPI-RECV-WINDOW': recv_window
            }
            
            response = requests.get(
                f"{base_url}/v5/account/wallet-balance",
                params=params,
                headers=headers
            )
            
            print(f"   Status with User-Agent: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
        else:
            print(f"   ❌ Failed to get IP: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Main debug function"""
    print("🤖 Bybit API Debug Session")
    print("=" * 70)
    
    # Debug API issue
    success = debug_api_issue()
    
    # Test IP restriction
    test_ip_restriction()
    
    print("\n" + "=" * 70)
    
    if success:
        print("🎉 SUCCESS: API issue resolved!")
    else:
        print("❌ ISSUE: API still not working")
        print("\n🔧 POSSIBLE SOLUTIONS:")
        print("1. Add your IP to Bybit API whitelist")
        print("2. Check if API key is fully activated")
        print("3. Verify API key permissions are applied")
        print("4. Try disabling IP restrictions temporarily")
        print("5. Check if there's a delay in API key activation")
        
        print("\n💡 IMMEDIATE ACTION:")
        print("Go to: https://www.bybit.com/app/user/api-management")
        print("Find key: hqtW8Wu0LIKkkXl7zW")
        print("Click Edit → Add IP: 103.178.187.121")
        print("Or disable IP restrictions temporarily")
    
    return success

if __name__ == "__main__":
    main() 