# Path to the Node.js script
$nodeScriptPath = "C:\Program Files (x86)\winx32\server.js"

# Check if the Node.js script exists
if (Test-Path $nodeScriptPath) {
    # Run the Node.js script
    node $nodeScriptPath
} else {
    Write-Host "Node.js script not found at $nodeScriptPath"
}
