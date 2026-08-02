[CmdletBinding()]
param(
    [switch]$IncludeSharedInfrastructure
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$stateFile = Join-Path $repositoryRoot 'tmp\local-dev\processes.json'
$environmentFile = Join-Path $repositoryRoot '.env.local'

function Import-LocalEnvironment {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }
    foreach ($rawLine in Get-Content -LiteralPath $Path -Encoding UTF8) {
        $line = $rawLine.Trim()
        if (-not $line -or $line.StartsWith('#')) { continue }
        $separator = $line.IndexOf('=')
        if ($separator -lt 1) { continue }
        $name = $line.Substring(0, $separator).Trim()
        $value = $line.Substring($separator + 1).Trim()
        if ($name -notmatch '^[A-Z][A-Z0-9_]*$') { continue }
        if ($value.Length -ge 2) {
            $quotedWithDouble = $value.StartsWith('"') -and $value.EndsWith('"')
            $quotedWithSingle = $value.StartsWith("'") -and $value.EndsWith("'")
            if ($quotedWithDouble -or $quotedWithSingle) {
                $value = $value.Substring(1, $value.Length - 2)
            }
        }
        [Environment]::SetEnvironmentVariable($name, $value, 'Process')
    }
}

function Get-DescendantProcessIds {
    param([Parameter(Mandatory = $true)][int]$ParentProcessId)

    $result = @()
    $children = @(Get-CimInstance Win32_Process -Filter "ParentProcessId = $ParentProcessId" -ErrorAction SilentlyContinue)
    foreach ($child in $children) {
        $result += Get-DescendantProcessIds -ParentProcessId ([int]$child.ProcessId)
        $result += [int]$child.ProcessId
    }
    return $result
}

function Test-ProcessIdentity {
    param(
        [Parameter(Mandatory = $true)][System.Diagnostics.Process]$Process,
        [Parameter(Mandatory = $true)][datetime]$ExpectedStartTime
    )

    try {
        $actualStartTime = $Process.StartTime.ToUniversalTime()
        return [Math]::Abs(($actualStartTime - $ExpectedStartTime.ToUniversalTime()).TotalSeconds) -lt 3
    } catch {
        return $false
    }
}

if (Test-Path -LiteralPath $stateFile) {
    $state = Get-Content -LiteralPath $stateFile -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($state.repository -ne $repositoryRoot) {
        throw 'The local process state belongs to a different repository path; refusing to stop anything.'
    }

    $records = @($state.processes)
    [array]::Reverse($records)
    foreach ($record in $records) {
        $processId = [int]$record.id
        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        if ($null -eq $process) {
            Write-Host "$($record.label) is already stopped."
            continue
        }
        $expectedStart = [datetime]::Parse([string]$record.startedAtUtc).ToUniversalTime()
        if (-not (Test-ProcessIdentity -Process $process -ExpectedStartTime $expectedStart)) {
            Write-Warning "Skipped PID $processId for $($record.label) because its identity no longer matches the recorded process."
            continue
        }

        $descendants = @(Get-DescendantProcessIds -ParentProcessId $processId)
        foreach ($childId in $descendants) {
            Stop-Process -Id $childId -ErrorAction SilentlyContinue
        }
        Stop-Process -Id $processId -ErrorAction SilentlyContinue
        Write-Host "Stopped $($record.label) (PID $processId)."
    }
    Remove-Item -LiteralPath $stateFile -Force
} else {
    Write-Host 'No Aikya-owned native process state was found.'
}

if ($IncludeSharedInfrastructure) {
    Import-LocalEnvironment -Path $environmentFile
    $wslCommand = Get-Command 'wsl.exe' -ErrorAction SilentlyContinue
    if ($null -eq $wslCommand) {
        Write-Warning 'WSL is unavailable; Redis and ClamAV were not stopped.'
    } else {
        $linuxCommand = 'if [ -d /run/systemd/system ]; then sudo systemctl stop clamav-daemon redis-server; else sudo service clamav-daemon stop; sudo service redis-server stop; fi'
        $arguments = @()
        $distribution = [Environment]::GetEnvironmentVariable('AIKYA_WSL_DISTRIBUTION', 'Process')
        if (-not [string]::IsNullOrWhiteSpace($distribution)) {
            $arguments += @('--distribution', $distribution)
        }
        $arguments += @('--', 'bash', '-lc', $linuxCommand)
        Write-Host 'Stopping shared WSL Redis and ClamAV services. sudo may request your Linux password...'
        & $wslCommand.Source @arguments
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "WSL service stop returned exit code $LASTEXITCODE."
        }
    }
}

Write-Host 'PostgreSQL is an independently managed Windows service and was not stopped.'
