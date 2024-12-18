#!/bin/python3

import sys
import socket
from datetime import datetime

# Define the target
if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid number of arguments.")
    print("Syntax: python3 scanner.py <hostname>")
    sys.exit()

# Adding the pretty banner
print("-" * 50)
print(f"Scanning target: {target}")
print(f"Time started: {datetime.now()}")
print("-" * 50)

# Set the default timeout for socket connections
socket.setdefaulttimeout(1)

try:
    for port in range(1, 85):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex((target, port))
            print(f"Checking port {port}")
            if result == 0:
                print(f"Port {port} is open")
except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()

except socket.gaierror:
    print("Hostname could not be resolved.")
    sys.exit()

except socket.error:
    print("Could not connect to server.")
    sys.exit()
