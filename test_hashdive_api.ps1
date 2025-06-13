# PowerShell script to test Hashdive API
$apiKey = "ecb19e0b9987e4d417ede921f1f7d2432b59044621f663e4e23935763dcc532"
$baseUrl = "https://hashdive.com/api"

$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

Write-Host "Testing Hashdive API..." -ForegroundColor Green
Write-Host "Base URL: $baseUrl"
Write-Host "API Key: $($apiKey.Substring(0,20))..."

# Test 1: API Root
Write-Host "`n=== Test 1: API Root ===" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/" -Headers $headers -Method Get
    Write-Host "Root endpoint accessible" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 2)"
} catch {
    Write-Host "Root endpoint error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Get Trades
Write-Host "`n=== Test 2: Get Trades Endpoint ===" -ForegroundColor Yellow
try {
    $params = @{
        "user_address" = "0x0000000000000000000000000000000000000000"
        "page" = 1
        "page_size" = 10
    }
    
    $queryString = ($params.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join "?"
    $url = "$baseUrl/get_trades?$queryString"
    
    $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Get
    Write-Host "Get trades successful" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 2)"
} catch {
    Write-Host "Get trades error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)"
    }
}

# Test 3: Common endpoints
Write-Host "`n=== Test 3: Common Endpoint Exploration ===" -ForegroundColor Yellow
$endpoints = @("/markets", "/get_markets", "/ohlcv", "/get_ohlcv", "/whale_activity", "/get_whale_activity")

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl$endpoint" -Headers $headers -Method Get
        Write-Host "$endpoint - Available" -ForegroundColor Green
        $responseText = $response | ConvertTo-Json -Depth 1 | Out-String
        Write-Host "   Response: $($responseText.Substring(0, [Math]::Min(200, $responseText.Length)))..."
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq 404) {
            Write-Host "$endpoint - Not found (404)" -ForegroundColor Red
        } else {
            Write-Host "$endpoint - Status $statusCode" -ForegroundColor Yellow
        }
    }
}

Write-Host "`nAPI testing complete!" -ForegroundColor Green