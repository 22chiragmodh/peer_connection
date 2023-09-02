# First, the server needs to accept new connections from clients. 
# we need to come up with some way to identify our unique users. We could display users by IP address


#  handle connections from server side


import socket
import select

# The select module gives us OS-level monitoring operations for things, including for sockets.
# It is especially useful in cases where we're attempting to monitor many connections simultaneously
HEADER_LENGTH=10

IP="127.0.0.1"

PORT=1234


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

# we'll create a list of sockets for select to keep track of, as well as begin our clients dict:

sockets_list = [server_socket]

# clein socket will be key and user data will be vale

clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving
def receive_message(client_socket):
    try:
        msg_header=client_socket.recv(HEADER_LENGTH)
        # if we didn't receive any data close the connection
        if not len(msg_header):
            return False
        
        # we can convert our header to a length:
        msg_length=int(msg_header.decode('utf-8').strip())
        return {"header":msg_header,"data":client_socket.recv(msg_length)}


    except:

        # Something went wrong like empty message or client exited abruptly.
        return False
    

#  receive messages for all of our client sockets, then send all of the messages out to all of the client sockets.
while True:
     read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

     for notified_socket in read_sockets:
            # smeone connect to server
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                user = receive_message(client_socket)
                if user is False:
                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user
                print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                # If the notified socket is not a server socket, then this means instead we've got a message to read:
            else:
                message = receive_message(notified_socket)
                if message is False:
                    print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                    sockets_list.remove(notified_socket)

                # Remove from our list of users
                    del clients[notified_socket]

                    continue

                user = clients[notified_socket]

                print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

                for client_socket in clients:
    
                # But don't sent it to sender
                    if client_socket != notified_socket:

                    # Send user and message (both with their headers)
                    # We are reusing here message header sent by sender, and saved username header send by user when he connected
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        

            # It's not really necessary to have this, but will handle some socket exceptions just in case
     for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]