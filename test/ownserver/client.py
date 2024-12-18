import socket
import argparse


class Client:
    def __init__(self, args):
        self.args = args
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def sendrequest(self):
        self.socket.connect((self.args.target, self.args.port));
        data = self.args.data.encode() 
        self.socket.send(data) # sending hte data to the server
        response = self.socket.recv(4096) # receiveing the data from the server
        print(f"this is the response from the server\n{response.decode()}")
        self.socket.close();


        


parser = argparse.ArgumentParser(
    description="Simple Request to the server",
)



parser.add_argument("-p", "--port", type=int, help="Specify port")
parser.add_argument("-t", "--target", help='Specify target')
parser.add_argument("-d", '--data', default="Default Data", help="Give some data")

args = parser.parse_args();
print("this is the args ",args)

client = Client(args)
client.sendrequest()






