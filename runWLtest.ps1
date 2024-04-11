# Define the path to the Python script
$pythonScriptPath = "S:\Work-Space\KeySpy\wlTest.py"

# Check if the file exists
if (Test-Path $pythonScriptPath) {
    # Run the Python script in the terminal
    python $pythonScriptPath
} else {
    Write-Host "Error: Python script not found at $pythonScriptPath"
}
