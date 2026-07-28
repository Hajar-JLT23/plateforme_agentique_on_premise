Param(
    [string]$Branch = "agents/fix-app-py-errors-add-rag-agent"
)

# Détermine le répertoire du script et passe au répertoire parent (racine du repo)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $scriptDir "..")
Write-Host "Répertoire de travail : $(Get-Location)"

Write-Host "Récupération de la branche $Branch..."
git fetch origin
git checkout $Branch
git pull origin $Branch
if ($LASTEXITCODE -ne 0) {
    Write-Error "Les commandes Git ont échoué. Vérifie la configuration et relance le script."
    exit 1
}

Write-Host "Construction et démarrage des conteneurs Docker..."
docker compose up --build --remove-orphans -d
if ($LASTEXITCODE -ne 0) {
    Write-Error "Échec de docker compose. Vérifie Docker Desktop et relance le script."
    exit 1
}

Write-Host "Attente que les services démarrent..."
Start-Sleep -Seconds 5

$url = "http://localhost:7860"
Write-Host "Ouverture de l'UI : $url"
Start-Process $url

Write-Host "Affichage des logs du container 'plateforme_agentique' (Ctrl+C pour arrêter)..."
docker compose logs -f plateforme_agentique
