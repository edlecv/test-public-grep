# 🚀 Complete Hashdive API Data Analysis Setup

## Overview

You now have a professional web-based data analysis dashboard that connects directly to your Hashdive API to fetch enriched Polymarket data. This system is based on the official Hashdive API documentation and includes all available endpoints.

## 📊 Available Data Endpoints

### 1. **📊 User Trades** (`/get_trades`)
- **Purpose**: Returns trades for a given user, enriched with market metadata
- **Required**: `user_address` (wallet address)
- **Optional**: `asset_id`, `timestamp_gte`, `timestamp_lte`, `format`, `page`, `page_size`
- **Use Case**: Analyze trading history, profit/loss tracking, trading patterns

### 2. **💼 User Positions** (`/get_positions`)
- **Purpose**: Returns current positions for a given user, enriched with market metadata
- **Required**: `user_address` (wallet address)
- **Optional**: `asset_id`, `format`, `page`, `page_size`
- **Use Case**: Portfolio analysis, current holdings, position tracking
- **Note**: Position data for inactive users is archived periodically to optimize costs

### 3. **💰 Last Price** (`/get_last_price`)
- **Purpose**: Returns the last price for a given asset (resolved or last traded price)
- **Required**: `asset_id` (Token ID)
- **Use Case**: Real-time price monitoring, market valuation

### 4. **📈 OHLCV Data** (`/get_ohlcv`)
- **Purpose**: Returns OHLCV bars for a token over a given time resolution
- **Required**: `asset_id` (Token ID), `resolution` (1m, 5m, 15m, 1h, 4h, 1d)
- **Optional**: `timestamp_gte`, `timestamp_lte`, `format`, `page`, `page_size`
- **Use Case**: Technical analysis, price charts, trend analysis

### 5. **🔍 Search Markets** (`/search_markets`)
- **Purpose**: Search markets by question name and retrieve associated asset_id
- **Required**: `query` (search term)
- **Optional**: `page`, `page_size`
- **Use Case**: Market discovery, finding specific prediction markets

### 6. **🐋 Whale Trades** (`/get_latest_whale_trades`)
- **Purpose**: Returns recent trades above a USD threshold
- **Optional**: `min_usd` (default 10,000), `limit` (default 1000), `format`
- **Use Case**: Following large traders, market sentiment analysis

### 7. **📊 API Usage** (`/get_api_usage`)
- **Purpose**: Returns current usage metrics for your API key
- **Use Case**: Monitor remaining credits, usage tracking

## 🔧 Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements_hashdive.txt
```

### Step 2: Start the Server
```bash
python hashdive_server.py
```

You should see:
```
🚀 Starting Hashdive Data Analysis Server...
📊 Dashboard will be available at: http://localhost:5000
🔑 Using API Key: ecb19e0b9987e4d41...
📋 Available Endpoints:
  • get_trades - User trade history
  • get_positions - Current user positions
  • get_last_price - Latest asset prices
  • get_ohlcv - OHLCV candlestick data
  • search_markets - Search for markets
  • get_latest_whale_trades - Large trades
  • get_api_usage - API usage metrics
```

### Step 3: Open Dashboard
Navigate to: **http://localhost:5000**

## 🎛️ Dashboard Features

### **Dynamic Parameter Forms**
- Each endpoint shows only relevant parameters
- Required fields are marked with *
- Smart input types (dropdowns for resolutions, number inputs for limits)
- Helpful placeholders and tooltips

### **Data Visualization**
- **Table View**: Sortable, searchable data tables with up to 200 rows displayed
- **Chart View**: Automatic chart generation from numeric data fields
- **Raw Data**: Developer-friendly JSON view with syntax highlighting

### **Export Capabilities**
- **CSV Export**: Download data for Excel/Google Sheets analysis
- **Direct CSV**: Some endpoints return CSV format directly
- **Formatted Data**: Clean, analysis-ready format

### **Real-time Analytics**
- **API Usage Tracking**: Monitor your 500 monthly credits
- **Record Counts**: Track data volume fetched
- **Last Update Times**: See when data was refreshed
- **Success/Error Reporting**: Clear status messages

## 🔑 Authentication Details

Your API key is pre-configured: `ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532`

The system uses the `x-api-key` header method as shown in the official documentation:
```python
headers = {'x-api-key': 'your_api_key_here'}
```

## 📖 Example Use Cases

### **1. Analyze a Specific User's Trading Activity**
1. Select "User Trades" endpoint
2. Enter wallet address: `0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE`
3. Set page size to 100
4. Fetch data to see complete trading history
5. Export to CSV for detailed analysis in Excel

### **2. Monitor Whale Activity**
1. Select "Whale Trades" endpoint
2. Set minimum USD to 50,000
3. Fetch latest large trades
4. Use charts to visualize trade patterns
5. Monitor for market-moving events

### **3. Search for Election Markets**
1. Select "Search Markets" endpoint
2. Enter query: "election"
3. Get list of election-related prediction markets
4. Copy asset_id for further analysis

### **4. Track Price History**
1. Select "OHLCV Data" endpoint
2. Enter asset_id from market search
3. Set resolution to "1h" for hourly data
4. View price charts and trends

### **5. Portfolio Analysis**
1. Select "User Positions" endpoint
2. Enter wallet address
3. See current holdings and values
4. Export for portfolio tracking

## 🔧 HTTP Request Logic

The dashboard makes authenticated HTTP requests like:

```http
GET https://hashdive.com/api/get_trades?user_address=0x123...&page_size=100
Headers: x-api-key: ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532
```

```http
GET https://hashdive.com/api/search_markets?query=election
Headers: x-api-key: ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532
```

```http
GET https://hashdive.com/api/get_ohlcv?asset_id=777...&resolution=1h
Headers: x-api-key: ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532
```

## 💡 Pro Tips

1. **Start with API Usage**: Check your remaining credits first
2. **Use Market Search**: Find asset_ids for specific markets
3. **Test with Popular Wallets**: Use known active addresses for testing
4. **Export Everything**: Download data for offline analysis
5. **Monitor Credits**: You have 500 monthly requests (1 credit each)

## 🚨 Important Notes

- **Data Updates**: Hashdive data is updated every minute
- **Rate Limits**: 500 monthly credits, 1 credit per request regardless of size
- **Pagination**: Max 1000 records per request
- **Both Formats**: JSON for analysis, CSV for spreadsheets
- **Archive Policy**: Inactive user positions are archived periodically

## 🛠️ File Structure

```
📁 Your Project/
├── 🐍 hashdive_server.py              # Flask backend with all endpoints
├── 📋 requirements_hashdive.txt        # Python dependencies  
├── 📁 templates/
│   └── 🌐 dashboard.html              # Complete web interface
├── 📖 HASHDIVE_COMPLETE_SETUP.md      # This comprehensive guide
└── 🔧 Additional files for reference
```

## ✅ What You've Achieved

You now have a **professional-grade data analysis platform** that:

✅ **Directly integrates** with your Hashdive API key  
✅ **Supports all 7 endpoints** from the official documentation  
✅ **Uses proper authentication** (x-api-key header method)  
✅ **Provides visual data analysis** with tables, charts, and exports  
✅ **Handles both JSON and CSV** output formats  
✅ **Tracks API usage** and remaining credits  
✅ **Offers professional UI** with dynamic form generation  
✅ **Enables bulk data export** for further analysis  

This is a complete solution for analyzing Polymarket data through HTTP requests to your Hashdive API!