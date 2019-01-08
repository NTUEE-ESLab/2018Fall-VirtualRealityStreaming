import socket
from socket import AF_INET, SOCK_DGRAM

serverIP = '192.168.1.219'
port = 8080
mySocket = socket.socket()
mySocket.connect((serverIP, port))
mySocket.send(b'789456')
mySocket.close()