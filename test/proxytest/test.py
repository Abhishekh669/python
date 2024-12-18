import socket 
import threading 
import sys


HEX_FILTER  = "".join(
    [
        (len(repr(chr(i))) == 3) and chr(i) or "." for i in range(256)
    ]
)


def hexdump(src, length = 1, show=True):
    if isinstance(src,bytes):
        src = src.decode()
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length]);
        printable = word.translate(HEX_FILTER);
        hexa = " ".join([f'{ord(c):02X}' for c in word]);
        hexwidth = length * 3
        results.append(f'{i:04X} {hexa:<{hexwidth}} {printable}')

    if show:
        for line in results:
            print(line)
    else:
        return results;

def response_handler(data):
    return data;

def request_handler(data):
    return data;



def receive_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data

    except Exception as e:
        pass
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    #since first   proxy is taking the response from the remote rever so creating the connection to the remote server
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    if receive_first:
        # now since the connection is made now geting the data from teh remtoe  server 
        remote_buffer = receive_from(remote_socket)
        # converting the data from the remtoe server to the hex dump 
        hexdump(remote_buffer)
        # if wanaa do any modification so send it to the response handler
        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):

            print(f"Sending data to  the localhost")

            client_socket.send(remote_buffer)

    while True:
        
        #now receiving hte data from the client side
        local_buffer =receive_from(client_socket)

        if len(local_buffer):

            print(f"Sending the data from the client to remote server ({local_buffer}) bytes")

            hexdump(local_buffer)

            local_buffer  = request_handler(local_buffer)

            remote_socket.send(local_buffer)

            print(f"Sending the data to the remote server")

        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):

            print("[<==] REceifed %d butes from remote."%len(remote_buffer))

            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)

            client_socket.send(remote_buffer)

            print("[<==] Sent to localhost")

        if not len(local_buffer) or not len(remote_buffer):

            client_socket.close()

            remote_socket.close()

            print("[*] No more  data. Closing Connection")

            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    #here creating a proxy  server  so that i can communicate with the client and the remote server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        server.bind((local_host, local_port))

    except Exception as e:

        print("problem on bind %r" %e)

        print("[!!] Failed to listen on %d:%d"%(local_host,local_port))

        print('[!!] Check for other listening sockets or correct peromissions.')

        sys.exit(0)

    print("Listenig on  %s:%d" %(local_host, local_port)) 

    server.listen(10)

    #listening contunously such that  client and remote server  can  make request and get resone on it 
    while True:

        client_socket, address = server.accept()

        print("[*] Connection established  %s:%d" %(address[0], address[1]))

        client_thread = threading.Thread(target=proxy_handler, args=(
            
            client_socket, remote_host, remote_port, receive_first

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