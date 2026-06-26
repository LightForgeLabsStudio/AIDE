#!/usr/bin/env pwsh
# Install AIDE skills for Codex (repo-local .codex/skills)

param(
    [switch]$Symlink = $true,
    [string]$RepoRoot = "",
    [string]$SkillsPath = ""
)

$ErrorActionPreference = "Stop"
$OnWindows = $env:OS -eq "Windows_NT"

Write-Host "Installing AIDE skills for Codex..." -ForegroundColor Cyan

function Remove-SkillInstallTarget {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }

    $item = Get-Item -LiteralPath $Path -Force
    if ($OnWindows -and $item.PSIsContainer -and $item.LinkType -eq "Junction") {
        cmd /c rmdir $Path | Out-Null
        return
    }

    Remove-Item -LiteralPath $Path -Recurse -Force
}

function New-SkillInstallLink {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Target
    )

    if ($OnWindows) {
        New-Item -ItemType Junction -Path $Path -Target $Target | Out-Null
        return "junction"
    }

    New-Item -ItemType SymbolicLink -Path $Path -Target $Target | Out-Null
    return "symlink"
}

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
    $SkillsPath = Join-Path $RepoRoot ".codex\\skills"
}

Write-Host "Repo root: $RepoRoot" -ForegroundColor Gray
Write-Host "Target Codex skills dir: $SkillsPath" -ForegroundColor Gray
Write-Host ("Install mode: {0}" -f ($(if ($Symlink) { "linked" } else { "copy" }))) -ForegroundColor Gray

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
        if (Test-Path $targetPath) {
            Write-Host "  Removing existing: $skillName" -ForegroundColor Yellow
            Remove-SkillInstallTarget -Path $targetPath
        }

        $linkType = New-SkillInstallLink -Path $targetPath -Target $sourcePath
        Write-Host "  Linking ($linkType): $skillName" -ForegroundColor Cyan
        continue
    }

    # Copy files
    if (Test-Path $targetPath) {
        Write-Host "  Updating: $skillName" -ForegroundColor Yellow
        Remove-SkillInstallTarget -Path $targetPath
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
Write-Host "  1. Ensure Codex is configured to load repo skills from .codex/skills"
Write-Host "  2. Reload VS Code / restart Codex if needed"
Write-Host ""

if ($Symlink) {
    Write-Host "Note: Skills were linked to the .aide canonicals." -ForegroundColor Gray
    Write-Host "      Windows uses directory junctions; non-Windows uses symbolic links." -ForegroundColor Gray
    Write-Host "      Re-run with -Symlink:`$false if you need a copied install instead." -ForegroundColor Gray
} else {
    Write-Host "Note: Skills were copied. Re-run with -Symlink to keep Codex skills synced to .aide." -ForegroundColor Gray
}
