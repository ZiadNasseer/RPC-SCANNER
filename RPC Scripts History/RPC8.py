import socket
import asyncio
import nmap
from scapy.all import IP, TCP, sr1
from impacket.dcerpc.v5 import transport, epm


class RPCScanner:

    def __init__(self, target):
        self.target = target


# -----------------------------
# SCAPY SCAN
# -----------------------------
    def scapy_scan(self):

        print("\n[+] Scapy SYN scan")

        try:

            ports = [135,445]

            for port in ports:

                pkt = IP(dst=self.target)/TCP(dport=port,flags="S")

                resp = sr1(pkt,timeout=1,verbose=0)

                if resp and resp.haslayer(TCP) and resp[TCP].flags == 18:
                    print(f"[+] Port {port} open")
                else:
                    print(f"[-] Port {port} closed")

        except PermissionError:

            print("[-] Scapy needs root privileges. Run with sudo.")


# -----------------------------
# ASYNC PORT SCANNER
# -----------------------------
    async def scan_port(self,port):

        try:

            reader,writer = await asyncio.open_connection(self.target,port)

            print(f"[OPEN] {port}")

            writer.close()

        except:
            pass


    async def scan_all_ports(self):

        print("\n[+] Scanning ALL ports (1-65535)")

        tasks = []

        for port in range(1,65536):

            tasks.append(self.scan_port(port))

            if len(tasks) >= 500:

                await asyncio.gather(*tasks)

                tasks = []

        if tasks:
            await asyncio.gather(*tasks)


# -----------------------------
# NMAP SCAN
# -----------------------------
    def nmap_scan(self):

        print("\n[+] Running Nmap scan")

        try:

            scanner = nmap.PortScanner()

            scanner.scan(self.target,"1-65535")

            for host in scanner.all_hosts():

                for proto in scanner[host].all_protocols():

                    ports = scanner[host][proto].keys()

                    for port in ports:

                        state = scanner[host][proto][port]['state']

                        if state == "open":

                            print(f"[Nmap] Port {port} -> open")

        except Exception as e:

            print("Nmap error:",e)


# -----------------------------
# RPC ENUMERATION
# -----------------------------
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

                uuid = entry['tower']['Floors'][0]

                try:

                    binding = epm.PrintStringBinding(entry['tower'])

                except:

                    binding = "No binding info"

                print("="*60)
                print("UUID:",uuid)
                print("Binding:",binding)

            except:
                continue


# -----------------------------
# RUN
# -----------------------------
    def run(self):

        print(f"\nTarget: {self.target}")

        self.scapy_scan()

        asyncio.run(self.scan_all_ports())

        self.nmap_scan()

        self.rpc_enum()


# -----------------------------
# START
# -----------------------------
if __name__ == "__main__":

    target = input("Enter Target IP: ").strip()

    scanner = RPCScanner(target)

    scanner.run()
