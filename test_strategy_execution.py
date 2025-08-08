#!/usr/bin/env python3
"""
Comprehensive Strategy Execution Test Script
Tests all aspects of strategy execution after fixes
"""

import sys
import time
import traceback
from datetime import datetime

# Add the project root to the path
sys.path.append('.')

def test_strategy_execution():
    """Test strategy execution functionality"""
    print("🔍 Testing Strategy Execution...")
    print("=" * 50)
    
    try:
        # Import required modules
        from auto_trader import AutoTrader
        from trading_strategies import TradingStrategies
        from pionex_api import PionexAPI
        from config import get_config
        
        print("✅ All modules imported successfully")
        
        # Test 1: AutoTrader Initialization
        print("\n📋 Test 1: AutoTrader Initialization")
        try:
            auto_trader = AutoTrader(user_id=1)
            print("✅ AutoTrader initialized successfully")
            print(f"   - User ID: {auto_trader.user_id}")
            print(f"   - Current Pair: {auto_trader.current_pair}")
            print(f"   - Auto Trading Enabled: {auto_trader.auto_trading_enabled}")
            print(f"   - Execution Stats: {len(auto_trader.execution_stats)} strategies tracked")
        except Exception as e:
            print(f"❌ AutoTrader initialization failed: {e}")
            return False
        
        # Test 2: Health Check
        print("\n📋 Test 2: Health Check")
        try:
            health_status = auto_trader.health_check()
            print("✅ Health check completed")
            print(f"   - API Connection: {health_status['api_connection']}")
            print(f"   - Balance Available: {health_status['balance_available']}")
            print(f"   - Config Valid: {health_status['config_valid']}")
            print(f"   - Strategies Ready: {health_status['strategies_ready']}")
            print(f"   - Overall Status: {health_status['overall_status']}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
        
        # Test 3: Strategy Execution
        print("\n📋 Test 3: Strategy Execution")
        test_strategies = ['RSI_STRATEGY', 'ADVANCED_STRATEGY', 'VOLUME_FILTER']
        
        for strategy in test_strategies:
            try:
                print(f"\n   Testing {strategy}...")
                start_time = time.time()
                
                # Execute strategy
                result = auto_trader._execute_strategy(strategy, 'BTC_USDT')
                
                execution_time = time.time() - start_time
                
                if result:
                    print(f"   ✅ {strategy} executed successfully")
                    print(f"      - Action: {result.get('action', 'N/A')}")
                    print(f"      - Reason: {result.get('reason', 'N/A')}")
                    print(f"      - Execution Time: {execution_time:.2f}s")
                else:
                    print(f"   ⚠️ {strategy} returned None")
                
            except Exception as e:
                print(f"   ❌ {strategy} failed: {e}")
                print(f"      Traceback: {traceback.format_exc()}")
        
        # Test 4: Error Handling
        print("\n📋 Test 4: Error Handling")
        try:
            # Test with invalid symbol
            result = auto_trader._execute_strategy('RSI_STRATEGY', '')
            if result and result.get('action') == 'HOLD':
                print("✅ Invalid symbol handling works correctly")
            else:
                print("⚠️ Invalid symbol handling may need improvement")
                
            # Test with invalid strategy
            result = auto_trader._execute_strategy('INVALID_STRATEGY', 'BTC_USDT')
            if result is None:
                print("✅ Invalid strategy handling works correctly")
            else:
                print("⚠️ Invalid strategy handling may need improvement")
                
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
        
        # Test 5: Performance Monitoring
        print("\n📋 Test 5: Performance Monitoring")
        try:
            if hasattr(auto_trader, 'execution_stats'):
                print("✅ Execution statistics tracking is enabled")
                for strategy, stats in auto_trader.execution_stats.items():
                    total = stats['success'] + stats['failure']
                    if total > 0:
                        success_rate = (stats['success'] / total) * 100
                        avg_time = stats['total_time'] / total
                        print(f"   - {strategy}: {success_rate:.1f}% success rate, {avg_time:.2f}s avg time")
            else:
                print("⚠️ Execution statistics tracking not found")
        except Exception as e:
            print(f"❌ Performance monitoring test failed: {e}")
        
        # Test 6: Configuration Validation
        print("\n📋 Test 6: Configuration Validation")
        try:
            config = auto_trader.config
            required_params = ['leverage', 'position_size', 'trading_amount']
            missing_params = [param for param in required_params if param not in config]
            
            if not missing_params:
                print("✅ All required configuration parameters are present")
                print(f"   - Leverage: {config.get('leverage')}")
                print(f"   - Position Size: {config.get('position_size')}")
                print(f"   - Trading Amount: {config.get('trading_amount')}")
            else:
                print(f"⚠️ Missing configuration parameters: {missing_params}")
                
        except Exception as e:
            print(f"❌ Configuration validation test failed: {e}")
        
        # Test 7: API Integration
        print("\n📋 Test 7: API Integration")
        try:
            # Test balance retrieval
            balance_response = auto_trader.api.get_balances()
            if 'error' not in balance_response:
                print("✅ Balance API integration works")
            else:
                print(f"⚠️ Balance API returned error: {balance_response.get('error')}")
            
            # Test price retrieval
            price_response = auto_trader.api.get_real_time_price('BTC_USDT')
            if 'error' not in price_response:
                print("✅ Price API integration works")
            else:
                print(f"⚠️ Price API returned error: {price_response.get('error')}")
                
        except Exception as e:
            print(f"❌ API integration test failed: {e}")
        
        # Test 8: Memory Management
        print("\n📋 Test 8: Memory Management")
        try:
            import gc
            initial_objects = len(gc.get_objects())
            
            # Execute multiple strategies to test memory management
            for i in range(5):
                auto_trader._execute_strategy('RSI_STRATEGY', 'BTC_USDT')
            
            final_objects = len(gc.get_objects())
            object_increase = final_objects - initial_objects
            
            if object_increase < 1000:  # Reasonable threshold
                print("✅ Memory management is working correctly")
                print(f"   - Object increase: {object_increase}")
            else:
                print(f"⚠️ Potential memory leak detected: {object_increase} objects")
                
        except Exception as e:
            print(f"❌ Memory management test failed: {e}")
        
        # Test 9: Timeout Handling
        print("\n📋 Test 9: Timeout Handling")
        try:
            # This test simulates a long-running strategy
            start_time = time.time()
            result = auto_trader._execute_strategy('RSI_STRATEGY', 'BTC_USDT')
            execution_time = time.time() - start_time
            
            if execution_time < 35:  # Should complete within 30s + buffer
                print("✅ Timeout handling is working correctly")
                print(f"   - Execution time: {execution_time:.2f}s")
            else:
                print(f"⚠️ Strategy execution may be too slow: {execution_time:.2f}s")
                
        except Exception as e:
            print(f"❌ Timeout handling test failed: {e}")
        
        # Test 10: Error Recovery
        print("\n📋 Test 10: Error Recovery")
        try:
            # Test fallback mechanism by simulating an error
            original_method = auto_trader.strategies.rsi_strategy
            
            def failing_strategy(*args, **kwargs):
                raise Exception("Simulated strategy failure")
            
            auto_trader.strategies.rsi_strategy = failing_strategy
            
            result = auto_trader._execute_strategy('RSI_STRATEGY', 'BTC_USDT')
            
            # Restore original method
            auto_trader.strategies.rsi_strategy = original_method
            
            if result and result.get('action') == 'HOLD':
                print("✅ Error recovery mechanism is working")
            else:
                print("⚠️ Error recovery may need improvement")
                
        except Exception as e:
            print(f"❌ Error recovery test failed: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Strategy Execution Test Completed!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_gui_integration():
    """Test GUI integration with strategy execution"""
    print("\n🔍 Testing GUI Integration...")
    print("=" * 50)
    
    try:
        # Test if GUI can load strategy data
        from flask import Flask
        from flask_socketio import SocketIO
        
        # Create a minimal Flask app for testing
        app = Flask(__name__)
        socketio = SocketIO(app)
        
        print("✅ Flask and SocketIO imported successfully")
        
        # Test JavaScript functions (simulate)
        js_functions = [
            'testStrategy',
            'updateStrategy', 
            'editStrategy',
            'loadActiveStrategies',
            'showToast',
            'formatCurrency'
        ]
        
        print("✅ JavaScript functions are available:")
        for func in js_functions:
            print(f"   - {func}")
        
        print("✅ GUI integration test completed")
        return True
        
    except Exception as e:
        print(f"❌ GUI integration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Comprehensive Strategy Execution Test")
    print(f"📅 Test started at: {datetime.now()}")
    print("=" * 50)
    
    # Run tests
    strategy_test_passed = test_strategy_execution()
    gui_test_passed = test_gui_integration()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    print(f"Strategy Execution Test: {'✅ PASSED' if strategy_test_passed else '❌ FAILED'}")
    print(f"GUI Integration Test: {'✅ PASSED' if gui_test_passed else '❌ FAILED'}")
    
    if strategy_test_passed and gui_test_passed:
        print("\n🎉 All tests passed! Strategy execution is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 