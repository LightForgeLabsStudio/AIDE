#!/usr/bin/env pwsh
# Install AIDE skills for Claude (repo-local .claude/skills)

param(
    [switch]$Symlink = $false,
    [string]$RepoRoot = "",
    [string]$SkillsPath = ""
)

$ErrorActionPreference = "Stop"

Write-Host "Installing AIDE skills for Claude..." -ForegroundColor Cyan

# This script lives in: <consumer-repo>/.aide/skills/
$aideSkillsDir = $PSScriptRoot
$aideRepoDir = Resolve-Path (Join-Path $aideSkillsDir "..")

if (-not (Test-Path $aideSkillsDir)) {
    Write-Error "AIDE skills directory not found: $aideSkillsDir"
    exit 1
}

if ($RepoRoot -eq "") {
    # Default to the repo that contains the .aide submodule
    $RepoRoot = (Resolve-Path (Join-Path $aideRepoDir "..")).Path
}

if ($SkillsPath -eq "") {
    $SkillsPath = Join-Path $RepoRoot ".claude\\skills"
}

Write-Host "Repo root: $RepoRoot" -ForegroundColor Gray
Write-Host "Target Claude skills dir: $SkillsPath" -ForegroundColor Gray

if (-not (Test-Path $SkillsPath)) {
    Write-Host "Creating skills directory: $SkillsPath" -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $SkillsPath | Out-Null
}

# Get all skill directories (exclude dist/ and any non-skill dirs)
$skills = Get-ChildItem -Path $aideSkillsDir -Directory | Where-Object {
    $_.Name -ne "dist" -and (Test-Path (Join-Path $_.FullName "SKILL.md"))
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
        # Create symlink (may require admin on Windows depending on policy)
        if (Test-Path $targetPath) {
            Write-Host "  Removing existing: $skillName" -ForegroundColor Yellow
            Remove-Item -Recurse -Force $targetPath
        }

        Write-Host "  Symlinking: $skillName" -ForegroundColor Cyan
        New-Item -ItemType SymbolicLink -Path $targetPath -Target $sourcePath | Out-Null
        continue
    }

    # Copy files
    if (Test-Path $targetPath) {
        Write-Host "  Updating: $skillName" -ForegroundColor Yellow
        Remove-Item -Recurse -Force $targetPath
    } else {
        Write-Host "  Installing: $skillName" -ForegroundColor Green
    }

    Copy-Item -Recurse -Force $sourcePath $targetPath
}

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Installed skills (repo-local):" -ForegroundColor Cyan
foreach ($skill in $skills) {
    Write-Host "  /$($skill.Name)" -ForegroundColor White
}
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Reload your tool (VS Code: Ctrl+Shift+P -> 'Reload Window')"
Write-Host "  2. Type '/' in Claude chat to see available commands"
Write-Host ""

if (-not $Symlink) {
    Write-Host "Note: Skills were copied. To auto-sync with AIDE updates, re-run with -Symlink" -ForegroundColor Gray
}
