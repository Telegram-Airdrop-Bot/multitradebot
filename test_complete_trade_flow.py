#!/usr/bin/env python3
"""
Complete Trade Flow Test
Test the complete trading flow with order placement and status checking
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pionex_api import PionexAPI

# Load environment variables
load_dotenv()

def test_complete_trade_flow():
    """Test the complete trading flow"""
    
    print("🚀 Complete Trade Flow Test")
    print("=" * 50)
    
    # Initialize API
    api = PionexAPI()
    
    # Test parameters
    symbol = "BTC_USDT"
    side = "BUY"
    quantity = 0.0001  # Very small amount
    order_type = "MARKET"
    client_order_id = f"test_{int(time.time())}"
    
    print(f"📊 Trade Parameters:")
    print(f"   Symbol: {symbol}")
    print(f"   Side: {side}")
    print(f"   Quantity: {quantity} BTC")
    print(f"   Order Type: {order_type}")
    print(f"   Client Order ID: {client_order_id}")
    print()
    
    try:
        # Step 1: Check balance
        print("💰 Checking Balance...")
        balance_response = api.get_account_balance()
        print(f"   Balance: {balance_response}")
        
        if 'error' in balance_response:
            print("   ❌ Failed to get balance")
            return
        
        available_balance = float(balance_response.get('available', 0))
        print(f"   Available Balance: ${available_balance:.2f} USDT")
        print()
        
        # Step 2: Get current price
        print("📈 Getting Current Price...")
        market_data = api.get_real_time_market_data(symbol)
        print(f"   Market Data: {market_data}")
        
        if 'error' in market_data:
            print("   ❌ Failed to get market data")
            return
        
        current_price = float(market_data.get('price', 0))
        print(f"   Current Price: ${current_price:,.2f}")
        print()
        
        # Step 3: Calculate estimated cost
        estimated_cost = quantity * current_price
        print(f"💵 Estimated Cost: ${estimated_cost:.4f}")
        print()
        
        # Step 4: Check if we have enough balance
        if available_balance < estimated_cost:
            print(f"❌ Insufficient balance. Need ${estimated_cost:.4f}, have ${available_balance:.2f}")
            return
        
        print("✅ Sufficient balance for trade")
        print()
        
        # Step 5: Place the order with client order ID
        print("🔄 Placing Order...")
        trade_params = {
            'symbol': symbol,
            'side': side,
            'order_type': order_type,
            'quantity': quantity,
            'client_order_id': client_order_id
        }
        
        print(f"   Trade Parameters: {trade_params}")
        
        # Place the order
        trade_response = api.place_order(**trade_params)
        print(f"   Trade Response: {trade_response}")
        
        if 'error' in trade_response:
            print(f"   ❌ Trade failed: {trade_response['error']}")
            print(f"   Error code: {trade_response.get('code', 'N/A')}")
            
            # Even if trade fails, let's show what we would do if it succeeded
            print()
            print("📋 Demonstrating order status checking flow:")
            print("   (This would work if the order was placed successfully)")
            
            # Simulate order status checking
            print("   🔍 Checking order by client order ID...")
            print(f"   Client Order ID: {client_order_id}")
            print("   Expected API call: GET /api/v1/trade/orderByClientOrderId")
            print("   Expected response format:")
            print("   {")
            print("     'data': {")
            print("       'orderId': 1234567890,")
            print("       'symbol': 'BTC_USDT',")
            print("       'type': 'MARKET',")
            print("       'side': 'BUY',")
            print("       'size': '0.0001',")
            print("       'status': 'CLOSED',")
            print("       'clientOrderId': '" + client_order_id + "',")
            print("       'createTime': 1566676132311,")
            print("       'updateTime': 1566676132311")
            print("     },")
            print("     'result': true")
            print("   }")
            
        else:
            print("   ✅ Order placed successfully!")
            
            # Get order details
            if 'data' in trade_response:
                order_data = trade_response['data']
                order_id = order_data.get('orderId')
                client_order_id = order_data.get('clientOrderId')
                
                print(f"   Order ID: {order_id}")
                print(f"   Client Order ID: {client_order_id}")
                
                # Check order status by client order ID
                print("   📊 Checking order status by client order ID...")
                status_response = api.get_order_by_client_order_id(client_order_id, symbol)
                print(f"   Order Status: {status_response}")
                
                if 'data' in status_response:
                    status_data = status_response['data']
                    print(f"   Order Status: {status_data.get('status', 'UNKNOWN')}")
                    print(f"   Filled Size: {status_data.get('filledSize', '0')}")
                    print(f"   Filled Amount: {status_data.get('filledAmount', '0')}")
                    print(f"   Fee: {status_data.get('fee', '0')} {status_data.get('feeCoin', '')}")
        
        print()
        
        # Step 6: Check updated balance
        print("💰 Checking Updated Balance...")
        updated_balance = api.get_account_balance()
        print(f"   Updated Balance: {updated_balance}")
        
    except Exception as e:
        print(f"❌ Error during trade flow test: {e}")
        import traceback
        traceback.print_exc()

def demonstrate_api_capabilities():
    """Demonstrate all API capabilities"""
    
    print("\n🔧 API Capabilities Demonstration")
    print("=" * 50)
    
    api = PionexAPI()
    
    # Test 1: Account balance
    print("1. 📊 Account Balance")
    balance = api.get_account_balance()
    print(f"   Result: {balance}")
    print()
    
    # Test 2: Market data
    print("2. 📈 Market Data")
    market_data = api.get_real_time_market_data("BTC_USDT")
    print(f"   Result: {market_data}")
    print()
    
    # Test 3: Live trades
    print("3. 🔄 Live Trades")
    trades = api.get_live_trades("BTC_USDT", 5)
    print(f"   Result: {trades}")
    print()
    
    # Test 4: Market depth
    print("4. 📊 Market Depth")
    depth = api.get_market_depth("BTC_USDT", 5)
    print(f"   Result: {depth}")
    print()
    
    # Test 5: 24hr ticker
    print("5. 📊 24hr Ticker")
    ticker = api.get_24hr_ticker("BTC_USDT")
    print(f"   Result: {ticker}")
    print()
    
    # Test 6: Klines
    print("6. 📈 Klines Data")
    klines = api.get_klines_realtime("BTC_USDT", "1m", 5)
    print(f"   Result: {klines}")
    print()

if __name__ == "__main__":
    print("🎯 Pionex Trading Bot - Complete Trade Flow Test")
    print("=" * 50)
    print()
    
    # Check if API credentials are set
    api_key = os.getenv('PIONEX_API_KEY')
    api_secret = os.getenv('PIONEX_SECRET_KEY')
    
    if not api_key or not api_secret:
        print("❌ Missing API credentials!")
        print("Please set PIONEX_API_KEY and PIONEX_SECRET_KEY in your .env file")
        sys.exit(1)
    
    print("✅ API credentials found")
    print()
    
    # Run the complete trade flow test
    test_complete_trade_flow()
    
    # Demonstrate API capabilities
    demonstrate_api_capabilities() 