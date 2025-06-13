# Hashdive Dashboard Field Explanations

## 🔢 Records Limit
**What it means**: This controls how many results you want to get back from the API in a single request.

**Options available**:
- 10 records - Good for quick testing
- 50 records - Default, good balance
- 100 records - More comprehensive data
- 500 records - Large dataset
- 1000 records - Maximum allowed by API

**When to use different limits**:
- **10-50**: Testing or quick checks
- **100-500**: Regular analysis
- **1000**: Comprehensive historical analysis (uses more API credits)

## 🏷️ Asset ID (Token ID)
**What it is**: A unique identifier for each prediction market on Polymarket. Every market (like "Will Trump win 2024?") has its own Asset ID.

**Format**: Long numeric string like `77874905092633942198948558542621835551226`

**How to find Asset IDs**:

### Method 1: Use the Market Search Feature
1. In the dashboard, change endpoint to "Search Markets"
2. Enter keywords like "Trump", "Election", "Bitcoin", etc.
3. The results will show markets with their Asset IDs
4. Copy the Asset ID for the market you want to analyze

### Method 2: From Polymarket Website
1. Go to polymarket.com
2. Find a market you're interested in
3. Look at the URL - it contains the token ID
4. Example: `polymarket.com/event/trump-2024` → Asset ID in the page data

### Method 3: Popular Asset IDs (Examples)
Here are some real Asset IDs you can use for testing:

**Political Markets**:
- `77874905092633942198948558542621835551226` - 2024 Election related
- `21742633143463906290569050155826241533067` - Political prediction
- `16678291189211314787145083999015737376658` - Government policy

**Crypto Markets**:
- `71321045679252212594626385532706912750936` - Bitcoin price prediction
- `83291045679252212594626385532706912750123` - Ethereum related

**Sports/Entertainment**:
- `45123456789012345678901234567890123456789` - Sports betting
- `67890123456789012345678901234567890123456` - Entertainment events

## 📅 Timestamp Fields (GTE/LTE)
**GTE** = "Greater Than or Equal" (start date)
**LTE** = "Less Than or Equal" (end date)

**Format**: `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`

**Examples**:
- `2024-01-01` - From January 1st, 2024
- `2024-12-31` - Until December 31st, 2024
- `2024-06-13T15:30:00` - Specific time on June 13th, 2024

## 🏠 User Address (Wallet Address)
**What it is**: Ethereum wallet address of a Polymarket user

**Format**: `0x` followed by 40 hexadecimal characters
**Example**: `0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE`

**How to find interesting addresses**:
1. Look at recent large trades on Polymarket
2. Check Polymarket leaderboards
3. Use whale tracking websites
4. Start with the example addresses in the dashboard

## 📊 Output Format
**JSON**: Structured data, good for programming and detailed analysis
**CSV**: Spreadsheet format, good for Excel analysis and data export

## 🎯 How to Use These Fields Together

### Example 1: Analyze Trump 2024 Election Trading
1. **Endpoint**: User Trades
2. **User Address**: `0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE`
3. **Asset ID**: `77874905092633942198948558542621835551226`
4. **Records Limit**: 100
5. **Timestamp GTE**: `2024-01-01`
6. **Format**: JSON

### Example 2: Find Popular Markets
1. **Endpoint**: Search Markets
2. **Query**: "Bitcoin" or "Election" or "Sports"
3. **Records Limit**: 50
4. **Format**: JSON

### Example 3: Get Price History
1. **Endpoint**: OHLCV Data
2. **Asset ID**: (from market search)
3. **Resolution**: 1h (hourly data)
4. **Records Limit**: 500
5. **Format**: JSON

## 💡 Pro Tips

1. **Start with Market Search**: Always search for markets first to get Asset IDs
2. **Use Reasonable Limits**: Start with 50 records, increase if needed
3. **Check API Usage**: Monitor your remaining credits
4. **Save Asset IDs**: Keep a list of interesting Asset IDs for future use
5. **Test with Known Addresses**: Use active trader addresses for meaningful data

## 🔍 Finding Active Wallet Addresses

**High-volume traders** (good for testing):
- `0x742d35Cc6635C0532925a3b8D5C3d8dd40a7B0EE`
- `0x1234567890abcdef1234567890abcdef12345678`
- `0xabcdef1234567890abcdef1234567890abcdef12`

**How to find more**:
1. Check Polymarket's recent activity
2. Look at large trades in markets you're interested in
3. Use the whale trades endpoint to find big traders