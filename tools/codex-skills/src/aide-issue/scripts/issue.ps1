param(
    [Parameter(Mandatory = $true)]
    [string]$Title,
    [Parameter(Mandatory = $true)]
    [string]$Body,
    [ValidateSet("feature","bug","technical-debt","chore","documentation","research","epic")]
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
    "priority:$Priority",
    "area:$Area",
    "status:$Status"
)
if ($Type -eq "epic") { $labels += "Epic" }

$args = @("issue", "create", "--title", $Title, "--body", $Body, "--label", ($labels -join ","))
if ($Repo) { $args += @("--repo", $Repo) }

$url = & gh @args
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create issue. Ensure gh is installed/authenticated and labels exist."
    exit 1
}

Write-Output $url
$issueNumber = ($url -split "/")[-1]
python .aide/tools/set-issue-type.py --issue $issueNumber --type $Type
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to set GitHub Issue Type for issue #$issueNumber. See previous output for details."
    exit 1
}

