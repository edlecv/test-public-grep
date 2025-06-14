from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Your Hashdive API configuration
HASHDIVE_API_KEY = "ecb19e0b9907e4d417ede921f1f7d2432b590446211f603e4e239357634cc532"
HASHDIVE_BASE_URL = "https://hashdive.com/api"

class HashdiveClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = HASHDIVE_BASE_URL
        self.session = requests.Session()
        # Based on the documentation, use x-api-key header
        self.session.headers.update({
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        })
        
    def _make_request(self, endpoint, params=None):
        """Make a request to the Hashdive API"""
        if params is None:
            params = {}
            
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Handle both JSON and CSV responses
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return response.json()
            else:
                # Return as text for CSV or other formats
                return {'raw_content': response.text, 'content_type': content_type}
                
        except requests.exceptions.RequestException as e:
            return {
                'error': f'API request failed: {str(e)}',
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                'response_text': getattr(e.response, 'text', None) if hasattr(e, 'response') else None
            }
    
    def get_trades(self, user_address, asset_id=None, timestamp_gte=None, timestamp_lte=None,
                   format='json', page=1, page_size=100):
        """Get trades for a given user, enriched with market metadata"""
        params = {
            'user_address': user_address,
            'format': format,
            'page': page,
            'page_size': min(page_size, 1000)  # API limit
        }
        
        if asset_id:
            params['asset_id'] = asset_id
        if timestamp_gte:
            # Convert datetime-local to Unix timestamp if needed
            if isinstance(timestamp_gte, str) and 'T' in timestamp_gte:
                try:
                    dt = datetime.fromisoformat(timestamp_gte)
                    params['timestamp_gte'] = int(dt.timestamp())
                except:
                    params['timestamp_gte'] = timestamp_gte
            else:
                params['timestamp_gte'] = timestamp_gte
        if timestamp_lte:
            # Convert datetime-local to Unix timestamp if needed
            if isinstance(timestamp_lte, str) and 'T' in timestamp_lte:
                try:
                    dt = datetime.fromisoformat(timestamp_lte)
                    params['timestamp_lte'] = int(dt.timestamp())
                except:
                    params['timestamp_lte'] = timestamp_lte
            else:
                params['timestamp_lte'] = timestamp_lte
            
        return self._make_request('get_trades', params)
    
    def get_all_trades_paginated(self, user_address, asset_id=None, timestamp_gte=None, timestamp_lte=None, format='json'):
        """Get ALL trades for a user by fetching multiple pages and ensuring proper ordering"""
        all_trades = []
        page = 1
        max_pages = 50  # Safety limit to prevent infinite loops
        
        while page <= max_pages:
            result = self.get_trades(
                user_address=user_address,
                asset_id=asset_id,
                timestamp_gte=timestamp_gte,
                timestamp_lte=timestamp_lte,
                format=format,
                page=page,
                page_size=1000  # Maximum per page
            )
            
            if 'error' in result:
                return result
            
            # Handle different response structures
            trades_batch = []
            if isinstance(result, list):
                trades_batch = result
            elif isinstance(result, dict):
                if 'trades' in result:
                    trades_batch = result['trades']
                elif 'data' in result:
                    trades_batch = result['data']
                else:
                    # Single trade or no trades
                    if result and 'user_address' in result:
                        trades_batch = [result]
            
            if not trades_batch or len(trades_batch) == 0:
                break  # No more trades
            
            all_trades.extend(trades_batch)
            
            # If we got less than the page size, we've reached the end
            if len(trades_batch) < 1000:
                break
                
            page += 1
        
        # Sort trades by timestamp (newest first) to ensure proper ordering
        def get_timestamp(trade):
            timestamp_fields = ['timestamp', 'created_at', 'date', 'time']
            for field in timestamp_fields:
                if field in trade and trade[field]:
                    try:
                        ts = trade[field]
                        if isinstance(ts, (int, float)):
                            return ts if ts < 1e10 else ts / 1000  # Handle milliseconds
                        elif isinstance(ts, str):
                            try:
                                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                                return dt.timestamp()
                            except:
                                try:
                                    dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                                    return dt.timestamp()
                                except:
                                    continue
                    except:
                        continue
            return 0  # Default for trades without timestamps
        
        # Sort by timestamp descending (newest first)
        all_trades.sort(key=get_timestamp, reverse=True)
        
        return {
            'trades': all_trades,
            'total_fetched': len(all_trades),
            'pages_fetched': page - 1,
            'ordered_by_timestamp': True
        }
    
    def get_positions(self, user_address, asset_id=None, format='json', page=1, page_size=100):
        """Get current positions for a given user, enriched with market metadata"""
        params = {
            'user_address': user_address,
            'format': format,
            'page': page,
            'page_size': min(page_size, 1000)
        }
        
        if asset_id:
            params['asset_id'] = asset_id
            
        return self._make_request('get_positions', params)
    
    def get_last_price(self, asset_id):
        """Get the last price for a given asset"""
        params = {'asset_id': asset_id}
        return self._make_request('get_last_price', params)
    
    def get_ohlcv(self, asset_id, resolution='1h', timestamp_gte=None, timestamp_lte=None,
                  format='json', page=1, page_size=100):
        """Get OHLCV bars for a token over a given time resolution"""
        params = {
            'asset_id': asset_id,
            'resolution': resolution,  # 1m, 5m, 15m, 1h, 4h, 1d
            'format': format,
            'page': page,
            'page_size': min(page_size, 1000)
        }
        
        if timestamp_gte:
            params['timestamp_gte'] = timestamp_gte
        if timestamp_lte:
            params['timestamp_lte'] = timestamp_lte
            
        return self._make_request('get_ohlcv', params)
    
    def search_markets(self, query, page=1, page_size=100):
        """Search markets by question name and retrieve the associated asset_id"""
        params = {
            'query': query,
            'page': page,
            'page_size': min(page_size, 1000)
        }
        return self._make_request('search_markets', params)
    
    def get_latest_whale_trades(self, min_usd=10000, limit=1000, format='json'):
        """Get recent trades above a USD threshold"""
        params = {
            'min_usd': min_usd,
            'limit': min(limit, 1000),
            'format': format
        }
        return self._make_request('get_latest_whale_trades', params)
    
    def get_api_usage(self):
        """Get current usage metrics for the calling API key"""
        return self._make_request('get_api_usage')

# Initialize client
hashdive_client = HashdiveClient(HASHDIVE_API_KEY)

def validate_trade_data_integrity(trades, timestamp_gte=None, timestamp_lte=None):
    """Validate trade data for completeness, ordering, and integrity"""
    if not trades or len(trades) == 0:
        return {
            'is_valid': True,  # Changed to True - empty data is valid
            'error_message': None,
            'total_trades': 0,
            'validation_details': {'message': 'No trades to validate'}
        }
    
    validation_details = {
        'total_trades': len(trades),
        'has_timestamps': 0,
        'has_amounts': 0,
        'has_prices': 0,
        'has_market_info': 0,
        'timestamp_gaps': [],
        'ordering_issues': [],
        'missing_critical_fields': []
    }
    
    # Check for critical fields and data quality
    prev_timestamp = None
    timestamp_fields = ['timestamp', 'created_at', 'date', 'time']
    
    for i, trade in enumerate(trades):
        # Check for timestamp
        trade_timestamp = None
        for field in timestamp_fields:
            if field in trade and trade[field]:
                validation_details['has_timestamps'] += 1
                try:
                    ts = trade[field]
                    if isinstance(ts, (int, float)):
                        trade_timestamp = ts if ts < 1e10 else ts / 1000
                    elif isinstance(ts, str):
                        try:
                            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                            trade_timestamp = dt.timestamp()
                        except:
                            dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                            trade_timestamp = dt.timestamp()
                except:
                    continue
                break
        
        # Check timestamp ordering (should be descending - newest first)
        if prev_timestamp is not None and trade_timestamp is not None:
            if trade_timestamp > prev_timestamp:
                validation_details['ordering_issues'].append(f"Trade {i} is newer than previous trade")
        
        if trade_timestamp is not None:
            prev_timestamp = trade_timestamp
        
        # Check for amount/price data
        if any(field in trade and trade[field] for field in ['amount', 'quantity', 'size']):
            validation_details['has_amounts'] += 1
        
        if any(field in trade and trade[field] for field in ['price', 'avg_price', 'execution_price']):
            validation_details['has_prices'] += 1
        
        # Check for market information
        if any(field in trade and trade[field] for field in ['market_question', 'question', 'symbol', 'asset_id']):
            validation_details['has_market_info'] += 1
        
        # Check for critical missing fields
        critical_fields = ['user_address', 'side']
        missing_fields = [field for field in critical_fields if field not in trade or not trade[field]]
        if missing_fields:
            validation_details['missing_critical_fields'].extend(missing_fields)
    
    # Calculate data quality percentages
    total_trades = len(trades)
    timestamp_coverage = validation_details['has_timestamps'] / total_trades
    amount_coverage = validation_details['has_amounts'] / total_trades
    price_coverage = validation_details['has_prices'] / total_trades
    market_coverage = validation_details['has_market_info'] / total_trades
    
    # Determine if data is valid - be more permissive
    is_valid = True  # Default to valid unless major issues
    error_messages = []
    
    # More permissive data quality thresholds - only warn, don't fail
    if timestamp_coverage < 0.3:  # Reduced from 0.8 to 0.3
        error_messages.append(f"Low timestamp data: {timestamp_coverage*100:.1f}% coverage")
    
    if amount_coverage < 0.2:  # Reduced from 0.5 to 0.2
        error_messages.append(f"Low amount data coverage: {amount_coverage*100:.1f}%")
    
    if price_coverage < 0.2:  # Reduced from 0.5 to 0.2
        error_messages.append(f"Low price data coverage: {price_coverage*100:.1f}%")
    
    if len(validation_details['ordering_issues']) > total_trades * 0.5:  # Increased tolerance
        error_messages.append(f"Some timestamp ordering issues: {len(validation_details['ordering_issues'])} out of {total_trades}")
    
    if len(validation_details['missing_critical_fields']) > total_trades * 0.8:  # Only fail if most trades missing critical fields
        is_valid = False
        error_messages.append(f"Too many trades missing critical fields: {set(validation_details['missing_critical_fields'])}")
    
    # Check timestamp filtering if specified
    if timestamp_gte or timestamp_lte:
        filtered_count = 0
        for trade in trades:
            trade_ts = None
            for field in timestamp_fields:
                if field in trade and trade[field]:
                    try:
                        ts = trade[field]
                        if isinstance(ts, (int, float)):
                            trade_ts = ts if ts < 1e10 else ts / 1000
                        break
                    except:
                        continue
            
            if trade_ts:
                if timestamp_gte and trade_ts < timestamp_gte:
                    continue
                if timestamp_lte and trade_ts > timestamp_lte:
                    continue
                filtered_count += 1
        
        if filtered_count == 0 and total_trades > 0:
            is_valid = False
            error_messages.append("No trades found within specified time range")
    
    return {
        'is_valid': is_valid,
        'error_message': '; '.join(error_messages) if error_messages else None,
        'data_quality': {
            'timestamp_coverage': f"{timestamp_coverage*100:.1f}%",
            'amount_coverage': f"{amount_coverage*100:.1f}%",
            'price_coverage': f"{price_coverage*100:.1f}%",
            'market_coverage': f"{market_coverage*100:.1f}%"
        },
        'validation_details': validation_details
    }

def enhance_trade_data(data):
    """Enhance trade data with better timestamp formatting and additional metrics"""
    if not data:
        return data
    
    # Handle different data structures
    records = []
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        if 'trades' in data and isinstance(data['trades'], list):
            records = data['trades']
        elif 'data' in data and isinstance(data['data'], list):
            records = data['data']
        else:
            records = [data]
    
    enhanced_records = []
    total_volume = 0
    total_trades = len(records)
    earliest_timestamp = None
    latest_timestamp = None
    
    for record in records:
        enhanced_record = record.copy()
        
        # Enhanced timestamp formatting
        timestamp_fields = ['timestamp', 'created_at', 'date', 'time']
        for field in timestamp_fields:
            if field in record and record[field]:
                try:
                    # Handle different timestamp formats
                    ts_value = record[field]
                    if isinstance(ts_value, (int, float)):
                        # Unix timestamp (seconds or milliseconds)
                        if ts_value > 1e10:  # Milliseconds
                            ts_value = ts_value / 1000
                        dt = datetime.fromtimestamp(ts_value)
                    elif isinstance(ts_value, str):
                        # ISO format or other string formats
                        try:
                            dt = datetime.fromisoformat(ts_value.replace('Z', '+00:00'))
                        except:
                            dt = datetime.strptime(ts_value, '%Y-%m-%d %H:%M:%S')
                    else:
                        continue
                    
                    # Add formatted timestamp fields
                    enhanced_record[f'{field}_formatted'] = dt.strftime('%Y-%m-%d %H:%M:%S')
                    enhanced_record[f'{field}_date'] = dt.strftime('%Y-%m-%d')
                    enhanced_record[f'{field}_time'] = dt.strftime('%H:%M:%S')
                    enhanced_record[f'{field}_readable'] = dt.strftime('%b %d, %Y at %I:%M %p')
                    
                    # Track earliest and latest timestamps
                    if earliest_timestamp is None or dt < earliest_timestamp:
                        earliest_timestamp = dt
                    if latest_timestamp is None or dt > latest_timestamp:
                        latest_timestamp = dt
                        
                except Exception as e:
                    print(f"Error formatting timestamp {field}: {e}")
                    continue
        
        # Calculate trade volume if possible
        if 'amount' in record and record['amount']:
            try:
                amount = float(record['amount'])
                total_volume += amount
                enhanced_record['amount_formatted'] = f"${amount:,.2f}" if amount > 1 else f"{amount:.6f}"
            except:
                pass
        
        # Add trade sequence number
        enhanced_record['trade_sequence'] = len(enhanced_records) + 1
        
        enhanced_records.append(enhanced_record)
    
    # Calculate user analytics
    user_analytics = {
        'total_trades': total_trades,
        'total_volume': total_volume,
        'trading_period_days': 0,
        'avg_trades_per_day': 0,
        'first_trade_date': None,
        'last_trade_date': None,
        'estimated_total_pnl': 0
    }
    
    if earliest_timestamp and latest_timestamp:
        trading_period = (latest_timestamp - earliest_timestamp).days
        user_analytics['trading_period_days'] = max(1, trading_period)
        user_analytics['avg_trades_per_day'] = total_trades / max(1, trading_period) if trading_period > 0 else total_trades
        user_analytics['first_trade_date'] = earliest_timestamp.strftime('%Y-%m-%d')
        user_analytics['last_trade_date'] = latest_timestamp.strftime('%Y-%m-%d')
    
    # Estimate PnL if possible
    total_pnl = 0
    pnl_count = 0
    for record in enhanced_records:
        pnl_fields = ['pnl', 'profit', 'profit_loss', 'realized_pnl']
        for field in pnl_fields:
            if field in record and record[field] is not None:
                try:
                    pnl_value = float(record[field])
                    total_pnl += pnl_value
                    pnl_count += 1
                    break
                except:
                    continue
    
    if pnl_count > 0:
        user_analytics['estimated_total_pnl'] = total_pnl
        user_analytics['avg_pnl_per_trade'] = total_pnl / pnl_count
    
    # Return enhanced data with analytics
    if isinstance(data, list):
        return {
            'trades': enhanced_records,
            'user_analytics': user_analytics,
            'data_enhanced': True
        }
    elif isinstance(data, dict) and 'trades' in data:
        data['trades'] = enhanced_records
        data['user_analytics'] = user_analytics
        data['data_enhanced'] = True
        return data
    else:
        return {
            'data': enhanced_records,
            'user_analytics': user_analytics,
            'data_enhanced': True
        }

@app.route('/')
def index():
    """Serve the dashboard"""
    return render_template('dashboard.html')

@app.route('/api/fetch_data', methods=['POST'])
def fetch_data():
    """Fetch data from Hashdive API"""
    try:
        data = request.json
        endpoint = data.get('endpoint', 'get_trades')
        
        # Common parameters
        user_address = data.get('user_address', '')
        asset_id = data.get('asset_id', '')
        page_size = int(data.get('page_size', 100))
        format_type = data.get('format', 'json')
        
        result = None
        
        if endpoint == 'get_trades':
            if not user_address:
                return jsonify({'error': 'User address required for trades endpoint'}), 400
            
            # Get timestamp filters from request
            timestamp_gte = data.get('timestamp_gte')
            timestamp_lte = data.get('timestamp_lte')
            
            # Use paginated method to get ALL trades with proper ordering
            result = hashdive_client.get_all_trades_paginated(
                user_address=user_address,
                asset_id=asset_id if asset_id else None,
                timestamp_gte=timestamp_gte,
                timestamp_lte=timestamp_lte,
                format=format_type
            )
            
            # Add optional validation info but never block data display
            if 'error' not in result:
                if 'trades' in result and result['trades'] and len(result['trades']) > 0:
                    trades = result['trades']
                    validation_result = validate_trade_data_integrity(trades, timestamp_gte, timestamp_lte)
                    # Always add validation info but never block the response
                    result['data_validation'] = validation_result
                else:
                    # No trades found or empty result - still valid
                    result['data_validation'] = {
                        'is_valid': True,
                        'error_message': None,
                        'data_quality': {
                            'timestamp_coverage': '0%',
                            'amount_coverage': '0%',
                            'price_coverage': '0%',
                            'market_coverage': '0%'
                        },
                        'validation_details': {
                            'total_trades': 0,
                            'message': 'No trades found for this user address'
                        }
                    }
            
        elif endpoint == 'get_positions':
            if not user_address:
                return jsonify({'error': 'User address required for positions endpoint'}), 400
            result = hashdive_client.get_positions(
                user_address=user_address,
                asset_id=asset_id if asset_id else None,
                format=format_type,
                page_size=page_size
            )
            
        elif endpoint == 'get_last_price':
            if not asset_id:
                return jsonify({'error': 'Asset ID required for last price endpoint'}), 400
            result = hashdive_client.get_last_price(asset_id)
            
        elif endpoint == 'get_ohlcv':
            if not asset_id:
                return jsonify({'error': 'Asset ID required for OHLCV endpoint'}), 400
            resolution = data.get('resolution', '1h')
            result = hashdive_client.get_ohlcv(
                asset_id=asset_id,
                resolution=resolution,
                format=format_type,
                page_size=page_size
            )
            
        elif endpoint == 'search_markets':
            query = data.get('query', '')
            if not query:
                return jsonify({'error': 'Query required for market search endpoint'}), 400
            result = hashdive_client.search_markets(query, page_size=page_size)
            
        elif endpoint == 'get_latest_whale_trades':
            min_usd = int(data.get('min_usd', 10000))
            limit = int(data.get('limit', 1000))
            result = hashdive_client.get_latest_whale_trades(
                min_usd=min_usd,
                limit=limit,
                format=format_type
            )
            
        elif endpoint == 'get_api_usage':
            result = hashdive_client.get_api_usage()
            
        else:
            return jsonify({'error': f'Unknown endpoint: {endpoint}'}), 400
        
        # Enhance the data with better timestamps and analytics
        enhanced_result = enhance_trade_data(result)
        
        return jsonify({
            'success': True,
            'data': enhanced_result,
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/export_csv', methods=['POST'])
def export_csv():
    """Export data as CSV"""
    try:
        data = request.json.get('data', [])
        
        if not data or len(data) == 0:
            return jsonify({'error': 'No data to export'}), 400
        
        # Handle different data types
        csv_content = ""
        
        if isinstance(data, dict) and 'raw_content' in data:
            # Already CSV content
            csv_content = data['raw_content']
        elif isinstance(data, list) and len(data) > 0:
            # Convert JSON to CSV
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            
            csv_content = output.getvalue()
            output.close()
        else:
            return jsonify({'error': 'Data format not suitable for CSV export'}), 400
            
        return jsonify({
            'success': True,
            'csv_content': csv_content,
            'filename': f'hashdive_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("Starting Hashdive Data Analysis Server...")
    print("Dashboard will be available at: http://localhost:5000")
    print("Using API Key:", HASHDIVE_API_KEY[:20] + "...")
    print("\nAvailable Endpoints:")
    print("  - get_trades - User trade history")
    print("  - get_positions - Current user positions")
    print("  - get_last_price - Latest asset prices")
    print("  - get_ohlcv - OHLCV candlestick data")
    print("  - search_markets - Search for markets")
    print("  - get_latest_whale_trades - Large trades")
    print("  - get_api_usage - API usage metrics")
    
    app.run(debug=True, host='0.0.0.0', port=5000)