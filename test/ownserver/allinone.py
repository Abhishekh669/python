import socket
import threading
import argparse
import shlex 
import sys
import subprocess

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(c)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        print("i am in the send")
        print("i am looking buffer value ",  self.buffer.encode())
        if self.buffer:
            print(" iam check")
            self.socket.send(self.buffer.encode())
            print("i am here too")
            try:
                while True:
                    print("i am i loopp")
                    recv_len = 1
                    response = ""
                    while recv_len:
                        data = self.socket.recv(4096)
                        recv_len = len(data)
                        print(" i am at data", data)
                        response += data.decode()
                        print("this isthe response",response)
                        if recv_len < 4096:
                            print("i am before break")
                            break
                    if response:
                        print("i am at respoen if")
                        buffer = input("Enter your message (or 'exit' to quit)") # take the input from user and show reslut when clicked enter 
                        if buffer == 'exit':
                            self.socket.close()
                        buffer += "\n"
                        print("this is the buffer now :: ",buffer)
                    self.socket.send(buffer.encode()) #sending the data to the server
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
    def listen(self): # should act as server
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(100)
        while True:
            client_socket, address = self.socket.accept()
            print(f"[*] Connection Received -> {address[0]}:{address[1]} ")
            client_handler = threading.Thread(target=self.handle, args=(client_socket,))
            print("i am here")
            client_handler.start()
    
    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.decode())
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
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
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

nc = NetCat(args, buffer)
nc.run()




