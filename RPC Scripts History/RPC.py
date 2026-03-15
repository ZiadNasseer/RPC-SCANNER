from impacket.dcerpc.v5 import transport

target = "192.168.1.76"
port = 135

stringBinding = r"ncacn_ip_tcp:%s[%d]" % (target, port)

rpctransport = transport.DCERPCTransportFactory(stringBinding)
dce = rpctransport.get_dce_rpc()

print("[+] Connecting to RPC...")
dce.connect()

print("[+] Connected to RPC endpoint")
