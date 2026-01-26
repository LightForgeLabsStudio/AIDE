param(
    [string]$Body = ""
)

function Get-PrBodyFromEvent {
    $eventPath = $env:GITHUB_EVENT_PATH
    if (-not $eventPath -or -not (Test-Path $eventPath)) {
        return ""
    }
    try {
        $json = Get-Content -Raw $eventPath | ConvertFrom-Json
        if ($json.pull_request -and $json.pull_request.body) {
            return [string]$json.pull_request.body
        }
    } catch {
        return ""
    }
    return ""
}

function Is-InlineCode {
    param(
        [string]$Line,
        [int]$Index
    )
    $prefix = $Line.Substring(0, $Index)
    $tickCount = ($prefix.ToCharArray() | Where-Object { $_ -eq '`' }).Count
    return ($tickCount % 2 -eq 1)
}

if (-not $Body) {
    $Body = Get-PrBodyFromEvent
}

if (-not $Body) {
    Write-Output "No PR body found to validate."
    exit 0
}

$errors = @()
$lines = $Body -split "`n"

$pathPatterns = @(
    "tools/",
    "\.github/",
    "\.aide/",
    "docs/",
    "scripts/",
    "[A-Za-z]:\\\\"
)

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]

    # Disallow stray control characters (excluding tab)
    if ($line -match "[\u0000-\u0008\u000B\u000C\u000E-\u001F]") {
        $errors += "Line $($i+1): contains control characters."
        continue
    }

    foreach ($pattern in $pathPatterns) {
        $matches = [regex]::Matches($line, $pattern)
        foreach ($m in $matches) {
            if (-not (Is-InlineCode -Line $line -Index $m.Index)) {
                $errors += "Line $($i+1): path/command appears outside backticks -> '$($m.Value)'"
            }
        }
    }

    # Disallow escaped leading backslash paths like \tools
    if ($line -match "(^|\\s)\\\\[A-Za-z0-9._-]+") {
        if (-not (Is-InlineCode -Line $line -Index $Matches[0].Index)) {
            $errors += "Line $($i+1): detected backslash path outside backticks -> '$($Matches[0].Trim())'"
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Output "PR body formatting check failed:"
    $errors | ForEach-Object { Write-Output "- $_" }
    Write-Output ""
    Write-Output "Guidance: wrap file paths/commands in backticks and avoid stray backslash paths."
    exit 1
}

Write-Output "PR body formatting check passed."

