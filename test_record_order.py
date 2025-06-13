import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('HASHDIVE_API_KEY')
headers = {'x-api-key': api_key}
user_address = '0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE'

# Test with small sample
response = requests.get(
    'https://hashdive.com/api/get_trades', 
    headers=headers, 
    params={'user_address': user_address, 'page_size': 5}
)

print("API Status:", response.status_code)
data = response.json()
print("Data Type:", type(data))
print("Number of records:", len(data) if isinstance(data, list) else "Not a list")

if isinstance(data, list) and len(data) > 0:
    print("\nFirst record keys:", list(data[0].keys()) if data[0] else "Empty")
    
    # Check if there are timestamp fields to determine order
    for i, record in enumerate(data[:3]):
        print(f"\nRecord {i+1}:")
        for key, value in record.items():
            if 'time' in key.lower() or 'date' in key.lower():
                print(f"  {key}: {value}")
            elif key in ['id', 'trade_id', 'block_number']:
                print(f"  {key}: {value}")
else:
    print("Response:", str(data)[:500])