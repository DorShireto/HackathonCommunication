import getch
# import msvcrt
import socket
import struct
import time
from scapy.all import *

class Client:
#**********************************************************************************************
#                                          ATRIBUTES
#
#**********************************************************************************************
    def __init__(self):
		self.listeningUDPPort = 13117
		#self.listeningUDPPort = 13115 #for tests uses only 
        self.teamName = "DeaD_l0ck_Av0idErs"
        self.serverPort = None
        self.gotPort=False
        self.serverAddress = None
        self.clientSocketTCP = None
        self.clientSocketUDP = None
        self.serverAddress= None
        self.setupConnections()

    #**********************************************************************************************
    #                                       FUNCTIONS PART
    #
    #**********************************************************************************************

    def getchar(self):
        # return msvcrt.getche() #uncomment me while using Windows OS
        return getch.getch() #uncomment me while using LINUX


    def setupConnections(self):

        self.clientSocketTCP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clientSocketUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.clientSocketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #SO_REUSEPORT allow multi client connection
        self.clientSocketUDP.bind(('',self.listeningUDPPort)) 
        self.serverAddress = get_if_addr("eth1") #get server address on Linux OS
		#self.serverAddress = socket.gethostbyname(socket.gethostname()) #get server address on Windows OS





    def searchForServer(self):
        #listening for udp over port 13117 - 1024 is buffer size
        while not self.gotPort:
            msg, serverDetails = self.clientSocketUDP.recvfrom(1024)
            msg = struct.unpack('Ibh',msg)
            if msg[0] == 4276993775 and msg[1] == 2: #4276993775 - Integer Magic coockie value instead hexa, 2 - Integer Message type
                self.serverPort=msg[2]
                self.gotPort=True
        serverAddress = serverDetails[0] #IP address
        print("Received offer from " + serverAddress +" attempting to connect... ”")


    def game(self):
        os.system("stty raw -echo") #reading chars from user input without blocking
        while 1:
            msgFromServerWaiting, _, _ = select([self.clientSocketTCP],[],[],0.2)
            if msgFromServerWaiting: # got stop game message from server
                os.system("stty -raw echo") #return to default
                return
            else: # no waiting msg from server -> GAME MODE STILL RUNING
                thereIsTypedChar, _, _ = select([sys.stdin],[],[],0.2) #check if user pressed any key
                if thereIsTypedChar:
                    #get the char from IO
                    char = sys.stdin.read(1)
                    self.clientSocketTCP.send(char.encode())

        

#**********************************************************************************************
#                         SCRIPT PART
#
#**********************************************************************************************
print("Client started, listening for UDP offer requests from remote server...")
while 1:
    client = Client()
    client.searchForServer()
    #connect to server
    client.clientSocketTCP.connect((client.serverAddress,client.serverPort))
    #sending client name to server over TCP (5)
    client.clientSocketTCP.send(client.teamName.encode())
    msg = client.clientSocketTCP.recv(1024) #welcome MSG
    print(msg.decode())
    client.game()
    msg = client.clientSocketTCP.recv(1024) #summary MSG
    print(msg.decode())
    print("Server disconnected, listening for offer requests...")
