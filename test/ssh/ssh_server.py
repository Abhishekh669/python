import os
import paramiko
import socket
import sys
import threading
import subprocess
import shlex

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    
    def check_channel_request(self, kind: str, chanid: int):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "lucid" and password == "@iamlucid669":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

def handle_client(chan):
    if chan is None:
        print("*** No channel")
        return
    
    print('[+] Authenticated')

    try:
        while True:
            # Receive command from client
            command = chan.recv(1024).decode().strip()
            if not command:
                continue
            
            if command.lower() == "exit":
                print("Exiting...")
                chan.send("Goodbye".encode())
                break

            try:
                # Execute the command locally
                cmd_output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
                chan.send(cmd_output)
            except subprocess.CalledProcessError as e:
                chan.send(f"Error executing command: {e.output.decode()}".encode())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        chan.close()

if __name__ == "__main__":
    server_ip = '127.0.0.1'
    ssh_port = 2222

    try:
        # Set up the socket and listen for incoming connections
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server_ip, ssh_port))
        sock.listen(100)

        print('[+] Listening for connections...')
        client, addr = sock.accept()
    except Exception as e:
        print(f'[-] Listen failed: {e}')
        sys.exit(1)
    else:
        print(f'[+] Got a connection! {client}, {addr}')
    
    # Create a Paramiko transport object and start the server
    transport = paramiko.Transport(client)
    transport.add_server_key(HOSTKEY)
    server = Server()
    transport.start_server(server=server)
    
    # Accept the channel
    channel = transport.accept(20)
    
    handle_client(channel)
    
    transport.close()
