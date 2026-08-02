[CmdletBinding()]
param(
    [switch]$SkipWslServiceStart
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$frontendDirectory = Join-Path $repositoryRoot 'frontend'
$backendDirectory = Join-Path $repositoryRoot 'backend'
$environmentFile = Join-Path $repositoryRoot '.env.local'
$runtimeDirectory = Join-Path $repositoryRoot 'tmp\local-dev'
$logDirectory = Join-Path $repositoryRoot 'logs\local-dev'
$stateFile = Join-Path $runtimeDirectory 'processes.json'
$pythonExecutable = Join-Path $backendDirectory '.venv\Scripts\python.exe'
$minioExecutable = Join-Path $runtimeDirectory 'tools\minio.exe'
$script:ownedProcesses = @()

function Import-LocalEnvironment {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        throw 'Missing .env.local. Run scripts/setup-local.ps1 first.'
    }

    foreach ($rawLine in Get-Content -LiteralPath $Path -Encoding UTF8) {
        $line = $rawLine.Trim()
        if (-not $line -or $line.StartsWith('#')) {
            continue
        }
        $separator = $line.IndexOf('=')
        if ($separator -lt 1) {
            throw "Invalid .env.local line: $rawLine"
        }
        $name = $line.Substring(0, $separator).Trim()
        $value = $line.Substring($separator + 1).Trim()
        if ($name -notmatch '^[A-Z][A-Z0-9_]*$') {
            throw "Invalid environment variable name '$name' in .env.local."
        }
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

function Get-ConfiguredPort {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][int]$Default
    )

    $rawValue = [Environment]::GetEnvironmentVariable($Name, 'Process')
    if ([string]::IsNullOrWhiteSpace($rawValue)) {
        return $Default
    }
    $parsed = 0
    if (-not [int]::TryParse($rawValue, [ref]$parsed) -or $parsed -lt 1 -or $parsed -gt 65535) {
        throw "$Name must be a TCP port between 1 and 65535."
    }
    return $parsed
}

function Assert-NoExistingFrontendNodeProcess {
    param([Parameter(Mandatory = $true)][string]$FrontendPath)

    $frontendPrefix = [IO.Path]::GetFullPath($FrontendPath).TrimEnd('\') + '\'
    $existingProcessIds = @()
    foreach ($nodeProcess in @(Get-Process -Name 'node' -ErrorAction SilentlyContinue)) {
        try {
            $usesFrontendModule = @($nodeProcess.Modules) | Where-Object {
                $_.FileName.StartsWith($frontendPrefix, [StringComparison]::OrdinalIgnoreCase)
            } | Select-Object -First 1
            if ($null -ne $usesFrontendModule) {
                $existingProcessIds += $nodeProcess.Id
            }
        } catch {
            # A process owned by another account may deny module inspection; port checks still apply.
        }
    }

    if ($existingProcessIds.Count -gt 0) {
        $processList = ($existingProcessIds | Sort-Object -Unique) -join ', '
        throw "An Aikya frontend Node process is already running (PID(s): $processList), possibly on Nuxt's default port 3000. Stop it from its original terminal before running start-local.ps1; concurrent Nuxt processes share generated directories."
    }
}

function Test-TcpPort {
    param(
        [Parameter(Mandatory = $true)][string]$HostName,
        [Parameter(Mandatory = $true)][int]$Port,
        [int]$TimeoutMilliseconds = 1200
    )

    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $task = $client.ConnectAsync($HostName, $Port)
        return $task.Wait($TimeoutMilliseconds) -and $client.Connected
    } catch {
        return $false
    } finally {
        $client.Dispose()
    }
}

function Wait-TcpPort {
    param(
        [Parameter(Mandatory = $true)][string]$HostName,
        [Parameter(Mandatory = $true)][int]$Port,
        [Parameter(Mandatory = $true)][int]$TimeoutSeconds
    )

    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    do {
        if (Test-TcpPort -HostName $HostName -Port $Port) {
            return $true
        }
        Start-Sleep -Milliseconds 500
    } while ([DateTime]::UtcNow -lt $deadline)
    return $false
}

function Wait-HttpEndpoint {
    param(
        [Parameter(Mandatory = $true)][string]$Uri,
        [Parameter(Mandatory = $true)][int]$TimeoutSeconds
    )

    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    do {
        try {
            $response = Invoke-WebRequest -UseBasicParsing -Uri $Uri -TimeoutSec 3
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400) {
                return $true
            }
        } catch {
            Start-Sleep -Milliseconds 700
        }
    } while ([DateTime]::UtcNow -lt $deadline)
    return $false
}

function Test-ClamAvProtocol {
    param(
        [Parameter(Mandatory = $true)][string]$HostName,
        [Parameter(Mandatory = $true)][int]$Port
    )

    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $connectTask = $client.ConnectAsync($HostName, $Port)
        if (-not $connectTask.Wait(3000) -or -not $client.Connected) {
            return $false
        }
        $stream = $client.GetStream()
        $stream.ReadTimeout = 3000
        $request = [Text.Encoding]::ASCII.GetBytes("zPING`0")
        $stream.Write($request, 0, $request.Length)
        $buffer = New-Object byte[] 64
        $read = $stream.Read($buffer, 0, $buffer.Length)
        $response = [Text.Encoding]::ASCII.GetString($buffer, 0, $read)
        return $response -match 'PONG'
    } catch {
        return $false
    } finally {
        $client.Dispose()
    }
}

function Start-WslInfrastructure {
    $wslCommand = Get-Command 'wsl.exe' -ErrorAction SilentlyContinue
    if ($null -eq $wslCommand) {
        throw 'Redis or ClamAV is unavailable and WSL is not installed. Follow LOCAL_DEVELOPMENT.md.'
    }

    $linuxCommand = 'if [ -d /run/systemd/system ]; then sudo systemctl start redis-server clamav-daemon; else sudo service redis-server start && sudo service clamav-daemon start; fi'
    $arguments = @()
    $distribution = [Environment]::GetEnvironmentVariable('AIKYA_WSL_DISTRIBUTION', 'Process')
    if (-not [string]::IsNullOrWhiteSpace($distribution)) {
        $arguments += @('--distribution', $distribution)
    }
    $arguments += @('--', 'bash', '-lc', $linuxCommand)
    Write-Host 'Starting Redis and ClamAV in WSL. sudo may request your Linux password...'
    & $wslCommand.Source @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "WSL infrastructure startup failed with exit code $LASTEXITCODE."
    }
}

function Start-OwnedProcess {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$ArgumentList,
        [Parameter(Mandatory = $true)][string]$WorkingDirectory
    )

    $stdoutPath = Join-Path $logDirectory "$Label.out.log"
    $stderrPath = Join-Path $logDirectory "$Label.err.log"
    $process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList `
        -WorkingDirectory $WorkingDirectory -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
    Start-Sleep -Milliseconds 400
    if ($process.HasExited) {
        throw "$Label exited during startup. Inspect $stdoutPath and $stderrPath."
    }
    $script:ownedProcesses += [pscustomobject]@{
        label = $Label
        id = $process.Id
        startedAtUtc = $process.StartTime.ToUniversalTime().ToString('o')
    }
    Save-ProcessState
    Write-Host "Started $Label (PID $($process.Id))."
    return $process
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

function Stop-OwnedProcessesAfterFailure {
    $records = @($script:ownedProcesses)
    [array]::Reverse($records)
    foreach ($record in $records) {
        $descendants = @(Get-DescendantProcessIds -ParentProcessId ([int]$record.id))
        foreach ($childId in $descendants) {
            Stop-Process -Id $childId -Force -ErrorAction SilentlyContinue
        }
        Stop-Process -Id ([int]$record.id) -Force -ErrorAction SilentlyContinue
    }
}

function Save-ProcessState {
    $state = [pscustomobject]@{
        repository = $repositoryRoot
        createdAtUtc = [DateTime]::UtcNow.ToString('o')
        processes = $script:ownedProcesses
    }
    $state | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $stateFile -Encoding UTF8
}

Import-LocalEnvironment -Path $environmentFile
$env:UV_CACHE_DIR = Join-Path $repositoryRoot '.uv-cache'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $repositoryRoot '.uv-python'
$env:npm_config_cache = Join-Path $frontendDirectory '.npm-cache'

$nativeEndpointValues = @(
    [Environment]::GetEnvironmentVariable('DATABASE_URL', 'Process'),
    [Environment]::GetEnvironmentVariable('REDIS_URL', 'Process'),
    [Environment]::GetEnvironmentVariable('CELERY_BROKER_URL', 'Process'),
    [Environment]::GetEnvironmentVariable('CELERY_RESULT_BACKEND', 'Process'),
    [Environment]::GetEnvironmentVariable('STORAGE_ENDPOINT', 'Process')
)
foreach ($endpointValue in $nativeEndpointValues) {
    if ($endpointValue -match '(?i)(://|@)(postgres|redis|minio|clamav)(:|/|$)') {
        throw "Docker service hostname detected in .env.local: $endpointValue. Use the localhost values from .env.local.example."
    }
}
if ([Environment]::GetEnvironmentVariable('CLAMAV_HOST', 'Process') -eq 'clamav') {
    throw 'Docker service hostname detected in CLAMAV_HOST. Use 127.0.0.1 for native development.'
}

New-Item -ItemType Directory -Force -Path $runtimeDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $logDirectory | Out-Null

if (-not (Test-Path -LiteralPath $pythonExecutable)) {
    throw 'Missing backend/.venv. Run scripts/setup-local.ps1 first.'
}
if (-not (Get-Command 'npm.cmd' -ErrorAction SilentlyContinue)) {
    throw 'npm.cmd is unavailable. Install the Node.js version required by frontend/package.json.'
}
if (Test-Path -LiteralPath $stateFile) {
    throw 'A local process state file already exists. Run scripts/stop-local.ps1 before starting again.'
}

$frontendPort = Get-ConfiguredPort -Name 'FRONTEND_PORT' -Default 3000
$backendPort = Get-ConfiguredPort -Name 'BACKEND_PORT' -Default 8000
$postgresPort = Get-ConfiguredPort -Name 'POSTGRES_PORT' -Default 5432
$redisPort = Get-ConfiguredPort -Name 'REDIS_PORT' -Default 6379
$minioApiPort = Get-ConfiguredPort -Name 'MINIO_API_PORT' -Default 9000
$minioConsolePort = Get-ConfiguredPort -Name 'MINIO_CONSOLE_PORT' -Default 9001
$clamAvPort = Get-ConfiguredPort -Name 'CLAMAV_PORT' -Default 3310
$clamAvHost = [Environment]::GetEnvironmentVariable('CLAMAV_HOST', 'Process')

Assert-NoExistingFrontendNodeProcess -FrontendPath $frontendDirectory
if (Test-TcpPort -HostName '127.0.0.1' -Port $backendPort) {
    throw "Backend port $backendPort is already in use."
}
if (Test-TcpPort -HostName '127.0.0.1' -Port $frontendPort) {
    throw "Frontend port $frontendPort is already in use."
}
if (-not (Test-TcpPort -HostName '127.0.0.1' -Port $postgresPort)) {
    throw "PostgreSQL is not reachable on 127.0.0.1:$postgresPort. Start the PostgreSQL 17 Windows service and initialize the local role/database."
}

$redisReady = Test-TcpPort -HostName '127.0.0.1' -Port $redisPort
$clamAvReady = Test-ClamAvProtocol -HostName $clamAvHost -Port $clamAvPort
if ((-not $redisReady -or -not $clamAvReady) -and -not $SkipWslServiceStart) {
    Start-WslInfrastructure
    $redisReady = Wait-TcpPort -HostName '127.0.0.1' -Port $redisPort -TimeoutSeconds 20
    $clamAvReady = $false
    $clamDeadline = [DateTime]::UtcNow.AddSeconds(90)
    do {
        $clamAvReady = Test-ClamAvProtocol -HostName $clamAvHost -Port $clamAvPort
        if (-not $clamAvReady) { Start-Sleep -Seconds 2 }
    } while (-not $clamAvReady -and [DateTime]::UtcNow -lt $clamDeadline)
}
if (-not $redisReady) {
    throw "Redis is not reachable on 127.0.0.1:$redisPort. Complete the WSL Redis setup in LOCAL_DEVELOPMENT.md."
}
if (-not $clamAvReady) {
    throw "ClamAV did not answer PING on $clamAvHost`:$clamAvPort. Complete the WSL clamd TCP setup in LOCAL_DEVELOPMENT.md."
}

try {
    $minioHealthUri = "http://127.0.0.1:$minioApiPort/minio/health/live"
    if (-not (Test-TcpPort -HostName '127.0.0.1' -Port $minioApiPort)) {
        if (Test-TcpPort -HostName '127.0.0.1' -Port $minioConsolePort) {
            throw "MinIO console port $minioConsolePort is already in use."
        }
        if (-not (Test-Path -LiteralPath $minioExecutable)) {
            throw 'Pinned MinIO binary is missing. Run scripts/setup-local.ps1 first.'
        }
        $minioDataDirectory = Join-Path $runtimeDirectory 'minio-data'
        New-Item -ItemType Directory -Force -Path $minioDataDirectory | Out-Null
        Start-OwnedProcess -Label 'minio' -FilePath $minioExecutable `
            -ArgumentList @('server', "`"$minioDataDirectory`"", '--address', "127.0.0.1:$minioApiPort", '--console-address', "127.0.0.1:$minioConsolePort") `
            -WorkingDirectory $runtimeDirectory | Out-Null
    }
    if (-not (Wait-HttpEndpoint -Uri $minioHealthUri -TimeoutSeconds 60)) {
        throw "MinIO did not become healthy at $minioHealthUri."
    }

    Write-Host 'Validating Redis protocol...'
    $redisProbe = 'import os; from redis import Redis; assert Redis.from_url(os.environ["REDIS_URL"]).ping()'
    Push-Location $backendDirectory
    try {
        & $pythonExecutable -c $redisProbe
        if ($LASTEXITCODE -ne 0) { throw 'Redis PING failed.' }

        Write-Host 'Creating missing private MinIO buckets...'
        $bucketBootstrap = 'import os, boto3; from botocore.client import Config; region=os.environ["STORAGE_REGION"]; c=boto3.client("s3",endpoint_url=os.environ["STORAGE_ENDPOINT"],aws_access_key_id=os.environ["STORAGE_ACCESS_KEY"],aws_secret_access_key=os.environ["STORAGE_SECRET_KEY"],region_name=region,config=Config(signature_version="s3v4",s3={"addressing_style":"path"})); existing={b["Name"] for b in c.list_buckets().get("Buckets",[])}; options={} if region=="us-east-1" else {"CreateBucketConfiguration":{"LocationConstraint":region}}; [c.create_bucket(Bucket=name,**options) for name in (os.environ["STORAGE_BUCKET_QUARANTINE"],os.environ["STORAGE_BUCKET_DOCUMENTS"],os.environ["STORAGE_BUCKET_OUTPUTS"]) if name not in existing]'
        & $pythonExecutable -c $bucketBootstrap
        if ($LASTEXITCODE -ne 0) { throw 'MinIO bucket bootstrap failed.' }

        Write-Host 'Applying Alembic migrations...'
        & $pythonExecutable -m alembic upgrade head
        if ($LASTEXITCODE -ne 0) { throw 'Alembic migration failed.' }
    } finally {
        Pop-Location
    }

    Start-OwnedProcess -Label 'backend' -FilePath $pythonExecutable `
        -ArgumentList @('-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', "$backendPort", '--reload') `
        -WorkingDirectory $backendDirectory | Out-Null
    if (-not (Wait-HttpEndpoint -Uri "http://127.0.0.1:$backendPort/health/live" -TimeoutSeconds 45)) {
        throw 'FastAPI liveness check failed.'
    }
    if (-not (Wait-HttpEndpoint -Uri "http://127.0.0.1:$backendPort/health/ready" -TimeoutSeconds 30)) {
        throw 'FastAPI readiness check failed.'
    }

    Start-OwnedProcess -Label 'worker' -FilePath $pythonExecutable `
        -ArgumentList @('-m', 'celery', '-A', 'app.worker:celery_app', 'worker', '--loglevel=INFO', '--pool=solo', '--hostname=aikya-local@%h') `
        -WorkingDirectory $backendDirectory | Out-Null

    $npmCommand = Get-Command 'npm.cmd'
    Start-OwnedProcess -Label 'frontend' -FilePath $npmCommand.Source `
        -ArgumentList @('run', 'dev', '--', '--host', '127.0.0.1', '--port', "$frontendPort") `
        -WorkingDirectory $frontendDirectory | Out-Null
    if (-not (Wait-HttpEndpoint -Uri "http://127.0.0.1:$frontendPort/healthz" -TimeoutSeconds 90)) {
        throw 'Nuxt health check failed.'
    }

    Save-ProcessState
    Write-Host "`nAikya native development stack is running." -ForegroundColor Green
    Write-Host "Frontend: http://127.0.0.1:$frontendPort"
    Write-Host "API docs: http://127.0.0.1:$backendPort/api/docs"
    Write-Host "Backend readiness: http://127.0.0.1:$backendPort/health/ready"
    Write-Host "MinIO console: http://127.0.0.1:$minioConsolePort"
    Write-Host "Logs: $logDirectory"
    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable('LIBRETRANSLATE_URL', 'Process'))) {
        Write-Warning 'LIBRETRANSLATE_URL is empty. Authentication/dashboard work, but translation requests intentionally return provider_unconfigured.'
    }
} catch {
    Stop-OwnedProcessesAfterFailure
    if (Test-Path -LiteralPath $stateFile) {
        Remove-Item -LiteralPath $stateFile -Force
    }
    throw
}
