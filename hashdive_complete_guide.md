# Complete Hashdive API Usage Guide

## Understanding Hashdive: Website vs API

### The Hashdive Website (Easy Way)
- **URL**: https://hashdive.com
- **What it is**: A web dashboard where you can view data visually
- **How to use**: Log in with your account and browse the interface
- **Best for**: Quick analysis, viewing charts, exploring data

### The Hashdive API (Developer Way)  
- **URL**: https://hashdive.com/api/
- **What it is**: A programming interface that returns raw data
- **How to use**: Make HTTP requests from code/tools
- **Best for**: Building custom apps, automated analysis, integrating into other systems

## Your API Details
- **API Key**: `ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532`
- **Base URL**: `https://hashdive.com/api/`
- **Credits**: 500 monthly credits (each request = 1 credit)

## Method 1: View Data on Hashdive Website

1. Go to https://hashdive.com
2. Log in with your account credentials 
3. Navigate through their dashboard to see:
   - Market analysis
   - Trade data
   - Whale activity
   - OHLCV charts
   - And more!

This is the **easiest way** to see your data with nice charts and tables.

## Method 2: Use the API Programmatically

The API returns raw data that you can use to build your own tools.

### Available Endpoints

Based on the documentation screenshot:

#### `/get_trades`
Returns trades for a given user, enriched with market metadata.

**Parameters:**
- `user_address` (required): Wallet address  
- `asset_id` (optional): Filter by market
- `timestamp_gte`, `timestamp_lte` (optional): ISO format time range
- `format`: "json" (default) or "csv"
- `page`, `page_size`: Pagination (max 1000 per page)

### How to Make API Calls

#### Using curl (Command Line)
```bash
# We need to figure out the correct authentication method
# The API key might need to be passed differently

# Try these different authentication methods:
curl -H "Authorization: Bearer YOUR_API_KEY" "https://hashdive.com/api/get_trades?user_address=WALLET_ADDRESS"

curl -H "X-API-Key: YOUR_API_KEY" "https://hashdive.com/api/get_trades?user_address=WALLET_ADDRESS"

curl "https://hashdive.com/api/get_trades?api_key=YOUR_API_KEY&user_address=WALLET_ADDRESS"
```

#### Using Python
```python
import requests

API_KEY = "ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532"
BASE_URL = "https://hashdive.com/api"

# Try different auth methods
headers_bearer = {"Authorization": f"Bearer {API_KEY}"}
headers_apikey = {"X-API-Key": API_KEY}

def get_trades(user_address, auth_method="bearer"):
    if auth_method == "bearer":
        headers = headers_bearer
        params = {"user_address": user_address, "page_size": 10}
    elif auth_method == "header":
        headers = headers_apikey  
        params = {"user_address": user_address, "page_size": 10}
    else:  # query param
        headers = {}
        params = {"api_key": API_KEY, "user_address": user_address, "page_size": 10}
    
    response = requests.get(f"{BASE_URL}/get_trades", headers=headers, params=params)
    return response.json()

# Example usage (you need a real wallet address)
wallet = "0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE"  # Example
trades = get_trades(wallet)
print(trades)
```

#### Using JavaScript (for web apps)
```javascript
const API_KEY = "ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532";

async function getHashdiveData(endpoint, params = {}) {
    const url = new URL(`https://hashdive.com/api${endpoint}`);
    
    // Add API key to params
    params.api_key = API_KEY;
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    
    const response = await fetch(url);
    return await response.json();
}

// Get trades for a wallet
getHashdiveData('/get_trades', {
    user_address: '0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE',
    page_size: 10
}).then(data => console.log(data));
```

## Building Your Own Dashboard

If you want to create your own interface to view the data:

### Simple HTML Dashboard
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Polymarket Data</title>
</head>
<body>
    <h1>Polymarket Trade Data</h1>
    <div id="data"></div>
    
    <script>
        const API_KEY = "your_api_key_here";
        
        async function loadData() {
            try {
                const response = await fetch(`https://hashdive.com/api/get_trades?api_key=${API_KEY}&user_address=WALLET_ADDRESS&page_size=20`);
                const data = await response.json();
                
                document.getElementById('data').innerHTML = 
                    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        loadData();
    </script>
</body>
</html>
```

## Next Steps

1. **Start with the website**: Go to hashdive.com and log in to see your data
2. **Find wallet addresses**: You need actual Polymarket user wallet addresses to get meaningful data
3. **Test the API**: Try the different authentication methods to see which works
4. **Build something cool**: Create your own dashboard or analysis tool

## Key Points

- ✅ **Hashdive.com = Website to VIEW data easily**
- ✅ **Hashdive.com/api/ = Programming interface to GET raw data**  
- ✅ **Your API key gives you 500 monthly requests**
- ✅ **Each API call uses 1 credit regardless of response size**
- ✅ **Data is updated every minute**
- ✅ **You can get JSON or CSV format**

The API doesn't show you data directly - it's like asking a question and getting an answer back that you then display however you want!