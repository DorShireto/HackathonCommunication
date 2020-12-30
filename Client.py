import getch
# import msvcrt
import socket
import struct

def getchar():
    # return msvcrt.getche()
    return getch.getch() #uncomment me while using LINUX


teamName = "DeaD_l0ck_Av0idErs"
gotPort=False
clientSocketTCP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocketUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientSocketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #SO_REUSEPORT allow multi client connection
# # client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
clientSocketUDP.bind(('',13115))



print("Client started, listening for UDP offer requests from remote server...")

#listening for udp over port 13117 - 1024 is buffer size
while not gotPort:
    msg, serverDetails = clientSocketUDP.recvfrom(1024)
    msg = struct.unpack('Ibh',msg)
    if msg[0] == 4276993775 and msg[1] == 2:
        serverPort=msg[2]
        gotPort=True

serverAddress = serverDetails[0]


#serverPort = port will be in l5-6 bytes of the msg
print("Received offer from " + serverAddress +" attempting to connect... ”")
clientSocketTCP.connect((serverAddress,serverPort))
print("connected to server via TCP...")
#sending client name to server over TCP (5)
clientSocketTCP.send(teamName.encode())


msg = clientSocketTCP.recv(1024)
print(msg.decode())
msg = clientSocketTCP.recv(1024)
print(msg.decode())

#TODO:handle connection exception
while True:
    char = getchar()
    print(char) #TODO debug
    clientSocketTCP.send(char.encode())


    