from socket import *
import struct
import threading
import time


class Server:
    # **********************************************************************************************
    #                                          ATRIBUTES
    #
    # **********************************************************************************************
    def __init__(self):
        self.serverSocketUDP = None
        self.serverSocket = None
        self.serverPort = 2058
        self.serverName = "DeaD_l0ck_Av0iders"
        self.connectionsList = []
        self.addresses = []
        self.teamANames = []
        self.teamBNames = []
        self.scoreA = 0
        self.scoreB = 0
        self.players = {}  # key: client address | value: [clientName, clientTeam(A or B)]

    

    # **********************************************************************************************
    #                                       FUNCTIONS PART
    #
    # **********************************************************************************************
    
    def createUDPSocket(self):
        # UDP
        # serverSocketUDP = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
        self.serverSocketUDP = socket(AF_INET, SOCK_DGRAM)
        self.serverSocketUDP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverSocketUDP.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # Broadcast connection over UDP
        self.serverSocketUDP.bind(("", self.serverPort))

    def createTCPSocket(self):
        if self.serverSocket is not None:
            try:   
                self.serverSocket.close()
            except:
                self.serverSocket = None
        self.serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverSocket.bind(("", self.serverPort))
        self.serverSocket.listen(20)  # 1 - mean how many clients can connect
        acceptThread = threading.Thread(target=self.acceptClients)
        acceptThread.daemon = True
        acceptThread.start()

    def broadcastUDP(self):
        # var = struct.pack('bi', 56, 0x12131415)
        msg = struct.pack('Ibh', 4276993775, 2, 2058)
        timeout = 10
        startTime = time.time()
        while timeout > time.time() - startTime:
            # serverSocketUDP.sendto(msg,('255.255.255.255',13117)) #turn on when client is other host
            self.serverSocketUDP.sendto(msg, ('255.255.255.255', 13115))  # use this line only in debug mode
            print("UDP broadcast inventation sent\n")  # TODO debug
            time.sleep(1)

    def acceptClients(self):
        team = 1
        while True:
            connectionSocketTCP, addr = self.serverSocket.accept()
            self.connectionsList.append(connectionSocketTCP)
            self.addresses.append(addr)
            clientName = connectionSocketTCP.recv(1024).decode()
            self.players[connectionSocketTCP] = [clientName, team]
            if team == 2:
                self.teamBNames.append(clientName)
                team = 1
            else:
                self.teamANames.append(clientName)
                team = 2
            print(clientName)
            print("established connection with", addr)  # TODO debug
            print("addres is : ",addr)
            # connectionSocketTCP.send(instructionsMsg.encode())

    def closePreGameSockets(self):
        # acceptThread.join()
        # self.serverSocket.close()
        self.serverSocketUDP.close()

    def gameOnAnnouncment(self):
        welcomeMSG = "Welcome to Keyboard Spamming Battle Royale.\nGroup A:\n==\n"
        for teamName in self.teamANames:
            welcomeMSG += teamName
        welcomeMSG += "Group B:\n==\n"
        for teamName in self.teamBNames:
            welcomeMSG += teamName
        welcomeMSG += "Start pressing keys on your keyboard as fast as you can!!"
        for TCP_connectionToClient in self.connectionsList:
            TCP_connectionToClient.send(welcomeMSG.encode())

    def summaryGame(self):
        print(self.scoreA)
        print(self.scoreB)
        summaryMSG = "Game over!\nGroup A typed in " + str(self.scoreA) + " characters.\nGroup B typed in " + str(
            self.scoreB) + " characters.\n"
        winningTeam = ""
        if self.scoreA > self.scoreB:
            winningTeam = "A"
            summaryMSG += "Group " + winningTeam + " wins!\n\nCongratulations to the winners:\n==\n"
            # loop over players and get clients names
            for name in self.teamANames:
                summaryMSG += name

        elif self.scoreB > self.scoreA:
            winningTeam = "B"
            summaryMSG += "Group " + winningTeam + " wins!\n\nCongratulations to the winners:\n==\n"
            # loop over players and get clients names
            for name in self.teamBNames:
                summaryMSG += name
        else:
            summaryMSG += "It's a draw!!\n"

        # iterate over all conections and send summaryMSG
        for TCP_connectionToClient in self.connectionsList:
            TCP_connectionToClient.send(summaryMSG.encode())

    # players = {} # key: client address | value: [clientName, clientTeam(A or B)]

    def game(self):
        print("In game mode")
        timeout = 10
        startTime = time.time()
        while timeout > time.time() - startTime:
            for connectionToClient in self.connectionsList:
                connectionToClient.settimeout(0.2)
                try:
                    char, clientAddr = connectionToClient.recvfrom(1024)                    
                    # print("ignore " ,ignore)
                    # if char == "":
                    #     connectionToClient.close()
                    print(char.decode())
                    if self.players[connectionToClient][1] == 1:  # team A
                        self.scoreA += 1
                    else:
                        self.scoreB += 1
                except Exception as e:
                    continue
                

    def clearServerInfo(self):
        # close all TCP sockets
        print("cleaning server info")
        for TCP_connectionToClient in self.connectionsList:
            TCP_connectionToClient.close()
            print("tcp closed ")
        
        # self.serverSocketUDP = None
        # self.serverSocket = None
        self.connectionsList = []
        self.addresses = []
        self.teamANames = []
        self.teamBNames = []
        self.scoreA = 0
        self.scoreB = 0
        self.players = {}


# **********************************************************************************************
#                         SCRIPT PART
#
# **********************************************************************************************


server = Server()
server.createTCPSocket()
while 1:
    try:
        server.createUDPSocket()
        server.broadcastUDP()
        server.closePreGameSockets()
        server.gameOnAnnouncment()
        server.game()
        server.summaryGame()
        print("Game over, sending out offer requests...")
        server.clearServerInfo()
    except Exception as e:
        print(e)
        continue

# server = Server()
# server.createTCPSocket()
# server.createUDPSocket()
# server.broadcastUDP()
# server.closePreGameSockets()
# server.gameOnAnnouncment()
# server.game()
# server.summaryGame()
# print("Game over, sending out offer requests...")
# server.clearServerInfo()




