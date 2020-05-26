# the following directory contains all the constants being used in the GP code.

# -----single chars-----
EMPTY = ''
SPACE = ' '
DOT = '.'
SLASH = '/'
LINE_DOWN = '\n'
DB_SEPARATOR = '~'

# -----general messages-----
INVALID_CHAR = "don't use the following char '~'"

# -----regex-----
REGEX_EMAIL = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# -----model.py-----
# tables' names:
USERS_TABLE_NAME = 'users'
PROJECTS_TABLE_NAME = 'projects'
DIRECTORIES_TABLE_NAME = 'directories'

# parameters of each table for repr functions:
TABLE_PAR_ID = "\nid: "
USERS_TABLE_PAR_FIRST_NAME = "\nfirst name: "
USERS_TABLE_PAR_LAST_NAME = "\nlast name: "
USERS_TABLE_PAR_EMAIL = "\nemail: "
USERS_TABLE_PAR_PHONE = "\nphone: "
USERS_TABLE_PAR_USERNAME = "\nusername: "
USERS_TABLE_PAR_PASSWORD = "\npassword: "
USERS_TABLE_PAR_PROJECTS = "\nprojects: "

PROJECTS_TABLE_PAR_CODE = "\ncode: "
PROJECTS_TABLE_PAR_NAME = "\nname: "
PROJECTS_TABLE_PAR_SLOGAN = "\nslogan: "
PROJECTS_TABLE_PAR_MANAGER = "\nmanager: "
PROJECTS_TABLE_PAR_USERS = "\nusers: "
PROJECTS_TABLE_PAR_MESSAGES = "\nmessages: "

DIRECTORIES_TABLE_PAR_PROJECT_NAME = "\nproject name: "
DIRECTORIES_TABLE_PAR_NAME = "\nname: "
DIRECTORIES_TABLE_PAR_ENDING = "\nending: "
DIRECTORIES_TABLE_PAR_DATA = "\ndata: "
DIRECTORIES_TABLE_PAR_LAST_EDITOR = "\nlast editor: "
DIRECTORIES_TABLE_PAR_AVAILABLE = "\navailable: "

# -----database.py-----
# signup possible messages:
SIGNUP_NOT_FILLED = "you didn't fill all fields!\n\nplease take another look on the form."
SIGNUP_INVALID_EMAIL = "invalid email address!"
SIGNUP_INVALID_PHONE = "invalid phone number!"
SIGNUP_TAKEN_USERNAME = "this username has been taken!"
SIGNUP_INVALID_USERNAME = "username is too short!"
SIGNUP_INVALID_PASSWORD = "password is too short!"
SIGNUP_SUCCESS = "you signed up successfully!\n\nenjoy using GP :)"

# login possible messages:
LOGIN_NOT_FILLED = "you didn't fill both username and password!"
LOGIN_SUCCESS = "you logged in successfully!"

# edit user possible messages:
EDITED_SUCCESS = "your profile edited successfully!"

# create project possible messages:
CREATE_PROJECT_NAME_LENGTH = "project_name should be between 1-15 chars!"
CREATE_PROJECT_TAKEN_NAME = "the project name is used already!"
CREATE_SUCCESS = "your project code is: {} \n\nremember it." \
                 "\n without it you won't be able to add users to work on the project!"
# SQL alchemy:
URL = 'sqlite:///GP.db'
ENGINE = 'check_same_thread'

# -----server.py-----
# ssl cert directory name:
CERT = "key_cert.pem"

# messages types dictionary:
types_dictionary = {"01": "signup", "02": "login", "03": "open_project", "04": "join_project", "05": "create_project",
                    "06": "logout", "07": "edit_profile", "08": "delete_user", "09": "send_message",
                    "10": "open_directory", "11": "close_directory", "12": "add_directory", "13": "release_directory",
                    "14": "delete_directory", "15": "mute", "16": "leave_project", "17": "delete_project",
                    "18": "close_project"}

# -----client-----
CLIENT_IP = '127.0.0.1'

# problems with connecting to server
CONNECTING_SERVER_PROBLEM = "some problems in our servers.\nplease try reconnect later."

# buttons and labels parameters:
NO_BORDER = '0'

# entry validation constants:
VALIDATE_COMMAND_TYPE = '%S'
VALIDATE_METHOD = 'key'

# screens name:
LOGO_SCREEN = "LogoScreen"
START_SCREEN = "StartScreen"
SIGNUP_SCREEN = "SignScreen"
LOGIN_SCREEN = "LogScreen"
HOME_SCREEN = "HomeScreen"
SETTINGS_SCREEN = "SettingsScreen"
PROFILE_SCREEN = "ProfileScreen"
EDIT_PROFILE_SCREEN = "EditProfileScreen"
SETTINGS_SCREEN = "Settings"

# colors:
BLACK = 'black'
RED = 'red'
WHITE = 'white'
PINK = 'pink'
INDIAN_RED = 'IndianRed1'
















# general chars`
WRONG = "Wrong"
NICE = "Nice"

# font's definitions
FIXEDSYS = "fixedsys"
HELVETICA = "Helvetica"
BOLD = "bold"
ITALIC = "italic"

# defining containers
BOTH = "both"
TOP = "top"
NSEW = "nsew"

# login alerts
WRONG_INFO = "wrong information. try again!"
LOGIN_SUCCESS = "you logged in successfully! enjoy using GP :)"

# join a project
ENTER_CODE1 = "Enter the "
ENTER_CODE2 = " project's code:"
WRONG_CODE = "wrong project's code!\n\ntry again."


# chat
TRY_USE_IN_CHAR = "the following char is not supported in this chat messages: '~'"


# directories issues
IS_OPEN = "someone works on the same directory your want to work on.\ntry again later"
NO_OPEN_DIRECTORIES = "all the directories are free!"
INVALID_DIRECTORIES_NAMES = ['old_client.py', 'constants.py', 'database.py', 'file.png', 'global_list.py',
                             'key_cert.pm', 'model.py', 'print_db.py', 'old_server.py', 'settings_button.png',
                             'GP.db', 'GP_logo.gif', 'GP_logo.ico']
ENTER_DIRECTORY_NAME = "enter the directory's name you aim to delete. spell it correctly with the ending!"
# -----server-client-----

PROBLEM_ACCORD = "A problem accord with the server. please try work the project later"

# checks that no project page will open twice.
OPEN_PROJECTS = {}
