# 🚀 Hashdive API Quick Start Guide

## ✅ What's Ready to Use NOW

### **Browser-Based Tool (Already Open)**
- **File**: `simple_hashdive_test.html` (just opened in your browser)
- **Features**: Test all Hashdive API endpoints directly in browser
- **No Installation Required**: Works immediately
- **API Key**: Pre-configured with your key

### **Professional Dashboard (Requires Python)**
- **File**: `hashdive_server.py` + `templates/dashboard.html`
- **Features**: Full data analysis, charts, CSV export, professional UI
- **Requires**: Python installation (see INSTALLATION_GUIDE.md)

## 🔧 Using the Browser Tool (Available Now)

The browser tool that just opened includes:

### **Available Endpoints**
1. **📊 User Trades** - Enter wallet address to see trade history
2. **🏪 Markets Data** - Get market information
3. **🐋 Whale Activity** - See large trades
4. **📈 OHLCV Prices** - Get price data

### **How to Use**
1. **Select Endpoint**: Choose from the dropdown
2. **Enter Parameters**: 
   - For trades: Use wallet `0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE`
   - For others: Leave default or adjust as needed
3. **Click "Test API"**: Fetch data from Hashdive
4. **View Results**: See JSON response in the result area

### **Your API Details**
- **API Key**: `ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532`
- **Base URL**: `https://hashdive.com/api/`
- **Credits**: 500 monthly requests

## 🐍 For Full Dashboard (Optional)

If you want the complete professional dashboard with charts and exports:

### **Install Python**
1. **Go to**: https://www.python.org/downloads/
2. **Download Python 3.11+**
3. **Install** (check "Add to PATH")
4. **Restart terminal**

### **Install Dependencies**
```bash
pip install Flask==2.3.3 Flask-CORS==4.0.0 requests==2.31.0 Werkzeug==2.3.7
```

### **Run Dashboard**
```bash
python hashdive_server.py
```

### **Open Dashboard**
Go to: http://localhost:5000

## 📊 What You Can Analyze

### **Trading Data**
- Individual user trade history
- Profit/loss analysis
- Trading patterns over time

### **Market Intelligence**
- Search for specific prediction markets
- Monitor whale activity (large trades)
- Track market prices and trends

### **Portfolio Analysis**
- Current user positions
- Portfolio value tracking
- Asset allocation

## 🔑 API Authentication

Your requests use the `x-api-key` header:
```http
GET https://hashdive.com/api/get_trades?user_address=WALLET
Headers: x-api-key: ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532
```

## 💡 Tips for Success

1. **Start with Browser Tool**: Test your API key and explore data
2. **Use Popular Wallets**: `0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE` for testing
3. **Monitor Credits**: You have 500 monthly requests
4. **Search Markets First**: Find asset IDs for specific analysis
5. **Export Data**: Use CSV format for spreadsheet analysis

## 🎯 Example Workflow

1. **Search Markets**: Find interesting prediction markets
2. **Get Asset IDs**: Copy asset IDs from search results
3. **Analyze Trades**: Look at user trading activity
4. **Monitor Whales**: Track large money movements
5. **Track Prices**: Monitor market price changes

## ✅ You're Ready!

- **Browser tool is open** and ready to test
- **All endpoints configured** with your API key
- **Professional dashboard available** when you install Python
- **Complete documentation** provided for all features

Start by testing the browser tool that's already open, then optionally install Python for the full dashboard experience!