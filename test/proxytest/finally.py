import threading
import sys
import socket 

HEX_FILTER = "".join([len(repr(chr(i))) and chr(i) or "." for i in range(256)])

def hexdump(src, length = 16, show= True):
    if isinstance(src, bytes):
        src = src.decode()

    results = list()

    for i in range(0, len(src), length):
        word = str(src[i: i+length])
        printable = word.translate(HEX_FILTER)
        hexa = " ".join([f'{ord(c):02X}' for c in word])
        hex_length = 3 * length
        results.append(f'{i:04X} {hexa:<{hex_length}} {printable}')

    if show:
        for line in results:
            print(line)
    else:
        return results;



def receive_from(connection):
    buffer = b""
    connection.settimeout(10)
    
    try:

        while True:
            data = connection.recv(4096)
            
            if not len(data):
                break
            buffer += data
    except:
        pass
    return buffer



def request_handler(data):
    return data


def response_handler(data):
    data =b"fuck off no data for you"
    return data


def proxy_handler(remote_host, remote_port, client_socket, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        print("Got the data from the  remote server by the proxy server")
        hexdump(remote_buffer)

        if len(remote_buffer):
            client_socket.send(remote_buffer)
            print("Sending the data to the client from the  proxy server")

    while True:
        local_buffer  = receive_from(client_socket)
        if len(local_buffer):
            print("Got the data to the proxy server from the client")
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("Sending the data from the proxy server to the server")
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("Received the data from the server to the proxy server")
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("Sending the data from the proxy  server to the client server")
        if not len(remote_buffer) or not len(local_buffer):
            remote_socket.close()
            client_socket.close()
            sys.exit()
            break

            



def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("Connection failed")
        print(f"Error : {e}")
        sys.exit();
    server.listen(10)

    while True:
        client_socket, address = server.accept()
        print("[*] Connection Established %s:%d"%(address[0], address[1]))
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
    local_port = int(sys.argv[2])
    
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)



if __name__ == "__main__":
    main()