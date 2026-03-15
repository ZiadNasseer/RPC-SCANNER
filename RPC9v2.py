import socket
import threading
import subprocess
from impacket.dcerpc.v5 import transport, epm


# ------------------------
# COLORS
# ------------------------
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


# ------------------------
# BANNER
# ------------------------
def print_banner():
    banner = r"""
                      __====-_  _-====___
              _--^^^#####//      \\#####^^^--_
           _-^##########// (    ) \\##########^-_
          -############//  |\^^/|  \\############-
        _/############//   (@::@)   \\############\_
       /#############((     \\//     ))#############\
      -###############\\    (oo)    //###############-
     -#################\\  / UUU \  //#################-
    -###################\\/  (v)  \/###################-
   _#/|##########/\######(   /   \   )######/\##########|\#_
   |/ |#/\#/\#/\/  \#/\##\  |(_ _)|  /##/\#/  \/\#/\#/\| \|
   `  |/  V  V  `   V  \#\| | | | | |/#/  V   '  V  V  \|  '
      `   `  `      `   / | | | | | \   '      '  '   '
                       (  | | | | |  )
                      __\ | | | | | /__
                     (vvv(VVV)(VVV)vvv)
    """

    print(RED + banner + RESET)
    print(YELLOW + "                    RPC-SCANNER\n" + RESET)

    print(GREEN + "Developer : ZiadNasserGharib")
    print("GitHub    : https://github.com/ZiadNasseer")
    print("Twitter/X : https://x.com/ZiadNasser01" + RESET)
    print("="*60)


open_ports = []


# ------------------------
# CHECK IF HOST ALIVE
# ------------------------
def check_host(ip):

    print("\n[+] Checking if target is alive...\n")

    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL
        )

        if result.returncode != 0:
            print("[-] Host unreachable or timeout")
            return False

        print("[+] Host is alive")
        return True

    except:
        return False


def scan_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip, port))
        print(f"[OPEN] {port}")
        open_ports.append(port)
        s.close()
    except:
        pass


def scan_all_ports(ip):
    print("\n[+] Scanning ALL ports (1-65535)\n")

    threads = []

    for port in range(1, 65536):

        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()

        if len(threads) >= 500:
            for th in threads:
                th.join()
            threads = []

    for th in threads:
        th.join()


def rpc_enum(ip):

    if 135 not in open_ports:
        print("\n[-] Port 135 not open → RPC enumeration skipped")
        return

    print("\n[+] Connecting to RPC Endpoint Mapper\n")

    try:
        stringbinding = f"ncacn_ip_tcp:{ip}[135]"

        rpctransport = transport.DCERPCTransportFactory(stringbinding)
        dce = rpctransport.get_dce_rpc()
        dce.connect()

        print("[+] RPC Connected")

        entries = epm.hept_lookup(ip, dce)

        print("\n[+] RPC Endpoints\n")

        for entry in entries:

            try:
                tower = entry['tower']
                uuid = str(tower['Floors'][0])

                try:
                    binding = epm.PrintStringBinding(tower)
                except:
                    binding = "unknown"

                print("="*60)
                print("UUID:", uuid)
                print("Binding:", binding)

            except:
                pass

    except Exception as e:
        print("RPC error:", e)


def main():

    target = input("Enter Target IP: ").strip()

    if not check_host(target):
        return

    print(f"\nTarget: {target}")

    scan_all_ports(target)

    rpc_enum(target)


if __name__ == "__main__":

    print_banner()

    try:
        main()

    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        print("[+] Exiting safely...")
