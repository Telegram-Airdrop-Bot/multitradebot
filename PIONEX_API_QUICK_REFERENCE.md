# Pionex API Quick Reference

A quick reference guide for the most commonly used Pionex API endpoints with practical examples.

## Base Configuration

```python
import requests
import hmac
import hashlib
import time
import json

# Base URL
BASE_URL = "https://api.pionex.com"

# Authentication headers
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'PionexTradingBot/1.0',
    'PIONEX-KEY': 'your_api_key',
    'PIONEX-SIGNATURE': 'generated_signature',
    'PIONEX-TIMESTAMP': 'timestamp_in_ms'
}
```

## Authentication Helper

```python
def generate_signature(method, endpoint, params, secret_key):
    """Generate HMAC SHA256 signature for Pionex API"""
    timestamp = str(int(time.time() * 1000))
    params['timestamp'] = timestamp
    
    # Sort parameters alphabetically
    sorted_items = sorted(params.items())
    query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
    
    # Create signature string
    sign_str = f"{method.upper()}{endpoint}?{query_string}"
    
    # Generate signature
    signature = hmac.new(
        secret_key.encode('utf-8'),
        sign_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return signature, timestamp
```

## Account Endpoints

### Get Account Balances

```python
def get_balances(api_key, secret_key):
    endpoint = '/api/v1/account/balances'
    params = {}
    
    signature, timestamp = generate_signature('GET', endpoint, params, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
    return response.json()

# Example usage
balances = get_balances('your_api_key', 'your_secret_key')
print(balances)
```

### Get Account Info

```python
def get_account_info(api_key, secret_key):
    endpoint = '/api/v1/account/account'
    params = {}
    
    signature, timestamp = generate_signature('GET', endpoint, params, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
    return response.json()
```

## Order Endpoints

### Place Market Order

```python
def place_market_order(api_key, secret_key, symbol, side, quantity):
    endpoint = '/api/v1/trade/order'
    params = {
        'symbol': symbol,
        'side': side.upper(),
        'type': 'MARKET',
        'size': str(quantity)
    }
    
    signature, timestamp = generate_signature('POST', endpoint, params, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=params)
    return response.json()

# Example usage
order = place_market_order('your_api_key', 'your_secret_key', 'BTC_USDT', 'BUY', 0.001)
print(order)
```

### Place Limit Order

```python
def place_limit_order(api_key, secret_key, symbol, side, quantity, price):
    endpoint = '/api/v1/trade/order'
    params = {
        'symbol': symbol,
        'side': side.upper(),
        'type': 'LIMIT',
        'size': str(quantity),
        'price': str(price),
        'timeInForce': 'GTC'
    }
    
    signature, timestamp = generate_signature('POST', endpoint, params, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=params)
    return response.json()

# Example usage
order = place_limit_order('your_api_key', 'your_secret_key', 'BTC_USDT', 'BUY', 0.001, 50000.00)
print(order)
```

### Get Order Status

```python
def get_order(api_key, secret_key, order_id, symbol):
    endpoint = '/api/v1/trade/order'
    params = {
        'orderId': order_id,
        'symbol': symbol
    }
    
    signature, timestamp = generate_signature('GET', endpoint, params, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
    return response.json()

# Example usage
order_status = get_order('your_api_key', 'your_secret_key', 123456789, 'BTC_USDT')
print(order_status)
```

### Cancel Order

```python
def cancel_order(api_key, secret_key, order_id, symbol):
    endpoint = '/api/v1/trade/order'
    params = {
        'orderId': order_id,
        'symbol': symbol
    }
    
    signature, timestamp = generate_signature('DELETE', endpoint, params, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers, params=params)
    return response.json()

# Example usage
result = cancel_order('your_api_key', 'your_secret_key', 123456789, 'BTC_USDT')
print(result)
```

### Get Open Orders

```python
def get_open_orders(api_key, secret_key, symbol=None):
    endpoint = '/api/v1/trade/openOrders'
    params = {}
    if symbol:
        params['symbol'] = symbol
    
    signature, timestamp = generate_signature('GET', endpoint, params, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
    return response.json()

# Example usage
open_orders = get_open_orders('your_api_key', 'your_secret_key', 'BTC_USDT')
print(open_orders)
```

## Market Data Endpoints

### Get Current Price

```python
def get_current_price(symbol):
    endpoint = '/api/v1/market/tickers'
    params = {'symbol': symbol}
    
    response = requests.get(f"{BASE_URL}{endpoint}", params=params)
    data = response.json()
    
    if 'data' in data and 'tickers' in data['data']:
        for ticker in data['data']['tickers']:
            if ticker.get('symbol') == symbol:
                return float(ticker.get('lastPrice', 0))
    return None

# Example usage
price = get_current_price('BTC_USDT')
print(f"Current BTC price: ${price}")
```

### Get Klines/Candlestick Data

```python
def get_klines(symbol, interval='1M', limit=100):
    endpoint = '/api/v1/market/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    
    response = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return response.json()

# Example usage
klines = get_klines('BTC_USDT', '1H', 24)  # Last 24 hours of hourly data
print(klines)
```

### Get Order Book

```python
def get_order_book(symbol, limit=20):
    endpoint = '/api/v1/market/depth'
    params = {
        'symbol': symbol,
        'limit': limit
    }
    
    response = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return response.json()

# Example usage
order_book = get_order_book('BTC_USDT', 10)
print(order_book)
```

### Get Recent Trades

```python
def get_recent_trades(symbol, limit=50):
    endpoint = '/api/v1/market/trades'
    params = {
        'symbol': symbol,
        'limit': limit
    }
    
    response = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return response.json()

# Example usage
trades = get_recent_trades('BTC_USDT', 10)
print(trades)
```

## Grid Bot Endpoints

### Create Grid Bot

```python
def create_grid_bot(api_key, secret_key, symbol, grid_params):
    endpoint = '/api/v1/grid/bot'
    params = {
        'symbol': symbol,
        **grid_params
    }
    
    signature, timestamp = generate_signature('POST', endpoint, params, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=params)
    return response.json()

# Example usage
grid_params = {
    'gridType': 'ARITHMETIC',
    'gridSize': 10,
    'priceUpper': '51000.00',
    'priceLower': '49000.00',
    'investment': '1000.00',
    'gridSpacing': '200.00'
}

grid_bot = create_grid_bot('your_api_key', 'your_secret_key', 'BTC_USDT', grid_params)
print(grid_bot)
```

### Get Grid Bot Status

```python
def get_grid_bot(api_key, secret_key, grid_id):
    endpoint = '/api/v1/grid/bot'
    params = {'gridId': grid_id}
    
    signature, timestamp = generate_signature('GET', endpoint, params, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'PIONEX-KEY': api_key,
        'PIONEX-SIGNATURE': signature,
        'PIONEX-TIMESTAMP': timestamp
    }
    
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
    return response.json()

# Example usage
grid_status = get_grid_bot('your_api_key', 'your_secret_key', 'grid-123456789')
print(grid_status)
```

## Error Handling

```python
def handle_api_response(response):
    """Handle API response and common errors"""
    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            print(f"API Error: {data['error']}")
            return None
        return data
    else:
        print(f"HTTP Error: {response.status_code} - {response.text}")
        return None

# Example usage
response = requests.get(f"{BASE_URL}/api/v1/market/tickers")
result = handle_api_response(response)
if result:
    print("Success:", result)
```

## Rate Limiting

```python
import time

class RateLimiter:
    def __init__(self, delay=0.1):
        self.delay = delay
        self.last_request = 0
    
    def wait(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request
        if time_since_last < self.delay:
            sleep_time = self.delay - time_since_last
            time.sleep(sleep_time)
        self.last_request = time.time()

# Example usage
rate_limiter = RateLimiter(0.1)  # 100ms between requests

def api_call_with_rate_limit():
    rate_limiter.wait()
    # Make your API call here
    response = requests.get(f"{BASE_URL}/api/v1/market/tickers")
    return response.json()
```

## Complete Example

```python
import requests
import hmac
import hashlib
import time
import json

class PionexAPIClient:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://api.pionex.com"
        self.rate_limiter = RateLimiter(0.1)
    
    def _generate_signature(self, method, endpoint, params):
        timestamp = str(int(time.time() * 1000))
        params['timestamp'] = timestamp
        
        sorted_items = sorted(params.items())
        query_string = '&'.join(f'{k}={v}' for k, v in sorted_items)
        
        sign_str = f"{method.upper()}{endpoint}?{query_string}"
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature, timestamp
    
    def _make_request(self, method, endpoint, params=None, signed=False):
        self.rate_limiter.wait()
        
        if params is None:
            params = {}
        
        headers = {'Content-Type': 'application/json'}
        
        if signed:
            signature, timestamp = self._generate_signature(method, endpoint, params)
            headers.update({
                'PIONEX-KEY': self.api_key,
                'PIONEX-SIGNATURE': signature,
                'PIONEX-TIMESTAMP': timestamp
            })
        
        if method == 'GET':
            response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(f"{self.base_url}{endpoint}", headers=headers, json=params)
        elif method == 'DELETE':
            response = requests.delete(f"{self.base_url}{endpoint}", headers=headers, params=params)
        
        return handle_api_response(response)
    
    def get_balances(self):
        return self._make_request('GET', '/api/v1/account/balances', signed=True)
    
    def place_market_order(self, symbol, side, quantity):
        params = {
            'symbol': symbol,
            'side': side.upper(),
            'type': 'MARKET',
            'size': str(quantity)
        }
        return self._make_request('POST', '/api/v1/trade/order', params, signed=True)
    
    def get_current_price(self, symbol):
        params = {'symbol': symbol}
        return self._make_request('GET', '/api/v1/market/tickers', params)

# Example usage
client = PionexAPIClient('your_api_key', 'your_secret_key')

# Get account balances
balances = client.get_balances()
print("Balances:", balances)

# Get current price
price = client.get_current_price('BTC_USDT')
print("BTC Price:", price)

# Place a market order
order = client.place_market_order('BTC_USDT', 'BUY', 0.001)
print("Order:", order)
```

## Common Parameters

### Order Types
- `MARKET`: Market order
- `LIMIT`: Limit order
- `STOP_MARKET`: Stop market order
- `STOP_LIMIT`: Stop limit order

### Sides
- `BUY`: Buy order
- `SELL`: Sell order

### Time In Force
- `GTC`: Good Till Canceled
- `IOC`: Immediate Or Cancel
- `FOK`: Fill Or Kill

### Intervals
- `1M`: 1 minute
- `5M`: 5 minutes
- `15M`: 15 minutes
- `30M`: 30 minutes
- `1H`: 1 hour
- `4H`: 4 hours
- `1D`: 1 day

## Security Notes

1. **Never share your API keys**
2. **Use environment variables for credentials**
3. **Implement IP whitelisting**
4. **Handle errors gracefully**
5. **Implement proper rate limiting**
6. **Log API calls for debugging**

---

*This quick reference is based on the [official Pionex API documentation](https://pionex-doc.gitbook.io/apidocs/) and the current implementation in this trading bot.* 