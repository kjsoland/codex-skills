[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RequirementsPath,

    [Parameter(Mandatory = $true)]
    [ValidateSet('P45', 'P225', 'P135', 'P315', 'P90', 'P270')]
    [string]$Port,

    [Parameter(Mandatory = $true)]
    [string]$EntriesJson,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [switch]$AllowVerifiedBy
)

$ErrorActionPreference = 'Stop'
$portColumns = @{ P45 = 17; P225 = 18; P135 = 19; P315 = 20; P90 = 21; P270 = 22 }
$allowedCompliance = @('Compliant', 'Compliant with Waiver', 'Non-compliant')
$allowedStatus = @('In Work', 'Ready for Review', 'Complete')

$RequirementsPath = [System.IO.Path]::GetFullPath($RequirementsPath)
$EntriesJson = [System.IO.Path]::GetFullPath($EntriesJson)
$OutputPath = [System.IO.Path]::GetFullPath($OutputPath)

if (-not (Test-Path -LiteralPath $RequirementsPath -PathType Leaf)) {
    throw "Requirements workbook not found: $RequirementsPath"
}
if (-not (Test-Path -LiteralPath $EntriesJson -PathType Leaf)) {
    throw "Entries JSON not found: $EntriesJson"
}
if ($RequirementsPath.Equals($OutputPath, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'OutputPath must differ from RequirementsPath; this script never overwrites its input.'
}
if (Test-Path -LiteralPath $OutputPath) {
    throw "Refusing to overwrite existing output: $OutputPath"
}
if ([System.IO.Path]::GetExtension($OutputPath) -ne '.xlsx') {
    throw 'OutputPath must use the .xlsx extension.'
}

$entries = @(Get-Content -LiteralPath $EntriesJson -Raw | ConvertFrom-Json)
if ($entries.Count -eq 0) {
    throw 'Entries JSON contains no verification entries.'
}

function Merge-UniqueText {
    param([string]$Existing, [string]$NewText)
    if ([string]::IsNullOrWhiteSpace($NewText)) { return $Existing }
    if ([string]::IsNullOrWhiteSpace($Existing)) { return $NewText.Trim() }
    if ($Existing.Contains($NewText.Trim())) { return $Existing }
    return "$($Existing.Trim())`n$($NewText.Trim())"
}

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$workbook = $null
$sheet = $null
$comObjects = @()

try {
    $workbook = $excel.Workbooks.Open($RequirementsPath, 0, $false)
    $sheet = $workbook.Worksheets.Item('Beam Delivery Requirements')

    foreach ($entry in $entries) {
        $requirementId = [string]$entry.requirement_id
        $compliance = [string]$entry.compliance
        $verificationValue = [string]$entry.verification_value
        $summary = [string]$entry.summary
        $status = if ($entry.status) { [string]$entry.status } else { 'In Work' }

        if ([string]::IsNullOrWhiteSpace($requirementId)) { throw 'Each entry needs requirement_id.' }
        if ($allowedCompliance -notcontains $compliance) {
            throw "$requirementId has invalid compliance value: $compliance"
        }
        if ($allowedStatus -notcontains $status) {
            throw "$requirementId has invalid status value: $status"
        }
        if ([string]::IsNullOrWhiteSpace($verificationValue)) {
            throw "$requirementId needs verification_value."
        }
        if ([string]::IsNullOrWhiteSpace($summary)) {
            throw "$requirementId needs summary."
        }
        if ($compliance -eq 'Compliant with Waiver' -and $entry.waiver_approved -ne $true) {
            throw "$requirementId needs waiver_approved=true before using Compliant with Waiver."
        }
        if ($entry.verified_by -and -not $AllowVerifiedBy) {
            throw "$requirementId includes verified_by; rerun with -AllowVerifiedBy only when explicitly authorized."
        }

        $row = $null
        for ($candidate = 2; $candidate -le $sheet.UsedRange.Rows.Count; $candidate++) {
            if ($sheet.Cells.Item($candidate, 1).Value2 -eq $requirementId) {
                $row = $candidate
                break
            }
        }
        if ($null -eq $row) { throw "Requirement not found: $requirementId" }

        $procedureCell = $sheet.Cells.Item($row, 15)
        $complianceCell = $sheet.Cells.Item($row, 16)
        $valueCell = $sheet.Cells.Item($row, $portColumns[$Port])
        $artifactCell = $sheet.Cells.Item($row, 23)
        $summaryCell = $sheet.Cells.Item($row, 24)
        $statusCell = $sheet.Cells.Item($row, 25)
        $verifiedCell = $sheet.Cells.Item($row, 26)
        $comObjects += @($procedureCell, $complianceCell, $valueCell, $artifactCell, $summaryCell, $statusCell, $verifiedCell)

        $procedureCell.Value2 = Merge-UniqueText ([string]$procedureCell.Value2) ([string]$entry.procedure)
        $complianceCell.Value2 = $compliance
        $valueCell.Value2 = $verificationValue
        $artifactCell.Value2 = Merge-UniqueText ([string]$artifactCell.Value2) ([string]$entry.artifacts)

        $currentSummary = [string]$summaryCell.Value2
        $summaryMode = if ($entry.summary_mode) { [string]$entry.summary_mode } else { 'append' }
        if ($summaryMode -notin @('append', 'replace')) {
            throw "$requirementId has invalid summary_mode: $summaryMode"
        }
        if ($summaryMode -eq 'replace' -or [string]::IsNullOrWhiteSpace($currentSummary)) {
            $summaryCell.Value2 = $summary
        }
        else {
            $marker = "[$Port]"
            if ($currentSummary.Contains($marker)) {
                throw "$requirementId already contains a $marker summary; review manually or use summary_mode=replace."
            }
            $summaryCell.Value2 = "$($currentSummary.Trim())`n`n$marker`n$($summary.Trim())"
        }
        $statusCell.Value2 = $status
        if ($entry.verified_by) { $verifiedCell.Value2 = [string]$entry.verified_by }

        foreach ($cell in @($procedureCell, $valueCell, $artifactCell, $summaryCell)) {
            $cell.WrapText = $true
            $cell.VerticalAlignment = -4160
        }
        $sheet.Rows.Item($row).AutoFit() | Out-Null
        Write-Output "$requirementId row ${row}: $Port=$verificationValue; $compliance / $status"
    }

    $outputDirectory = Split-Path -Parent $OutputPath
    if (-not (Test-Path -LiteralPath $outputDirectory -PathType Container)) {
        New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    }
    $workbook.SaveCopyAs($OutputPath)
    $workbook.Close($false)
}
finally {
    foreach ($comObject in $comObjects) {
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($comObject)
    }
    if ($null -ne $sheet) { [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($sheet) }
    if ($null -ne $workbook) { [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($workbook) }
    $excel.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel)
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

if (-not (Test-Path -LiteralPath $OutputPath -PathType Leaf)) {
    throw "Excel did not create the expected output: $OutputPath"
}
Write-Output "OUTPUT=$OutputPath"
