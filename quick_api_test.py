#!/usr/bin/env python3
"""
Quick API Test - Run this after fixing IP restrictions
"""

import requests
import hashlib
import hmac
import time

def quick_test():
    """Quick test of the API after IP fix"""
    api_key = "hqtW8Wu0LIKkkXl7zW"
    api_secret = "tkjQxgMREM810JYEJ9ndhkOC3MS64yCtxaRb"
    base_url = "https://api.bybit.com"
    
    print("🚀 Quick API Test - After IP Fix")
    print("=" * 50)
    
    # Test private endpoint
    try:
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
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-SIGNATURE': signature,
            'X-BAPI-SIGNATURE-TYPE': '2',
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': recv_window
        }
        
        print(f"Testing account balance endpoint...")
        response = requests.get(
            f"{base_url}/v5/account/wallet-balance",
            params=params,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('retCode') == 0:
                print("🎉 SUCCESS: API working! IP restrictions fixed!")
                print("✅ Ready for live trading!")
                return True
            else:
                print(f"❌ API Error: {data.get('retMsg', 'Unknown')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print("💡 IP restrictions still need to be fixed")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Main function"""
    print("🔧 API Permission Fix Test")
    print("=" * 50)
    
    success = quick_test()
    
    if success:
        print("\n🎉 CONGRATULATIONS!")
        print("Your API is now working for live trading!")
        print("\n🚀 Next Steps:")
        print("1. Test the full bot: python demo_futures_bot.py")
        print("2. Start live trading with real money")
        print("3. Monitor your positions and P&L")
    else:
        print("\n❌ API still not working")
        print("\n🔧 Please fix IP restrictions:")
        print("1. Go to: https://www.bybit.com/app/user/api-management")
        print("2. Find key: hqtW8Wu0LIKkkXl7zW")
        print("3. Add IP: 103.178.187.100")
        print("4. Save and run this test again")
    
    return success

if __name__ == "__main__":
    main() 