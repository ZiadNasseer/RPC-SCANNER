# RPC-SCANNER

Advanced RPC Endpoint Scanner & Port Scanner

RPC-SCANNER is a Python-based tool designed to scan all TCP ports on a target system and enumerate RPC endpoints using Microsoft's RPC Endpoint Mapper.

This tool is useful for:
- Red Team operations
- Security research
- RPC service discovery
- Attack surface analysis
- Network reconnaissance


-------------------------------------

Features

- Scan all ports (1-65535)
- Detect open ports
- RPC Endpoint enumeration
- Multi-threaded port scanning
- Graceful CTRL+C exit
- Host availability detection
- Colored banner output

-------------------------------------

Requirements

Python 3.8+

Python Libraries:

impacket

-------------------------------------

Installation

Clone the repository:

git clone https://github.com/ZiadNasseer/RPC-SCANNER.git

Enter the project folder:

cd RPC-SCANNER

Install dependencies:

1-python3 -m venv my_venv

2-source my_venv/bin/activate

3-python3 -m pip install -r requirements.txt


-------------------------------------

Usage

Run the script:

sudo python3 RPC9v2.py

Enter the target IP when prompted.

Example:

Enter Target IP: 192.168.1.10

-------------------------------------

Output Example

[OPEN] 135
[OPEN] 445
[OPEN] 5985

RPC Endpoints:

UUID: XXXXXXXX
Binding: ncacn_ip_tcp

-------------------------------------

Author

Developer: ZiadNasserGharib

GitHub:
https://github.com/ZiadNasseer

Twitter / X:
https://x.com/ZiadNasser01

-------------------------------------

Disclaimer

This tool is intended for educational purposes and authorized security testing only.
Unauthorized use against systems you do not own or have permission to test is illegal.
