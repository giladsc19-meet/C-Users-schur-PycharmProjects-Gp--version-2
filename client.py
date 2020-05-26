# for the constants that replace strings.
from constants import *
# for the tkinter gui
from tkinter import Tk, Frame, messagebox, simpledialog, Label, Entry, Button, StringVar, BOTH, PhotoImage, Text,\
    Scrollbar, RIGHT, Y
from tkinter import font as tkfont
# for the communication with the server.
import ssl
from socket import create_connection
from random import choices
from string import ascii_letters, digits
import datetime
from time import sleep
from threading import Thread
from old_project_class import Project
import re


# ------- global vars -------
# saves the client socket so all classes will be able contacting the server.
CLIENT_SOCKET = EMPTY
# keeping the user object available from the moment he's logged.
USER = EMPTY

# does the user clicked already the my_projects button?
MY_PROJECTS_BUTTON = False
MY_PROJECTS_BUTTONS_LIST = []
# does the user clicked already the projects button?
JOIN_PROJECTS_BUTTON = False
JOIN_PROJECTS_BUTTONS_LIST = []


# application class to create all the frames.
class GP(Tk):
    # kwargs and args are fluid what means you can put how many variables as you want in the init and from all types.
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # defining font types before creating the frames.
        self.title_font = tkfont.Font(family=HELVETICA, size=30, weight=BOLD)
        self.normal_font = tkfont.Font(family=FIXEDSYS, size=16)

        # the container is where we'll stack a bunch of frames on top of each other, then the one we want visible will
        # be raised above the others.
        container = Frame(self)
        # makes the container to spread on all over the window even if it's resized. don't know what the fields do.
        container.pack(side=TOP, fill=BOTH, expand=True)
        # if there's a space, it will be filled by the container.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # dictionary that contains all the frames
        self.frames = {}
        # creating all the frames, and write them to the dictionary.
        for F in (LogoScreen, StartScreen, SignupScreen, LoginScreen, HomeScreen, EditProfileScreen,
                  CreateProjectScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location; the one on the top of the stacking order will be the one that
            # is visible.
            frame.grid(row=0, column=0, sticky=NSEW)
        UpdateHomePage(self.frames[HOME_SCREEN]).start()
        self.show_frame(LOGO_SCREEN)

    # switches the frame the user sees, by raise it upon the others.
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        # if its first time the user visits the home page it'll print his name and the date in HomePage frame.
        if page_name == HOME_SCREEN:
            self.frames[HOME_SCREEN].change_user_and_date()
            self.frames[HOME_SCREEN].join_projects_button()
            self.frames[HOME_SCREEN].my_Projects_button()
        frame.tkraise()

    # responding to user actions.
    def alert(self, message):
        messagebox.showinfo(EMPTY, message)
        return message

    # opening a new Tk window to the chosen project.
    def openProject(self, project_name):
        project_object = query_project_by_name(project_name)
        print(project_object)
        if project_name not in OPEN_PROJECTS:
            project = Project(self, USER, project_object)
            OPEN_PROJECTS[project_name] = project
            project.start()

    def send_server(self, data):
        CLIENT_SOCKET.write(data.encode())


# the LogoPage is the first screen the user sees when opening the program. it contains athe GP logo and a button
# underneath that by clicking it the user creates a connection with the server
class LogoScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # self.controller is the GP frame root, that can be used to activate the functions defined in it's class in the
        # different classes that inherit it.
        self.controller = controller
        self.configure(bg=BLACK)

        # defining the logo image and placing it on the logo screen.
        logo = PhotoImage(file="GP_logo.gif")
        img = Label(self, image=logo, bg=BLACK)
        img.image = logo
        img.place(x=150, y=100)

        Label(text="programmed by Gilad Schurr").place(x=290, y=650)

        # create button
        button = Button(self, text="click here to continue", borderwidth=NO_BORDER, fg=WHITE, bg=BLACK,
                        command=lambda: self.create_connection())
        button_font = tkfont.Font(size=20)
        button['font'] = button_font
        button.place(x=250, y=680)

    def create_connection(self):
        global CLIENT_SOCKET
        # creating connection with the server and setting up the ssl.
        try:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            CLIENT_SOCKET = create_connection((CLIENT_IP, 1025))
            CLIENT_SOCKET = context.wrap_socket(CLIENT_SOCKET, server_hostname=CLIENT_IP)
            self.controller.show_frame(START_SCREEN)
        except ConnectionRefusedError:
            self.controller.alert(CONNECTING_SERVER_PROBLEM)


class StartScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # self.controller is the GP frame root, that can be used to activate the functions defined in it's class in the
        # different classes that inherit it.
        self.controller = controller
        self.configure(bg=BLACK)

        title_font = tkfont.Font(family='Bauhaus 93', size=40, weight=BOLD)
        normal_font = tkfont.Font(family=FIXEDSYS, size=18)

        Label(self, text="Welcome to GP - Group Projects", font=title_font, fg=RED, bg=BLACK).pack()

        Label(self, text="if you don't have a user, please signup.", font=normal_font, fg=RED, bg=BLACK)\
            .place(x=100, y=150)
        Button(self, text="Signup", padx=40, pady=5, bg=INDIAN_RED,
               command=lambda: controller.show_frame(SIGNUP_SCREEN)).place(x=350, y=250)
        Label(self, text="already have a user? login.", font=normal_font, fg=RED, bg=BLACK)\
            .place(x=190, y=400)
        Button(self, text="Login", padx=46, pady=5, bg=INDIAN_RED,
               command=lambda: controller.show_frame(LOGIN_SCREEN)).place(x=350, y=500)


class SignupScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=BLACK)

        Label(self, text="Sign Up", font=controller.title_font, fg=RED, bg=BLACK).place(x=350, y=0)

        # defining vars for creating a new user.
        first_name = StringVar()
        last_name = StringVar()
        email = StringVar()
        phone = StringVar()
        username = StringVar()
        password = StringVar()

        # fields to fill with info for signing up.
        Label(self, text="first name", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=90)
        Entry(self, textvariable=first_name, validate=VALIDATE_METHOD,
              validatecommand=(self.register(self.signup_entry_validation), VALIDATE_COMMAND_TYPE, first_name, 20),
              width=50).place(x=310, y=100)
        Label(self, text="last name", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=190)
        Entry(self, textvariable=last_name, validate=VALIDATE_METHOD,
              validatecommand=(self.register(self.signup_entry_validation), VALIDATE_COMMAND_TYPE, last_name, 20),
              width=50).place(x=310, y=200)
        Label(self, text="email", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=290)
        Entry(self, textvariable=email, validate=VALIDATE_METHOD,
              validatecommand=(self.register(self.signup_entry_validation), VALIDATE_COMMAND_TYPE, email, 30),
              width=50).place(x=310, y=300)
        Label(self, text="phone", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=390)
        Entry(self, textvariable=phone, validate=VALIDATE_METHOD,
              validatecommand=(self.register(self.signup_entry_validation), VALIDATE_COMMAND_TYPE, phone, 10),
              width=50).place(x=310, y=400)
        Label(self, text="username", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=490)
        Entry(self, textvariable=username, validate=VALIDATE_METHOD,
              validatecommand=(self.register(self.signup_entry_validation), VALIDATE_COMMAND_TYPE, username, 16),
              width=50).place(x=310, y=500)
        Label(self, text="password", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=590)
        Entry(self, textvariable=password, validate=VALIDATE_METHOD,
              validatecommand=(self.register(self.signup_entry_validation), VALIDATE_COMMAND_TYPE, password, 16),
              width=50).place(x=310, y=600)
        Button(self, text="Back", padx=18, pady=7, bg=INDIAN_RED, command=lambda: controller.show_frame(START_SCREEN))\
            .place(x=280, y=700)
        Button(self, text="sign up", padx=10, pady=7, bg=INDIAN_RED, command=lambda: self.signup_button(
            first_name.get(), last_name.get(), email.get(), phone.get(), username.get(), password.get()))\
            .place(x=430, y=700)

    # prevent the user from using spaces and '~' in the signup form.
    def signup_entry_validation(self, char, string_var, length):
        try:
            if char == SPACE or char == DB_SEPARATOR or len(string_var.get()) > length:
                return False
            return True
        except:
            return False

    # sign in, by passing all the info that the user gave to a function in the database.
    def signup_button(self, first_name, last_name, email, phone, username, password):
        global USER
        if not re.search(REGEX_EMAIL, email):
            self.controller.alert(SIGNUP_INVALID_EMAIL)
        if not len(phone) == 10 and not phone.isdecimal():
            self.controller.alert(SIGNUP_INVALID_PHONE)
        elif not len(username) < 6:
            self.controller.alert(SIGNUP_INVALID_USERNAME)
        elif not len(password) < 6:
            self.controller.alert(SIGNUP_INVALID_PASSWORD)
        elif first_name == EMPTY or last_name == EMPTY or email == EMPTY:
            self.controller.alert(SIGNUP_NOT_FILLED)
        else:
            message = "01" + first_name + SPACE + last_name + SPACE + email + SPACE + phone + SPACE + username +\
                      SPACE + password
            self.controller.send_server(message)
            # saving the user object in a global variable for later uses.
            USER = query_user_by_username(username)
            self.controller.show_frame(HOME_SCREEN)


class LoginScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=BLACK)


        Label(self, text="Log in", font=controller.title_font, fg=RED, bg=BLACK).pack(side="top", fill="x", pady=10)

        # defining vars for logging in with an existing user.
        username = StringVar()
        password = StringVar()

        # fields to fill with info for login in and positioning of those fields.
        Label(self, text="username", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=170)
        Entry(self, textvariable=username, validate=VALIDATE_METHOD,
              validatecommand=(self.register(self.login_entry_validation), VALIDATE_COMMAND_TYPE, username, 16),
              width=50).place(x=310, y=170)

        Label(self, text="password", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=270)
        Entry(self, textvariable=password, validate=VALIDATE_METHOD,
              validatecommand=(self.register(self.login_entry_validation), VALIDATE_COMMAND_TYPE, password, 16),
              width=50).place(x=310, y=270)

        Button(self, text="Back", padx=18, pady=7, bg=INDIAN_RED, command=lambda: controller.show_frame(StartScreen))\
            .place(x=280, y=400)
        Button(self, text="log in", padx=12, pady=7, bg=INDIAN_RED, command=lambda: self.login_button(
            username.get(), password.get())).place(x=430, y=400)

    # prevent the user from using spaces and '~' in the login form.
    def login_entry_validation(self, char, string_var, length):
        try:
            if char == SPACE or char == DB_SEPARATOR or len(string_var.get()) > length:
                return False
            return True
        except:
            return False

    # kog in, by passing all the info that the user gave to a function in the database.
    def login_button(self, username, password):
        global USER
        if username == EMPTY or password == EMPTY:
            self.controller.alert(LOGIN_NOT_FILLED)
        message = "02" + username + SPACE + password
        self.controller.send_server(message)
        # saving the user object in a global variable for later uses.
        USER = query_user_by_username(username)
        self.controller.alert(LOGIN_SUCCESS)
        self.controller.show_frame(HOME_SCREEN)


class HomeScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=BLACK)

        # changeable labels in the home-page
        x = datetime.datetime.now()
        self.__hello_label = Label(self, text=EMPTY, fg=RED, bg=BLACK)
        self.__hello_label.place(x=50, y=80)
        self.__date_label = Label(self, text=EMPTY, fg=RED, bg=BLACK)
        self.__date_label.place(x=50, y=60)

        # scrollbars for the buttons. place to put the buttons (Text objects).
        join_frame = Frame(self)
        my_frame = Frame(self)
        join_frame.place(x=350, y=250)
        my_frame.place(x=150, y=250)
        self.__join_scrollbar = Scrollbar(join_frame, orient="vertical")
        self.__join_text = Text(join_frame, wrap="none", width=20, height=5)
        self.__join_text.pack()
        self.__join_scrollbar.pack(side=RIGHT, fill=Y)
        self.__my_scrollbar = Scrollbar(my_frame, orient="vertical")
        self.__my_text = Text(my_frame, wrap="none", width=20, height=5)
        self.__my_text.pack()
        self.__my_scrollbar.pack(side=RIGHT, fill=Y)

        self.__join_text.config(yscrollcommand=self.__join_scrollbar.set)
        self.__join_scrollbar.config(command=self.__join_text.yview)
        self.__my_text.config(yscrollcommand=self.__my_scrollbar.set)
        self.__my_scrollbar.config(command=self.__my_text.yview)

        Label(self, text="Home", fg=RED, bg=BLACK, font=controller.title_font).pack(side="top", fill="x")

        Button(self, text="Edit My Profile", padx=8, pady=5, bg=INDIAN_RED, command=lambda: controller.show_frame(
            "EditProfile")).place(x=680, y=60)
        Button(self, text="Log Out", padx=8, pady=5, bg=INDIAN_RED, command=lambda: self.logout())\
            .place(x=700, y=20)
        Label(self, text="My Projects").place(x=150, y=200)
        Label(self, text="Join Project").place(x=350, y=200)
        Button(self, text="Create Project", padx=8, pady=5, bg=INDIAN_RED, command=lambda: controller.show_frame(
            "CreateProjectPage")).place(x=550, y=200)

    def change_user_and_date(self):
        self.__hello_label.config(text="hello " + get_user_name(USER))
        x = datetime.datetime.now()
        self.__date_label.config(text=str(x.day) + DOT + str(x.month) + DOT + str(x.year))

    # destroying the root and creating a new one so all the changes that were done on frames will be deleted.
    def logout(self):
        global USER, MY_PROJECTS_BUTTON, JOIN_PROJECTS_BUTTON, OPEN_PROFILE_PAGES\
        # restarting all the global variables so all the functions used would be reusable.
        USER = EMPTY
        MY_PROJECTS_BUTTON = False
        JOIN_PROJECTS_BUTTON = False
        OPEN_PROFILE_PAGES = {}
        OPEN_PROJECTS = {}
        # destroying the root
        self.controller.destroy()
        # creating a new root
        main()

    # print to the screen all the projects that the user doesn't part of.
    def join_projects_button(self):
        global USER, JOIN_PROJECTS_BUTTON, JOIN_PROJECTS_BUTTONS_LIST
        if JOIN_PROJECTS_BUTTON:
            JOIN_PROJECTS_BUTTON = False
            for b in JOIN_PROJECTS_BUTTONS_LIST:
                b.destroy()
            JOIN_PROJECTS_BUTTONS_LIST = []
        else:
            # this variable make sure the projects won't print the projects list twice.
            JOIN_PROJECTS_BUTTON = True
            my_projects = get_user_projects(USER).split(DB_SEPARATOR)
            all_projects = query_all_projects()
            # defining empty list for all the projects the user not taking part in.
            projects = []
            for p in all_projects:
                projects.append(p.name)
                for m in my_projects:
                    if p.name == m:
                        projects.remove(p.name)
            # create buttons match to the amount of the projects.
            for p in range(len(projects)):
                button = Button(self.controller.frames[HOME_SCREEN], text=projects[p], borderwidth=NO_BORDER, bg=PINK,
                                command=lambda p=p: self.join_project(projects[p]))
                self.__join_text.window_create("end", window=button)
                self.__join_text.insert("end", LINE_DOWN)
                # button.place(x=350, y=250 + p * 25)
                JOIN_PROJECTS_BUTTONS_LIST.append(button)

    # opening a simple-dialog object to put the asked project's code in. if true, moving to the project page.
    def join_project(self, project_name):
        global USER
        project = query_project_by_name(project_name)
        code = simpledialog.askstring(EMPTY, ENTER_CODE1 + get_project_name(project) + ENTER_CODE2)
        if join_project(get_user_name(USER), get_project_name(project), code):
            # sends to function in database.py .
            self.join_projects_button()
            self.join_projects_button()
            self.my_Projects_button()
            self.my_Projects_button()
            self.controller.openProject(get_project_name(project))
        else:
            self.controller.alert(WRONG_CODE)

    # printing all the projects the user worked on before.
    def my_Projects_button(self):
        global USER, MY_PROJECTS_BUTTON, MY_PROJECTS_BUTTONS_LIST
        if MY_PROJECTS_BUTTON:
            MY_PROJECTS_BUTTON = False
            for b in MY_PROJECTS_BUTTONS_LIST:
                b.destroy()
            MY_PROJECTS_BUTTONS_LIST = []
        else:
            MY_PROJECTS_BUTTON = True
            projects = get_user_projects(USER).split(DB_SEPARATOR)
            # when reading lists from the db there's almost always a separating char at the end. when splitting the
            # string that was used as a list, there is a need in taking away the last object in the list because of it.
            projects.pop(-1)
            for p in range(len(projects)):
                button = Button(self.controller.frames[HOME_SCREEN], text=projects[p], borderwidth=NO_BORDER, bg=PINK,
                                command=lambda p=p: self.controller.openProject(projects[p]))
                self.__my_text.window_create("end", window=button)
                self.__my_text.insert("end", LINE_DOWN)
                # button.place(x=150, y=250 + p * 25)
                MY_PROJECTS_BUTTONS_LIST.append(button)


class UpdateHomeScreen(Thread):
    def __init__(self, homepage_object):
        super(UpdateHomeScreen, self).__init__()
        self.daemon = True

        self.__homePage = homepage_object
        self.__all_projects = query_all_projects()

    # overrides the function 'run' that exists in the threading package.
    def run(self):
        while True:
            sleep(0.5)
            real_time_situation = query_all_projects()
            if not self.__all_projects == real_time_situation:
                self.__homePage.join_projects_button()
                self.__homePage.join_projects_button()
                self.__homePage.my_Projects_button()
                self.__homePage.my_Projects_button()
                self.__all_projects = real_time_situation


class EditProfileScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=BLACK)

        Label(self, text="Edit Profile", font=controller.title_font, fg=RED, bg=BLACK).place(x=350, y=0)

        # defining vars for saving the info from the user.
        email = StringVar()
        phone = StringVar()
        username = StringVar()
        password = StringVar()

        # fields to fill with info for signing up.

        Label(self, text="email", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=150)
        Entry(self, textvariable=email, width=50).place(x=310, y=155)

        Label(self, text="phone", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK).place(x=170, y=300)
        Entry(self, textvariable=phone, width=50).place(x=310, y=305)

        Label(self, text="username", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK)\
            .place(x=170, y=450)
        Entry(self, textvariable=username, width=50).place(x=310, y=455)

        Label(self, text="password", font=controller.cretiria_font, anchor='w', fg=RED, bg=BLACK)\
            .place(x=170, y=600)
        Entry(self, textvariable=password, width=50).place(x=310, y=605)

        Button(self, text="Back", padx=18, pady=6, bg=INDIAN_RED, command=lambda: controller.show_frame(HOME_SCREEN))\
            .place(x=280, y=700)
        Button(self, text="Save Changes", padx=10, pady=8, bg=INDIAN_RED, command=lambda: self.edit_profile(
            email.get(), phone.get(), username.get(), password.get())).place(x=430, y=700)

    def edit_profile(self, email, phone, username, password):
        # sending all the info given to a check in database.py .
        global USER
        alerted_message = self.controller.alert(edit_user(USER, email, phone, username, password))
        if alerted_message == EDITED_SUCCESS:
            USER = query_user_by_username(username)
            self.controller.show_frame(GOME_SCREEN)


class CreateProjectPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=BLACK)

        Label(self, text="create project", fg=RED, bg=BLACK, font=controller.title_font)\
            .pack(side="top", fill="x", pady=10)

        # defining vars for creating a new project.
        name = StringVar()
        slogan = StringVar()
        description = StringVar()
        photo = StringVar()

        # fields to fill with info for creating a new project.
        Label(self, text="project's name", fg=RED, bg=BLACK, font=controller.cretiria_font, anchor='w')\
            .place(x=100, y=115)
        Entry(self, textvariable=name, width=50).place(x=350, y=120)

        Label(self, text="project's slogan", fg=RED, bg=BLACK, font=controller.cretiria_font, anchor='w')\
            .place(x=100, y=230)
        Entry(self, textvariable=slogan, width=50).place(x=350, y=235)

        Label(self, text="project's description", fg=RED, bg=BLACK, font=controller.cretiria_font, anchor='w')\
            .place(x=100, y=345)
        Entry(self, textvariable=description, width=50).place(x=350, y=350)

        Label(self, text="project's photo\n(photo address)", fg=RED, bg=BLACK,
              font=controller.cretiria_font, anchor='w').place(x=100, y=460)
        Entry(self, textvariable=photo, width=50).place(x=350, y=465)

        Button(self, text="Back", padx=10, pady=7, bg=INDIAN_RED, command=lambda: controller.show_frame(HOME_SCREEN))\
            .place(x=250, y=600)
        Button(self, text="create project", padx=8, pady=7, bg=INDIAN_RED, command=lambda: self.createProject_button(
            name.get(), slogan.get(), description.get(), photo.get())).place(x=420, y=600)

    # creating a new project, by passing all the info that the user gave to a function in the database.
    def createProject_button(self, project_name, slogan, description, photo):
        project_code = EMPTY.join(choices(ascii_letters + digits, k=6))
        global USER
        validate_info = create_project(project_code, project_name, slogan, description, photo, get_user_name(USER))
        if validate_info != CREATE_SUCCESS:
            self.controller.alert(validate_info)
        else:
            self.controller.alert(CREATE_SUCCESS.format(project_code))
            self.controller.show_frame("HomePage")
            self.controller.openProject(project_name)


# the main function runs the client.
def main():
    # creates the GP window and main root.
    app = GP()
    # define the size of the GP window, and make it un-resizable.
    app.geometry('800x900')
    app.resizable(width=False, height=False)
    # define the GP logo as the application logo.
    app.iconbitmap('GP_logo.ico')
    # make sure the application won't close itself even after running all the functions.
    app.mainloop()


# runs the main function.
if __name__ == "__main__":
    main()
