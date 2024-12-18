import socket
import shlex
import threading
import sys
import argparse
import subprocess

class NetCat:
    def __init__(self, args, buffer=None):
        self.buffer = buffer
        self.args = args
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    
    def send(self):
        self.socket.connect((self.args.target, self.args.port))

        if self.buffer:
            self.socket.send(self.buffer.encode())
            try:
                while True:
                    recv_len = 1
                    print("i am her")
                    response = ""
                    while recv_len :
                        data = self.socket.recv(4096)
                        recv_len = len(data)
                        response += data.decode()
                        if recv_len < 100:
                            break
                    if response:
                        buffer = input("> ")
                        if buffer == "exit":
                            self.socket.close()
                            sys.exit()
                    self.socket.send(self.buffer.encode())
            except Exception as e:
                self.socket.send(b"Operation Failed :: ",e)
                self.socket.close()
                sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5);
        while True:
            client_socket, address = self.socket.accept()
            print(f"[*] Listening in {address[0]}:{address[1]}")
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()
    

    def handle(self, client_socket):
        if self.args.execute:

            output = execute(self.args.execute)
            client_socket.send(output.encodes())
        elif self.args.command:
            print("i am finllay in command")
            cmd_buffer = b""
            while True:
                try:
                    print("this is the cmd_buffer before while loop :: ",cmd_buffer.decode())
                    while '\n' not in cmd_buffer.decode():
                        client_socket.send(b"Server: #> ")
                        cmd_buffer += client_socket.recv(64)
                        print("this is the command buffer in server ", cmd_buffer)
                        response = execute(cmd_buffer.decode())
                        print("this is the repsone calling execute ", response)
                        if response:
                            client_socket.send(response.encode())
                        cmd_buffer = b""
                except Exception as e:
                    print(f' server killed {e}')
                    client_socket.send(b"Terminating.....")
                    self.socket.close()
                    sys.exit()

def execute(cmd):
    cmd = cmd.strip()
    if  not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
    return output.decode()


parser = argparse.ArgumentParser(description="---NetCat Tools---")
parser.add_argument("-l", "--listen", action="store_true", help="Listen")
parser.add_argument("-p", "--port", type=int, help="port")
parser.add_argument("-t", '--target', help="Target")
parser.add_argument("-c", "--command", action='store_true', help="Command Shell")
parser.add_argument("-e", "--execute",  help="Execute")

args = parser.parse_args()

if args.listen:
    buffer = ""
else:
    buffer = sys.stdin.read()


nc  = NetCat(args, buffer)
nc.run()



