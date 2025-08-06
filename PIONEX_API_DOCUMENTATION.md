# Pionex API Documentation

This document provides a comprehensive overview of the Pionex API endpoints, their parameters, and response formats based on the [official Pionex API documentation](https://pionex-doc.gitbook.io/apidocs/) and the current implementation in this trading bot.

## Table of Contents

1. [Authentication](#authentication)
2. [Rate Limits](#rate-limits)
3. [Base URL](#base-url)
4. [Account Endpoints](#account-endpoints)
5. [Order Endpoints](#order-endpoints)
6. [Market Data Endpoints](#market-data-endpoints)
7. [Grid Bot Endpoints](#grid-bot-endpoints)
8. [Error Handling](#error-handling)
9. [Response Formats](#response-formats)

## Authentication

Pionex API uses HMAC SHA256 signature authentication. The following headers are required for authenticated requests:

- `PIONEX-KEY`: Your API key
- `PIONEX-SIGNATURE`: HMAC SHA256 signature
- `PIONEX-TIMESTAMP`: Current timestamp in milliseconds

### Signature Generation

```python
# Method: UPPER(method) + endpoint + ? + sorted_query_string
sign_str = f"{method.upper()}{endpoint}?{query_string}"
signature = hmac.new(secret_key.encode('utf-8'), sign_str.encode('utf-8'), hashlib.sha256).hexdigest()
```

## Rate Limits

- Default rate limit: 0.1 seconds between requests
- Maximum retry attempts: 3
- Backoff multiplier: 1.5x

## Base URL

```
https://api.pionex.com
```

## Account Endpoints

### Get Account Balances

**Endpoint:** `GET /api/v1/account/balances`

**Authentication:** Required

**Parameters:** None

**Response Format:**
```json
{
  "success": true,
  "data": {
    "balances": [
      {
        "currency": "BTC",
        "available": 1.23456789,
        "locked": 0.0,
        "total": 1.23456789
      }
    ],
    "total_count": 1
  }
}
```

### Get Account Assets

**Endpoint:** `GET /api/v1/account/assets`

**Authentication:** Required

**Parameters:** None

**Response Format:**
```json
{
  "success": true,
  "data": {
    "assets": [
      {
        "coin": "BTC",
        "free": "1.23456789",
        "frozen": "0.0"
      }
    ]
  }
}
```

### Get Account Info

**Endpoint:** `GET /api/v1/account/account`

**Authentication:** Required

**Parameters:** None

**Response Format:**
```json
{
  "success": true,
  "data": {
    "accountId": "123456789",
    "accountType": "SPOT",
    "permissions": ["SPOT", "MARGIN"]
  }
}
```

## Order Endpoints

### Place Order

**Endpoint:** `POST /api/v1/trade/order`

**Authentication:** Required

**Parameters:**
```json
{
  "clientOrderId": "uuid-string",
  "symbol": "BTC_USDT",
  "side": "BUY",
  "type": "LIMIT",
  "size": "0.001",
  "price": "50000.00",
  "stopLoss": "49000.00",
  "takeProfit": "51000.00",
  "timeInForce": "GTC",
  "leverage": 10,
  "marginType": "ISOLATED",
  "positionSide": "LONG",
  "reduceOnly": false,
  "postOnly": false,
  "icebergQty": "0.0005",
  "workingType": "MARK_PRICE",
  "priceProtect": false,
  "activationPrice": "49000.00",
  "callbackRate": "1.0"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "orderId": 123456789,
    "clientOrderId": "uuid-string",
    "symbol": "BTC_USDT",
    "side": "BUY",
    "type": "LIMIT",
    "size": "0.001",
    "price": "50000.00",
    "status": "NEW",
    "timeInForce": "GTC",
    "createTime": 1640995200000
  }
}
```

### Get Order

**Endpoint:** `GET /api/v1/trade/order`

**Authentication:** Required

**Parameters:**
```json
{
  "orderId": 123456789,
  "symbol": "BTC_USDT"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "orderId": 123456789,
    "clientOrderId": "uuid-string",
    "symbol": "BTC_USDT",
    "side": "BUY",
    "type": "LIMIT",
    "size": "0.001",
    "price": "50000.00",
    "status": "FILLED",
    "timeInForce": "GTC",
    "createTime": 1640995200000,
    "updateTime": 1640995210000,
    "fills": [
      {
        "price": "50000.00",
        "size": "0.001",
        "commission": "0.000001",
        "commissionAsset": "BTC"
      }
    ]
  }
}
```

### Cancel Order

**Endpoint:** `DELETE /api/v1/trade/order`

**Authentication:** Required

**Parameters:**
```json
{
  "orderId": 123456789,
  "symbol": "BTC_USDT"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "orderId": 123456789,
    "clientOrderId": "uuid-string",
    "symbol": "BTC_USDT",
    "status": "CANCELED"
  }
}
```

### Get Open Orders

**Endpoint:** `GET /api/v1/trade/openOrders`

**Authentication:** Required

**Parameters:**
```json
{
  "symbol": "BTC_USDT"  // Optional
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "orders": [
      {
        "orderId": 123456789,
        "clientOrderId": "uuid-string",
        "symbol": "BTC_USDT",
        "side": "BUY",
        "type": "LIMIT",
        "size": "0.001",
        "price": "50000.00",
        "status": "NEW",
        "timeInForce": "GTC",
        "createTime": 1640995200000
      }
    ]
  }
}
```

### Get All Orders

**Endpoint:** `GET /api/v1/trade/allOrders`

**Authentication:** Required

**Parameters:**
```json
{
  "symbol": "BTC_USDT",  // Optional
  "limit": 100
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "orders": [
      {
        "orderId": 123456789,
        "clientOrderId": "uuid-string",
        "symbol": "BTC_USDT",
        "side": "BUY",
        "type": "LIMIT",
        "size": "0.001",
        "price": "50000.00",
        "status": "FILLED",
        "timeInForce": "GTC",
        "createTime": 1640995200000,
        "updateTime": 1640995210000
      }
    ]
  }
}
```

### Get Fills

**Endpoint:** `GET /api/v1/trade/fills`

**Authentication:** Required

**Parameters:**
```json
{
  "symbol": "BTC_USDT",  // Optional
  "orderId": 123456789   // Optional
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "fills": [
      {
        "orderId": 123456789,
        "symbol": "BTC_USDT",
        "price": "50000.00",
        "size": "0.001",
        "commission": "0.000001",
        "commissionAsset": "BTC",
        "time": 1640995210000
      }
    ]
  }
}
```

## Market Data Endpoints

### Get Klines/Candlestick Data

**Endpoint:** `GET /api/v1/market/klines`

**Authentication:** Not required

**Parameters:**
```json
{
  "symbol": "BTC_USDT",
  "interval": "1M",  // 1M, 5M, 15M, 30M, 1H, 4H, 8H, 12H, 1D
  "limit": 100
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "klines": [
      [
        1640995200000,  // Open time
        "50000.00",     // Open price
        "50100.00",     // High price
        "49900.00",     // Low price
        "50050.00",     // Close price
        "100.5",        // Volume
        1640995260000,  // Close time
        "5025000.00",   // Quote asset volume
        100,            // Number of trades
        "50.00",        // Taker buy base asset volume
        "50.50"         // Taker buy quote asset volume
      ]
    ]
  }
}
```

### Get Ticker Information

**Endpoint:** `GET /api/v1/market/tickers`

**Authentication:** Not required

**Parameters:**
```json
{
  "symbol": "BTC_USDT"  // Optional
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "tickers": [
      {
        "symbol": "BTC_USDT",
        "priceChange": "100.00",
        "priceChangePercent": "2.00",
        "weightedAvgPrice": "50000.00",
        "prevClosePrice": "49900.00",
        "lastPrice": "50000.00",
        "lastQty": "0.001",
        "bidPrice": "49999.00",
        "bidQty": "0.001",
        "askPrice": "50001.00",
        "askQty": "0.001",
        "openPrice": "49900.00",
        "highPrice": "50100.00",
        "lowPrice": "49900.00",
        "volume": "100.5",
        "quoteVolume": "5025000.00",
        "openTime": 1640995200000,
        "closeTime": 1640995260000,
        "firstId": 123456789,
        "lastId": 123456790,
        "count": 2
      }
    ]
  }
}
```

### Get Order Book Depth

**Endpoint:** `GET /api/v1/market/depth`

**Authentication:** Not required

**Parameters:**
```json
{
  "symbol": "BTC_USDT",
  "limit": 100
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "lastUpdateId": 123456789,
    "bids": [
      ["49999.00", "0.001"],
      ["49998.00", "0.002"]
    ],
    "asks": [
      ["50001.00", "0.001"],
      ["50002.00", "0.002"]
    ]
  }
}
```

### Get Recent Trades

**Endpoint:** `GET /api/v1/market/trades`

**Authentication:** Not required

**Parameters:**
```json
{
  "symbol": "BTC_USDT",
  "limit": 100
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "trades": [
      {
        "id": 123456789,
        "price": "50000.00",
        "size": "0.001",
        "side": "BUY",
        "time": 1640995210000
      }
    ]
  }
}
```

### Get 24hr Ticker

**Endpoint:** `GET /api/v1/market/ticker/24hr`

**Authentication:** Not required

**Parameters:**
```json
{
  "symbol": "BTC_USDT"  // Optional
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "tickers": [
      {
        "symbol": "BTC_USDT",
        "priceChange": "100.00",
        "priceChangePercent": "2.00",
        "weightedAvgPrice": "50000.00",
        "prevClosePrice": "49900.00",
        "lastPrice": "50000.00",
        "lastQty": "0.001",
        "bidPrice": "49999.00",
        "bidQty": "0.001",
        "askPrice": "50001.00",
        "askQty": "0.001",
        "openPrice": "49900.00",
        "highPrice": "50100.00",
        "lowPrice": "49900.00",
        "volume": "100.5",
        "quoteVolume": "5025000.00",
        "openTime": 1640995200000,
        "closeTime": 1640995260000,
        "firstId": 123456789,
        "lastId": 123456790,
        "count": 2
      }
    ]
  }
}
```

## Grid Bot Endpoints

### Create Grid Bot

**Endpoint:** `POST /api/v1/grid/bot`

**Authentication:** Required

**Parameters:**
```json
{
  "symbol": "BTC_USDT",
  "gridType": "ARITHMETIC",
  "gridSize": 10,
  "priceUpper": "51000.00",
  "priceLower": "49000.00",
  "investment": "1000.00",
  "gridSpacing": "200.00"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "gridId": "grid-123456789",
    "symbol": "BTC_USDT",
    "status": "RUNNING",
    "createTime": 1640995200000
  }
}
```

### Get Grid Bot

**Endpoint:** `GET /api/v1/grid/bot`

**Authentication:** Required

**Parameters:**
```json
{
  "gridId": "grid-123456789"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "gridId": "grid-123456789",
    "symbol": "BTC_USDT",
    "status": "RUNNING",
    "gridType": "ARITHMETIC",
    "gridSize": 10,
    "priceUpper": "51000.00",
    "priceLower": "49000.00",
    "investment": "1000.00",
    "gridSpacing": "200.00",
    "totalProfit": "50.00",
    "createTime": 1640995200000,
    "updateTime": 1640995210000
  }
}
```

### Stop Grid Bot

**Endpoint:** `DELETE /api/v1/grid/bot`

**Authentication:** Required

**Parameters:**
```json
{
  "gridId": "grid-123456789"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "gridId": "grid-123456789",
    "status": "STOPPED"
  }
}
```

### List Grid Bots

**Endpoint:** `GET /api/v1/grid/bots`

**Authentication:** Required

**Parameters:** None

**Response Format:**
```json
{
  "success": true,
  "data": {
    "bots": [
      {
        "gridId": "grid-123456789",
        "symbol": "BTC_USDT",
        "status": "RUNNING",
        "gridType": "ARITHMETIC",
        "gridSize": 10,
        "priceUpper": "51000.00",
        "priceLower": "49000.00",
        "investment": "1000.00",
        "totalProfit": "50.00",
        "createTime": 1640995200000
      }
    ]
  }
}
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": 1001,
    "message": "Invalid API key",
    "details": "The provided API key is invalid or expired"
  }
}
```

### Common Error Codes

- `1001`: Invalid API key
- `1002`: Invalid signature
- `1003`: Invalid timestamp
- `1004`: Rate limit exceeded
- `1005`: Invalid symbol
- `1006`: Invalid order type
- `1007`: Insufficient balance
- `1008`: Order not found
- `1009`: Invalid price
- `1010`: Invalid quantity

## Response Formats

### Standard Success Response

```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "timestamp": 1640995200000
}
```

### Standard Error Response

```json
{
  "success": false,
  "error": {
    "code": 1001,
    "message": "Error message",
    "details": "Additional error details"
  },
  "timestamp": 1640995200000
}
```

## Symbol Format Conversion

The API automatically converts symbol formats:

- Input: `BTC_USDT` → API: `BTC_USDT`
- Input: `BTCUSDT` → API: `BTC_USDT`
- Input: `btc_usdt` → API: `BTC_USDT`

## Order Types

- `MARKET`: Market order
- `LIMIT`: Limit order
- `STOP_MARKET`: Stop market order
- `STOP_LIMIT`: Stop limit order
- `TAKE_PROFIT_MARKET`: Take profit market order
- `TAKE_PROFIT_LIMIT`: Take profit limit order
- `TRAILING_STOP_MARKET`: Trailing stop market order

## Time In Force

- `GTC`: Good Till Canceled
- `IOC`: Immediate Or Cancel
- `FOK`: Fill Or Kill

## Side

- `BUY`: Buy order
- `SELL`: Sell order

## Status

- `NEW`: Order is new
- `PARTIALLY_FILLED`: Order is partially filled
- `FILLED`: Order is completely filled
- `CANCELED`: Order is canceled
- `REJECTED`: Order is rejected
- `EXPIRED`: Order is expired

## Intervals

- `1M`: 1 minute
- `5M`: 5 minutes
- `15M`: 15 minutes
- `30M`: 30 minutes
- `1H`: 1 hour
- `4H`: 4 hours
- `8H`: 8 hours
- `12H`: 12 hours
- `1D`: 1 day

## Security Recommendations

1. **IP Whitelisting**: Set up IP whitelisting along with API key for enhanced security
2. **API Key Protection**: Never share your API key/secret with anyone
3. **Environment Variables**: Store API credentials in environment variables
4. **Rate Limiting**: Implement proper rate limiting in your application
5. **Error Handling**: Always handle API errors gracefully
6. **Logging**: Log API requests and responses for debugging
7. **Validation**: Validate all input parameters before sending requests

## Official Resources

- [Pionex API Documentation](https://pionex-doc.gitbook.io/apidocs/)
- [Official Telegram Group](https://t.me/pionexapi)
- [Rate Limits](https://pionex-doc.gitbook.io/apidocs/restful/general-info/rate-limit)
- [Authentication](https://pionex-doc.gitbook.io/apidocs/restful/general-info/authentication)

---

*This documentation is based on the official Pionex API documentation and the current implementation in this trading bot. For the most up-to-date information, always refer to the [official Pionex API documentation](https://pionex-doc.gitbook.io/apidocs/).* 