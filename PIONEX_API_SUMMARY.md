# Pionex API Endpoints Summary

This document provides a quick overview of all available Pionex API endpoints organized by category.

## Base Information

- **Base URL**: `https://api.pionex.com`
- **Authentication**: HMAC SHA256 signature
- **Rate Limit**: 0.1 seconds between requests
- **Documentation**: [Official Pionex API Docs](https://pionex-doc.gitbook.io/apidocs/)

## Account Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/account/balances` | GET | ✅ | Get account balances |
| `/api/v1/account/assets` | GET | ✅ | Get account assets |
| `/api/v1/account/account` | GET | ✅ | Get account information |

## Order Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/trade/order` | POST | ✅ | Place new order |
| `/api/v1/trade/order` | GET | ✅ | Get order status |
| `/api/v1/trade/order` | DELETE | ✅ | Cancel order |
| `/api/v1/trade/openOrders` | GET | ✅ | Get open orders |
| `/api/v1/trade/allOrders` | GET | ✅ | Get all orders |
| `/api/v1/trade/fills` | GET | ✅ | Get order fills |

## Market Data Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/market/klines` | GET | ❌ | Get candlestick data |
| `/api/v1/market/tickers` | GET | ❌ | Get ticker information |
| `/api/v1/market/depth` | GET | ❌ | Get order book depth |
| `/api/v1/market/trades` | GET | ❌ | Get recent trades |
| `/api/v1/market/ticker/24hr` | GET | ❌ | Get 24hr ticker |

## Grid Bot Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/grid/bot` | POST | ✅ | Create grid bot |
| `/api/v1/grid/bot` | GET | ✅ | Get grid bot status |
| `/api/v1/grid/bot` | DELETE | ✅ | Stop grid bot |
| `/api/v1/grid/bots` | GET | ✅ | List grid bots |

## Authentication Headers

```python
headers = {
    'PIONEX-KEY': 'your_api_key',
    'PIONEX-SIGNATURE': 'hmac_sha256_signature',
    'PIONEX-TIMESTAMP': 'timestamp_in_ms'
}
```

## Common Parameters

### Order Parameters
- `symbol`: Trading pair (e.g., "BTC_USDT")
- `side`: "BUY" or "SELL"
- `type`: Order type ("MARKET", "LIMIT", etc.)
- `size`: Order quantity
- `price`: Order price (for limit orders)
- `timeInForce`: "GTC", "IOC", or "FOK"

### Market Data Parameters
- `symbol`: Trading pair
- `interval`: Time interval ("1M", "5M", "1H", etc.)
- `limit`: Number of records to return

### Grid Bot Parameters
- `symbol`: Trading pair
- `gridType`: "ARITHMETIC" or "GEOMETRIC"
- `gridSize`: Number of grid levels
- `priceUpper`: Upper price limit
- `priceLower`: Lower price limit
- `investment`: Total investment amount

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "timestamp": 1640995200000
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": 1001,
    "message": "Error message",
    "details": "Additional details"
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 1001 | Invalid API key |
| 1002 | Invalid signature |
| 1003 | Invalid timestamp |
| 1004 | Rate limit exceeded |
| 1005 | Invalid symbol |
| 1006 | Invalid order type |
| 1007 | Insufficient balance |
| 1008 | Order not found |
| 1009 | Invalid price |
| 1010 | Invalid quantity |

## Rate Limits

- **Default**: 0.1 seconds between requests
- **Retry Attempts**: 3
- **Backoff Multiplier**: 1.5x

## Security Recommendations

1. **IP Whitelisting**: Enable IP whitelisting for enhanced security
2. **API Key Protection**: Never share API keys
3. **Environment Variables**: Store credentials securely
4. **Rate Limiting**: Implement proper rate limiting
5. **Error Handling**: Handle errors gracefully
6. **Logging**: Log API calls for debugging

## Quick Examples

### Get Account Balances
```python
GET /api/v1/account/balances
Headers: PIONEX-KEY, PIONEX-SIGNATURE, PIONEX-TIMESTAMP
```

### Place Market Order
```python
POST /api/v1/trade/order
Body: {
  "symbol": "BTC_USDT",
  "side": "BUY",
  "type": "MARKET",
  "size": "0.001"
}
```

### Get Current Price
```python
GET /api/v1/market/tickers?symbol=BTC_USDT
```

### Get Klines Data
```python
GET /api/v1/market/klines?symbol=BTC_USDT&interval=1H&limit=100
```

## Implementation Notes

- All timestamps are in milliseconds
- Symbol format: "BTC_USDT" (with underscore)
- Quantities should be strings to preserve precision
- Prices should be strings to preserve precision
- Authentication is required for all trading operations
- Market data endpoints do not require authentication

## Official Resources

- [Pionex API Documentation](https://pionex-doc.gitbook.io/apidocs/)
- [Official Telegram Group](https://t.me/pionexapi)
- [Rate Limits](https://pionex-doc.gitbook.io/apidocs/restful/general-info/rate-limit)
- [Authentication](https://pionex-doc.gitbook.io/apidocs/restful/general-info/authentication)

---

*This summary is based on the [official Pionex API documentation](https://pionex-doc.gitbook.io/apidocs/) and the current implementation in this trading bot.* 