import getch
from socket import * 



serverName ="127.0.0.1"
serverPort = 2058 
clientSocket = socket(AF_INET,SOCK_STREAM)
#TODO: find server to connect to
clientSocket.connect((serverName,serverPort))
print("connected to server...")
#TODO:handle connection exception
while True:
    char = getch.getch()
    print(char) #TODO debug
    clientSocket.send(char.encode())


    