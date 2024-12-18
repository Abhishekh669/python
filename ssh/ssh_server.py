import os
import paramiko
import socket
import sys
import threading

# Define the current working directory and host key
CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, "test_rsa.key"))

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "lucid" and password == "lucid":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

if __name__ == "__main__":
    server_ip = '127.0.0.1'
    ssh_port = 2222

    try:
        # Create a socket and bind it to the server address and port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server_ip, ssh_port))
        sock.listen(5)  # Limit the number of queued connections
        print("[*] Listening for connections...")
        client, addr = sock.accept()
    except Exception as e:
        print(f'[-] Listening Failed: {str(e)}')
        sys.exit(1)
    
    print(f'[+] Got a connection from {addr}')

    # Start the Paramiko transport session
    try:
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(HOSTKEY)
        server = Server()
        bhSession.start_server(server=server)

        chan = bhSession.accept(20)
        if chan is None:
            print("*** No channel")
            sys.exit(1)

        print('[+] Authenticated!')
        
        # Receive initial data from the client
        try:
            print(chan.recv(1024).decode())
        except Exception as e:
            print(f"Error receiving initial data: {e}")

        # Send a welcome message to the client
        chan.send("Welcome to bh_ssh".encode())
        
        while True:
            try:
                command = input("Enter command: ")
                if command == "exit":
                    chan.send("exit".encode())
                    print('Exiting')
                    break
                else:
                    chan.send(command.encode())
                    response = chan.recv(8192)
                    print(response.decode())
            except Exception as e:
                print(f"Error during command execution: {e}")
                break
    except KeyboardInterrupt:
        print('Interrupted by user.')
    finally:
        bhSession.close()
        client.close()
        sock.close()
