# PowerShell script to prepare and deploy to GitHub
# Run this script from the project root directory

Write-Host "Preparing files for GitHub Pages deployment..." -ForegroundColor Green

# Ensure VLPIM_Web_services directory exists
if (-not (Test-Path "VLPIM_Web_services")) {
    New-Item -ItemType Directory -Path "VLPIM_Web_services" | Out-Null
}

# Copy necessary files
Write-Host "Copying files..." -ForegroundColor Yellow

Copy-Item "web_service\static_example.html" "VLPIM_Web_services\index.html" -Force
Write-Host "  - Copied static_example.html -> VLPIM_Web_services/index.html" -ForegroundColor Gray

if (Test-Path "web_service\readme.html") {
    Copy-Item "web_service\readme.html" "VLPIM_Web_services\" -Force
    Write-Host "  - Copied readme.html" -ForegroundColor Gray
}

if (Test-Path "web_service\toolset.html") {
    Copy-Item "web_service\toolset.html" "VLPIM_Web_services\" -Force
    Write-Host "  - Copied toolset.html" -ForegroundColor Gray
}

if (Test-Path "web_service\DP_P03146_NetMHCIIpan.xls") {
    Copy-Item "web_service\DP_P03146_NetMHCIIpan.xls" "VLPIM_Web_services\" -Force
    Write-Host "  - Copied DP_P03146_NetMHCIIpan.xls" -ForegroundColor Gray
}

if (Test-Path "web_service\6htx.pdb") {
    Copy-Item "web_service\6htx.pdb" "VLPIM_Web_services\" -Force
    Write-Host "  - Copied 6htx.pdb" -ForegroundColor Gray
}

Write-Host "`nFiles prepared successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Initialize git (if not done): git init" -ForegroundColor White
Write-Host "2. Add remote: git remote add origin https://github.com/RuijinHospitalVNAR/Toolboxes.git" -ForegroundColor White
Write-Host "3. Add files: git add ." -ForegroundColor White
Write-Host "4. Commit: git commit -m 'Initial commit: Add VLPIM Web Services'" -ForegroundColor White
Write-Host "5. Push: git push -u origin main" -ForegroundColor White
Write-Host "6. Enable GitHub Pages in repository settings" -ForegroundColor White

