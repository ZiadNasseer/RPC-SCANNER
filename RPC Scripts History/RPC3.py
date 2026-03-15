import socket
import time
from impacket.dcerpc.v5 import transport, epm

target = "192.168.1.76"
timeout = 3
retries = 3

try:
    ip = socket.gethostbyname(target)
    print(f"[+] Target resolved: {target} -> {ip}")
except socket.gaierror:
    print("[-] Invalid hostname or IP")
    exit()

binding = f"ncacn_ip_tcp:{ip}[135]"

connected = False

for attempt in range(1, retries + 1):
    try:
        print(f"[+] Attempt {attempt} connecting to RPC...")

        rpctransport = transport.DCERPCTransportFactory(binding)
        rpctransport.set_connect_timeout(timeout)

        dce = rpctransport.get_dce_rpc()
        dce.connect()

        print("[+] Connected to RPC Endpoint Mapper\n")
        connected = True
        break

    except Exception as e:
        print(f"[-] Connection failed: {e}")
        time.sleep(1)

if not connected:
    print("\n[-] No connection to RPC service")
    exit()

print("[+] Enumerating RPC services...\n")

entries = epm.hept_lookup(ip, dce)

for entry in entries:
    try:
        tower = entry['tower']
        uuid = str(tower['Floors'][0])

        try:
            binding_string = epm.PrintStringBinding(tower)
        except:
            binding_string = "Unknown binding"

        port = "N/A"
        if "[" in binding_string:
            port = binding_string.split("[")[1].split("]")[0]

        print("=" * 60)
        print(f"UUID    : {uuid}")
        print(f"Binding : {binding_string}")
        print(f"Port    : {port}")

    except Exception:
        continue

print("\n[+] Enumeration complete")
