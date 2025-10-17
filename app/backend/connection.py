import os
import pymysql

SQL_DUMP_PATH = os.path.join(os.path.dirname(__file__), "db_crm.sql")


DB_NAME = "db_crm"

def _connect_server():
    """Connect to MySQL server without specifying any database."""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        cursorclass=pymysql.cursors.DictCursor
    )

def _database_exists():
    """Return True if DB exists."""
    conn = _connect_server()
    with conn.cursor() as cursor:
        cursor.execute("SHOW DATABASES LIKE %s", (DB_NAME,))
        exists = cursor.fetchone() is not None
    conn.close()
    return exists

def _table_count():
    """Return table count if DB exists, else 0."""
    if not _database_exists():
        return 0
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        count = len(cursor.fetchall())
    conn.close()
    return count

def _import_sql_dump():
    """Import the SQL dump file (creates DB if missing)."""
    print("🔁 Importing SQL dump... Please wait.")
    with open(SQL_DUMP_PATH, "r", encoding="utf-8") as f:
        sql_content = f.read()

    conn = _connect_server()
    cursor = conn.cursor()

    # Run each SQL statement one by one
    statements = sql_content.split(';')
    for stmt in statements:
        stmt = stmt.strip()
        if not stmt or stmt.startswith('--') or stmt.startswith('/*'):
            continue
        try:
            cursor.execute(stmt)
        except Exception as e:
            # Ignore known harmless system commands
            if not stmt.lower().startswith(("set ", "/*!")):
                print(f"⚠️ Skipped statement due to error: {e}")

    conn.commit()
    conn.close()
    print("✅ Database and tables successfully imported.")

# ------------------------------
# 🔹 Main Function
# ------------------------------

def get_connection():
    """
    Ensures db_crm exists and is populated.
    Returns a working pymysql connection.
    """

    # Check if database exists
    if not _database_exists():
        print(f"⚠️ Database '{DB_NAME}' not found — importing from SQL file...")
        _import_sql_dump()

    # Check if tables exist
    elif _table_count() == 0:
        print(f"⚠️ No tables found in '{DB_NAME}' — importing structure...")
        _import_sql_dump()

    # Return working connection (only now DB is guaranteed to exist)
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.err.OperationalError as e:
        # Failsafe in case import failed
        print(f"❌ Connection failed even after import: {e}")
        raise
