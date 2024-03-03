# -*- coding: utf-8 -*-
"""
Скрипт для заповнення таблиць у базі даних через Faker"""

import logging
import random
from psycopg2 import DatabaseError
from faker import Faker
import psycopg2
from connect import HOST, DATABASE, USER, PASSWORD

STUDENTS_COUNT = 50
TASKS_COUNT = 180
fake = Faker()

def main():
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    # Додавання студентів
    for _ in range(STUDENTS_COUNT):
        cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fake.name(), fake.email()))
    # Додавання тасок
    for task_id in range(1, TASKS_COUNT + 1):
        if task_id > STUDENTS_COUNT:
            task_id = task_id % STUDENTS_COUNT or STUDENTS_COUNT
        cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                       (fake.word(), fake.text(), random.randint(1, 3), task_id))

    try:
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
