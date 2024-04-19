<p align="center"><a href="https://github.com/3rr0r-505/KeySpy"><img alt="" src="https://github.com/3rr0r-505/KeySpy/blob/main/img/KeySpy-cover.png?raw=true"  height="50%" width="100%"/></a></p>

<p align="center"> 
<a href="https://www.python.org/"><img alt="" src="https://img.shields.io/badge/python-3.9%2B-brighten?logo=python&label=pyhton&color=blue"/></a>
&nbsp;
<a href="https://www.gnu.org/gnu/linux-and-gnu.en.html"><img alt="" src="https://img.shields.io/badge/OS-GNU%2FLINUX-brighten?logo=linux&label=OS&labelColor=grey&color=red"/></a>
&nbsp;
<a href="https://www.microsoft.com/en-us/windows?r=1"><img alt="" src="https://img.shields.io/badge/OS-Windows-brighten?logo=windows&label=OS&labelColor=grey&color=blue"/></a><br>
</p>

# KeySpy - Remote Keylogger Tool

KeySpy is a simple Python keylogger with a web interface for viewing captured keystrokes in real-time.

## W3bSpy - Browser Extension of KeySpy

A Browser Extension to detect the site and key strokes, store the data in mongoDB server.

<!--## Features

- Captures keystrokes in the background while running.
- Stores captured keystrokes in a `keylogs.txt` file.
- Displays captured keystrokes in a web interface using Flask.
- Automatically starts the keylogger and web interface upon running the `weblogger.py` script.
- Allows viewing keystrokes from multiple sessions.-->

## Installation
### Victim Device:
  - Load the extension into Chrome:-
      - Open Google Chrome and go to chrome://extensions/.
      - Enable Developer Mode by toggling the switch in the top right corner.
      - Click on the "Load unpacked" button and select the W3bSpy-Client directory.
### Attacker Device :
   - Setting up the server:
      - Install dependencies and start the server:
        ```bash
        cd KeySpy/W3bSpy/W3bSpy-Server
        npm install express mongoose
        node server.js
