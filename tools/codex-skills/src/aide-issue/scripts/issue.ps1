param(
    [Parameter(Mandatory = $true)]
    [string]$Title,
    [Parameter(Mandatory = $true)]
    [string]$Body,
    [ValidateSet("bug","enhancement","technical-debt")]
    [string]$Type = "bug",
    [ValidateSet("critical","high","medium","low")]
    [string]$Priority = "medium",
    [Parameter(Mandatory = $true)]
    [string]$Area,
    [ValidateSet("needs-spec","ready","in-progress")]
    [string]$Status = "needs-spec",
    [string]$Repo
)

$labels = @(
    $Type,
    "priority:$Priority",
    "area:$Area",
    "status:$Status"
)

$args = @("issue", "create", "--title", $Title, "--body", $Body, "--label", ($labels -join ","))
if ($Repo) { $args += @("--repo", $Repo) }

$url = & gh @args
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create issue. Ensure gh is installed/authenticated and labels exist."
    exit 1
}

Write-Output $url

