#!/usr/bin/env python3
"""
Script to help you find real Asset IDs from Hashdive API
This will search for markets and show you their Asset IDs
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AssetIDFinder:
    def __init__(self):
        self.api_key = os.getenv("HASHDIVE_API_KEY")
        self.base_url = "https://hashdive.com/api"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def search_markets(self, query, limit=10):
        """Search for markets and return their Asset IDs"""
        params = {
            "query": query,
            "page": 1,
            "page_size": limit
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/search_markets", 
                headers=self.headers, 
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Search failed: {str(e)}"}
    
    def get_popular_searches(self):
        """Get Asset IDs for popular market categories"""
        searches = [
            "Trump",
            "Election", 
            "Bitcoin",
            "Ethereum",
            "Sports",
            "AI",
            "Stock Market",
            "Weather"
        ]
        
        results = {}
        for search_term in searches:
            print(f"\n🔍 Searching for: {search_term}")
            result = self.search_markets(search_term, 3)
            results[search_term] = result
            
            if "error" in result:
                print(f"   ❌ Error: {result['error']}")
            else:
                # Display results in a user-friendly way
                if isinstance(result, list) and len(result) > 0:
                    for i, market in enumerate(result[:3], 1):
                        asset_id = market.get('asset_id', 'N/A')
                        title = market.get('question', market.get('title', 'Unknown Market'))
                        print(f"   {i}. Asset ID: {asset_id}")
                        print(f"      Market: {title[:60]}...")
                elif isinstance(result, dict) and 'data' in result:
                    for i, market in enumerate(result['data'][:3], 1):
                        asset_id = market.get('asset_id', 'N/A')
                        title = market.get('question', market.get('title', 'Unknown Market'))
                        print(f"   {i}. Asset ID: {asset_id}")
                        print(f"      Market: {title[:60]}...")
                else:
                    print(f"   📝 Response: {str(result)[:100]}...")
        
        return results
    
    def test_api_connection(self):
        """Test if the API key is working"""
        try:
            response = requests.get(
                f"{self.base_url}/get_api_usage",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                usage = response.json()
                print("✅ API Connection successful!")
                print(f"📊 API Usage: {usage}")
                return True
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return False

def main():
    print("🚀 Hashdive Asset ID Finder")
    print("=" * 50)
    
    finder = AssetIDFinder()
    
    # Test API connection first
    if not finder.test_api_connection():
        print("\n❌ Cannot connect to Hashdive API. Please check your API key.")
        return
    
    print("\n🔍 Finding Asset IDs for popular market categories...")
    results = finder.get_popular_searches()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY: Copy these Asset IDs for testing")
    print("=" * 50)
    
    # Extract and display all found Asset IDs
    all_asset_ids = []
    for category, result in results.items():
        if "error" not in result:
            if isinstance(result, list):
                for market in result:
                    asset_id = market.get('asset_id')
                    if asset_id:
                        all_asset_ids.append(asset_id)
            elif isinstance(result, dict) and 'data' in result:
                for market in result['data']:
                    asset_id = market.get('asset_id')
                    if asset_id:
                        all_asset_ids.append(asset_id)
    
    if all_asset_ids:
        print("\n📝 Asset IDs you can use in the dashboard:")
        for i, asset_id in enumerate(all_asset_ids[:10], 1):  # Show first 10
            print(f"{i:2d}. {asset_id}")
    else:
        print("\n⚠️  No Asset IDs found. The API might be returning different data structure.")
        print("   Try using the dashboard's Market Search feature instead.")
    
    print(f"\n💡 Tip: Use these Asset IDs in the dashboard's 'Asset ID' field")
    print(f"💡 Tip: You can also search for specific topics using the Market Search endpoint")

if __name__ == "__main__":
    main()