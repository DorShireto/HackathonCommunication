import getch
# import msvcrt
import socket
import struct
import time
#**********************************************************************************************
#                                          ATRIBUTES
#
#**********************************************************************************************
teamName = "DeaD_l0ck_Av0idErs"
gotPort=False
serverAddress = None
clientSocketTCP = None

#**********************************************************************************************
#                                       FUNCTIONS PART
#
#**********************************************************************************************

def getchar():
    # return msvcrt.getche()
    return getch.getch() #uncomment me while using LINUX


def setupConnections():
    clientSocketTCP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocketUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    clientSocketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #SO_REUSEPORT allow multi client connection
    # # client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    clientSocketUDP.bind(('',13115)) #TODO change port before submitting 13117!!!!!!




def searchForServer():
    #listening for udp over port 13117 - 1024 is buffer size
    while not gotPort:
        msg, serverDetails = clientSocketUDP.recvfrom(1024)
        msg = struct.unpack('Ibh',msg)
        if msg[0] == 4276993775 and msg[1] == 2:
            serverPort=msg[2]
            gotPort=True
    serverAddress = serverDetails[0]
    print("Received offer from " + serverAddress +" attempting to connect... ”")

def game():
    timeout = 10
    startTime = time.time()
    while timeout > time.time() - startTime :        
        char = getchar()
        print(char) #TODO debug
        clientSocketTCP.send(char.encode())


#**********************************************************************************************
#                         SCRIPT PART
#
#**********************************************************************************************
print("Client started, listening for UDP offer requests from remote server...")
while 1:
    setupConnections()
    searchForServer()
    #connect to server
    clientSocketTCP.connect((serverAddress,serverPort))
    print("connected to server via TCP...") #TODO DEBUG
    #sending client name to server over TCP (5)
    clientSocketTCP.send(teamName.encode())
    msg = clientSocketTCP.recv(1024) #welcomeMSG
    print(msg.decode())
    game()
    msg = clientSocketTCP.recv(1024) #summaryMSG
    print(msg.decode())
    print("Server disconnected, listening for offer requests...")


