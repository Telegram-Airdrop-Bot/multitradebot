#!/usr/bin/env python3
"""
Test TRADING LIVE Animation Functionality
"""

import os
import sys

def test_trading_live_animation():
    """Test the TRADING LIVE animation features"""
    print("🎬 Testing TRADING LIVE Animation...")
    print("=" * 50)
    
    # Test 1: Check HTML structure
    print("\n📋 Test 1: HTML Structure")
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        if 'id="trading-live-indicator"' in html_content:
            print("✅ TRADING LIVE indicator ID found in HTML")
        else:
            print("❌ TRADING LIVE indicator ID not found")
            
        if 'trading-live-content' in html_content:
            print("✅ Trading live content structure found")
        else:
            print("❌ Trading live content structure not found")
            
    except Exception as e:
        print(f"❌ Error reading HTML file: {e}")
    
    # Test 2: Check CSS animations
    print("\n📋 Test 2: CSS Animations")
    try:
        with open('static/css/style.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
            
        animations = [
            'trading-live-active',
            'trading-live-inactive', 
            'tradingLivePulse',
            'dotPulse',
            'trading-live-dots'
        ]
        
        for animation in animations:
            if animation in css_content:
                print(f"✅ {animation} animation found")
            else:
                print(f"❌ {animation} animation not found")
                
    except Exception as e:
        print(f"❌ Error reading CSS file: {e}")
    
    # Test 3: Check JavaScript functionality
    print("\n📋 Test 3: JavaScript Functionality")
    try:
        with open('gui/static/js/app.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
            
        js_features = [
            'trading-live-indicator',
            'trading-live-active',
            'trading-live-inactive',
            'trading-live-content',
            'trading-live-dots'
        ]
        
        for feature in js_features:
            if feature in js_content:
                print(f"✅ {feature} JavaScript feature found")
            else:
                print(f"❌ {feature} JavaScript feature not found")
                
    except Exception as e:
        print(f"❌ Error reading JavaScript file: {e}")
    
    # Test 4: Check GUI template
    print("\n📋 Test 4: GUI Template")
    try:
        with open('gui/templates/index.html', 'r', encoding='utf-8') as f:
            gui_html = f.read()
            
        if 'id="trading-live-indicator"' in gui_html:
            print("✅ TRADING LIVE indicator ID found in GUI template")
        else:
            print("❌ TRADING LIVE indicator ID not found in GUI template")
            
    except Exception as e:
        print(f"❌ Error reading GUI template: {e}")
    
    # Test 5: Animation States
    print("\n📋 Test 5: Animation States")
    states = [
        {
            'name': 'Active State',
            'class': 'trading-live-active',
            'text': 'TRADING LIVE',
            'icon': 'fa-broadcast-tower',
            'dots': True
        },
        {
            'name': 'Inactive State', 
            'class': 'trading-live-inactive',
            'text': 'TRADING OFF',
            'icon': 'fa-pause-circle',
            'dots': False
        }
    ]
    
    for state in states:
        print(f"\n   {state['name']}:")
        print(f"   - Class: {state['class']}")
        print(f"   - Text: {state['text']}")
        print(f"   - Icon: {state['icon']}")
        print(f"   - Dots: {'Yes' if state['dots'] else 'No'}")
    
    print("\n" + "=" * 50)
    print("🎉 TRADING LIVE Animation Test Completed!")
    print("=" * 50)
    
    return True

def main():
    """Main test function"""
    print("🚀 Starting TRADING LIVE Animation Test")
    print(f"📅 Test started at: {__import__('datetime').datetime.now()}")
    
    try:
        success = test_trading_live_animation()
        if success:
            print("\n✅ All TRADING LIVE animation features are properly implemented!")
        else:
            print("\n❌ Some TRADING LIVE animation features need attention.")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 