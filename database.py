from model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# the following directory's goal is term between the actual database table to the server.
# it contain all the function that connecting directly with the tables, for getting some info or setting a new one.
# all the functions are used through the server. the client sends the info towords the server, the server sends it to
# one of the database.py functions that connects it to the table if needed or sending a message back to client.

engine = create_engine(URL, connect_args={ENGINE: False})
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# '01' 'first_name last_name email phone username password'. the signing up function receives information needed for
# creating a new GP user. most of checks towords the info were made in the client file. the following function checks if
# the username that sent by client exists already. if not, the function creates a new GP user and returns __________ to
# the server. if the username exist in system already, the function cause no changes in database and returns __________
# to server.
def signup(data):
    first_name, last_name, email, phone, username, password = data.split()
    # sends the username to another check. the username, like 'id' is unique for each object (foreign_key).
    if query_user_by_username(username):
        return False, SIGNUP_TAKEN_USERNAME
    # after all checks, if approved, the function creates the new user object.
    user = User(first_name=first_name, last_name=last_name, email=email, phone=phone, username=username,
                password=password, projects=EMPTY)
    # 'session.add' is adding the object just created to it's table.
    session.add(user)
    # 'session.commit' saves the changes accord in the table after adding, deleting or editing an object's parameters.
    session.commit()
    return True, SIGNUP_SUCCESS


# '02' 'username password' the login function receives a username and a password. it checks if there's a user object
# with identical username and password in the users table. if there is, it approves the user that sent the request in to
# log in the program. the function will return ________. if not, the function returns ________.
def login(data):
    username, password = data.split()
    # query the user with the same username from the table. as mentioned, the username is unique for each user.
    user = query_user_by_username(username)
    if user:
        if get_user_password(user) == password:
            return True
    return False


# '03' 'project_name' the function open_project, used to send all the necessary information about a specific project to
# a client so it would be able to build the project page and present it to the user. the function returns the project
# object to the sender client.
def open_project(data):
    project_name = data
    project = query_project_by_name(project_name)
    return project


# '04' 'username~project_name~project_code' the join_project function get's the code of a project and checks if it's the
# same code of the project object (that has the project_name). if yes, the function will return the project object and
# will add the the username of the user who joined the new project to the users parameter in the project object in DB.
# in addition it will add it to the projects parameter in the user's object in DB. if the code wasn't match, the
# function won't change DB and return ______.
def join_project(data):
    username, project_name, project_code = data.split(DB_SEPARATOR)
    project = query_project_by_name(project_name)
    if get_project_code(project) == project_code:
        user = query_user_by_username(username)
        user.projects = user.projects + project_name + DB_SEPARATOR
        project.users = project.users + username + DB_SEPARATOR
        session.commit()
    else:
        pass


# '05' 'project_name~project_slogan~project_manager' the create_project function, gets all the needed data
# for creating a new GP project object. it checks
def create_project(data):
    pass


# '06' '' the function
def logout(data):
    pass


# '07' '' the function
def edit_profile(data):
    pass


# '08' '' the function
def delete_user(data):
    pass


# '09' '' the function
def send_message(data):
    u_len = str(len(username))
    t = message[0]
    p_len = int(message[1:3])
    message = message[3+p_len:]
    project.messages = project.messages + t + u_len + message + DB_SEPARATOR
    print(get_project_messages(project))
    session.commit()


# '10' '' the function
def open_directory(data):
    pass


# '11' '' the function
def close_directory(data):
    pass


# '12' '' the function
def add_directory(data):
    pass


# '13' '' the function
def release_directory(data):
    pass


# '14' '' the function
def delete_directory(data):
    pass


# '15' '' the function
def mute(data):
    pass


# '16' '' the function
def leave_project(data):
    pass


# '17' '' the function
def delete_project(data):
    pass


# '18' '' the function
def close_project(data):
    pass


# the edit_user function allows the user to edit his personal data (not his first & last name because it's not
# changeable) if he desires. it get's the same info like the signup function (except first and last name). it makes the
# same checks like the signup function as well and if it funds that all the info is 'legal' it approves the changes and
# edit the object's values in the db. the function make sure to delete all the traces for the old user's info.
def edit_user(user, email, phone, username, password):
    # check the validity of the info was given from user with the same checks from signup.
    if email == EMPTY or phone == EMPTY or username == EMPTY or password == EMPTY:
        return SIGNUP_NOT_FILLED
    if not username_validation(username):
        return SIGNUP_INVALID_USERNAME
    if query_user_by_username(username):
        return SIGNUP_TAKEN_USERNAME
    if not email_validation(email):
        return SIGNUP_INVALID_EMAIL
    if not phone.isdecimal():
        return SIGNUP_INVALID_PHONE
    # if all checks went positive, before editing the user's object in the table, the function changes all the directory
    # & project objects that has traces of the old information of the user.
    projects = get_user_projects(user)
    # checks if the user works on project because if yes his name is kept in the the project objects in db.
    if not projects == EMPTY:
        old_username = get_user_username(user)
        projects = projects.split(DB_SEPARATOR)
        for p in projects:
            # i know i supposed to be able using pop or remove instead of the if but it's just don't working
            if p == EMPTY:
                break
            project_object = query_project_by_name(p)
            # saves all the project's users in a users list.
            users = get_project_users(project_object).split(DB_SEPARATOR)
            # saves the project manager.
            manager = get_project_manager(project_object)
            # if the user is the manager of the project, changes the manager parameter to the new user's username.
            if manager == old_username:
                project_object.manager = username
            # removes the old username from the users list in the project object in db and insert the new username.
            users.remove(old_username)
            users.append(username)
            project_object.users = DB_SEPARATOR.join(users)
            # go through all the messages that saved to the project object, and switches the old name with the new one.
            messages = get_project_messages(project_object)
            if not messages == EMPTY:
                messages = messages.split(DB_SEPARATOR)
                clear_project_chat(project_object)
                for m in messages:
                    if not m == EMPTY:
                        # splitting the message to switch only the username part and then joining it again into one
                        # string and concatenate it together to the database.
                        t = m[0]
                        username_len = int(m[1])
                        time = m[2:8]
                        content = m[username_len+8:]
                        message_username = m[8:username_len+8]
                        if message_username == old_username:
                            new_username_len = str(len(username))
                            project_object.messages = project_object.messages + t + new_username_len + time + username \
                                + content + DB_SEPARATOR
                        # if it's a message not hte edited user sent, it concatenate the message as it was.
                        else:
                            project_object.messages = project_object.messages + m + DB_SEPARATOR
            # if the user was the last to edit a directory in the project, the following for loop changes the last
            # editor parameter to his new username.
            project_directories = query_project_directories(get_project_name(p))
            for d in project_directories:
                if get_directory_last_editor(d) == old_username:
                    set_directory_last_editor(d, username)

        # saves all the changes the accord to db.
        session.commit()
    # finally, changes the user's info.
    set_user_email(user, email)
    set_user_phone(user, phone)
    set_user_username(user, username)
    set_user_password(user, password)
    # a message that the function sends to approve the user editing.
    return EDITED_SUCCESS


# the function 'create_project' gets the needed information for creating a new GP project, checks some of it, and
# returns a message to server whether the project was created and added to db or not.
def create_project(code, name, slogan, description, photo, manager):
    # checks the length of the project name
    if name == EMPTY or len(name) > 20:
        return CREATE_PROJECT_NAME_LENGTH
    # checks if there is a project with the same name as the given name (the name is unique)
    if query_project_by_name(name):
        return CREATE_PROJECT_TAKEN_NAME
    # the char '~' used as a separator in database, therefor, when reading from db, it can harm the splitting process
    # of the project names.
    if name.find(DB_SEPARATOR) != -1:
        return INVALID_CHAR
    # creating a new project object.
    project = Project(code=code, name=name, slogan=slogan, photo=photo,
                      description=description, manager=manager, users=manager, messages=EMPTY)
    user = query_user_by_username(manager)
    # adding to the user's 'projects' column in db the new project he manages.
    user.projects = user.projects + project.name + DB_SEPARATOR
    session.add(project)
    # sace the changes in db.
    session.commit()
    return


# the 'add_directory' function gets the project_name that one of it's user want to add a new directory, and a directory
# object. in constants.py there's a list of invalid directories names that contains the code directories, names. the
# function checks there's no collaboration between those, so the new directory when being open, wont override a code
# directory. in addition it checks there's no other file with the same name.
def add_directory(project_name, directory):
    path = get_directory_name(directory)
    name = path.split(SLASH)[-1]
    for i in INVALID_DIRECTORIES_NAMES:
        if i == name:
            return False
    if query_certain_project_directory(project_name, get_directory_name(directory)):
        return False
    ending = directory.name.split(DOT)[-1]
    # encoding the dir data before saving it in db.
    data = directory.read().encode('ascii')
    # creating the new directory object.
    new_directory = Directory(project_name=project_name, name=name, ending=ending, data=data,
                              last_editor=EMPTY, available=True)
    session.add(new_directory)
    # saving the changes in the db.
    session.commit()
    # the function returns True if after all the checks the directory found to be non problematic.
    return True


# the 'delete_directory' function gets the name of the project a directory belongs to and the directory name. it looks
# for the directory place in db and delete it.
def delete_directory(project_name, directory_name):
    project_directories = query_project_directories(project_name)
    for directory in project_directories:
        if get_directory_name(directory) == directory_name:
            session.delete(directory)
            session.commit()
            return True
    # if the function finds there's no such directory it returns False.
    return False


# ----------get functions (for later)----------
# user get functions
def get_user_first_name(user):
    return user.first_name


def get_user_last_name(user):
    return user.last_name


def get_user_email(user):
    return user.email


def get_user_phone(user):
    return user.phone


def get_user_username(user):
    return user.username


def get_user_password(user):
    return user.password


def get_user_projects(user):
    return user.projects


# project get functions
def get_project_code(project):
    return project.code


def get_project_name(project):
    return project.name


def get_project_slogan(project):
    return project.slogan


def get_project_description(project):
    return project.description


def get_project_manager(project):
    return project.manager


def get_project_users(project):
    return project.users


def get_project_messages(project):
    return project.messages


# directory get functions
def get_directory_project_name(directory):
    return directory.project_name


def get_directory_name(directory):
    return directory.name


def get_directory_ending(directory):
    return directory.ending


def get_directory_data(directory):
    return directory.data


def get_directory_last_editor(directory):
    return directory.last_editor


def get_directory_available(directory):
    return directory.available


# ----------query functions----------
# the query functions returns all the objects or a specific object according to a parameter.
def query_user_by_username(username):
    user = session.query(User).filter_by(username=username).first()
    return user


def query_project_by_name(name):
    project = session.query(Project).filter_by(name=name).first()
    return project


def query_all_users():
    users = session.query(User).username.all()
    return users


def query_all_projects():
    projects = session.query(Project).all()
    return projects


def query_all_directories():
    directories = session.query(Directory).all()
    return directories


def query_certain_project_directory(project_name, directory_name):
    project_directories = query_project_directories(project_name)
    for directory in project_directories:
        if get_directory_name(directory) == directory_name:
            return directory


def query_project_directories(project_name):
    directories = session.query(Directory).filter_by(project_name=project_name).all()
    return directories


# user = User(first_name="1", last_name="1", email="1", phone="1", username="1", password="1", projects="1~")
# session.add(user)
# project = Project(code="1", name="1", slogan="1", photo="", description="1", manager="1", users="1", messages=EMPTY)
# session.add(project)
# user = User(first_name="2", last_name="2", email="2", phone="2", username="2", password="2", projects="2~")
# session.add(user)
# project = Project(code="2", name="2", slogan="2", photo="", description="2", manager="2", users="2", messages=EMPTY)
# session.add(project)

# session.commit()
