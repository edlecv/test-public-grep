# Manual VSCode Terminal Integration Fix

If the automatic fix doesn't work, here are manual steps:

## Method 1: VSCode Settings Fix
1. Open VSCode Settings (`Ctrl + ,`)
2. Search for: `terminal.integrated.shellIntegration.enabled`
3. Make sure it's checked (enabled)
4. Search for: `terminal.integrated.shellIntegration.decorationsEnabled`  
5. Make sure it's checked (enabled)

## Method 2: PowerShell Profile Fix
1. Open PowerShell as Administrator
2. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine`
3. Run: `notepad $PROFILE.CurrentUserAllHosts`
4. Add these lines to the file:
```powershell
# VSCode Terminal Integration
if ($env:TERM_PROGRAM -eq "vscode") {
    if (Get-Command code -ErrorAction SilentlyContinue) {
        $env:VSCODE_SHELL_INTEGRATION = "1"
    }
}
```
5. Save and close

## Method 3: Reset Terminal
1. In VSCode, open Command Palette (`Ctrl+Shift+P`)
2. Type: "Terminal: Kill All Terminals"
3. Type: "Developer: Reload Window"
4. Open a new terminal

## Test Commands
After applying fixes, test with:
- `Get-Date`
- `Get-Location` 
- `Write-Host "Test output" -ForegroundColor Green`

You should see colorized output and proper command completion.