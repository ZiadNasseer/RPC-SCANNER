package main

import (
	"fmt"
	"net"
	"os"
	"time"
)

func checkPort(ip string, port int) bool {

	address := fmt.Sprintf("%s:%d", ip, port)

	conn, err := net.DialTimeout("tcp", address, 2*time.Second)
	if err != nil {
		return false
	}

	conn.Close()
	return true
}

func main() {

	if len(os.Args) < 2 {
		fmt.Println("Usage: ./rpcscan <target-ip>")
		return
	}

	ip := os.Args[1]

	fmt.Println("[+] Checking RPC Endpoint Mapper (135)...")

	if !checkPort(ip, 135) {
		fmt.Println("[-] RPC port 135 closed")
		return
	}

	fmt.Println("[+] RPC Endpoint Mapper reachable\n")

	fmt.Println("[+] Checking SMB (445)...")

	if checkPort(ip, 445) {
		fmt.Println("[+] SMB port 445 open")
	}

	fmt.Println("\n[+] Scanning Dynamic RPC Ports (49152-65535)...\n")

	for port := 49152; port <= 65535; port++ {

		if checkPort(ip, port) {
			fmt.Printf("[+] RPC Dynamic Port Open: %d\n", port)
		}

	}

	fmt.Println("\n[+] Scan complete")
}
