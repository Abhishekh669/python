import os
import paramiko
import socket 
import sys
import threading 

CWD = os.path.dirname(os.path.realpath(__file__))
print(os.path.join(CWD, 'test_rsa.key'))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))
print("htis is the host key", HOSTKEY)


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'lucid') and (password == '@iamlucid669'):
            return paramiko.AUTH_SUCCESSFUL
    

if __name__ == '__main__':
    server = "127.0.0.1"
    ssh_port = 4000

    try:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.bind((server, ssh_port))
        socket_server.listen(100)
        print("Listening for connection in %s:%d"%(server,ssh_port ))
        client, addr = socket_server.accept()
    except Exception as e:
        print('[-] Listen failed : ', str(e))
        sys.exit(1)

    else: 
        print('[+] Got a connection ! %s:%d' %(addr[0], addr[1]))

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()

    bhSession.start_server(server=server)

    chan = bhSession.accept(20)

    if chan is None:
        print('*** Bi channel')
        sys.exit(1)

    print('[+] Authenticated!')
    print(chan.recv(1024))

    chan.send("Welcome to bh_ssh")
    try:
        while True:
            command = input("Enter command : ")
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print("i have received from the client side",r )
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()

