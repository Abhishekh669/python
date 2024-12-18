import socket

# Define the target IP address and port
target_ip = '192.168.1.19'  # Replace with the target's IP address
target_port = 5000  # Replace with the port that the target is listening on

# Create a socket connection to the target
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((target_ip, target_port))
    print(f"Connected to {target_ip}:{target_port}")

    # Receive the data from the target and write it to a local file
    with open("downloaded_newfile.txt", "wb") as file:
        while True:
            # Read 4096 bytes from the socket
            data = s.recv(4096)
            if not data:
                break  # Break if no more data is received
            file.write(data)
            print("Receiving data...")

    print("File downloaded successfully as 'downloaded_newfile.txt'")
