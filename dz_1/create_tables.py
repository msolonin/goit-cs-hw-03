# -*- coding: utf-8 -*-
"""
Скрипт для створення таблиць у базі даних"""

import logging
from psycopg2 import DatabaseError
from connect import create_connect

SCHEMA_FILE = "create_tables.sql"

def create_table(conn, sql_stmt: str):
    c = conn.cursor()
    try:
        c.execute(sql_stmt)
        conn.commit()
    except DatabaseError as err:
        logging.error(f"Database error: {err}")
        conn.rollback()
    finally:
        c.close()


def main():
    # Read schema from file
    with open(SCHEMA_FILE, 'r') as schema_file:
        schema_sql = schema_file.read()
    # Try to create tables
    try:
        with create_connect() as conn:
            create_table(conn, schema_sql)
    except RuntimeError as err:
        logging.error(f"Runtime error: {err}")


if __name__ == "__main__":
    main()
