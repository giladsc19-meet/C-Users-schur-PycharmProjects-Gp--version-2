from database import *
from socket import socket
from select import select
from ssl import create_default_context, Purpose

# the 'server.py' directory responsible for getting data from other sockets and send them data in exchange. it
# cooperates with the 'analyze.py' directory that contains all the function that analyze the data.

# a list that contains all the messages that were;nt sent yet.
messages_to_send = []
# lists that record the open clients that exist in chat.
open_client_sockets = []
# from the moment a client logs in with his user, the following list records his socket with his username.
socket_username = []


def new_connection(server_socket, context):
    (new_socket, address) = server_socket.accept()
    new_socket = context.wrap_socket(new_socket, server_side=True)
    open_client_sockets.append(new_socket)


def find_type(data):
    t = data[0:2]
    data = data[2:]
    return types_dictionary[t], data


# sends waiting message to everyone.
def send_waiting_messages(writable):
    for message in messages_to_send:
        (client_socket, data) = message
        for user in writable:
            if user is not client_socket:
                print(data)
                user.write(data.encode())
        messages_to_send.remove(message)


# the 'process_income_messages' responsible for directing each message according to it's content to a specific function
# that will take care of it.
def process_income_messages(readable, context, server_socket):
    for current_socket in readable:
        # the next if checks if the current_socket is a new connection. if yes, it applies it, and append it to the open
        # client socket list so he can contact him later if needed.
        if current_socket is server_socket:
            new_connection(current_socket, context)
        # if the message just arrived belongs to a known socket already, the function starts analyze the data.
        else:
            try:
                data = current_socket.recv(1024).decode()
                if data == EMPTY:
                    pass
                else:
                    function_name, data = find_type(data)
                    answer, message = eval(function_name)(data)
            except:
                pass


# the main function creates the server socket and makes him listen in th port of '1025' to check if a client wants to
# connect to him.
def main():
    # adding an ssl layer that encode the messages passing from the clients to the server, and from the server to the
    # client.
    context = create_default_context(Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT)
    # creating the server socket.
    server_socket = socket()
    server_socket.bind((EMPTY, 1025))
    server_socket.listen(5)
    # receiving an sending messages.
    connected = True
    while connected:
        readable, writable, exceptional = select([server_socket] + open_client_sockets, open_client_sockets, [])
        process_income_messages(readable, context, server_socket)
        send_waiting_messages(writable)


if __name__ == '__main__':
    main()
