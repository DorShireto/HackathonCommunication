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
        self.broadcastADDR = '255.255.255.255'
        self.broadcastPort = 13117
        self.serverName = "DeaD_l0ck_Av0iders\n"
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
        # UDP - set up connection as SOCK_DGRAM, SO_REUSEADDR and SO_BROADCAST
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
		# TCP - set up connection as SOCK_STREAM, SO_REUSEADDR
        self.serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverSocket.bind(("", self.serverPort))
        self.serverSocket.listen(20)  #mean how many clients can connect
        acceptThread = threading.Thread(target=self.acceptClients) #start acceptClients on diffrent thread
        acceptThread.daemon = True # allows the thread to not block other program, when the main program will die the thread will die to (if program died unexpectedly)
        acceptThread.start()


    def broadcastUDP(self):
		#broadcast UDP message to all listenrs -runs for 10 seconds each call
		#message struct is: 4276993775 - Megic cookie, 2 - offer, 2058 - Server port
		#message formt - Ibh: I(4 bytes) - unsigned int, b(1 byte) - singed char, h(2 bytes) - short
        msg = struct.pack('Ibh', 4276993775, 2, 2058)
        timeout = 10
        startTime = time.time()
        while timeout > time.time() - startTime: #run for 10 seconds - send broadcast every 1 second
            # serverSocketUDP.sendto(msg,(self.broadcastADDR,self.broadcastPort)) #turn on when client is other host
            self.serverSocketUDP.sendto(msg, (self.broadcastADDR, 13115))  # use this line only in debug mode
            time.sleep(1)

    def acceptClients(self):
        team = 1
        while True: #method will die onces acceptClients thread will die
            connectionSocketTCP, addr = self.serverSocket.accept()
            self.connectionsList.append(connectionSocketTCP) # add new client conection to connectionsList
            self.addresses.append(addr) # andd new client to address list
            clientName = connectionSocketTCP.recv(1024).decode()
            self.players[connectionSocketTCP] = [clientName, team] # add new client to players dict, key: socket, value: list[ clientName, team clients plays for]
            if team == 2:
                self.teamBNames.append(clientName) #add client name to team B clients name list
                team = 1
            else:
                self.teamANames.append(clientName) #add client name to team A clients name list
                team = 2

    def closePreGameSockets(self):
        self.serverSocketUDP.close()

    def gameOnAnnouncment(self):
		#build welcome message part:
        welcomeMSG = "Welcome to Keyboard Spamming Battle Royale.\nGroup A:\n==\n"
        for teamName in self.teamANames:
            welcomeMSG += teamName
        welcomeMSG += "Group B:\n==\n"
        for teamName in self.teamBNames:
            welcomeMSG += teamName
        welcomeMSG += "Start pressing keys on your keyboard as fast as you can!!"
		#end of welcome message
		#send welcomeMSG to all connected clients
        for TCP_connectionToClient in self.connectionsList:
            TCP_connectionToClient.send(welcomeMSG.encode())

    def summaryGame(self):
		#build summary message part:
        summaryMSG = "Game over!\nGroup A typed in " + str(self.scoreA) + " characters.\nGroup B typed in " + str(
            self.scoreB) + " characters.\n"
        winningTeam = ""
        if self.scoreA > self.scoreB: #team A wins
            winningTeam = "A"
            summaryMSG += "Group " + winningTeam + " wins!\n\nCongratulations to the winners:\n==\n"
            # loop over players and get clients names
            for name in self.teamANames: #add team A clients names to summary message
                summaryMSG += name

        elif self.scoreB > self.scoreA: #team B wins
            winningTeam = "B"
            summaryMSG += "Group " + winningTeam + " wins!\n\nCongratulations to the winners:\n==\n"
            # loop over players and get clients names
            for name in self.teamBNames: #add team B clients names to summary message
                summaryMSG += name
        else: #draw
            summaryMSG += "It's a draw!!\n"

        # iterate over all conections and send summaryMSG
        for TCP_connectionToClient in self.connectionsList:
            TCP_connectionToClient.send(summaryMSG.encode())

    def game(self):
		#game main method, runs for 10 second
        print("In game mode")
        timeout = 10
        startTime = time.time()
        while timeout > time.time() - startTime:
            for connectionToClient in self.connectionsList:
                connectionToClient.settimeout(0.2)
                try:
                    char, clientAddr = connectionToClient.recvfrom(1024) #get char from client                    
                    if self.players[connectionToClient][1] == 1:  # player belong to team A
                        self.scoreA += 1
                    else: # player belond go team B
                        self.scoreB += 1
                except Exception as e: #player didn't press any key for 0.2 seconds
                    continue
                

    def clearServerInfo(self):
        # close all TCP sockets
        for TCP_connectionToClient in self.connectionsList: #close all clients sockets
            TCP_connectionToClient.close()
		#reset all class atributes
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
serverAddr = "172.18.0.58"
while 1: #Server machine will keep on running until forced to stop
    print("Server started, listening on IP address: ", serverAddr)
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
