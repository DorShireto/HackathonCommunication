import getch
import socket
import struct

serverPort = 2058 
clientSocketTCP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocketUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientSocketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #SO_REUSEPORT allow multi client connection
# # client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
clientSocketUDP.bind(('',13117))



print("Client started, listening for offer requests from remote server...")

#listening for udp over port 13117 - 1024 is buffer size
msg, serverDetails = clientSocketUDP.recvfrom(1024)
msg = struct.unpack('Ibh',b'10')
print(msg)
serverAddress = serverDetails[0]


#serverPort = port will be in l5-6 bytes of the msg

clientSocketTCP.connect((serverAddress,serverPort))
print("connected to server...")
#TODO:handle connection exception
while True:
    char = getch.getch()
    print(char) #TODO debug
    clientSocketTCP.send(char.encode())


    