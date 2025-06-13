# VSCode Terminal Integration Test Script
# This script tests various terminal features to verify integration is working

Write-Host "Testing VSCode Terminal Integration..." -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# Test 1: Basic colored output
Write-Host "`nTest 1: Colored Output" -ForegroundColor Green
Write-Host "Success message" -ForegroundColor Green
Write-Host "Warning message" -ForegroundColor Yellow  
Write-Host "Error message" -ForegroundColor Red
Write-Host "Info message" -ForegroundColor Blue

# Test 2: System information
Write-Host "`nTest 2: System Information" -ForegroundColor Cyan
Write-Host "Current Date/Time: $(Get-Date)" -ForegroundColor White
Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor White
Write-Host "Current Location: $(Get-Location)" -ForegroundColor White
Write-Host "Execution Policy: $(Get-ExecutionPolicy)" -ForegroundColor White

# Test 3: Environment variables
Write-Host "`nTest 3: VSCode Environment Check" -ForegroundColor Cyan
if ($env:TERM_PROGRAM -eq "vscode") {
    Write-Host "[SUCCESS] Running in VSCode terminal" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Not detected as VSCode terminal" -ForegroundColor Red
}

if ($env:VSCODE_SHELL_INTEGRATION) {
    Write-Host "[SUCCESS] VSCode Shell Integration: Enabled" -ForegroundColor Green
} else {
    Write-Host "[INFO] VSCode Shell Integration: Not detected (normal after restart)" -ForegroundColor Yellow
}

# Test 4: File operations
Write-Host "`nTest 4: File Operations" -ForegroundColor Cyan
$testFile = "terminal_test.tmp"
"Test content from PowerShell" | Out-File -FilePath $testFile -Encoding UTF8
if (Test-Path $testFile) {
    Write-Host "[SUCCESS] File created successfully: $testFile" -ForegroundColor Green
    $content = Get-Content $testFile
    Write-Host "File content: $content" -ForegroundColor White
    Remove-Item $testFile -Force
    Write-Host "[CLEANUP] Test file removed" -ForegroundColor Yellow
} else {
    Write-Host "[ERROR] Failed to create test file" -ForegroundColor Red
}

# Test 5: Command execution with output
Write-Host "`nTest 5: Command Output" -ForegroundColor Cyan
$services = Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object -First 3 Name, Status
Write-Host "Sample Running Services:" -ForegroundColor White
$services | Format-Table -AutoSize

# Test 6: Error handling
Write-Host "`nTest 6: Error Handling" -ForegroundColor Cyan
try {
    Get-Item "NonExistentFile.txt" -ErrorAction Stop
} catch {
    Write-Host "[SUCCESS] Error caught successfully: File not found" -ForegroundColor Yellow
}

# Test 7: Variable demonstration
Write-Host "`nTest 7: Variable Operations" -ForegroundColor Cyan
$testVar = "Hello from PowerShell!"
Write-Host "Variable value: $testVar" -ForegroundColor White
$numbers = 1..5
Write-Host "Array of numbers: $($numbers -join ', ')" -ForegroundColor White

# Final summary
Write-Host "`n" + "=" * 50 -ForegroundColor Gray
Write-Host "Terminal Integration Test Complete!" -ForegroundColor Green
Write-Host "If you can see colors and formatted output," -ForegroundColor White
Write-Host "your VSCode terminal integration is working!" -ForegroundColor White
Write-Host "=" * 50 -ForegroundColor Gray