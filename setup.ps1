# Create frontend directory structure
$frontendDirs = @(
    "frontend\public",
    "frontend\src\components",
    "frontend\src\pages",
    "frontend\src\services",
    "frontend\src\utils"
)

# Create backend directory structure
$backendDirs = @(
    "backend\app\api",
    "backend\app\core",
    "backend\app\models",
    "backend\app\services",
    "backend\app\utils",
    "backend\tests"
)

# Create all directories
foreach ($dir in ($frontendDirs + $backendDirs)) {
    if (-not (Test-Path -Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir"
    } else {
        Write-Host "Directory already exists: $dir"
    }
}

Write-Host "Project structure created successfully!"
