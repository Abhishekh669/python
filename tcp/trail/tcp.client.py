import socket


target_host = "0.0.0.0"
target_port = 10000


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

client.send(b"hello world")

response = client.recv(1024)

print(response.decode())


client.close();