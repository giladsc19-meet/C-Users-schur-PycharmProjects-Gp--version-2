from socket import socket
from select import select
from database import *
from constants import *
import ssl

# split the data the server received according to the protocol parts.
def split_data(data):
    if data == EMPTY:
        return
    t = data[0]
    project_len = int(data[1:3])
    project_name = data[3:project_len+3]
    u_len = int(data[project_len+3])
    time = data[project_len+4:project_len+9]
    username = data[project_len+9:project_len+u_len+9]
    content = data[project_len+u_len+9:]
    project_len = str(project_len)
    while len(project_len) != 2:
        project_len = "0" + project_len
    print(t + "\n" + project_len + "\n" + project_name + "\n" + time + "\n" + username + "\n" + content)
    return t, project_len, project_name, time, username, content


# sends waiting message to everyone.
def send_waiting_messages(writable):
    for message in messages_to_send:
        (client_socket, data) = message
        for user in writable:
            if user is not client_socket:
                print(data)
                user.write(data.encode())
        messages_to_send.remove(message)


# adds a new socket that connected or getting the new data and do what it says.
def process_income_messages(readable, context, server_socket):
    for current_socket in readable:
        if current_socket is server_socket:
            (new_socket, address) = current_socket.accept()
            new_socket = context.wrap_socket(new_socket, server_side=True)
            open_client_sockets.append(new_socket)
            print("new user")
        else:
            try:
                data = current_socket.recv(1024).decode()
                if data == EMPTY:
                    pass
                else:
                    t, project_len, project_name, time, username, content = split_data(data)
                    act_according_type(current_socket, project_len, project_name, time, username, t, content)
            except:
                pass


# global lists for messages. lists that record the open clients that exist in chat.
messages_to_send = []
open_client_sockets = []
socket_username = []


# checks the type of the info got from the client and send it to it's matched function.
# the function send the message when it's only need to have the length.
def act_according_type(sending_socket, project_len, project_name, time, username, t, content):
    # a user open his project and created a new connection with the server.
    if t == "1":
        socket_username.append(username)
        message = t + project_len + project_name + time + SPACE + username + ":" + SPACE + content
        messages_to_send.append((sending_socket, message))
    # a user sent a message for all the other users in the project.
    if t == "2":
        message = t + project_len + project_name + time + SPACE + username + ":" + SPACE + content
        # saving the new message to database.
        save_message_to_project_chat(query_project_by_name(project_name), username, message)
        messages_to_send.append((sending_socket, message))
    # in future, will support private message.
    if t == "4":
        pass
    # adding a directory to the projects database.
    if t == "5":
        message = t + project_len + project_name + time + SPACE + username + ":" + SPACE + content
        messages_to_send.append((sending_socket, message))
    # changing a directory state from open to closed.
    if t == "6":
        pass
    # deleting a directory from the project database.
    if t == "7":
        message = t + project_len + project_name + time + SPACE + username + ":" + SPACE + content
        messages_to_send.append((sending_socket, message))
    # a user closed the project page, and want to close the connection.
    if t == "9":
        i = socket_username.index(username)
        socket_username.pop(i)
        open_client_sockets.pop(i)


# runs the server.
def main():
    # adding ssl.
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT)
    # creating a server socket.
    server_socket = socket()
    server_socket.bind(('', 1025))
    server_socket.listen(5)
    # receiving an sending messages.
    connected = True
    while connected:
        readable, writable, exceptional = select([server_socket] + open_client_sockets, open_client_sockets, [])
        process_income_messages(readable, context, server_socket)
        send_waiting_messages(writable)


if __name__ == '__main__':
    main()
