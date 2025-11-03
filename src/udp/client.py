import socket

serverAddressPort = ("192.168.1.4", 20001)
bufferSize = 1024
msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)

def init():
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    
    message = msgFromServer[0]
    address = msgFromServer[1]
    
    print("Message from Server: {}".format(message))
    print("Server IP Address: {}".format(address))
    
    UDPClientSocket.close()
    
init()