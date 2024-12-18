import socket

target_host = "0.0.0.0"

target_port = 9998


# create the socket object 
# sock_dgram => udp is used 

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# this is udp so connection should not be established 


# send some data 
# sendto => sendign the data to the server 

client.sendto(b"AAAAA", (target_host, target_port))


# receive some data 
# recvfrom => to receive udp data back 

data, addr = client.recvfrom(4096)

print(data.decode())

client.close()