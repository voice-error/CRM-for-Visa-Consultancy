import pymysql
import os

SQL_FILE = os.path.join("app", "backend", "db_crm.sql")

def create_db_and_import():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password=""
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS db_crm CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        conn.commit()
    finally:
        conn.close()

    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="db_crm",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            with open(SQL_FILE, "r", encoding="utf-8") as f:
                sql_commands = f.read()

            commands = sql_commands.split(";")

            for command in commands:
                command = command.strip()
                if command and not command.startswith("--") and not command.startswith("/*"):
                    try:
                        cursor.execute(command)
                    except Exception as e:
                        print(f"⚠️ Skipped: {command[:50]}...  -> {e}")
    finally:
        conn.close()

def get_connection():
    create_db_and_import()

    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="db_crm",
        cursorclass=pymysql.cursors.DictCursor
    )