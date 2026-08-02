[CmdletBinding()]
param(
    [switch]$SkipFrontend,
    [switch]$SkipBackend,
    [switch]$SkipMinioDownload
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$frontendDirectory = Join-Path $repositoryRoot 'frontend'
$backendDirectory = Join-Path $repositoryRoot 'backend'
$localRuntimeDirectory = Join-Path $repositoryRoot 'tmp\local-dev'
$localToolsDirectory = Join-Path $localRuntimeDirectory 'tools'
$localLogDirectory = Join-Path $repositoryRoot 'logs\local-dev'
$localEnvironmentExample = Join-Path $repositoryRoot '.env.local.example'
$localEnvironmentFile = Join-Path $repositoryRoot '.env.local'

function Write-Step {
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Get-RequiredCommand {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$InstallHelp
    )

    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $command) {
        throw "Required command '$Name' was not found. $InstallHelp"
    }
    return $command
}

function Assert-NodeVersion {
    param([Parameter(Mandatory = $true)][System.Management.Automation.CommandInfo]$NodeCommand)

    $rawVersion = (& $NodeCommand.Source --version).Trim()
    $currentVersion = [version]$rawVersion.TrimStart('v')
    $minimumVersion = [version]'24.18.0'
    if ($currentVersion.Major -ne 24 -or $currentVersion -lt $minimumVersion) {
        throw "Node.js $rawVersion is unsupported. frontend/package.json requires >=24.18.0 <25."
    }
    Write-Host "Node.js $rawVersion satisfies >=24.18.0 <25."
}

function Assert-NoFrontendNodeProcess {
    param([Parameter(Mandatory = $true)][string]$FrontendPath)

    $frontendPrefix = [IO.Path]::GetFullPath($FrontendPath).TrimEnd('\') + '\'
    $lockingProcessIds = @()
    foreach ($nodeProcess in @(Get-Process -Name 'node' -ErrorAction SilentlyContinue)) {
        try {
            $usesFrontendModule = @($nodeProcess.Modules) | Where-Object {
                $_.FileName.StartsWith($frontendPrefix, [StringComparison]::OrdinalIgnoreCase)
            } | Select-Object -First 1
            if ($null -ne $usesFrontendModule) {
                $lockingProcessIds += $nodeProcess.Id
            }
        } catch {
            # A process owned by another account may deny module inspection; npm remains the authority.
        }
    }

    if ($lockingProcessIds.Count -gt 0) {
        $processList = ($lockingProcessIds | Sort-Object -Unique) -join ', '
        throw "Frontend dependencies are in use by Node PID(s): $processList. Run scripts/stop-local.ps1 or close the Aikya Nuxt/npm terminals, then rerun setup. Do not stop unrelated Node processes."
    }
}

function Assert-NoBackendPythonProcess {
    param([Parameter(Mandatory = $true)][string]$BackendPath)

    $virtualEnvironmentPrefix = [IO.Path]::GetFullPath(
        (Join-Path $BackendPath '.venv')
    ).TrimEnd('\') + '\'
    $lockingProcessIds = @()

    foreach ($pythonProcess in @(Get-CimInstance Win32_Process -Filter "Name = 'python.exe' OR Name = 'pythonw.exe'" -ErrorAction SilentlyContinue)) {
        $executablePath = [string]$pythonProcess.ExecutablePath
        $commandLine = [string]$pythonProcess.CommandLine
        $usesVirtualEnvironment = (
            $executablePath.StartsWith($virtualEnvironmentPrefix, [StringComparison]::OrdinalIgnoreCase) -or
            $commandLine.IndexOf($virtualEnvironmentPrefix, [StringComparison]::OrdinalIgnoreCase) -ge 0
        )
        if ($usesVirtualEnvironment) {
            $lockingProcessIds += [int]$pythonProcess.ProcessId
        }
    }

    if ($lockingProcessIds.Count -gt 0) {
        $processList = ($lockingProcessIds | Sort-Object -Unique) -join ', '
        throw "Backend .venv is in use by Python PID(s): $processList. Stop Aikya backend/worker terminals and close or reload VS Code Python formatters using backend\.venv, then rerun setup. Do not stop unrelated Python processes."
    }
}

function Install-PinnedMinio {
    $release = 'RELEASE.2025-04-22T22-12-26Z'
    $expectedSha256 = '2ceb3b3d68bdf1c4def9702cb02c5c8adb235197d1c8f2eaad24136833ab9a57'
    $downloadUrl = "https://dl.min.io/server/minio/release/windows-amd64/archive/minio.$release"
    $destination = Join-Path $localToolsDirectory 'minio.exe'

    if (Test-Path -LiteralPath $destination) {
        $actualHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualHash -eq $expectedSha256) {
            Write-Host "Pinned MinIO $release is already installed."
            return
        }
        throw "Existing $destination does not match the repository-pinned MinIO SHA-256. Remove only that file and rerun setup."
    }

    Write-Host "Downloading repository-pinned MinIO $release..."
    Invoke-WebRequest -UseBasicParsing -Uri $downloadUrl -OutFile $destination
    $downloadedHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($downloadedHash -ne $expectedSha256) {
        Remove-Item -LiteralPath $destination -Force
        throw 'Downloaded MinIO binary failed SHA-256 verification and was removed.'
    }
    Write-Host 'MinIO download verified.'
}

if ($env:OS -ne 'Windows_NT') {
    throw 'This setup script targets Windows 11 PowerShell.'
}

Write-Step 'Preparing ignored local runtime directories'
New-Item -ItemType Directory -Force -Path $localRuntimeDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $localToolsDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $localLogDirectory | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $localRuntimeDirectory 'minio-data') | Out-Null

if (-not (Test-Path -LiteralPath $localEnvironmentFile)) {
    Copy-Item -LiteralPath $localEnvironmentExample -Destination $localEnvironmentFile
    Write-Host 'Created ignored .env.local from .env.local.example. Review it before first startup.'
} else {
    Write-Host 'Preserved existing .env.local.'
}

if (-not $SkipFrontend) {
    Write-Step 'Installing locked Nuxt dependencies'
    $nodeCommand = Get-RequiredCommand -Name 'node.exe' -InstallHelp 'Install Node.js 24.18.x from https://nodejs.org/en/download.'
    $npmCommand = Get-RequiredCommand -Name 'npm.cmd' -InstallHelp 'npm is included with the supported Node.js installation.'
    Assert-NodeVersion -NodeCommand $nodeCommand
    Assert-NoFrontendNodeProcess -FrontendPath $frontendDirectory
    $env:npm_config_cache = Join-Path $frontendDirectory '.npm-cache'
    Push-Location $frontendDirectory
    try {
        & $npmCommand.Source ci
        if ($LASTEXITCODE -ne 0) {
            throw "npm ci failed with exit code $LASTEXITCODE. If npm reported EPERM/unlink or a missing Shiki runtime, follow 'Frontend install is corrupt or locked' in LOCAL_DEVELOPMENT.md."
        }
    } finally {
        Pop-Location
    }
}

if (-not $SkipBackend) {
    Write-Step 'Installing Python 3.14 and locked FastAPI dependencies'
    $uvCommand = Get-RequiredCommand -Name 'uv.exe' -InstallHelp 'Install uv with: winget install --id=astral-sh.uv -e'
    Assert-NoBackendPythonProcess -BackendPath $backendDirectory
    & $uvCommand.Source --version
    $env:UV_CACHE_DIR = Join-Path $repositoryRoot '.uv-cache'
    $env:UV_PYTHON_INSTALL_DIR = Join-Path $repositoryRoot '.uv-python'
    & $uvCommand.Source python install 3.14
    if ($LASTEXITCODE -ne 0) {
        throw "uv python install 3.14 failed with exit code $LASTEXITCODE."
    }
    Push-Location $backendDirectory
    try {
        & $uvCommand.Source sync --frozen --python 3.14
        if ($LASTEXITCODE -ne 0) {
            throw "uv sync --frozen failed with exit code $LASTEXITCODE."
        }
    } finally {
        Pop-Location
    }
}

if (-not $SkipMinioDownload) {
    Write-Step 'Installing the repository-pinned MinIO Windows binary'
    Install-PinnedMinio
}

Write-Step 'Setup summary'
Write-Host 'Application dependencies are installed and .env.local is available.' -ForegroundColor Green
Write-Host 'Before startup, complete PostgreSQL 17 plus WSL Redis/ClamAV provisioning in LOCAL_DEVELOPMENT.md.'
Write-Host 'Then run: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-local.ps1'
