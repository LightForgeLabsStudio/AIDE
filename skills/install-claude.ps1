#!/usr/bin/env pwsh
# Install AIDE skills for Claude Code (VS Code Extension or CLI)

param(
    [switch]$Symlink = $false,
    [string]$SkillsPath = "$HOME\.claude\skills"
)

$ErrorActionPreference = "Stop"

Write-Host "Installing AIDE skills for Claude Code..." -ForegroundColor Cyan

# Get AIDE skills directory (script is in .aide/skills/)
$aideSkillsDir = $PSScriptRoot
if (-not (Test-Path $aideSkillsDir)) {
    Write-Error "AIDE skills directory not found: $aideSkillsDir"
    exit 1
}

# Ensure target directory exists
if (-not (Test-Path $SkillsPath)) {
    Write-Host "Creating skills directory: $SkillsPath" -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $SkillsPath | Out-Null
}

# Get all skill directories (exclude README.md, scripts, etc.)
$skills = Get-ChildItem -Path $aideSkillsDir -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "SKILL.md")
}

if ($skills.Count -eq 0) {
    Write-Warning "No skills found in $aideSkillsDir"
    exit 0
}

Write-Host "Found $($skills.Count) skills to install" -ForegroundColor Green

foreach ($skill in $skills) {
    $skillName = $skill.Name
    $sourcePath = $skill.FullName
    $targetPath = Join-Path $SkillsPath $skillName

    if ($Symlink) {
        # Create symlink (requires admin on Windows)
        if (Test-Path $targetPath) {
            Write-Host "  Removing existing: $skillName" -ForegroundColor Yellow
            Remove-Item -Recurse -Force $targetPath
        }

        Write-Host "  Symlinking: $skillName" -ForegroundColor Cyan
        New-Item -ItemType SymbolicLink -Path $targetPath -Target $sourcePath | Out-Null
    } else {
        # Copy files
        if (Test-Path $targetPath) {
            Write-Host "  Updating: $skillName" -ForegroundColor Yellow
            Remove-Item -Recurse -Force $targetPath
        } else {
            Write-Host "  Installing: $skillName" -ForegroundColor Green
        }

        Copy-Item -Recurse -Force $sourcePath $targetPath
    }
}

Write-Host ""
Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Installed skills:" -ForegroundColor Cyan
foreach ($skill in $skills) {
    Write-Host "  /$($skill.Name)" -ForegroundColor White
}
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Reload VS Code (Ctrl+Shift+P → 'Reload Window')"
Write-Host "  2. Type '/' in Claude Code chat to see available commands"
Write-Host ""

if (-not $Symlink) {
    Write-Host "Note: Skills were copied. To auto-sync with AIDE updates, re-run with -Symlink" -ForegroundColor Gray
}
