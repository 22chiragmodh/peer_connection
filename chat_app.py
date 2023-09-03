import socket
import select
import errno
import threading


HEADER_LENGTH =10

PORT=1234

IP='127.0.0.1'

my_username=input("Enter your username: ")


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP,PORT))

# client_socket.setblocking(False)

username = my_username.encode('utf-8')

username_header=f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

client_socket.send(username_header+username)


def multiThreadingOn(client_socket):
    while True:
            try:
                 username_header=client_socket.recv(HEADER_LENGTH)
                 if not len(username_header):
                     print("closed connection server")
                     sys.exit()

                 username_length=int(username_header.decode('utf-8').strip())
                 username=client_socket.recv(username_length).decode('utf-8').strip()

                 msg_header=client_socket.recvhe(HEADER_LENGTH)
                 msg_length=int(msg_header.decode('utf-8').strip())
                 msg=client_socket.recv(msg_length).decode('utf-8').strip()


            # Print message
                 print(f'{username} > {msg}')
                 
            
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno!=errno.EWOULDBLOCK:
                   print('Reading error: {}'.format(str(e)))
                   sys.exit()
       

                   continue


            except Exception as e:
                print('Reading error'.format(str(e)))
                sys.exit()



threading.Thread(target=multiThreadingOn,args=(client_socket,)).start()
def sendMessage(msg):
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        
        msg=msg.encode('utf-8')
        msg_header=f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(msg_header+msg)

while True:
    # user msg
    msg=input(f'{my_username}>')
    if msg:
         sendMessage(msg)

         

  

   
       

  



    

        


        

