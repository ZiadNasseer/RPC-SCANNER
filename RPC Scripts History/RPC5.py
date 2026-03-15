import socket
from impacket.dcerpc.v5 import transport, epm

target = input("Target IP: ").strip()

binding = f"ncacn_ip_tcp:{target}[135]"

print("[+] Connecting to RPC Endpoint Mapper (135)...")

rpctransport = transport.DCERPCTransportFactory(binding)
rpctransport.set_connect_timeout(3)

dce = rpctransport.get_dce_rpc()
dce.connect()

print("[+] Connected\n")

print("[+] Enumerating RPC endpoints...\n")

entries = epm.hept_lookup(target, dce)

for entry in entries:
    try:
        tower = entry['tower']
        uuid = str(tower['Floors'][0])

        try:
            binding_string = epm.PrintStringBinding(tower)
        except:
            binding_string = str(tower)

        print("="*60)
        print("UUID    :", uuid)
        print("Binding :", binding_string)

        if "[" in binding_string and "]" in binding_string:
            endpoint = binding_string.split("[")[1].split("]")[0]
            print("Endpoint:", endpoint)

    except:
        continue

print("\n[+] Done")
