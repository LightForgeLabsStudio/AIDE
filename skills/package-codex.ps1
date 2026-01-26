#!/usr/bin/env pwsh
# Package AIDE skills for Codex (creates .skill zip files)

param(
    [string]$OutputDir = "$PSScriptRoot\dist"
)

$ErrorActionPreference = "Stop"

Write-Host "Packaging AIDE skills for Codex..." -ForegroundColor Cyan

# Get AIDE skills directory
$aideSkillsDir = $PSScriptRoot
if (-not (Test-Path $aideSkillsDir)) {
    Write-Error "AIDE skills directory not found: $aideSkillsDir"
    exit 1
}

# Ensure output directory exists
if (-not (Test-Path $OutputDir)) {
    Write-Host "Creating output directory: $OutputDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
}

# Get all skill directories
$skills = Get-ChildItem -Path $aideSkillsDir -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "SKILL.md")
}

if ($skills.Count -eq 0) {
    Write-Warning "No skills found in $aideSkillsDir"
    exit 0
}

Write-Host "Found $($skills.Count) skills to package" -ForegroundColor Green

# Load compression assembly
Add-Type -AssemblyName System.IO.Compression.FileSystem

foreach ($skill in $skills) {
    $skillName = $skill.Name
    $sourcePath = $skill.FullName
    $outputFile = Join-Path $OutputDir "aide-$skillName.skill"

    Write-Host "  Packaging: aide-$skillName.skill" -ForegroundColor Cyan

    # Remove existing package
    if (Test-Path $outputFile) {
        Remove-Item -Force $outputFile
    }

    # Create zip archive
    [System.IO.Compression.ZipFile]::CreateFromDirectory(
        $sourcePath,
        $outputFile,
        [System.IO.Compression.CompressionLevel]::Optimal,
        $false
    )

    # Verify package was created
    if (Test-Path $outputFile) {
        $size = (Get-Item $outputFile).Length
        $sizeKB = [math]::Round($size / 1KB, 2)
        Write-Host "    ✓ Created: $sizeKB KB" -ForegroundColor Green
    } else {
        Write-Error "Failed to create package: $outputFile"
    }
}

Write-Host ""
Write-Host "✅ Packaging complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Packaged skills:" -ForegroundColor Cyan
Get-ChildItem -Path $OutputDir -Filter "*.skill" | ForEach-Object {
    $sizeKB = [math]::Round($_.Length / 1KB, 2)
    Write-Host "  $($_.Name) ($sizeKB KB)" -ForegroundColor White
}
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Import .skill files via Codex extension UI ('Import Skill')"
Write-Host "  2. Or attach to GitHub Release for distribution"
Write-Host ""
Write-Host "Output directory: $OutputDir" -ForegroundColor Gray
