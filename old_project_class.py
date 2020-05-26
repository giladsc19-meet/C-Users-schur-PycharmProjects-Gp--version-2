from database import *
from select import select
import ssl
from os import system, remove
from socket import create_connection
from tkinter import messagebox, simpledialog, Label, Entry, Button, font as tkfont, scrolledtext as tktext
from tkinter.filedialog import askopenfilename
from tkinter import END, Toplevel, WORD, DISABLED, NORMAL, Menu,  Listbox, ACTIVE, SINGLE
import datetime
from threading import Thread
import constants


# checks that no profile pages will open twice.
OPEN_PROFILE_PAGES = {}


# this class is the different than the others. it's not a frame, but a new window that created on top of the old one.
class Project(Thread):
    def __init__(self, gp_root, user, project):
        super(Project, self).__init__()

        # root of GP and the root of the specific object. for doing Top-level
        self.__gp_root = gp_root
        self.__project_root = None

        # useful objects to match the presented window to a specific user and specific project.
        self.__user = user
        self.__project = project
        self.__client_socket = None

        # objects
        self.__chatText = None
        self.__chatEntry = None
        self.__users_list = None

        self.__presented_directories = []

    # responding to user actions.
    def alert(self, message):
        messagebox.showinfo(EMPTY, message)

    # overrides the function 'run' that exists in the threading package.
    def run(self):
        # creating connection with the server and setting up the ssl.
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # try:
        self.__client_socket = create_connection(('127.0.0.1', 1025))
        self.__client_socket = context.wrap_socket(self.__client_socket, server_hostname='127.0.0.1')
        self.__client_socket.write(self.complete_protocol("1", get_user_name(self.__user), EMPTY).encode())
        self.create_window()
        # except:
        # self.controller.alert("there is a problem with1 the servers.\nplease try connecting again in few minutes.")

    # create a new tkinter window for the project.
    def create_window(self):
        # Toplevel means that if the GP window will be closed the project page will be closed to.
        window = Toplevel(self.__gp_root)
        self.__project_root = window
        window.iconbitmap('GP_logo.ico')
        window.geometry('1200x800')
        window.resizable(width=False, height=False)

        window.title_font = tkfont.Font(family=HELVETICA, size=18, weight=BOLD)
        window.cretiria_font = tkfont.Font(family=FIXEDSYS, size=10)

        self.menuBar()

        self.present_project_directories()

        Label(window, text=get_project_name(self.__project), font=window.title_font).pack()

        self.__chatText = tktext.ScrolledText(master=window, wrap=WORD, state=DISABLED, width=45, height=40)
        self.__chatText.place(x=700, y=50)
        self.__chatEntry = Entry(window, width=60)
        self.__chatEntry.place(x=700, y=720)
        self.__users_list = Listbox(self.__project_root, width=15, height=40, selectmode=SINGLE)
        self.__users_list.place(x=1070, y=50)
        self.users_list()
        self.__users_list.bind('<Double-1>', self.open_profile_pages)
        self.chat_history()
        self.__chatEntry.bind('<Return>', self.send_messages)
        GetMessages(self.__client_socket, self.__chatText, self.__project, self).start()
        self.__project_root.protocol("WM_DELETE_WINDOW", self.close_project_page)

    def menuBar(self):
        menu_bar = Menu(self.__project_root)
        # create a pull-down menu, and add it to the menu bar

        project_menu = Menu(menu_bar, tearoff=0)
        project_menu.add_command(label="project information", command=self.delete_directory)
        project_menu.add_separator()
        if get_user_name(self.__user) == get_project_manager(self.__project):
            project_menu.add_command(label="edit project info", command=self.release_directory)
            project_menu.add_separator()
            project_menu.add_command(label="delete project", command=self.delete_directory)
            project_menu.add_separator()

        menu_bar.add_cascade(label="Project", menu=project_menu)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="add directory", command=self.add_directory)
        file_menu.add_separator()
        if get_user_name(self.__user) == get_project_manager(self.__project):
            file_menu.add_command(label="release directory", command=self.release_directory)
            file_menu.add_separator()
            file_menu.add_command(label="delete directory", command=self.delete_directory)
            file_menu.add_separator()

        menu_bar.add_cascade(label="File", menu=file_menu)

        if get_user_name(self.__user) == get_project_manager(self.__project):
            users_menu = Menu(menu_bar, tearoff=0)
            users_menu.add_command(label="block user", command=self.release_directory)
            users_menu.add_separator()
            users_menu.add_command(label="fire user", command=self.delete_directory)
            users_menu.add_separator()
            menu_bar.add_cascade(label="Manage Users", menu=users_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        help_menu.add_separator()

        menu_bar.add_cascade(label="Help", menu=help_menu)

        # display the menu
        self.__project_root.config(menu=menu_bar)

    # when clicking a name in user list, open a user page.
    def open_profile_pages(self, event):
        profile_user_username = self.__users_list.get(ACTIVE)
        if profile_user_username not in OPEN_PROFILE_PAGES:
            profile_page = Profile(self.__project_root, self.__user, query_user_by_username(profile_user_username))
            OPEN_PROFILE_PAGES[profile_user_username] = profile_page
            profile_page.start()

    # ----------directories functions
    # adding a new directory for the project.
    def add_directory(self):
        directory_name = askopenfilename(parent=self.__project_root, initialdir="/", title="select a directory",
                                   filetypes=(("python files", "*.py"), ("all types", "*.*")))
        if directory_name is not None and directory_name != '':
            directory = open(directory_name, encoding='latin-1')
            if not add_new_directory(get_project_name(self.__project), directory):
                self.alert("invalid directories names:\n" + str(INVALID_DIRECTORIES_NAMES))
            else:
                message = self.complete_protocol("5", get_user_name(self.__user), EMPTY)
                self.__client_socket.write(message.encode())
                self.present_project_directories()
                self.alert("directory added successfully!")
            directory.close()

    def open_directory(self, directory):
        if not get_directory_isopen(directory):
            set_directory_isopen(directory)
            set_directory_lasteditor(directory, get_user_name(self.__user))
            RunDirectory(get_project_name(self.__project), directory).start()
        else:
            self.alert(IS_OPEN)

    def release_directory(self):
        directories = query_project_directories(get_project_name(self.__project))
        project_open_directories = []
        for directory in directories:
            if get_directory_isopen(directory):
                print("ahahahaha")
                project_open_directories.append(get_directory_name(directory))
        print(project_open_directories)
        if not project_open_directories:
            self.alert(NO_OPEN_DIRECTORIES)
        else:
            directories_list = Listbox(self.__project_root, width=15, height=40, selectmode=SINGLE)
            directories_list.pack()
            for i in range(len(project_open_directories)):
                directories_list.insert(i + 1, project_open_directories[i])
                directories_list.bind('<Double-1>', lambda x: self.release_directory_2(directories_list))
            directories_list.insert(i + 1, "non of the above")
            directories_list.bind('<Double-1>', lambda x: self.release_directory_2(directories_list))

    def release_directory_2(self, object):
        directory_name = object.get(ACTIVE)
        object.destroy()
        project_directories = query_project_directories(get_project_name(self.__project))
        for directory in project_directories:
            if get_directory_name(directory) == directory_name:
                set_directory_isopen(directory)
                break

    def delete_directory(self):
        directory_name = simpledialog.askstring(EMPTY, ENTER_DIRECTORY_NAME)
        if not delete_directory(get_project_name(self.__project), directory_name):
            self.alert("no such directory. check you spelled it correctly!")
        else:
            message = self.complete_protocol("7", get_user_name(self.__user), EMPTY)
            self.__client_socket.write(message.encode())
            self.present_project_directories()
            self.alert("directory deleted successfully!")

    def present_project_directories(self):
        directories = query_project_directories(get_project_name(self.__project))
        if self.__presented_directories:
            for d in self.__presented_directories:
                d.destroy()
            self.__presented_directories = []
        # Creating a photoimage object to use image
        # photo = PhotoImage(file=r"C:\Users\schur\PycharmProjects\GP\file.png")
        # Resizing image to fit on button
        # photo_image = photo.subsample(2, 2)
        num = 0
        num_y = 100
        for d in directories:
            # compound- align the image to a side of the button. (((, image=photo_image, compound=TOP,)))
            p = Button(self.__project_root, text=get_directory_name(d),
                       command=lambda directory=d: self.open_directory(directory))
            p.place(x=50 + 200*num, y=num_y)
            self.__presented_directories.append(p)
            num = num + 1
            if num == 3:
                num = 0
                num_y = num_y + 200

    def users_list(self):
        users_names = get_project_users(self.__project).split(INVALID_CHAR1)
        for i in range(len(users_names)):
            self.__users_list.insert(i+1, users_names[i])

    # writing all the chats history in the chatText object.
    def chat_history(self):
        if get_project_messages(self.__project) != EMPTY:
            messages = get_project_messages(self.__project).split(INVALID_CHAR1)
            messages.pop(-1)
            self.__chatText.config(state=NORMAL)
            for i in messages:
                message = self.split_old_message(i)
                self.__chatText.insert(END, message + '\n\n')
                self.__chatText.yview(END)
            self.__chatText.config(state=DISABLED)

    def split_old_message(self, message):
        t = message[0]
        u_len = int(message[1])
        time = message[2:8]
        username = message[8:u_len+8]
        useful_part = message[u_len+8:u_len+10]
        message = message[u_len+10:]
        if not username == get_user_name(self.__user):
            return time + username + useful_part + message
        return time + message

    def send_messages(self, event):
        message = self.__chatEntry.get()
        # --------------------------------------- check why I need it...
        if message == EMPTY:
            pass
        elif not message.find(INVALID_CHAR1) == -1:
            self.alert(TRY_USE_IN_CHAR)
        else:
            self.write_message(self.add_time() + SPACE + message)
            message = self.complete_protocol("2", get_user_name(self.__user), message)
            self.__client_socket.write(message.encode())

    def add_time(self):
        time = datetime.datetime.now()
        hour = str(time.hour)
        if len(hour) == 1:
            hour = "0" + hour
        minute = str(time.minute)
        if len(minute) == 1:
            minute = "0" + minute
        return hour + ":" + minute

    def complete_protocol(self, message_type, username, message):
        project_name = get_project_name(self.__project)
        project_name_len = str(len(project_name))
        while len(project_name_len) != 2:
            project_name_len = "0" + project_name_len
        u_len = str(len(username))
        final_message = message_type + project_name_len + project_name + u_len + self.add_time() + username + message
        return final_message

    def write_message(self, message):
        self.__chatText.config(state=NORMAL)
        self.__chatText.insert(END, message + '\n\n')
        self.__chatText.yview(END)
        self.__chatText.config(state=DISABLED)
        self.__chatEntry.delete(0, 'end')

    def close_project_page(self):
        del constants.OPEN_PROJECTS[get_project_name(self.__project)]
        message = self.complete_protocol("9", get_user_name(self.__user), EMPTY)
        self.__client_socket.write(message.encode())
        self.__client_socket.close()
        self.__project_root.destroy()


class RunDirectory(Thread):
    def __init__(self, project_name, directory):
        super(RunDirectory, self).__init__()

        self.__project_name = project_name
        self.__directory = directory

    # overrides the function 'run' that exists in the threading package.
    def run(self):
        self.open_directory()

    def open_directory(self):
        demo_directory = open(get_directory_name(self.__directory), "w")
        demo_directory.write(get_directory_data(self.__directory).decode('ascii'))
        demo_directory.close()
        demo_directory = open(get_directory_name(self.__directory), "r")
        system("notepad.exe " + get_directory_name(self.__directory))
        if query_certain_project_directory(self.__project_name, get_directory_name(self.__directory)):
            if get_directory_isopen(self.__directory) and get_directory_lasteditor(self.__directory):
                data = demo_directory.read()
                set_directory_data(self.__directory, data)
                set_directory_isopen(self.__directory)
        demo_directory.close()
        remove(get_directory_name(self.__directory))


class Profile(Thread):
    def __init__(self, project_root, user, user_profile):
        super(Profile, self).__init__()

        self.__project_root = project_root
        self.__profile_root = None
        self.__user = user
        self.__user_profile = user_profile

    def run(self):
        self.create_window()

    def create_window(self):
        window = Toplevel(self.__project_root)
        self.__profile_root = window
        window.iconbitmap('GP_logo.ico')
        window.geometry('400x400')
        window.resizable(width=False, height=False)

        window.title_font = tkfont.Font(family=HELVETICA, size=20, weight=BOLD)
        window.cretiria_font = tkfont.Font(family=FIXEDSYS, size=10)

        if self.__user_profile == self.__user:
            Label(window, text="My Profile\n\n", font=window.title_font).pack()
        else:
            Label(window, text=get_user_name(self.__user_profile) + "'s Profile\n\n", font=window.title_font).pack()
        Label(window, text="first name: " + get_user_firstname(self.__user) + "\n", font=window.cretiria_font).pack()
        Label(window, text="last name: " + get_user_lastname(self.__user) + "\n", font=window.cretiria_font).pack()
        Label(window, text="email: " + get_user_email(self.__user) + "\n", font=window.cretiria_font).pack()
        Label(window, text="phone: " + get_user_phone(self.__user) + "\n", font=window.cretiria_font).pack()
        self.__profile_root.protocol("WM_DELETE_WINDOW", self.close_profile_page)

    def close_profile_page(self):
        global OPEN_PROFILE_PAGES
        del OPEN_PROFILE_PAGES[str(get_user_name(self.__user_profile))]
        self.__profile_root.destroy()

