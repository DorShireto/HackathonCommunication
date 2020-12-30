from socket import *
import struct
import threading
import time

#**********************************************************************************************
#                                          ATRIBUTES
#
#**********************************************************************************************

serverPort = 2058
serverName = "DeaD_l0ck_Av0idErs"
connectionsList = []
addresses=[]
teamANames = []
teamBNames = []
scoreA = 0
scoreB = 0
players = {} # key: client address | value: [clientName, clientTeam(A or B)]
# instructionsMsg = "************************************************\n " \
#                   "Hello Player!!!\n" \
#                   "Welcome to "+serverName+" server.\n" \
#                   " game will start in 10 seconds.\n" \
#                   " Your goal is to type as much charecters as you can within 10 seconds\n" \
#                   "Now wait for starting announcement\n" \
#                   "************************************************"


#**********************************************************************************************
#                                       FUNCTIONS PART
#
#**********************************************************************************************
def acceptClients():
    while True:
        connectionSocketTCP, addr = serverSocket.accept()
        connectionsList.append(connectionSocketTCP)
        addresses.append(addr)
        clientName = connectionSocketTCP.recv(1024)
        print(clientName.decode())
        print("established connection with",addr)
        # connectionSocketTCP.send(instructionsMsg.encode())


def createUDPSocket():
    # UDP
    # serverSocketUDP = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
    serverSocketUDP = socket(AF_INET, SOCK_DGRAM)
    serverSocketUDP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocketUDP.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # Broadcast connection over UDP
    serverSocketUDP.bind(("", serverPort))

def createTCPSocket():
    serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    serverSocket.bind(("", serverPort))
    serverSocket.listen()  # 1 - mean how many clients can connect
    acceptThread = threading.Thread(target=acceptClients)
    acceptThread.daemon = True
    acceptThread.start()

def broadcastUDP():
    # var = struct.pack('bi', 56, 0x12131415)
    msg = struct.pack('Ibh', 4276993775, 2, 2058)
    timeout = 10
    startTime = time.time()
    while timeout > time.time() - startTime :
        # serverSocketUDP.sendto(msg,('255.255.255.255',13117)) #turn on when client is other host
        serverSocketUDP.sendto(msg, ('255.255.255.255', 13115))  # use this line only in debug mode
        print("UDP broadcast inventation sent\n") #TODO debug


def acceptClients():
    while True:
        team = 1
        connectionSocketTCP, addr = serverSocket.accept()
        connectionsList.append(connectionSocketTCP)
        addresses.append(addr)
        clientName = connectionSocketTCP.recv(1024)
        players[addr] = [clientName,team]
        if team == 2:
            teamBNames.append(clientName)
            team = 1
        else:
            teamANames.append(clientName)
            team = 2
        print(clientName.decode())
        print("established connection with",addr) #TODO debug
        connectionSocketTCP.send(instructionsMsg.encode())

def closePreGameSockets():
    # acceptThread.join()
    serverSocket.close()
    serverSocketUDP.close()


def gameOnAnnouncment():
    welcomeMSG = "Welcome to Keyboard Spamming Battle Royale.\nGroup A:\n==\n"
    for teamName in teamANames:
        welcomeMSG+=teamName
    welcomeMSG+="Group B:\n==\n"
    for teamName in teamBNames:
        welcomeMSG+=teamName
    welcomeMSG += "Start pressing keys on your keyboard as fast as you can!!"
    for TCP_connectionToClient in connectionsList:
        TCP_connectionToClient.send(welcomeMSG.encode())

def summaryGame():
    summaryMSG = "Game over!\n Group A typed in " + scoreA + " characters.\n Group B typed in " + scoreB + " characters.\n"
    winningTeam = ""
    if scoreA > scoreB:
        winningTeam = "A"
        summaryMSG += "Group "+ winningTeam + " wins!\n\nCongratulations to the winners:\n==\n"
        #loop over players and get clients names
        for name in teamANames:
            summaryMSG+=name

    elif scoreB > scoreA:
        winningTeam = "B"
        summaryMSG += "Group "+ winningTeam + " wins!\n\nCongratulations to the winners:\n==\n"
        #loop over players and get clients names
        for name in teamBNames:
            summaryMSG+=name
    else:
        summaryMSG += "It's a draw!!\n"

    #iterate over all conections and send summaryMSG
    for TCP_connectionToClient in connectionsList:
        TCP_connectionToClient.send(summaryMSG.encode())





# players = {} # key: client address | value: [clientName, clientTeam(A or B)]

def game():
    timeout = 10
    startTime = time.time()
    while timeout > time.time() - startTime :
        for connectionToClient in connectionsList:
            connectionToClient.settimeout(0.1)
            try:
                char, clientAddr = connectionToClient.recvfrom(1)
                if players[clientAddr][1] == 1: #team A
                    scoreA += 1
                else:
                    scoreB += 1
                # print("ignore " ,ignore)
                # if char == "":
                #     connectionToClient.close()
                print(char.decode())
            except Exception as e:
                continue

def clearServerInfo():
    #close all TCP sockets
    for TCP_connectionToClient in connectionsList:
        TCP_connectionToClient.close()
    connectionsList = []
    addresses=[]
    teamANames = []
    teamBNames = []
    scoreA = 0
    scoreB = 0
    players = {}


#**********************************************************************************************
#                         SCRIPT PART
#
#**********************************************************************************************


while 1:
    createTCPSocket()
    createUDPSocket()
    broadcastUDP()
    closePreGameSockets()
    gameOnAnnouncment()
    game()
    summaryGame()
    print("Game over, sending out offer requests...")



    
