param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..\\..")).Path
)

function New-SkillPackage {
    param(
        [Parameter(Mandatory = $true)][string]$SkillDir,
        [Parameter(Mandatory = $true)][string]$OutFile
    )

    if (Test-Path $OutFile) {
        Remove-Item -Force $OutFile
    }

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory(
        $SkillDir,
        $OutFile,
        [System.IO.Compression.CompressionLevel]::Optimal,
        $false
    )
}

$src = Join-Path $RepoRoot "tools\\codex-skills\\src"
$dist = Join-Path $RepoRoot "tools\\codex-skills\\dist"

if (-not (Test-Path $src)) { throw "Missing: $src" }
New-Item -ItemType Directory -Force -Path $dist | Out-Null

$skillDirs = Get-ChildItem -Path $src -Directory | Sort-Object Name
if ($skillDirs.Count -eq 0) {
    Write-Output "No skills found in $src"
    exit 0
}

foreach ($d in $skillDirs) {
    $out = Join-Path $dist ($d.Name + ".skill")
    Write-Output "Packaging: $($d.Name) -> $out"
    New-SkillPackage -SkillDir $d.FullName -OutFile $out
}

Write-Output "Done."

