# Hashdive API Usage Guide

## Your API Details
- **API Key**: `ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532`
- **Base URL**: `https://hashdive.com/api/`
- **Service**: Enriched Polymarket trade data, OHLCV aggregates, market search, whale activity
- **Update Frequency**: Every minute
- **Formats**: JSON and CSV

## Important: This is NOT the py-clob-client

The py-clob-client in this repository is for the **official Polymarket CLOB API**, which requires:
- Private keys for authentication
- Direct interaction with Polymarket's trading system

**Hashdive** is a **separate third-party service** that provides:
- Enriched and processed Polymarket data
- REST API with simple authentication
- Historical data analysis
- Whale tracking and market analysis

## How to Use Your Hashdive API

### 1. Using curl (Command Line)

Test your API access:
```bash
# Test the get_trades endpoint
curl -H "Authorization: Bearer ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532" \
     "https://hashdive.com/api/get_trades?user_address=0x1234567890abcdef1234567890abcdef12345678&page=1&page_size=10"

# Test other possible endpoints
curl -H "Authorization: Bearer ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532" \
     "https://hashdive.com/api/markets"

curl -H "Authorization: Bearer ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532" \
     "https://hashdive.com/api/whale_activity"
```

### 2. Using Python (requests library)

```python
import requests
import json

# Your API credentials
API_KEY = "ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532"
BASE_URL = "https://hashdive.com/api"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Get trades for a specific user
def get_user_trades(user_address, asset_id=None, page=1, page_size=100):
    params = {
        "user_address": user_address,
        "page": page,
        "page_size": page_size
    }
    if asset_id:
        params["asset_id"] = asset_id
    
    response = requests.get(f"{BASE_URL}/get_trades", headers=headers, params=params)
    return response.json()

# Example usage
trades = get_user_trades("0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE")  # Example address
print(json.dumps(trades, indent=2))
```

### 3. Using JavaScript (fetch API)

```javascript
const API_KEY = "ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532";
const BASE_URL = "https://hashdive.com/api";

async function getHashdiveData(endpoint, params = {}) {
    const url = new URL(`${BASE_URL}${endpoint}`);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    
    const response = await fetch(url, {
        headers: {
            'Authorization': `Bearer ${API_KEY}`,
            'Content-Type': 'application/json'
        }
    });
    
    return await response.json();
}

// Example: Get trades
getHashdiveData('/get_trades', {
    user_address: '0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE',
    page: 1,
    page_size: 10
}).then(data => console.log(data));
```

## Available Endpoints (Based on Documentation Screenshot)

### 1. `/get_trades`
Returns trades for a given user, enriched with market metadata.

**Parameters:**
- `user_address` (required): Wallet address
- `asset_id` (optional): Filter by market
- `timestamp_gte` (optional): ISO format time range start
- `timestamp_lte` (optional): ISO format time range end
- `format`: "json" (default) or "csv"
- `page`: Page number
- `page_size`: Max page size (1000)

### 2. Likely Other Endpoints:
- `/markets` - Get market data
- `/ohlcv` - Get OHLCV (price) data
- `/whale_activity` - Get whale trading activity
- `/search` - Search markets

## Next Steps

1. **Test your API**: Use the curl commands above to verify your access
2. **Find real wallet addresses**: You'll need actual Polymarket user addresses to get meaningful data
3. **Explore endpoints**: Try different endpoints to see what data is available
4. **Build your application**: Use the Python or JavaScript examples as starting points

## Key Differences from py-clob-client

| Feature | Hashdive API | py-clob-client |
|---------|--------------|----------------|
| **Purpose** | Historical data & analytics | Live trading & market data |
| **Authentication** | REST API key | Private key + signatures |
| **Data** | Enriched, processed | Raw trading data |
| **Trading** | Read-only | Full trading capabilities |
| **Setup** | Simple HTTP requests | Complex wallet setup |

Your Hashdive API is perfect for:
- ✅ Market analysis and research
- ✅ Historical trade tracking
- ✅ Whale activity monitoring
- ✅ Building dashboards and analytics

It's NOT for:
- ❌ Placing orders
- ❌ Real-time trading
- ❌ Account management