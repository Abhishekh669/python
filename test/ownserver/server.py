import socket
import threading

IP = "127.0.0.1"  # Typically use 127.0.0.1 for localhost
PORT = 1234

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Define IPv4 and TCP
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))  # Bind to IP and port
    server.listen(1000)  # Listen for up to 5 connections

    while True:
        client, address = server.accept()  # Accept incoming connections
        print(f"Connection established Successfully {address[0]} : {address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = client_socket.recv(1024)
        print(f"Received {request.decode()}")
        sock.send(b"you are authenticated")

if __name__ == "__main__":
    main()
