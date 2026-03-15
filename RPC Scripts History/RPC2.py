from impacket.dcerpc.v5 import transport, epm

target = "192.168.1.76"

print(f"[+] Target: {target}")
print("[+] Connecting to RPC Endpoint Mapper...\n")

binding = f"ncacn_ip_tcp:{target}[135]"
rpctransport = transport.DCERPCTransportFactory(binding)

dce = rpctransport.get_dce_rpc()
dce.connect()

print("[+] Connected to RPC\n")
print("[+] Enumerating RPC services...\n")

entries = epm.hept_lookup(target, dce)

uuid_services = {
    "12345778-1234-abcd-ef00-0123456789ab": "SAMR",
    "12345778-1234-abcd-ef00-0123456789ac": "LSARPC",
    "8a885d04-1ceb-11c9-9fe8-08002b104860": "EPMAPPER",
    "6bffd098-a112-3610-9833-012892020162": "BROWSER",
    "367abb81-9844-35f1-ad32-98f038001003": "SVCCTL (Service Control Manager)",
    "4b324fc8-1670-01d3-1278-5a47bf6ee188": "SRVSVC (SMB Server)",
}

for entry in entries:
    tower = entry['tower']

    uuid = str(tower['Floors'][0])
    binding_string = epm.PrintStringBinding(tower)

    service = uuid_services.get(uuid, "Unknown")

    protocol = "Unknown"
    port = "N/A"
    pipe = "N/A"

    if "ncacn_ip_tcp" in binding_string:
        protocol = "RPC over TCP"
        port = binding_string.split("[")[1].split("]")[0]

    elif "ncacn_np" in binding_string:
        protocol = "RPC over SMB Named Pipe"
        pipe = binding_string.split(":")[-1]

    elif "ncalrpc" in binding_string:
        protocol = "Local RPC"

    print("=" * 60)
    print(f"Service Name : {service}")
    print(f"UUID         : {uuid}")
    print(f"Protocol     : {protocol}")
    print(f"Port         : {port}")
    print(f"Named Pipe   : {pipe}")
    print(f"Binding      : {binding_string}")

print("\n[+] Scan Complete")
