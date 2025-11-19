import socket

localHost = "192.168.1.4"
localPort   = 20001
bufferSize  = 1024
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

def init():
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    UDPServerSocket.bind((localHost, localPort))

    print("UDP server up and listening")

    while True:
        msgFromClient = UDPServerSocket.recvfrom(bufferSize)
        
        message = msgFromClient[0]
        address = msgFromClient[1]
        
        print("Message from Client: {}".format(message))
        print("Client IP Address: {}".format(address) + "\n")
        
        UDPServerSocket.sendto(bytesToSend, address)
        
#init()