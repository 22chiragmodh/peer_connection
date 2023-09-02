import socket

# socket take to parameter i)  AF_INET = ipv4  ii) SOCK_STREAM == tcp type of socket -> conn..ections orientaed

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The socket itself is just one of the endpoints in a communication between programs on some network.

#  socket is generally endpoint. two endponts to have communications to send and recieve data.

s.bind((socket.gethostname(), 1234))

# In the case of the server, you will bind a socket to some port on the server (localhost). In the case of a client, you will connect a socket to that server, on the same port that the server-side code is using.
s.listen(5)

while True:
    clientsocket, address=s.accept()
    print(f"connection from {address} is established")
    clientsocket.send(bytes("Hey there!!! Chirag modh","utf-8"))
    clientsocket.close()