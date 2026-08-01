$ErrorActionPreference = 'Stop'

$repositoryRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')
Push-Location $repositoryRoot
try {
    docker compose -f docker/docker-compose.yml config --quiet
    docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml config --quiet

    $diagramFiles = Get-ChildItem -LiteralPath docs/diagrams -Filter *.excalidraw
    if ($diagramFiles.Count -ne 6) {
        throw "Expected 6 Excalidraw files, found $($diagramFiles.Count)."
    }

    foreach ($diagramFile in $diagramFiles) {
        $diagram = Get-Content -Raw -LiteralPath $diagramFile.FullName | ConvertFrom-Json
        if ($diagram.type -ne 'excalidraw' -or $diagram.version -ne 2 -or $diagram.elements.Count -eq 0) {
            throw "Invalid Excalidraw document: $($diagramFile.Name)"
        }
    }

    Write-Output 'Foundation configuration is structurally valid.'
}
finally {
    Pop-Location
}
