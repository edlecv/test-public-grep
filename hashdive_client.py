import requests
import json
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HashdiveClient:
    def __init__(self, api_key: str):
        self.base_url = "https://hashdive.com/api"
        self.api_key = api_key
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[Any, Any]:
        """Make a request to the Hashdive API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return {}
    
    def get_trades(self, 
                   user_address: str, 
                   asset_id: Optional[str] = None,
                   timestamp_gte: Optional[str] = None,
                   timestamp_lte: Optional[str] = None,
                   format: str = "json",
                   page: int = 1,
                   page_size: int = 100) -> Dict[Any, Any]:
        """
        Get trades for a given user, enriched with market metadata.
        
        Args:
            user_address: Wallet address (required)
            asset_id: Optional filter by market
            timestamp_gte: ISO format time range start
            timestamp_lte: ISO format time range end  
            format: "json" (default) or "csv"
            page: Page number
            page_size: Max page size (1000)
        """
        params = {
            "user_address": user_address,
            "format": format,
            "page": page,
            "page_size": page_size
        }
        
        if asset_id:
            params["asset_id"] = asset_id
        if timestamp_gte:
            params["timestamp_gte"] = timestamp_gte
        if timestamp_lte:
            params["timestamp_lte"] = timestamp_lte
            
        return self._make_request("/get_trades", params)
    
    def explore_api(self):
        """Explore available endpoints by making a simple request"""
        # Try to get API info or make a test request
        print("Exploring Hashdive API...")
        print(f"Base URL: {self.base_url}")
        print(f"API Key: {self.api_key[:10]}...")
        
        # You can add more endpoint methods here as you discover them
        # For example: get_markets(), get_ohlcv(), get_whale_activity(), etc.

def main():
    # Load API key from environment
    api_key = os.getenv("HASHDIVE_API_KEY")
    if not api_key:
        print("Error: HASHDIVE_API_KEY not found in environment variables")
        print("Please check your .env file")
        return
    
    # Create client
    client = HashdiveClient(api_key)
    
    # Explore the API
    client.explore_api()
    
    # Example: Get trades for a specific address
    # You'll need a real wallet address to test this
    example_address = "0x1234567890abcdef1234567890abcdef12345678"  # Replace with real address
    
    print(f"\n=== Getting trades for address: {example_address} ===")
    trades = client.get_trades(user_address=example_address)
    print(json.dumps(trades, indent=2))

if __name__ == "__main__":
    main()