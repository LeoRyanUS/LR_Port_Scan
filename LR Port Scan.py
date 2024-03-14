import socket
from concurrent.futures import ThreadPoolExecutor
import os
import concurrent.futures

def display_welcome_message():
    print('''
          #> Port Scan
          #> --------
          #>               \
          #>                \
          #>                 \
          #> _       _____   _____  
          #>| |     |  ___| |  _  \ 
          #>| |     | |_    | |_| | 
          #>| |     |  _|   |  _  / 
          #>| |___  | |___  | | \ \ 
          #>|_____| |_____| |_|  \_\
           Made By: @LeoRyanUS


''')

def get_ports_range():
    while True:
        ports_range = input("Enter ports range (e.g., 0:10000): ")
        if ports_range == '0:0':
            return 0, 0
        try:
            start, end = map(int, ports_range.split(':'))
            if 0 <= start <= 65535 and 0 <= end <= 65535 and start <= end:
                return start, end
            else:
                print("Invalid ports range! Port number should be between 0 and 65535.")
        except ValueError:
            print("Invalid input! Please enter ports range in the format 'start:end'.")

def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            return port
        else:
            return None

def scan_ports(target, start_port, end_port):
    open_ports = []
    print(f"\nScanning ports on {target}...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            if future.result():
                open_ports.append(port)
    return open_ports

if __name__ == "__main__":
    display_welcome_message()
    
    target = input("Enter target IP address or domain: ")
    start_port, end_port = get_ports_range()

    if start_port != 0 or end_port != 0:
        open_ports = scan_ports(target, start_port, end_port)
        if open_ports:
            print("\nOpen ports:", open_ports)
        else:
            print("No open ports found.")
    else:
        print("Skipping port scan as no port range specified.")
