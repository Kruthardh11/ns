# scanner.py
import os
from scapy.all import ICMP, IP, sr1
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from scapy.config import conf

# conf.use_pcap = False  # Critical for Windows stability
print_lock = Lock()

def ping(host):
    try:
        # Added inter and retry parameters for Windows compatibility
        response = sr1(IP(dst=str(host))/ICMP(), timeout=1, verbose=0, inter=0.1, retry=0)
        return str(host) if response else None
    except Exception as e:
        return None

def ping_sweep(network, netmask):
    live_hosts = []
    hosts = list(ip_network(f"{network}/{netmask}").hosts())
    total_hosts = len(hosts)
    
    # Reduced thread count for Windows stability
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(ping, host): host for host in hosts}
        for i, future in enumerate(as_completed(futures), 1):
            host = futures[future]
            result = future.result()
            with print_lock:
                print(f"Scanned: {i}/{total_hosts}", end="\r")
                if result:
                    print(f"\n✅ Live host: {host}")
                    live_hosts.append(result)
    
    return live_hosts

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python scanner.py <network> <netmask>")
        print("Example: python scanner.py 192.168.1.0 24")
        sys.exit(1)
        
    network = sys.argv[1]
    netmask = sys.argv[2]
    live_hosts = ping_sweep(network, netmask)
    print("\nLive hosts:", live_hosts)
