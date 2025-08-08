#!/usr/bin/env python3
"""
Quick Trade Test
Test the fixed timestamp issue with a small trade
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pionex_api import PionexAPI

# Load environment variables
load_dotenv()

def test_small_trade():
    """Test a small trade with the fixed timestamp"""
    
    print("🚀 Quick Trade Test with Fixed Timestamp")
    print("=" * 50)
    
    # Initialize API
    api = PionexAPI()
    
    # Test parameters
    symbol = "BTC_USDT"
    side = "BUY"
    quantity = 0.0001  # Very small amount
    order_type = "MARKET"
    
    print(f"📊 Trade Parameters:")
    print(f"   Symbol: {symbol}")
    print(f"   Side: {side}")
    print(f"   Quantity: {quantity} BTC")
    print(f"   Order Type: {order_type}")
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
        
        # Step 5: Execute the trade
        print("🔄 Executing Trade...")
        trade_params = {
            'symbol': symbol,
            'side': side,
            'order_type': order_type,
            'quantity': quantity  # Keep 'quantity' for function parameter
        }
        
        print(f"   Trade Parameters: {trade_params}")
        
        # Execute the trade
        trade_response = api.place_order(**trade_params)
        print(f"   Trade Response: {trade_response}")
        
        if 'error' in trade_response:
            print(f"   ❌ Trade failed: {trade_response['error']}")
        else:
            print("   ✅ Trade executed successfully!")
            
            # Get order details
            if 'data' in trade_response and 'orderId' in trade_response['data']:
                order_id = trade_response['data']['orderId']
                print(f"   Order ID: {order_id}")
                
                # Check order status
                print("   📊 Checking order status...")
                status_response = api.get_order(order_id, symbol)
                print(f"   Order Status: {status_response}")
        
        print()
        
        # Step 6: Check updated balance
        print("💰 Checking Updated Balance...")
        updated_balance = api.get_account_balance()
        print(f"   Updated Balance: {updated_balance}")
        
    except Exception as e:
        print(f"❌ Error during trade test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🎯 Pionex Trading Bot - Quick Trade Test")
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
    
    # Run the test
    test_small_trade() 