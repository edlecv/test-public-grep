# VSCode Terminal Integration Test Script
# This script tests various terminal features to verify integration is working

Write-Host "🧪 Testing VSCode Terminal Integration..." -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# Test 1: Basic colored output
Write-Host "`n✅ Test 1: Colored Output" -ForegroundColor Green
Write-Host "Success message" -ForegroundColor Green
Write-Host "Warning message" -ForegroundColor Yellow  
Write-Host "Error message" -ForegroundColor Red
Write-Host "Info message" -ForegroundColor Blue

# Test 2: System information
Write-Host "`n🖥️ Test 2: System Information" -ForegroundColor Cyan
Write-Host "Current Date/Time: $(Get-Date)" -ForegroundColor White
Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor White
Write-Host "Current Location: $(Get-Location)" -ForegroundColor White
Write-Host "Execution Policy: $(Get-ExecutionPolicy)" -ForegroundColor White

# Test 3: Environment variables
Write-Host "`n🌍 Test 3: VSCode Environment Check" -ForegroundColor Cyan
if ($env:TERM_PROGRAM -eq "vscode") {
    Write-Host "✅ Running in VSCode terminal" -ForegroundColor Green
} else {
    Write-Host "❌ Not detected as VSCode terminal" -ForegroundColor Red
}

if ($env:VSCODE_SHELL_INTEGRATION) {
    Write-Host "✅ VSCode Shell Integration: Enabled" -ForegroundColor Green
} else {
    Write-Host "⚠️ VSCode Shell Integration: Not detected" -ForegroundColor Yellow
}

# Test 4: File operations
Write-Host "`n📁 Test 4: File Operations" -ForegroundColor Cyan
$testFile = "terminal_test.tmp"
"Test content from PowerShell" | Out-File -FilePath $testFile -Encoding UTF8
if (Test-Path $testFile) {
    Write-Host "✅ File created successfully: $testFile" -ForegroundColor Green
    $content = Get-Content $testFile
    Write-Host "📄 File content: $content" -ForegroundColor White
    Remove-Item $testFile -Force
    Write-Host "🗑️ Test file cleaned up" -ForegroundColor Yellow
} else {
    Write-Host "❌ Failed to create test file" -ForegroundColor Red
}

# Test 5: Progress simulation
Write-Host "`n⏳ Test 5: Progress Indicator" -ForegroundColor Cyan
for ($i = 1; $i -le 5; $i++) {
    Write-Progress -Activity "Testing Terminal Integration" -Status "Step $i of 5" -PercentComplete (($i / 5) * 100)
    Start-Sleep -Milliseconds 500
}
Write-Progress -Activity "Testing Terminal Integration" -Completed
Write-Host "✅ Progress test completed" -ForegroundColor Green

# Test 6: Command execution with output
Write-Host "`n🔧 Test 6: Command Output" -ForegroundColor Cyan
$processes = Get-Process | Select-Object -First 3 Name, Id, CPU
Write-Host "Top 3 Processes:" -ForegroundColor White
$processes | Format-Table -AutoSize

# Test 7: Error handling
Write-Host "`n⚠️ Test 7: Error Handling" -ForegroundColor Cyan
try {
    Get-Item "NonExistentFile.txt" -ErrorAction Stop
} catch {
    Write-Host "✅ Error caught successfully: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test 8: Interactive-style output
Write-Host "`n🎯 Test 8: Interactive Output" -ForegroundColor Cyan
Write-Host "Simulating AI command execution..." -ForegroundColor Magenta
Start-Sleep -Seconds 1
Write-Host "Command: Get-ComputerInfo | Select-Object WindowsProductName, TotalPhysicalMemory" -ForegroundColor Gray
$computerInfo = Get-ComputerInfo | Select-Object WindowsProductName, TotalPhysicalMemory
Write-Host "✅ Command executed successfully!" -ForegroundColor Green
$computerInfo | Format-List

# Final summary
Write-Host "`n" + "=" * 50 -ForegroundColor Gray
Write-Host "🎉 Terminal Integration Test Complete!" -ForegroundColor Green
Write-Host "If you can see all colors, progress bars, and formatted output," -ForegroundColor White
Write-Host "then your VSCode terminal integration is working perfectly!" -ForegroundColor White
Write-Host "=" * 50 -ForegroundColor Gray