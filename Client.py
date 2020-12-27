import getch
from socket import * 



serverName =""
serverPort = 0 
clientSocket = socket(AF_INET,SOCK_STREAM)
#TODO: find server to connect to
# clientSocket.connect((serverName,serverPort))

#TODO:handle connection exception
while True:
    char = getch.getch()
    print(char)

