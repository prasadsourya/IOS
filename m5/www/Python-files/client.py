import socket
s = socket.socket()
port = 7000
s.connect(('', port))
s.send(("Hello ").encode())
print (s.recv(1024).decode())
s.close()
