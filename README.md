# 🚀 HashDive Data Analysis Dashboard

A comprehensive web dashboard for analyzing Polymarket trading data using the HashDive API with enhanced timestamp formatting, user analytics, and robust data validation.

## ✨ Features

### 📅 **Enhanced Timestamp Processing**
- **Multiple timestamp formats**: Readable dates, formatted timestamps, date/time separation
- **Automatic detection**: Handles Unix timestamps (seconds/milliseconds) and ISO formats
- **Chronological ordering**: Trades displayed from newest to oldest
- **Time range filtering**: Working TIMESTAMP_GTE and TIMESTAMP_LTE parameters

### 👤 **User Analytics Dashboard**
- **Trading metrics**: Total trades, trading period, average trades per day
- **Performance tracking**: Estimated PnL calculations and profit analysis
- **Timeline analysis**: First and last trade dates with trading period calculation
- **Data quality reporting**: Real-time validation status and coverage percentages

### 🔍 **Robust Data Fetching**
- **Paginated retrieval**: Fetches ALL available trades across multiple API pages
- **Complete coverage**: Maximum data retrieval without gaps or missing records
- **Error handling**: Graceful handling of empty results and API errors
- **Data validation**: Quality checks without blocking legitimate results

### 📊 **Advanced Data Display**
- **Prioritized columns**: Important fields (timestamps, amounts, market info) shown first
- **Color-coded data**: Buy/sell indicators, PnL values, trade sequences
- **Enhanced tooltips**: Full data values available on hover
- **Export functionality**: CSV export with all enhanced data fields

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- Flask 2.3+
- Valid HashDive API key

### Quick Start
1. **Clone the repository**:
   ```bash
   git clone https://github.com/edlecv/test-public-grep.git
   cd test-public-grep
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements_hashdive.txt
   ```

3. **Install the package**:
   ```bash
   pip install -e .
   ```

4. **Configure API key** (edit `hashdive_server.py`):
   ```python
   HASHDIVE_API_KEY = "your_api_key_here"
   ```

5. **Run the server**:
   ```bash
   python -m flask --app hashdive_server run --host=0.0.0.0 --port=5000
   ```

6. **Access the dashboard**:
   - Local: http://localhost:5000
   - Network: http://your-ip:5000

## 📋 API Endpoints

### Available Data Sources
- **User Trades**: Complete trading history with market metadata
- **User Positions**: Current positions with enriched data
- **Market Prices**: Latest asset prices and OHLCV data
- **Market Search**: Find markets by question name
- **Whale Trades**: Large trades above USD threshold
- **API Usage**: Current usage metrics

### Enhanced Parameters
- **User Address**: Ethereum wallet address (0x...)
- **Asset ID**: Specific token ID from Polymarket
- **Timestamp Filters**: GTE/LTE for time range selection
- **Output Format**: JSON or CSV export options

## 🔧 Technical Architecture

### Core Components
- **Flask Server**: [`hashdive_server.py`](hashdive_server.py) - Main application server
- **Dashboard UI**: [`templates/dashboard.html`](templates/dashboard.html) - Enhanced web interface
- **Data Processing**: Advanced timestamp formatting and user analytics
- **Validation System**: Comprehensive data integrity checks

### Key Functions
- **`get_all_trades_paginated()`**: Retrieves complete trading history
- **`enhance_trade_data()`**: Adds timestamp formatting and analytics
- **`validate_trade_data_integrity()`**: Ensures data quality and completeness
- **Real-time analytics**: User trading behavior analysis

## 📊 Data Quality Features

### Validation Metrics
- **Timestamp Coverage**: Percentage of trades with valid timestamps
- **Amount Coverage**: Percentage of trades with amount data
- **Price Coverage**: Percentage of trades with price information
- **Market Coverage**: Percentage of trades with market metadata

### Quality Thresholds
- **Minimum timestamp coverage**: 30% (permissive for various data sources)
- **Ordering validation**: Ensures chronological sequence
- **Critical field checks**: Validates essential trade information
- **Gap detection**: Identifies missing or incomplete data

## 🎯 Usage Examples

### Fetch User Trading History
1. Enter Ethereum wallet address
2. Select "User Trades" endpoint
3. Optionally set timestamp filters
4. Click "Fetch Data" to retrieve complete history

### Analyze Trading Performance
- View comprehensive user analytics
- Check win rate analysis (when PnL data available)
- Export data for external analysis
- Monitor data quality metrics

### Time Range Analysis
- Use TIMESTAMP_GTE for start date
- Use TIMESTAMP_LTE for end date
- System automatically converts datetime inputs
- Fetches all trades within specified period

## 🔒 Security & Configuration

### API Key Management
- Store API keys securely
- Never commit keys to version control
- Use environment variables in production

### Data Privacy
- No data is stored permanently
- All processing happens in real-time
- User addresses are only used for API queries

## 🚀 Recent Enhancements

### v2.0 Features
- ✅ **Fixed data fetching integrity** - Resolved blocking validation issues
- ✅ **Enhanced timestamp processing** - Multiple format support
- ✅ **User analytics dashboard** - Comprehensive trading metrics
- ✅ **Improved error handling** - Graceful handling of edge cases
- ✅ **Data validation system** - Quality reporting without blocking
- ✅ **Chronological ordering** - Proper trade sequence display

### Performance Improvements
- **Paginated data fetching**: Handles large datasets efficiently
- **Memory optimization**: Processes data without performance issues
- **Smart caching**: Reduces redundant API calls
- **Responsive UI**: Enhanced user experience

## 📈 Analytics Capabilities

### Trading Metrics
- **Total Trades**: Complete count of user activity
- **Trading Period**: Days between first and last trade
- **Average Frequency**: Trades per day calculation
- **Volume Analysis**: Total trading volume (when available)

### Performance Analysis
- **PnL Estimation**: Profit/loss calculations from available data
- **Win Rate Analysis**: Success rate when sufficient data available
- **Timeline Visualization**: Trading activity over time
- **Market Participation**: Analysis of market involvement

## 🛡️ Error Handling

### Robust Data Processing
- **Never generates fake data**: Only displays actual API results
- **Graceful degradation**: Works with partial or incomplete data
- **Clear error messages**: Distinguishes between different error types
- **Validation reporting**: Shows data quality without blocking display

### API Error Management
- **Connection timeouts**: Proper handling of network issues
- **Rate limiting**: Respects API usage limits
- **Invalid responses**: Graceful handling of malformed data
- **Empty results**: Proper display of "no data found" scenarios

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
- Check the validation messages in the dashboard
- Review server logs for detailed error information
- Ensure API key has proper permissions
- Verify user addresses have trading history

---

**Built with ❤️ for the Polymarket community**
