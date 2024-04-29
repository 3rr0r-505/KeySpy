# Path to the Node.js script
$pythonScriptPath = "C:\Program Files (x86)\winx32\kSpy.py"

# Check if the Node.js script exists
if (Test-Path $pythonScriptPath) {
    # Run the Node.js script
    python $pythonScriptPath
} else {
    Write-Host "kSpy.py script not found at $pythonScriptPath"
}
