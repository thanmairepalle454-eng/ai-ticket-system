# AI Ticket System - One-Click Deploy Script
# Run: powershell -ExecutionPolicy Bypass -File deploy.ps1

Write-Host ""
Write-Host "==========================================="-ForegroundColor Cyan
Write-Host "  AI Ticket System - Deploy to Render"    -ForegroundColor Cyan
Write-Host "==========================================="  -ForegroundColor Cyan
Write-Host ""

# Step 1: GitHub Token
Write-Host "STEP 1: GitHub Token" -ForegroundColor Yellow
Write-Host "Get one at: https://github.com/settings/tokens/new" -ForegroundColor Green
Write-Host "  - Note: ai-ticket-deploy"
Write-Host "  - Expiration: 30 days"
Write-Host "  - Check the 'repo' scope checkbox"
Write-Host "  - Click Generate token and copy it"
Write-Host ""
$token = Read-Host "Paste your GitHub token"
$token = $token.Trim()

# Step 2: Get username
Write-Host ""
Write-Host "Verifying token..." -ForegroundColor Yellow
$userResp = Invoke-RestMethod -Uri "https://api.github.com/user" `
    -Headers @{ Authorization = "token $token"; "User-Agent" = "deploy-script" }
$username = $userResp.login
Write-Host "Logged in as: $username" -ForegroundColor Green

# Step 3: Create repo
Write-Host ""
Write-Host "STEP 2: Creating GitHub repository..." -ForegroundColor Yellow
try {
    $body = "{`"name`":`"ai-ticket-system`",`"description`":`"AI IT Ticket System`",`"private`":false}"
    Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
        -Method POST -Body $body -ContentType "application/json" `
        -Headers @{ Authorization = "token $token"; "User-Agent" = "deploy-script" } | Out-Null
    Write-Host "Repo created!" -ForegroundColor Green
} catch {
    Write-Host "Repo may already exist, continuing..." -ForegroundColor Yellow
}

# Step 4: Push code
Write-Host ""
Write-Host "STEP 3: Pushing code to GitHub..." -ForegroundColor Yellow
$remoteUrl = "https://${token}@github.com/${username}/ai-ticket-system.git"
git remote remove origin 2>$null
git remote add origin $remoteUrl
git branch -M main
git push -u origin main --force 2>&1 | Out-Null
Write-Host "Code pushed!" -ForegroundColor Green

# Step 5: Open Render
Write-Host ""
Write-Host "==========================================="  -ForegroundColor Cyan
Write-Host "  STEP 4: Deploy on Render (2 minutes)"    -ForegroundColor Cyan
Write-Host "==========================================="  -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Render will open in your browser"
Write-Host "2. Sign up or log in with GitHub"
Write-Host "3. Click New + then Web Service"
Write-Host "4. Connect the repo: ai-ticket-system"
Write-Host "5. Render detects render.yaml automatically"
Write-Host "6. In Environment Variables section:"
Write-Host "   SMTP_PASSWORD = qmjycppylrsevvoz" -ForegroundColor Yellow
Write-Host "   APP_URL = (fill after deploy with your Render URL)" -ForegroundColor Yellow
Write-Host "7. Click Create Web Service"
Write-Host "8. Wait 3 minutes - you get a live URL!"
Write-Host ""
Write-Host "Your GitHub repo:"
Write-Host "  https://github.com/$username/ai-ticket-system" -ForegroundColor Green
Write-Host ""
Write-Host "Opening browser..." -ForegroundColor Cyan

Start-Process "https://render.com"
Start-Sleep -Seconds 2
Start-Process "https://github.com/$username/ai-ticket-system"

Write-Host ""
Write-Host "Done! Follow the steps above on Render." -ForegroundColor Green
Write-Host "Once deployed, your app works on ANY device worldwide." -ForegroundColor White
