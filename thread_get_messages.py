from threading import Thread
from select import select


USER = None

class GetMessages(Thread):
    def __init__(self, client_socket, chatText, project, object):
        super(GetMessages, self).__init__()
        self.daemon = True

        self.__chatText = chatText
        self.__client_socket = client_socket
        self.__project = project
        self.__object = object

    # overrides the function 'run' that exists in the threading package.
    def run(self):
        self.get_messages()

    # gets messages that other clients sent trough the server
    def get_messages(self):
        while True:
            try:
                readable, writable, exceptional = select([self.__client_socket], [], [], 0.0001)
                if self.__client_socket in readable:
                    data = self.__client_socket.recv(1024).decode()
                    if data[0:2] == '09':
                        pass
            except:
                break

    def check_split(self, data):
        t = int(data[0])
        project_len = int(data[1:3])
        project_name = data[3:project_len+3]
        message = data[project_len+3:]
        return t, project_name, message

    def write_message(self, message):
        self.__chatText.config(state=NORMAL)
        self.__chatText.insert(END, message + '\n\n')
        self.__chatText.yview(END)
        self.__chatText.config(state=DISABLED)

    def directories_changes(self):
        self.__object.present_project_directories()
