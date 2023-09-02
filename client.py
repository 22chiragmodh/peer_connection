import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# client side connection 
s.connect((socket.gethostname(),1234))


#  many applications that use sockets will eventually desire to send some amount of bytes far over the buffer size. Instead, we need to probably build our program from the ground up to actually accept the entirety of the messages in chunks of the buffer
while True:
    full_msg=''
    while True:
        msg=s.recv(8)
        if len(msg)<=0:
            break
        full_msg+=msg.decode('utf-8')
    if len(full_msg) > 0:
        print(full_msg)
  

# socket is going to attempt to receive data, in a buffer size of 1024 bytes at a time.
