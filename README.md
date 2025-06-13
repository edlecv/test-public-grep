# 🚀 Hashdive API Integration - Advanced Polymarket Trading Analysis

A comprehensive Flask-based dashboard for analyzing Polymarket trading data using the Hashdive enriched API, featuring sophisticated win rate calculations and real-time data visualization.

## ✨ Key Features

### 📊 **Advanced Win Rate Analysis**
- **Zero Random Data**: Complete elimination of synthetic data generation
- **Polymarket-Specific Logic**: Understands prediction market mechanics (Yes/No positions)
- **Multi-Method Detection**: Analyzes PnL fields, trade outcomes, amounts, and prices
- **Data Quality Scoring**: High/medium/low confidence based on data completeness
- **Intelligent Validation**: Requires 50%+ valid trades for accurate analysis

### 🔧 **Professional Dashboard**
- **Real-Time Data**: Live integration with Hashdive API
- **Maximum Data Retrieval**: Automatically fetches 1000 records (API maximum)
- **Multiple Endpoints**: User trades, positions, OHLCV, whale trades, market search
- **Interactive Charts**: Chart.js visualizations with PnL curves
- **CSV Export**: Download trading data for external analysis

### 🛡️ **Data Integrity**
- **API-Only Data**: No fallback random data generation
- **Robust Error Handling**: Detailed, actionable error messages
- **Quality Validation**: Comprehensive data structure analysis
- **Credit Optimization**: Maximum data per API request

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Hashdive API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/edlecv/test-public-grep.git
cd test-public-grep
```

2. **Install dependencies**
```bash
pip install -r requirements_hashdive.txt
```

3. **Configure API key**
```bash
# Create .env file
echo "HASHDIVE_API_KEY=your_api_key_here" > .env
```

4. **Run the dashboard**
```bash
python hashdive_server.py
```

5. **Access dashboard**
Open http://localhost:5000 in your browser

## 📋 API Endpoints

### 🏆 **Best for Win Rate Analysis**
- **User Trades** - Complete trading history with outcomes and PnL data

### ⚠️ **Limited for Win Rate**
- **User Positions** - Current holdings (lacks complete trading history)

### 📈 **Market Data**
- **Last Price** - Current market prices
- **OHLCV Candlesticks** - Market price charts
- **Search Markets** - Market discovery
- **Whale Trades** - Large trades from all users
- **API Usage** - Usage statistics

## 🎯 Win Rate Calculation Methods

### **Method 1: Direct PnL (Most Reliable)**
```python
if record.pnl !== undefined:
    tradeValue = parseFloat(record.pnl)
    isProfitable = tradeValue > 0
```

### **Method 2: Calculated PnL (Polymarket Specific)**
```python
# For prediction markets
if side === 'buy' and outcome === 'Yes':
    tradeValue = amount * (1 - price)
    isProfitable = true
```

### **Method 3: Basic Outcome (Last Resort)**
```python
if record.outcome === 'win':
    isProfitable = true
```

## 📊 Data Quality Requirements

- **Minimum 50% valid trades** for analysis
- **PnL data preferred** for highest accuracy
- **Trade outcomes required** for basic analysis
- **Timestamps needed** for chronological ordering

## 🔒 Security Features

- **Environment Variables**: API keys stored securely
- **Input Validation**: All user inputs validated
- **Error Boundaries**: Graceful error handling
- **No Data Leakage**: Zero random data generation

## 📁 Project Structure

```
├── hashdive_server.py          # Main Flask application
├── templates/
│   └── dashboard.html          # Enhanced dashboard with win rate analysis
├── hashdive_client.py          # API client implementation
├── requirements_hashdive.txt   # Python dependencies
├── SETUP_GUIDE.md             # Detailed setup instructions
├── FIELD_EXPLANATIONS.md      # API field documentation
├── WINRATE_CALCULATION_GUIDE.md # Win rate methodology
└── test_*.py                  # Testing utilities
```

## 🧪 Testing

```bash
# Test API connectivity
python test_hashdive_api.py

# Test win rate system
python test_winrate_system.py

# Test record ordering
python test_record_order.py
```

## 📖 Documentation

- **[Setup Guide](SETUP_GUIDE.md)** - Complete installation instructions
- **[Field Explanations](FIELD_EXPLANATIONS.md)** - API field documentation
- **[Win Rate Guide](WINRATE_CALCULATION_GUIDE.md)** - Calculation methodology
- **[Installation Guide](INSTALLATION_GUIDE.md)** - System requirements

## 🔧 Configuration

### Environment Variables
```bash
HASHDIVE_API_KEY=your_api_key_here
```

### API Limits
- **Maximum Records**: 1000 per request
- **Rate Limits**: Respect Hashdive API limits
- **Credit Usage**: Optimized for maximum data per credit

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hashdive** for providing enriched Polymarket API
- **Polymarket** for prediction market data
- **Chart.js** for visualization capabilities

## 📞 Support

For issues and questions:
1. Check the documentation files
2. Review error messages in the dashboard
3. Verify API key configuration
4. Ensure sufficient trading data exists

---

**Built with ❤️ for accurate Polymarket trading analysis**
