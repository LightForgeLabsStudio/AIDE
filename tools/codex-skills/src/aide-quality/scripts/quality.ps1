param(
    [string]$StartPath = (Get-Location).Path,
    [switch]$Full,
    [switch]$DryRun
)

function Find-RepoRoot {
    param([string]$Path)
    $current = Resolve-Path $Path
    while ($true) {
        $agentsPath = Join-Path $current "AGENTS.md"
        if (Test-Path $agentsPath) {
            return $current
        }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current -or [string]::IsNullOrWhiteSpace($parent)) {
            return $null
        }
        $current = $parent
    }
}

function Get-CommandValue {
    param([string]$Content, [string]$Placeholder)
    $pattern = [regex]::Escape($Placeholder) + "\s*\|\s*`?([^`\r\n]+)`?\s*\|"
    $match = [regex]::Match($Content, $pattern)
    if ($match.Success) { return $match.Groups[1].Value.Trim() }
    return $null
}

$repoRoot = Find-RepoRoot -Path $StartPath
if (-not $repoRoot) {
    Write-Output "Repo root not found (AGENTS.md missing)."
    exit 1
}

$agentsPath = Join-Path $repoRoot "AGENTS.md"
$content = Get-Content -Raw $agentsPath

$lint = Get-CommandValue $content "{{LINT_COMMAND}}"
$format = Get-CommandValue $content "{{FORMAT_COMMAND}}"
$unit = Get-CommandValue $content "{{RUN_UNIT_TESTS_COMMAND}}"
$all = Get-CommandValue $content "{{RUN_ALL_TESTS_COMMAND}}"
$smoke = Get-CommandValue $content "{{SMOKE_TEST_COMMAND}}"

$commands = @()
if ($Full) {
    if ($lint) { $commands += $lint }
    if ($all) { $commands += $all }
    if ($smoke) { $commands += $smoke }
} else {
    if ($lint) { $commands += $lint }
    if ($unit) { $commands += $unit }
}

Write-Output "Repo: $repoRoot"
Write-Output "Detected: lint=[$lint] unit=[$unit] all=[$all] smoke=[$smoke] format=[$format]"
if ($DryRun) {
    Write-Output "Dry-run. Commands:"
    $commands | ForEach-Object { Write-Output " - $_" }
    exit 0
}

if ($commands.Count -eq 0) {
    Write-Output "No commands found. Provide the correct commands or update AGENTS.md."
    exit 1
}

$results = @()
foreach ($cmd in $commands) {
    Write-Output "Running: $cmd"
    try {
        & powershell -NoProfile -ExecutionPolicy Bypass -Command $cmd
        $code = $LASTEXITCODE
        $results += [PSCustomObject]@{ Command = $cmd; ExitCode = $code }
        if ($code -ne 0) {
            Write-Output "FAILED: $cmd (exit $code)"
        } else {
            Write-Output "OK: $cmd"
        }
    } catch {
        Write-Output "ERROR: $cmd"
        $results += [PSCustomObject]@{ Command = $cmd; ExitCode = 1 }
    }
}

Write-Output "Summary:"
$results | ForEach-Object {
    Write-Output (" - {0}: {1}" -f $_.Command, ($(if ($_.ExitCode -eq 0) {'OK'} else {'FAIL'})))
}

