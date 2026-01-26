param(
    [string]$StartPath = (Get-Location).Path,
    [string]$Pr,
    [string]$Repo,
    [switch]$Fast,
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

function Run-Step {
    param([string]$Label, [string]$Cmd, [switch]$DryRun)
    if (-not $Cmd) {
        return [PSCustomObject]@{ Label = $Label; Command = $null; Status = "SKIP"; ExitCode = 0 }
    }
    if ($DryRun) {
        return [PSCustomObject]@{ Label = $Label; Command = $Cmd; Status = "DRY"; ExitCode = 0 }
    }
    Write-Output "Running ($Label): $Cmd"
    & powershell -NoProfile -ExecutionPolicy Bypass -Command $Cmd
    $code = $LASTEXITCODE
    return [PSCustomObject]@{
        Label = $Label
        Command = $Cmd
        Status = $(if ($code -eq 0) { "OK" } else { "FAIL" })
        ExitCode = $code
    }
}

if (-not $Pr) {
    Write-Error "Provide -Pr (number or URL)."
    exit 2
}

$repoRoot = Find-RepoRoot -Path $StartPath
if (-not $repoRoot) {
    Write-Error "Repo root not found (AGENTS.md missing)."
    exit 1
}

$agentsPath = Join-Path $repoRoot "AGENTS.md"
$agentsContent = Get-Content -Raw $agentsPath

$lint = Get-CommandValue $agentsContent "{{LINT_COMMAND}}"
$unit = Get-CommandValue $agentsContent "{{RUN_UNIT_TESTS_COMMAND}}"
$all = Get-CommandValue $agentsContent "{{RUN_ALL_TESTS_COMMAND}}"
$smoke = Get-CommandValue $agentsContent "{{SMOKE_TEST_COMMAND}}"

$steps = @()
$steps += Run-Step -Label "lint" -Cmd $lint -DryRun:$DryRun
if ($Fast) {
    $steps += Run-Step -Label "unit" -Cmd $unit -DryRun:$DryRun
} else {
    $steps += Run-Step -Label "all-tests" -Cmd $all -DryRun:$DryRun
    $steps += Run-Step -Label "smoke" -Cmd $smoke -DryRun:$DryRun
}

$failed = $steps | Where-Object { $_.Status -eq "FAIL" }

$lines = @()
$lines += "### Validation Summary"
$lines += ""
$lines += ("- Repo: `{0}`" -f $repoRoot)
$lines += ("- Mode: `{0}`" -f ($(if ($Fast) { "fast" } else { "full" })))
$lines += ""
$lines += "Results:"
foreach ($s in $steps) {
    if ($s.Command) {
        $lines += ("- `{0}`: **{1}** (`{2}`)" -f $s.Label, $s.Status, $s.Command)
    } else {
        $lines += ("- `{0}`: **{1}**" -f $s.Label, $s.Status)
    }
}

if ($DryRun) {
    $lines += ""
    $lines += "_Dry-run: no commands executed._"
}

$commentBody = ($lines -join "`n")

if ($DryRun) {
    Write-Output $commentBody
    exit 0
}

$ghArgs = @("pr", "comment", $Pr, "-F", "-")
if ($Repo) { $ghArgs += @("--repo", $Repo) }
$commentBody | & gh @ghArgs
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to post PR comment. Ensure gh is installed and authenticated."
    exit 1
}

if ($failed.Count -gt 0) {
    Write-Output "Validation failed; not marking PR ready."
    exit 1
}

$readyArgs = @("pr", "ready", $Pr)
if ($Repo) { $readyArgs += @("--repo", $Repo) }
& gh @readyArgs
exit $LASTEXITCODE

