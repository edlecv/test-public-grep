import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_api_ordering():
    api_key = os.getenv('HASHDIVE_API_KEY')
    headers = {'x-api-key': api_key}
    base_url = 'https://hashdive.com/api'
    
    print("=== API RECORD ORDERING ANALYSIS ===\n")
    
    # Try to find markets first to get asset IDs with actual activity
    print("1. Searching for active markets...")
    try:
        markets_response = requests.get(
            f"{base_url}/search_markets",
            headers=headers,
            params={'query': 'Trump', 'page_size': 3}
        )
        if markets_response.status_code == 200:
            markets = markets_response.json()
            if markets and len(markets) > 0:
                print(f"   Found {len(markets)} markets")
                # Get first market's asset ID
                if markets[0].get('outcomes'):
                    asset_id = markets[0]['outcomes'][0].get('asset_id')
                    print(f"   Sample Asset ID: {asset_id[:20]}...")
                else:
                    asset_id = None
            else:
                asset_id = None
        else:
            print(f"   Market search failed: {markets_response.status_code}")
            asset_id = None
    except Exception as e:
        print(f"   Error searching markets: {e}")
        asset_id = None
    
    # Test different approaches to understand ordering
    print("\n2. Testing API ordering behavior...")
    
    # Test 1: Check if there are pagination parameters
    test_params = [
        {'page': 1, 'page_size': 3},
        {'page': 2, 'page_size': 3},
    ]
    
    for i, params in enumerate(test_params, 1):
        print(f"\n   Test {i}: page={params['page']}, page_size={params['page_size']}")
        try:
            response = requests.get(
                f"{base_url}/get_latest_whale_trades",
                headers=headers,
                params=params
            )
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"      Records returned: {len(data)}")
                    if len(data) > 0 and isinstance(data[0], dict):
                        # Look for timestamp fields
                        timestamp_fields = [k for k in data[0].keys() if 'time' in k.lower() or 'date' in k.lower()]
                        print(f"      Timestamp fields: {timestamp_fields}")
                        
                        if timestamp_fields:
                            first_timestamp = data[0].get(timestamp_fields[0])
                            print(f"      First record timestamp: {first_timestamp}")
                else:
                    print(f"      Response type: {type(data)}")
            else:
                print(f"      API error: {response.status_code}")
        except Exception as e:
            print(f"      Error: {e}")

def explain_typical_api_behavior():
    print("\n=== TYPICAL API ORDERING BEHAVIOR ===")
    print("""
Most trading/financial APIs follow these patterns:

📊 STANDARD ORDERING (Most Common):
   • Most Recent First (Descending by timestamp)
   • This means: Latest trades → Older trades
   • With 1000 limit: You get the 1000 most recent records

🔄 PAGINATION LOGIC:
   • Page 1: Most recent 1000 records
   • Page 2: Next 1000 older records
   • Page 3: Even older records, etc.

📈 FOR WIN RATE CALCULATION:
   • Records Limit 1000 = Last 1000 trades/positions
   • This gives you RECENT performance (most relevant)
   • To get ALL 9000+ records: Use pagination (multiple requests)

⚠️  IMPORTANT FOR 9000+ POSITIONS:
   If user has 9000+ positions and you set limit to 1000:
   • You get: The 1000 MOST RECENT positions
   • You miss: The 8000+ older positions
   
   For complete win rate: Need to paginate through all pages
   or use timestamp filters to get specific time periods.
""")

if __name__ == "__main__":
    test_api_ordering()
    explain_typical_api_behavior()