import sys
import socket
import asyncio
import nmap
from scapy.all import IP,TCP,sr1
from impacket.dcerpc.v5 import transport, epm


class RPCScanner:

    def __init__(self,target):
        self.target = target


    # ------------------------
    # Fast async port scanner
    # ------------------------
    async def scan_port(self,port):

        try:
            reader,writer = await asyncio.open_connection(self.target,port)
            writer.close()
            return port
        except:
            return None


    async def scan_dynamic_ports(self):

        print("\n[+] Scanning Dynamic RPC Ports (49152-65535)...")

        tasks = []

        for port in range(49152,49250):
            tasks.append(self.scan_port(port))

        results = await asyncio.gather(*tasks)

        open_ports = [p for p in results if p]

        if open_ports:
            print("[+] Open RPC dynamic ports:",open_ports)
        else:
            print("[-] No dynamic RPC ports detected")

        return open_ports


    # ------------------------
    # Scapy quick scan
    # ------------------------
    def scapy_scan(self):

        print("\n[+] Scapy SYN scan")

        ports = [135,445]

        for port in ports:

            pkt = IP(dst=self.target)/TCP(dport=port,flags="S")

            resp = sr1(pkt,timeout=1,verbose=0)

            if resp and resp.haslayer(TCP) and resp[TCP].flags == 18:
                print(f"[+] Port {port} open")
            else:
                print(f"[-] Port {port} closed")


    # ------------------------
    # Nmap service detection
    # ------------------------
    def nmap_scan(self):

        print("\n[+] Running Nmap scan")

        scanner = nmap.PortScanner()

        scanner.scan(self.target,"135,445,49152-49250")

        for host in scanner.all_hosts():

            for proto in scanner[host].all_protocols():

                ports = scanner[host][proto].keys()

                for port in ports:

                    state = scanner[host][proto][port]['state']

                    print(f"[Nmap] Port {port} -> {state}")


    # ------------------------
    # RPC Enumeration
    # ------------------------
    def rpc_enum(self):

        print("\n[+] Connecting to RPC Endpoint Mapper")

        binding = f"ncacn_ip_tcp:{self.target}[135]"

        try:

            rpctransport = transport.DCERPCTransportFactory(binding)

            dce = rpctransport.get_dce_rpc()

            dce.connect()

            print("[+] RPC Connected")

        except Exception as e:

            print("[-] RPC connection failed:",e)
            return


        print("\n[+] Enumerating RPC endpoints")

        try:

            entries = epm.hept_lookup(self.target,dce)

        except Exception as e:

            print("[-] Enumeration error:",e)
            return


        for entry in entries:

            try:

                uuid = str(entry['tower']['Floors'][0])

                binding = epm.PrintStringBinding(entry['tower'])

                print("="*60)
                print("UUID:",uuid)
                print("Binding:",binding)

            except:
                continue


    # ------------------------
    # Run everything
    # ------------------------
    def run(self):

        print(f"\nTarget: {self.target}")

        self.scapy_scan()

        asyncio.run(self.scan_dynamic_ports())

        self.nmap_scan()

        self.rpc_enum()



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python rpc_super_scanner.py <target_ip>")
        sys.exit()

    target = sys.argv[1]

    scanner = RPCScanner(target)

    scanner.run()
