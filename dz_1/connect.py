import psycopg2
from contextlib import contextmanager


HOST = "localhost"
DATABASE = "hw"
USER = "postgres"
PASSWORD = "567234" # POSTGRES_PASSWORD

@contextmanager
def create_connect():
    try:
        conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        try:
            yield conn
        finally:
            conn.close()
    except psycopg2.OperationalError:
        print("Connection failed")
