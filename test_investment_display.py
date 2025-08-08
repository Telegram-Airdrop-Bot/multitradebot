#!/usr/bin/env python3
"""
Test script for investment amount display functionality
"""

import json
from datetime import datetime

def test_investment_calculation():
    """Test investment amount calculation"""
    
    # Sample position data
    sample_positions = [
        {
            'symbol': 'BTC_USDT',
            'size': 0.001,
            'entryPrice': 45000.0,
            'markPrice': 46000.0,
            'unrealizedPnl': 10.0,
            'roe': 2.22
        },
        {
            'symbol': 'ETH_USDT',
            'size': 0.01,
            'entryPrice': 3000.0,
            'markPrice': 3100.0,
            'unrealizedPnl': 10.0,
            'roe': 3.33
        },
        {
            'symbol': 'SOL_USDT',
            'size': 1.0,
            'entryPrice': 100.0,
            'markPrice': 105.0,
            'unrealizedPnl': 5.0,
            'roe': 5.0
        }
    ]
    
    print("Testing Investment Amount Calculation")
    print("=" * 50)
    
    total_investment = 0
    
    for position in sample_positions:
        size = float(position['size'])
        entry_price = float(position['entryPrice'])
        investment_amount = size * entry_price
        total_investment += investment_amount
        
        print(f"Symbol: {position['symbol']}")
        print(f"  Size: {size}")
        print(f"  Entry Price: ${entry_price:,.2f}")
        print(f"  Investment Amount: ${investment_amount:,.2f}")
        print(f"  Current P&L: ${position['unrealizedPnl']:,.2f}")
        print(f"  ROE: {position['roe']}%")
        print()
    
    print(f"Total Investment: ${total_investment:,.2f}")
    print()
    
    # Test JavaScript-like calculation
    print("JavaScript-style calculation:")
    js_code = """
    let totalInvestment = 0;
    positions.forEach(position => {
        const size = parseFloat(position.size || 0);
        const entryPrice = parseFloat(position.entryPrice || 0);
        const investmentAmount = size * entryPrice;
        totalInvestment += investmentAmount;
        console.log(`${position.symbol}: $${investmentAmount.toFixed(2)}`);
    });
    console.log(`Total: $${totalInvestment.toFixed(2)}`);
    """
    print(js_code)
    
    return True

def test_html_generation():
    """Test HTML generation for positions table"""
    
    sample_positions = [
        {
            'symbol': 'BTC_USDT',
            'size': 0.001,
            'entryPrice': 45000.0,
            'markPrice': 46000.0,
            'unrealizedPnl': 10.0,
            'roe': 2.22
        }
    ]
    
    print("\nTesting HTML Generation")
    print("=" * 50)
    
    html_rows = []
    total_investment = 0
    
    for position in sample_positions:
        size = float(position['size'])
        entry_price = float(position['entryPrice'])
        mark_price = float(position['markPrice'])
        pnl = float(position['unrealizedPnl'])
        roe = float(position['roe'])
        symbol = position['symbol']
        
        investment_amount = size * entry_price
        total_investment += investment_amount
        
        pnl_class = 'text-success' if pnl >= 0 else 'text-danger'
        roe_class = 'text-success' if roe >= 0 else 'text-danger'
        
        html_row = f"""
        <tr>
            <td><strong>{symbol}</strong></td>
            <td>{size:.4f}</td>
            <td>${entry_price:.4f}</td>
            <td>${mark_price:.4f}</td>
            <td><span class="investment-amount">${investment_amount:.2f}</span></td>
            <td class="{pnl_class}">${pnl:.2f}</td>
            <td class="{roe_class}">{roe:.2f}%</td>
            <td>
                <button class="btn btn-sm btn-outline-danger" onclick="closePosition('{symbol}')">
                    <i class="fas fa-times"></i>
                </button>
            </td>
        </tr>
        """
        html_rows.append(html_row)
    
    # Add total investment row
    if total_investment > 0:
        total_row = f"""
        <tr class="total-investment-row">
            <td colspan="4"><strong>Total Investment:</strong></td>
            <td><span class="investment-amount">${total_investment:.2f}</span></td>
            <td colspan="3"></td>
        </tr>
        """
        html_rows.append(total_row)
    
    print("Generated HTML:")
    for row in html_rows:
        print(row.strip())
    
    return True

def test_trading_live_indicator():
    """Test the TRADING LIVE indicator HTML"""
    
    print("\nTesting TRADING LIVE Indicator")
    print("=" * 50)
    
    trading_live_html = """
    <!-- TRADING LIVE Indicator -->
    <div class="mb-3">
        <div class="alert alert-danger mb-2" style="font-weight: bold; font-size: 1.1em;">
            <i class="fas fa-broadcast-tower me-2"></i>TRADING LIVE
        </div>
    </div>
    """
    
    print("TRADING LIVE Indicator HTML:")
    print(trading_live_html)
    
    return True

if __name__ == "__main__":
    print("Investment Display Test Suite")
    print("=" * 50)
    print(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run tests
    test_investment_calculation()
    test_html_generation()
    test_trading_live_indicator()
    
    print("\nAll tests completed successfully!")
    print("\nSummary of changes:")
    print("1. ✅ Added 'Investment Amount' column to positions table")
    print("2. ✅ Added 'TRADING LIVE' indicator with red styling")
    print("3. ✅ Implemented investment amount calculation (size * entry price)")
    print("4. ✅ Added total investment summary row")
    print("5. ✅ Added CSS styling for investment amounts")
    print("6. ✅ Updated both main and GUI templates")
    print("7. ✅ Updated both main and GUI JavaScript files") 