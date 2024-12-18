import socket
import threading
import sys

HEX_FILTER = "".join([len(repr(chr(i))) == 3 and chr(i) or "." for i in range(256)])

def hexdump(src, length = 16, show = True):
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    for i in len(src):
        word = str(src[i:i + length])
        printable = word.translate(HEX_FILTER)
        hexa = " ".join([f'{ord(c):02X}' for c in word])
        

def receive_from(connection):
    buffer = ""
    
    connection.settimeout(10)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except :
        print("No data send")
    return buffer


def proxy_handler(remote_host, remote_port, client_socket, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)




def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))
    server.listen(10)
    while True:
        client_socket, address = server.accept()
        print("[*] Connection Received from %s:%d"%(address[0], address[1]))
        client_thread = threading.Thread(target=proxy_handler, args=(
            remote_host, remote_port, client_socket, receive_first
        ))
        client_thread.start()




def main():
    if len(sys.argv[1:]) != 5:
        print("usage : .proxy.py [localhost] [local_port]",end="")
        print("[remotehost] [remoteport] [receive_first]")
        print("Example : ./proxy 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit()
    local_host = sys.argv[1]
    local_port = sys.argv[2]

    remote_host = sys.argv[3]
    remote_port = sys.argv[4]

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == "__main__":
    main()