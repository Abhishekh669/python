import socket
import threading


IP = "0.0.0.0"
PORT = 10000



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(10)
    print(f"Listening on {IP}:{PORT}")
    while True:
        client, address = server.accept();
        print(f"Accepted connection from {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start();

def handle_client(client_sock):
    with client_sock as sock:
        request = sock.recv(1024)
        print(f'Received : {request.decode("utf-8")}')
        sock.send(b"hello from the server")


if __name__ == "__main__":
    main()


    