from socket import *
import struct
import threading
import time
#### ATRIBUTES ###

def acceptClients():
    while True:
        connectionSocketTCP, addr = serverSocket.accept()
        connectionsList.append(connectionSocketTCP)
        addresses.append(addr)
        print("established connection with",addr)
        connectionSocketTCP.send(instructionsMsg.encode())


serverPort = 2058
serverName = "DeaD_l0ck_Av0idErs"
connectionsList = []
addresses=[]
instructionsMsg = "************************************************\n " \
                  "Hello Player!!!\n" \
                  "Welcome to "+serverName+" server.\n" \
                  " game will start in 10 seconds.\n" \
                  " Your goal is to type as much charecters as you can within 10 seconds\n" \
                  "Now wait for starting announcement\n" \
                  "************************************************"

# TCP
serverSocket = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
serverSocket.bind(("",serverPort))
serverSocket.listen() # 1 - mean how many clients can connect
acceptThread = threading.Thread(target=acceptClients)
acceptThread.daemon=True
acceptThread.start()


#UDP
# serverSocketUDP = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
serverSocketUDP = socket(AF_INET,SOCK_DGRAM)
serverSocketUDP.setsockopt(SOL_SOCKET, SO_REUSEADDR ,1)
serverSocketUDP.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) # Broadcast connection over UDP
serverSocketUDP.bind(("",serverPort))
#serverSocketUDP.settimeout(10)#close the socket after 10 sec
print("Server started, listening on IP address 132.72.200.153")
# var = struct.pack('bi', 56, 0x12131415)
msg = struct.pack('Ibh',4276993775,2,2058)
cnt=0
while cnt<10:
    # serverSocketUDP.sendto(msg,('255.255.255.255',13117)) #turn on when client is other host
    serverSocketUDP.sendto(msg,('255.255.255.255',13117)) # use this line only in debug mode
    print("UDP broadcast inventation sent\n")
    time.sleep(1)
    cnt+=1


for TCP_connectionToClient in connectionsList:

    TCP_connectionToClient.send(b'GAME ON !!!!!!!!\nSTART SPAMMING !!!!!!!')




while True:
    for connectionToClient in connectionsList:
        ignore = connectionToClient.recv(1024)
        print("ignore " ,ignore)
        if char == "":
            connectionToClient.close()
        print(char.decode())




#def sendBroadcastInvite():
    
