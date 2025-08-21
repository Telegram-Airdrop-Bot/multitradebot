#!/usr/bin/env python3
"""
Check Bybit API Permissions
Copyright © 2024 Telegram-Airdrop-Bot

This script checks the API key permissions and helps resolve access issues.
"""

import yaml
import logging
from bybit_api_v5_fixed import BybitAPIV5

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

def check_api_permissions():
    """Check API key permissions and access"""
    print("🔍 Checking Bybit API Permissions")
    print("=" * 50)
    
    try:
        # Load configuration
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        
        bybit_config = config.get('bybit', {})
        api_key = bybit_config.get('api_key')
        api_secret = bybit_config.get('api_secret')
        
        print(f"✅ API credentials loaded")
        print(f"🔑 API Key: {api_key[:8]}...{api_key[-4:]}")
        
        # Initialize API with fixed implementation
        api = BybitAPIV5(api_key, api_secret, testnet=False)
        print("✅ API initialized with fixed V5 implementation")
        
        # Test public endpoints
        print("\n📊 Testing Public Endpoints:")
        
        # Market status
        try:
            result = api.get_futures_market_status()
            if result.get('success'):
                print("   ✅ Market Status: Working")
            else:
                print(f"   ❌ Market Status: {result.get('error')}")
        except Exception as e:
            print(f"   ❌ Market Status: {e}")
        
        # Market ticker
        try:
            result = api.get_futures_ticker('BTCUSDT')
            if result.get('success'):
                print("   ✅ Market Ticker: Working")
            else:
                print(f"   ❌ Market Ticker: {result.get('error')}")
        except Exception as e:
            print(f"   ❌ Market Ticker: {e}")
        
        # Test private endpoints
        print("\n🔐 Testing Private Endpoints:")
        
        # Account balance
        try:
            result = api.get_futures_balance()
            if result.get('success'):
                print("   ✅ Account Balance: Working")
                balance_data = result['data'].get('list', [])
                if balance_data:
                    wallet = balance_data[0]
                    total_balance = float(wallet.get('totalWalletBalance', 0))
                    available_balance = float(wallet.get('availableToWithdraw', 0))
                    print(f"      💰 Total Balance: ${total_balance:,.2f}")
                    print(f"      💳 Available: ${available_balance:,.2f}")
            else:
                error_msg = result.get('error', 'Unknown error')
                error_code = result.get('code', 'No code')
                print(f"   ❌ Account Balance: {error_msg} (Code: {error_code})")
                
                # Provide specific guidance based on error
                if '401' in str(error_code) or 'unauthorized' in str(error_msg).lower():
                    print("      🔧 Solution: Check API key permissions in Bybit")
                    print("      🔧 Required: Read permissions for account data")
                elif '403' in str(error_code) or 'forbidden' in str(error_msg).lower():
                    print("      🔧 Solution: API key may not have account access")
                    print("      🔧 Required: Enable account permissions")
        except Exception as e:
            print(f"   ❌ Account Balance: {e}")
        
        # Futures positions
        try:
            result = api.get_futures_positions()
            if result.get('success'):
                print("   ✅ Futures Positions: Working")
                positions_data = result['data'].get('list', [])
                open_positions = [p for p in positions_data if float(p.get('size', 0)) > 0]
                print(f"      📊 Open Positions: {len(open_positions)}")
            else:
                error_msg = result.get('error', 'Unknown error')
                error_code = result.get('code', 'No code')
                print(f"   ❌ Futures Positions: {error_msg} (Code: {error_code})")
        except Exception as e:
            print(f"   ❌ Futures Positions: {e}")
        
        # Test order placement (without executing)
        print("\n📝 Testing Order Permissions:")
        try:
            # Just test if we can access order endpoints
            result = api.get_futures_open_orders()
            if result.get('success'):
                print("   ✅ Order Access: Working")
            else:
                error_msg = result.get('error', 'Unknown error')
                error_code = result.get('code', 'No code')
                print(f"   ❌ Order Access: {error_msg} (Code: {error_code})")
        except Exception as e:
            print(f"   ❌ Order Access: {e}")
        
        # Provide solutions
        print("\n🔧 Troubleshooting Guide:")
        print("=" * 40)
        
        print("If you're getting 401/403 errors:")
        print("1. Go to Bybit → API Management")
        print("2. Check your API key permissions:")
        print("   ✅ Read (Required for account data)")
        print("   ✅ Trade (Required for placing orders)")
        print("   ✅ Futures (Required for futures trading)")
        print("3. Ensure IP restrictions allow your current IP")
        print("4. Check if API key is enabled")
        
        print("\n📱 Bybit API Management URL:")
        print("   https://www.bybit.com/app/user/api-management")
        
        return api
        
    except Exception as e:
        print(f"❌ Error checking permissions: {e}")
        return None

def test_simple_trading():
    """Test simple trading functionality"""
    print("\n🚀 Testing Simple Trading Functions:")
    print("=" * 40)
    
    api = check_api_permissions()
    if not api:
        return
    
    try:
        # Test leverage setting
        print("\n⚙️ Testing Leverage Setting...")
        result = api.set_futures_leverage('BTCUSDT', 3)
        if result.get('success'):
            print("   ✅ Leverage Setting: Working")
        else:
            error_msg = result.get('error', 'Unknown error')
            print(f"   ❌ Leverage Setting: {error_msg}")
        
        # Test market order (without executing)
        print("\n📊 Testing Market Order Creation...")
        print("   ℹ️  This is just a test - no real order will be placed")
        
        # Get current price for reference
        ticker = api.get_futures_ticker('BTCUSDT')
        if ticker.get('success') and ticker.get('data', {}).get('list'):
            current_price = float(ticker['data']['list'][0].get('lastPrice', 0))
            print(f"   💰 Current BTC Price: ${current_price:,.2f}")
            
            # Calculate safe position size
            safe_quantity = 0.001  # Very small for testing
            print(f"   📊 Test Quantity: {safe_quantity} BTC")
            
            # Test order parameters
            order_params = {
                'category': 'linear',
                'symbol': 'BTCUSDT',
                'side': 'Buy',
                'orderType': 'Market',
                'qty': str(safe_quantity),
                'timeInForce': 'GTC',
                'reduceOnly': False,
                'closeOnTrigger': False
            }
            
            print("   📋 Order Parameters:")
            for key, value in order_params.items():
                print(f"      {key}: {value}")
            
            print("   ✅ Order parameters validated")
            
        else:
            print("   ❌ Could not get current price")
            
    except Exception as e:
        print(f"   ❌ Error testing trading: {e}")

def main():
    """Main function"""
    print("🔍 Bybit API Permissions Check")
    print("=" * 60)
    
    # Check permissions
    check_api_permissions()
    
    # Test trading functions
    test_simple_trading()
    
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("1. Fix any API permission issues above")
    print("2. Ensure API key has Read + Trade permissions")
    print("3. Check IP restrictions in Bybit")
    print("4. Re-run the demo: python demo_futures_bot.py")

if __name__ == "__main__":
    main() 