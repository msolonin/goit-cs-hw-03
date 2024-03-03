# -*- coding: utf-8 -*-
"""
Завдання для виконання:
Читання (Read)
    Реалізуйте функцію для виведення всіх записів із колекції.
    Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
Оновлення (Update)
    Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
    Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
Видалення (Delete)
    Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
    Реалізуйте функцію для видалення всіх записів із колекції."""

import readline
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

URI = f"mongodb://localhost:27017/"

# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))
db = client.mds

def get_input(_string, verification_func=None):
    """ Get input in cmd, optional verify input
    """
    while True:
        value = input(f"{_string}: ")
        if verification_func:
            try:
                if verification_func(value):
                    return value
                else:
                    print("Incorrect input")
            except Exception as e:
                print(f"Incorrect input {e}")
        else:
            return value


def read():
    """ Read all items
    """
    return db.cats.find()


def create():
    """ Create new item
    """
    _name = get_input("Enter name: ", verification_func=lambda x: type(x) is str)
    _age = get_input("Enter age: ", verification_func=lambda x: type(int(x)) is int)
    _features = get_input("Enter features(split by comma): ")
    _features = _features.split(",")
    cat = {
        "name": _name,
        "age": _age,
        "features": _features
    }
    return db.cats.insert_one(cat)


def update():
    """ Update item by pk
    """
    _pk = get_input("Enter pk: ", verification_func=lambda x: type(x) is str)
    _name = get_input("Enter name: ", verification_func=lambda x: type(x) is str)
    _age = get_input("Enter age: ", verification_func=lambda x: type(int(x)) is int)
    _features = get_input("Enter features(split by comma): ")
    _features = _features.split(",")
    new_cat = {
        "name": _name,
        "age": _age,
        "features": _features
    }
    return db.cats.update_one({"_id": ObjectId(_pk)}, {"$set": new_cat})


def update_features():
    """ Update features by pk
    """
    _pk = get_input("Enter pk: ", verification_func=lambda x: type(x) is str)
    _features = get_input("Enter features(split by comma): ")
    _features = _features.split(",")
    new_cat = {
        "features": {"$each": _features}
    }
    return db.cats.update_one({"_id": ObjectId(_pk)}, {"$push": new_cat})

def update_age():
    """ Update age by pk
    """
    _pk = get_input("Enter pk: ", verification_func=lambda x: type(x) is str)
    _age = get_input("Enter age: ", verification_func=lambda x: type(int(x)) is int)
    new_cat = {
        "age": _age
    }
    return db.cats.update_one({"_id": ObjectId(_pk)}, {"$set": new_cat})


def delete():
    """ Delete item by pk
    """
    _pk = get_input("Enter pk: ", verification_func=lambda x: type(x) is str)
    return db.cats.delete_one({"_id": ObjectId(_pk)})

def delete_by_name():
    """ Delete item by name
    """
    _name = get_input("Enter name: ", verification_func=lambda x: type(x) is str)
    return db.cats.delete_one({"name": _name})

def delete_all():
    """ Delete all items from DB
    """
    return db.cats.delete_many({})

def read_by_name():
    """ Read cat by name
    """
    _name = get_input("Enter name: ", verification_func=lambda x: type(x) is str)
    document = db.cats.find_one({"name": _name})
    if document is not None:
        print(document)
    else:
        print("Not found")

def init_db():
    """ Init data in DB
    """
    try:
        document = db.cats.insert_many([
            {""
             "name": 'Lama',
             "age": 2,
             "features": ['ходить в лоток', 'не дає себе гладити', 'сірий'],
             },
            {
                "name": 'Liza',
                "age": 4,
                "features": ['ходить в лоток', 'дає себе гладити', 'білий'],
            },
            {
                "name": 'Boris',
                "age": 12,
                "features": ['ходить в лоток', 'не дає себе гладити', 'сірий'],
            },
            {
                "name": 'Murzik',
                "age": 1,
                "features": ['ходить в лоток', 'дає себе гладити', 'чорний'],
            }
        ])
        print(document)
    except Exception as e:
        print(e)


def input_error(func):
    """Common wrapper for intercept all exceptions
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return "Please use correct number of arguments"
        except KeyError:
            return "Name is not present in address book"
        except AttributeError:
            return "Could not show, list of birthdays empty"
        except ValueError:
            return "Please add command"
        except Exception as ex:
            print(f"Unexpected exception {ex}: in def {func.__name__}()")
    return wrapper

@input_error
def parse_input(user_input):
    """ Method for parse cmd input
    :param user_input:
    :type user_input:
    :return: cmd command for execution, *args for continue usage in methods,
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

class CommandCompleter:

    def __init__(self, options):
        self.options = sorted(options)
        self.matches = []

    def complete(self, text, state):
        """ Method for autocomplete
        """
        response = None
        if state == 0:
            if text:
                self.matches = [
                    _ for _ in self.options if _ and _.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


class Commands:
    INIT = "init"
    READ = "read"
    READ_BY_NAME = "read_by_name"
    CREATE = "create"
    UPDATE = "update"
    UPDATE_AGE = "update_age"
    UPDATE_FEATURES = "update_features"
    DELETE = "delete"
    DELETE_BY_NAME = "delete_by_name"
    DELETE_ALL = "delete_all"
    CLOSE = "close"
    EXIT = "exit"

    @classmethod
    def all_keys(cls):
        """ Show list of all names of variables in Class
        :return: names
        :rtype: list
        """
        return [_ for _ in dir(Commands) if not _.startswith('_') and _.isupper()]

    @classmethod
    def all_values(cls):
        """ Show list of all values of variables in Class
        :return: values
        :rtype: list
        """
        return [getattr(cls, _) for _ in cls.all_keys()]

@input_error
def main():
    """ Main method for execution, start point
    """
    def greetings():
        print("""Welcome to the mongo db assistant bot!
        Available commands:
            ° init
            ° read
            ° read_by_name
            ° create
            ° update
            ° update_age
            ° update_features
            ° delete
            ° delete_by_name
            ° delete_all
            ° close/exit""")

    greetings()
    while True:
        readline.set_completer(CommandCompleter(
            Commands.all_values()).complete)
        readline.set_completer_delims(' ')
        readline.parse_and_bind('tab: complete')
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in [Commands.CLOSE, Commands.EXIT]:
            print("Good bye!")
            break
        elif command == Commands.INIT:
            print(init_db())
        elif command == Commands.READ:
            print([print(cat) for cat in read()])
        elif command == Commands.READ_BY_NAME:
            read_by_name()
        elif command == Commands.CREATE:
            print(create())
        elif command == Commands.UPDATE:
            print(update())
        elif command == Commands.UPDATE_AGE:
            print(update_age())
        elif command == Commands.UPDATE_FEATURES:
            print(update_features())
        elif command == Commands.DELETE:
            print(delete())
        elif command == Commands.DELETE_BY_NAME:
            print(delete_by_name())
        elif command == Commands.DELETE_ALL:
            print(delete_all())
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
