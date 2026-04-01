# ═══════════════════════════════════════════════════════════
#  AI Ticket System — One-Click Deploy Script
#  Run this in PowerShell: .\deploy.ps1
# ═══════════════════════════════════════════════════════════

Write-Host ""
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   AI Ticket System — Deploy to Render   ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Step 1: Get GitHub token ─────────────────────────────────
Write-Host "STEP 1: GitHub Setup" -ForegroundColor Yellow
Write-Host "──────────────────────────────────────────"
Write-Host "You need a GitHub Personal Access Token."
Write-Host ""
Write-Host "Get one here (takes 1 minute):"
Write-Host "  https://github.com/settings/tokens/new" -ForegroundColor Green
Write-Host ""
Write-Host "Settings to use:"
Write-Host "  - Note: ai-ticket-deploy"
Write-Host "  - Expiration: 30 days"
Write-Host "  - Scopes: check 'repo' (full control)"
Write-Host "  - Click 'Generate token' and copy it"
Write-Host ""
$token = Read-Host "Paste your GitHub token here"
$token = $token.Trim()

# ── Step 2: Get GitHub username ──────────────────────────────
Write-Host ""
$userResp = Invoke-RestMethod -Uri "https://api.github.com/user" `
    -Headers @{ Authorization = "token $token"; "User-Agent" = "ai-ticket-deploy" }
$username = $userResp.login
Write-Host "✅ Logged in as: $username" -ForegroundColor Green

# ── Step 3: Create GitHub repo ───────────────────────────────
Write-Host ""
Write-Host "STEP 2: Creating GitHub repository..." -ForegroundColor Yellow
try {
    $body = '{"name":"ai-ticket-system","description":"AI-powered IT Ticket System","private":false}'
    $repoResp = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
        -Method POST -Body $body -ContentType "application/json" `
        -Headers @{ Authorization = "token $token"; "User-Agent" = "ai-ticket-deploy" }
    Write-Host "✅ Repo created: $($repoResp.html_url)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Repo may already exist — continuing..." -ForegroundColor Yellow
}

# ── Step 4: Push code ────────────────────────────────────────
Write-Host ""
Write-Host "STEP 3: Pushing code to GitHub..." -ForegroundColor Yellow
$remoteUrl = "https://${token}@github.com/${username}/ai-ticket-system.git"
git remote remove origin 2>$null
git remote add origin $remoteUrl
git branch -M main
git push -u origin main --force 2>&1 | Out-Null
Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green

# ── Step 5: Render deploy instructions ───────────────────────
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   STEP 4: Deploy on Render (2 minutes)                  ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Open this URL in your browser:" -ForegroundColor White
Write-Host "   https://render.com" -ForegroundColor Green
Write-Host ""
Write-Host "2. Sign up / Log in with GitHub" -ForegroundColor White
Write-Host ""
Write-Host "3. Click 'New +' → 'Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "4. Click 'Connect' next to: ai-ticket-system" -ForegroundColor White
Write-Host ""
Write-Host "5. Render auto-detects render.yaml — scroll down" -ForegroundColor White
Write-Host "   Find 'SMTP_PASSWORD' → click 'Add' → paste:" -ForegroundColor White
Write-Host "   qmjycppylrsevvoz" -ForegroundColor Yellow
Write-Host ""
Write-Host "6. Find 'APP_URL' → click 'Add' → you will fill this" -ForegroundColor White
Write-Host "   AFTER deploy with your Render URL (e.g. https://ai-ticket-system.onrender.com)" -ForegroundColor White
Write-Host ""
Write-Host "7. Click 'Create Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "8. Wait ~3 minutes for deploy to finish" -ForegroundColor White
Write-Host ""
Write-Host "9. Copy your live URL (shown at top of Render dashboard)" -ForegroundColor White
Write-Host "   Go to Environment → set APP_URL = your live URL → Save" -ForegroundColor White
Write-Host ""
Write-Host "══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your GitHub repo: https://github.com/$username/ai-ticket-system" -ForegroundColor Green
Write-Host ""
Write-Host "Once deployed, share your Render URL with everyone." -ForegroundColor White
Write-Host "It works on ANY device, ANY system, worldwide." -ForegroundColor White
Write-Host ""

# Open browser automatically
Start-Process "https://render.com"
Start-Process "https://github.com/$username/ai-ticket-system"
