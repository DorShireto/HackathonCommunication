from socket import *
import struct
import threading
import time
#### ATR ###
serverPort = 2058
connections=[]
addresses=[]

def acceptClients():
    while True:
        connectionSocketTCP, addr = serverSocketDoor.accept()
        connections.append(connectionSocketTCP)
        addresses.append(addr)
        print("established connection with",addr)


# TCP
serverSocketDoor = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
serverSocketDoor.bind(("",serverPort))
serverSocketDoor.listen() # 1 - mean how many clients can connect
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
msg = struct.pack('Ibh',4276993775,2,2058)
# msg = b"YOUVE BEEN HACKED BY US. YOUR CODE WILL BE DELETED IN 3 Minutes"
while 1:
    # serverSocketUDP.sendto(msg,('255.255.255.255',13117)) #turn on when client is other host
    serverSocketUDP.sendto(msg,('255.255.255.255',13117)) # use this line only in debug mode
    print("UDP broadcast inventation sent\n")
    # time.sleep(1)




while True:
    for connectionToClient in connections:
        char = connectionToClient.recv(1024)
        if char == "":
            connectionToClient.close()
        print(char.decode())




#def sendBroadcastInvite():
    
