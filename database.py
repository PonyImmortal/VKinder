import psycopg2
from config import *

conn = psycopg2.connect(
    user=user,
    password=password,
    database=db_name
)

conn.autocommit = True


def create_table_seen_users(conn):
    """Создание таблицы просмотренные пользователи"""
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS seen_users(
            id serial,
            vk_id INTEGER,
            seen_user_id INTEGER);"""
    )


def insert_data_seen_users(vk_id, seen_user_id):
    """Заполнение таблицы просмотренные пользователи"""
    with conn.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO seen_users (vk_id, seen_user_id)
            VALUES (%s, %s);""", (vk_id, seen_user_id)
        )


def select(vk_id, seen_user_id):
    """Подбор пользователей из непросмотренных"""
    with conn.cursor() as cursor:
        cursor.execute(
            f"""SELECT vk_id, seen_user_id FROM seen_users WHERE vk_id=%s AND seen_user_id=%s;""",
            (vk_id, seen_user_id))
        return cursor.fetchone()


def drop_seen_users(user_id):
    """Удаление таблицы"""
    with conn.cursor() as cursor:
        cursor.execute(
            f"""DELETE FROM seen_users WHERE vk_id=%s;""", (user_id,))


with conn.cursor() as cur:
    def creating_database():
        create_table_seen_users(conn)
