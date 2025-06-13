# 🚀 Hashdive Data Analysis Web Interface Setup

## What You're Getting

A professional web-based dashboard that uses your Hashdive API key to fetch and analyze Polymarket data through HTTP requests. This includes:

- **📊 Data Tables**: View your data in organized tables
- **📈 Charts & Visualizations**: Automatic chart generation 
- **📁 CSV Export**: Download your data for further analysis
- **🔄 Real-time Fetching**: Fresh data from Hashdive API
- **🌐 Web Interface**: Professional dashboard accessible via browser

## Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements_hashdive.txt
```

### 2. Start the Flask Server
```bash
python hashdive_server.py
```

### 3. Open Your Dashboard
Open your browser and go to: **http://localhost:5000**

## How It Works

### Architecture
```
Your Browser → Flask Server → Hashdive API → Data Analysis
```

1. **Flask Server** (`hashdive_server.py`): Handles HTTP requests to Hashdive API
2. **Web Dashboard** (`templates/dashboard.html`): Professional interface for data analysis
3. **API Client**: Tries multiple authentication methods automatically

### Available Data Sources

#### 📊 User Trades (`/get_trades`)
- Requires: Wallet address
- Returns: Trade history with market metadata
- Use for: Analyzing trading patterns, profit/loss, market activity

#### 🏪 Markets Data (`/markets`)
- Requires: Nothing
- Returns: Available markets information
- Use for: Market discovery, trending topics

#### 🐋 Whale Activity (`/whale_activity`)
- Requires: Nothing  
- Returns: Large trader movements
- Use for: Following big money, market sentiment

#### 📈 OHLCV Data (`/ohlcv`)
- Requires: Nothing (optional asset_id)
- Returns: Price and volume data
- Use for: Technical analysis, price charts

## Features

### 🎛️ Dashboard Controls
- **Data Source Selection**: Choose which endpoint to query
- **Wallet Address**: Enter specific wallets for trades data
- **Record Limits**: Control how much data to fetch (10-500 records)
- **One-Click Fetching**: Simple button to get fresh data

### 📊 Data Visualization
- **Table View**: Sortable, searchable data tables
- **Chart View**: Automatic chart generation from numeric data
- **Raw JSON**: Developer-friendly view of API responses

### 📁 Export Capabilities
- **CSV Export**: Download data for Excel/Google Sheets
- **Formatted Data**: Clean, ready-to-analyze format

### 📈 Analytics
- **Record Counts**: Track how much data you've fetched
- **API Usage**: Monitor your API call count
- **Last Update**: See when data was refreshed
- **Data Source**: Track which endpoint you're using

## Authentication

The system automatically tries multiple authentication methods:
1. API key as query parameter (`?api_key=...`)
2. Bearer token header (`Authorization: Bearer ...`)
3. X-API-Key header (`X-API-Key: ...`)

Your API key is pre-configured in the server.

## Example Use Cases

### 📊 Analyze Trading Performance
1. Select "User Trades"
2. Enter a wallet address
3. Fetch data to see trade history
4. Export to CSV for detailed analysis

### 🐋 Track Whale Activity
1. Select "Whale Activity"
2. Fetch data to see large trades
3. Use charts to visualize patterns
4. Monitor for market-moving events

### 📈 Market Research
1. Select "Markets Data"
2. Browse available prediction markets
3. Export data to identify trends
4. Use for market intelligence

## Troubleshooting

### If the server won't start:
```bash
# Install dependencies
pip install Flask Flask-CORS requests

# Try running again
python hashdive_server.py
```

### If data won't load:
- Check console for error messages
- Verify your API key is correct
- Try different endpoints
- Check your internet connection

### If charts don't show:
- Ensure data has numeric fields
- Try different data sources
- Check browser console for errors

## File Structure
```
📁 Your Project/
├── 🐍 hashdive_server.py        # Flask backend server
├── 📋 requirements_hashdive.txt  # Python dependencies
├── 📁 templates/
│   └── 🌐 dashboard.html        # Web dashboard interface
├── 📊 hashdive_client.py        # Python API client
├── 🌐 simple_hashdive_test.html # Simple testing tool
└── 📖 SETUP_GUIDE.md           # This guide
```

## Benefits Over Direct API Calls

✅ **No CORS Issues**: Server handles API calls  
✅ **Professional Interface**: Better than command line  
✅ **Data Visualization**: Automatic charts and tables  
✅ **Export Functionality**: Easy data download  
✅ **Authentication Handling**: Tries multiple methods  
✅ **Error Handling**: User-friendly error messages  
✅ **Real-time Updates**: Fresh data on demand  

## Next Steps

1. **Start the server**: `python hashdive_server.py`
2. **Open dashboard**: Go to http://localhost:5000
3. **Fetch some data**: Try different endpoints
4. **Analyze results**: Use tables, charts, and exports
5. **Build insights**: Use the data for your analysis

You now have a professional-grade data analysis platform powered by your Hashdive API!