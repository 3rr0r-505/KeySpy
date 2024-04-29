# Path to the python script
$pythonScriptPath = "C:\Program Files (x86)\winx32\kSpy.py"

# Check if the Node.js script exists
if (Test-Path $pythonScriptPath) {
    # Run the python script
    python $pythonScriptPath
} else {
    Write-Host "kSpy.py script not found at $pythonScriptPath"
}
