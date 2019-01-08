import socket

s = socket.socket()
host = socket.gethostbyname('192.168.1.219')
port = 8080
s.bind((host, port))
print("host:",host)
s.listen(1)

while True:
    print("Waiting for connection...")
    c, addr = s.accept()
    print("Receive!!")
    print("c:   ", c)
    print("addr:", addr)
    c.close()
