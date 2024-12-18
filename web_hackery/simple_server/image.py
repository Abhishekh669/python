import socket 
import time 


HOST = "10.10.143.196"
PORT = 80

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect((HOST, PORT))
mysock.sendall(b'GET http://10.10.143.196/assets/images/oneforall.jpg HTTP/1.0\r\n\r\n')
count = 0 
picutre = b""


while True:
    data = mysock.recv(5120)
    if len(data) < 1: break
    count = count + len(data)
    print(len(data), count)
    picutre = picutre + data
mysock.close()

pos = picutre.find(b"\r\n\r\n")
# print("this ishte pos  :",pos)
print("Header length ", pos)
print(picutre[:pos].decode())



picutre = picutre[pos+ 4:]
fhand  = open("oneforall.jpg","wb")
fhand.write(picutre)
fhand.close()


