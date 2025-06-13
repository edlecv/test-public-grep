# Fix VSCode Terminal Integration Script
Write-Host "Fixing VSCode Terminal Integration..." -ForegroundColor Green

# 1. Check current PowerShell execution policy
$currentPolicy = Get-ExecutionPolicy
Write-Host "Current PowerShell Execution Policy: $currentPolicy" -ForegroundColor Yellow

# 2. If execution policy is too restrictive, we need to change it
if ($currentPolicy -eq "Restricted") {
    Write-Host "Setting PowerShell execution policy to RemoteSigned..." -ForegroundColor Yellow
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Host "✅ Execution policy updated successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to update execution policy. You may need to run as administrator." -ForegroundColor Red
        Write-Host "Manual fix: Run PowerShell as Administrator and execute:" -ForegroundColor Yellow
        Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine" -ForegroundColor Cyan
    }
}

# 3. Check if VSCode shell integration is working
$vscodeShellIntegration = $env:VSCODE_SHELL_INTEGRATION
if ($vscodeShellIntegration) {
    Write-Host "✅ VSCode Shell Integration environment variable is set" -ForegroundColor Green
} else {
    Write-Host "❌ VSCode Shell Integration environment variable not found" -ForegroundColor Red
}

# 4. Create/Update PowerShell profile for VSCode integration
$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path $profilePath -Parent

if (!(Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force
    Write-Host "✅ Created PowerShell profile directory" -ForegroundColor Green
}

# 5. Add VSCode integration to PowerShell profile
$vscodeIntegrationScript = @'
# VSCode Terminal Integration
if ($env:TERM_PROGRAM -eq "vscode") {
    if (Get-Command code -ErrorAction SilentlyContinue) {
        # Enable VSCode shell integration
        $env:VSCODE_SHELL_INTEGRATION = "1"
    }
}
'@

if (Test-Path $profilePath) {
    $profileContent = Get-Content $profilePath -Raw
    if ($profileContent -notlike "*VSCODE_SHELL_INTEGRATION*") {
        Add-Content -Path $profilePath -Value "`n$vscodeIntegrationScript"
        Write-Host "✅ Added VSCode integration to PowerShell profile" -ForegroundColor Green
    } else {
        Write-Host "✅ VSCode integration already exists in PowerShell profile" -ForegroundColor Green
    }
} else {
    Set-Content -Path $profilePath -Value $vscodeIntegrationScript
    Write-Host "✅ Created PowerShell profile with VSCode integration" -ForegroundColor Green
}

Write-Host "`n🔧 Configuration Summary:" -ForegroundColor Cyan
Write-Host "- PowerShell Profile: $profilePath" -ForegroundColor White
Write-Host "- Execution Policy: $(Get-ExecutionPolicy)" -ForegroundColor White
$integrationStatus = if ($env:VSCODE_SHELL_INTEGRATION -eq '1') { 'Enabled' } else { 'Needs Restart' }
Write-Host "- VSCode Integration: $integrationStatus" -ForegroundColor White

Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Close all VSCode windows" -ForegroundColor Yellow
Write-Host "2. Restart VSCode completely" -ForegroundColor Yellow
Write-Host "3. Open a new terminal in VSCode" -ForegroundColor Yellow
Write-Host "4. Test with a simple command like 'Get-Date'" -ForegroundColor Yellow

Write-Host "`n✨ VSCode Terminal Integration Fix Complete!" -ForegroundColor Green