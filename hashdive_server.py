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
            params['timestamp_gte'] = timestamp_gte
        if timestamp_lte:
            params['timestamp_lte'] = timestamp_lte
            
        return self._make_request('get_trades', params)
    
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
            result = hashdive_client.get_trades(
                user_address=user_address,
                asset_id=asset_id if asset_id else None,
                format=format_type,
                page_size=page_size
            )
            
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
        
        return jsonify({
            'success': True,
            'data': result,
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