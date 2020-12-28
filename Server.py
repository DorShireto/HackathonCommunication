from socket import *
serverPort = 2058

#UDP
#serverSocketUDP = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
#serverSocketUDP.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) # Broadcast connection over UDP




# TCP
serverSocketTCP = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
serverSocketTCP.bind(("",serverPort))
serverSocketTCP.listen() # 1 - mean how many clients can connect
connectionSocketTCP, addr = serverSocketTCP.accept()





while True:
    char = connectionSocketTCP.recv(1024)
    if char == "":
        connectionSocketTCP.close()
    print(char.decode())





#def sendBroadcastInvite():
    