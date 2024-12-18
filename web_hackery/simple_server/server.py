import socket 
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(("192.168.1.19", 5000 ))
cmd = "this is mt message".encode()
mysock.send(cmd)


while True:
    data = mysock.recv(4096)
    if len(data) < 1:
        break
    print(data.decode(), end='')
mysock.close()
        