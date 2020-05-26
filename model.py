from constants import *
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

# the following file contains all the database tables that are used in the GP program.
# it's possible to see a circular type of writing in each class (table):
# giving the table's name, than defining the 'id', and then name the columns of the table and pick their type.
# for the first table, iim adding a full documentation that serves the others as well.

Base = declarative_base()


# the class name- the object's name that the following table will contain.
class User(Base):
    # the name of the table. when using the 'print_db.py', it will be used as the table title.
    __tablename__ = USERS_TABLE_NAME
    # id is a unique parameter each object has.
    # in a case all the other parameters are equal in two object's it help differentiate between them
    id = Column(Integer, primary_key=True)
    # the columns of the table and their names.
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    username = Column(String)
    password = Column(String)
    projects = Column(String)

    # each class/table usually has a 'repr' function. printing the object (print(User)) the repr function will work.
    # it print all the info of a specific object to the console. if one of the parameters of an object is not a string,
    # as id for example, there's a need to change it's type.
    def __repr__(self):
        return TABLE_PAR_ID + str(self.id) + USERS_TABLE_PAR_FIRST_NAME + self.first_name + USERS_TABLE_PAR_LAST_NAME +\
               self.last_name + USERS_TABLE_PAR_EMAIL + self.email + USERS_TABLE_PAR_PHONE + self.phone +\
               USERS_TABLE_PAR_USERNAME + self.username + USERS_TABLE_PAR_PASSWORD + self.password +\
               USERS_TABLE_PAR_PROJECTS + self.projects + LINE_DOWN


class Project(Base):
    __tablename__ = PROJECTS_TABLE_NAME
    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    slogan = Column(String)
    manager = Column(String)
    users = Column(String)
    messages = Column(String)

    def __repr__(self):
        return TABLE_PAR_ID + str(self.id) + PROJECTS_TABLE_PAR_CODE + self.code + PROJECTS_TABLE_PAR_NAME + self.name\
               + PROJECTS_TABLE_PAR_SLOGAN + self.slogan + PROJECTS_TABLE_PAR_MANAGER + self.manager \
               + PROJECTS_TABLE_PAR_USERS + self.users + PROJECTS_TABLE_PAR_MESSAGES + self.messages + LINE_DOWN


class Directory(Base):
    __tablename__ = DIRECTORIES_TABLE_NAME
    id = Column(Integer, primary_key=True)
    project_name = Column(String)
    name = Column(String)
    ending = Column(String)
    data = Column(LargeBinary)
    last_editor = Column(String)
    available = Column(Boolean)

    def __repr__(self):
        return TABLE_PAR_ID + str(self.id) + DIRECTORIES_TABLE_PAR_PROJECT_NAME + self.project_name +\
               DIRECTORIES_TABLE_PAR_NAME + self.name + DIRECTORIES_TABLE_PAR_ENDING + self.ending +\
               DIRECTORIES_TABLE_PAR_DATA + str(self.data) + DIRECTORIES_TABLE_PAR_LAST_EDITOR + self.last_editor +\
               DIRECTORIES_TABLE_PAR_AVAILABLE + str(self.available) + LINE_DOWN
