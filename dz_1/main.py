# -*- coding: utf-8 -*-
"""
Скрипт для створення запитів до постгресу
    Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
    Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
    Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
    Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
    Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.
    Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.
    Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.
    Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
    Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
    Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
    Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, чия електронна пошта містить певний домен (наприклад, '%@example.com').
    Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
    Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
    Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
"""

import logging
import random
import readline
from connect import create_connect

AVAILABLE_STATUSES = (1, 2, 3,)

TASKS_BY_USER = "SELECT title, description FROM tasks WHERE user_id = %s"
TASKS_BY_STATUS = """
SELECT t.title , t.description FROM tasks AS t JOIN status AS s ON s.id = t.status_id where s.name = '%s';"""
USERS_WITHOUT_TASKS = "SELECT fullname FROM users WHERE id not IN (SELECT user_id FROM tasks);"
UPDATE_STATUS = "UPDATE tasks SET status_id = %s WHERE id = %s;"
ADD_NEW_TASK = "INSERT INTO tasks (title, description, status_id, user_id) VALUES ('%s', '%s', %s, %s)"
ALL_NOT_COMPLETED_TASKS = "SELECT title, description FROM tasks WHERE status_id IN (1, 2);"
DELETE_TASK = "DELETE FROM tasks WHERE id = %s"
UPDATE_USER_NAME = "UPDATE users SET fullname = '%s' WHERE id = %s;"
TASK_STATUS_COUNT = "SELECT s.name, count(*) FROM tasks AS t JOIN status AS s ON s.id = t.status_id GROUP BY s.name;"
USER_TASKS_COUNT = "SELECT u.fullname, count(*) FROM tasks AS t JOIN users AS u ON u.id = t.user_id GROUP BY u.fullname;"
TASKS_BY_EMAIL = """
SELECT t.title, t.description FROM tasks AS t JOIN users AS u ON u.id = t.user_id WHERE u.email LIKE '%@%s';
"""
EMPTY_DESCRIPTION_TASKS = "SELECT title, description FROM tasks WHERE description = '';"
GET_USERS_IN_PROGRESS_TASKS = """
SELECT
    users.fullname,
    tasks.title,
    tasks.description
FROM
    users
INNER JOIN
    tasks ON users.id = tasks.user_id
INNER JOIN
    status ON tasks.status_id = status.id
WHERE
    status.name = 'in progress';
"""

def execute_query(sql_stmt, returning=True):
    try:
        with create_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_stmt)
            if returning:
                results = cursor.fetchall()
                return results
            else:
                conn.commit()
    except RuntimeError as err:
        logging.error(f"Runtime error: {err}")

def get_tasks_by_user():
    user_id = input(f"Enter USER ID: ")
    return execute_query(TASKS_BY_USER % user_id)
def get_tasks_by_status():
    status = input(f"Enter STATUS: ")
    return execute_query(TASKS_BY_STATUS % status)

def update_status():
    task_id = input(f"Enter TASK ID: ")
    status_id = input(f"Enter STATUS ID(1-3): ")
    if status_id in AVAILABLE_STATUSES:
        execute_query(UPDATE_STATUS % (status_id, task_id), False)
    else:
        print("Wrong status id")

def get_users_without_tasks():
    return execute_query(USERS_WITHOUT_TASKS)

def add_new_task_for_user():
    user_id = input(f"Enter USER ID: ")
    title = input(f"Enter TASK TITLE: ")
    description = input(f"Enter TASK DESCRIPTION: ")
    execute_query(ADD_NEW_TASK % (title, description, random.choice(AVAILABLE_STATUSES), user_id), False)

def get_not_completed_tasks():
    return execute_query(ALL_NOT_COMPLETED_TASKS)

def delete_task():
    task_id = input(f"Enter TASK ID: ")
    execute_query(DELETE_TASK % task_id, False)

def get_user_by_email():
    email = input(f"Enter EMAIL: ")
    return execute_query(f"SELECT fullname, email FROM users WHERE email LIKE '%{email}%';")

def update_user_name():
    user_id = input(f"Enter USER ID: ")
    fullname = input(f"Enter FULLNAME: ")
    execute_query(UPDATE_USER_NAME %(fullname, user_id), False)

def get_count_of_each_status():
    return execute_query(TASK_STATUS_COUNT)

def get_tasks_by_email():
    email = input(f"Enter EMAIL: ")
    return execute_query(TASKS_BY_EMAIL % email)

def get_empty_description_tasks():
    return execute_query(EMPTY_DESCRIPTION_TASKS)

def get_users_with_in_progress_tasks():
    return execute_query(GET_USERS_IN_PROGRESS_TASKS)

def get_users_all_tasks_count():
    return execute_query(USER_TASKS_COUNT)

def input_error(func):
    """Common wrapper for intercept all exceptions
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
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
    GTU = "get_tasks_by_user"
    GTS = "get_tasks_by_status"
    UWT = "get_users_without_tasks"
    US = "update_status"
    ANTU = "add_new_task_for_user"
    NCT = "get_not_completed_tasks"
    DT = "delete_task"
    UBM = "get_user_by_email"
    USN = "update_user_name"
    CES = "get_count_of_each_status"
    TBE = "get_tasks_by_email"
    EDT = "get_empty_description_tasks"
    UWIT = "get_users_with_in_progress_tasks"
    UATC = "get_users_all_tasks_count"
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

if __name__ == "__main__":
    def greetings():
        print("""Welcome to the postgres db assistant bot!
        Available commands:
            ° get_tasks_by_user
            ° get_tasks_by_status
            ° get_users_without_tasks
            ° update_status
            ° add_new_task_for_user
            ° get_not_completed_tasks
            ° delete_task
            ° get_user_by_email
            ° update_user_name
            ° get_count_of_each_status
            ° get_tasks_by_email
            ° get_empty_description_tasks
            ° get_users_with_in_progress_tasks
            ° get_users_all_tasks_count
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
        elif command == Commands.GTU:
            print(get_tasks_by_user())
        elif command == Commands.GTS:
            print(get_tasks_by_status())
        elif command == Commands.UWT:
            print(get_users_without_tasks())
        elif command == Commands.US:
            update_status()
        elif command == Commands.ANTU:
            add_new_task_for_user()
        elif command == Commands.NCT:
            print(get_not_completed_tasks())
        elif command == Commands.DT:
            delete_task()
        elif command == Commands.UBM:
            print(get_user_by_email())
        elif command == Commands.USN:
            update_user_name()
        elif command == Commands.CES:
            print(get_count_of_each_status())
        elif command == Commands.TBE:
            print(get_tasks_by_email())
        elif command == Commands.EDT:
            print(get_empty_description_tasks())
        elif command == Commands.UWIT:
            print(get_users_with_in_progress_tasks())
        elif command == Commands.UATC:
            print(get_users_all_tasks_count())
        else:
            print("Invalid command.")
