import requests
import json

def test_hashdive_api():
    """Test the Hashdive API with your key"""
    
    # Your API key from Hashdive
    api_key = "ecb19e0b9907e4d417ede921f1f7d2432b590446211f603e4e239357634cc532"
    base_url = "https://hashdive.com/api"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Testing Hashdive API...")
    print(f"Base URL: {base_url}")
    print(f"API Key: {api_key[:20]}...")
    
    # Test 1: Try to get API info or root endpoint
    print("\n=== Test 1: API Root ===")
    try:
        response = requests.get(f"{base_url}/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.text[:500])
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Try the get_trades endpoint with minimal parameters
    print("\n=== Test 2: Get Trades Endpoint ===")
    try:
        # We need a user address - let's try a common format
        params = {
            "user_address": "0x0000000000000000000000000000000000000000",  # Zero address as test
            "page": 1,
            "page_size": 10
        }
        
        response = requests.get(f"{base_url}/get_trades", headers=headers, params=params)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:1000]}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Successfully retrieved data!")
                print(f"Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            except json.JSONDecodeError:
                print("Response is not JSON")
                
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Check what other endpoints might be available
    print("\n=== Test 3: Common Endpoint Exploration ===")
    common_endpoints = [
        "/markets",
        "/get_markets", 
        "/ohlcv",
        "/get_ohlcv",
        "/whale_activity",
        "/get_whale_activity",
        "/search",
        "/get_search"
    ]
    
    for endpoint in common_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            print(f"{endpoint}: Status {response.status_code}")
            if response.status_code == 200:
                print(f"  ✅ Available - Response: {response.text[:200]}...")
            elif response.status_code == 404:
                print(f"  ❌ Not found")
            else:
                print(f"  ⚠️  Status {response.status_code}: {response.text[:100]}")
        except Exception as e:
            print(f"{endpoint}: Error - {e}")

if __name__ == "__main__":
    test_hashdive_api()