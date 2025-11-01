import os
import pymysql
import sys
from flask import flash
from flask_socketio import emit

SQL_DUMP_PATH = os.path.join(os.path.dirname(__file__), "db_crm.sql")

# Database connection details
DB_NAME = "db_crm"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""



def _connect_server():
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            cursorclass=pymysql.cursors.DictCursor,
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS 
        )
    except pymysql.err.OperationalError as e:
        flash("Could not connect to MySQL server. ", "error")
        print(f"Error: {e}")
        # Exit if can't connect
        sys.exit(1)



def _connect_db():
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.err.OperationalError as e:
        print(f"Error: {e}")
        return None

def _database_exists():
    conn = _connect_server()
    exists = False
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW DATABASES LIKE %s", (DB_NAME,))
            exists = cursor.fetchone() is not None
    except Exception as e:
        flash("Error checking database existence. ", "error")
    finally:
        conn.close()
    return exists

def _table_count():
    if not _database_exists():
        return 0
        
    conn = _connect_db()
    if conn is None:
        return 0 # Can't connect, so assume 0 tables

    count = 0
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            count = len(cursor.fetchall())
    except Exception as e:
        flash("Error checking table count. ", "error")
    finally:
        conn.close()
    return count

def _import_sql_dump():
    
    conn = _connect_server()
    
    current_statement = ""
    delimiter = ";"
    
    try:
        with open(SQL_DUMP_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line_strip = line.strip()

                
                if line_strip.startswith('--') or line_strip.startswith('/*') or not line_strip:
                    continue
                    
                
                if line_strip.lower().startswith("delimiter "):
                    delimiter = line_strip.split(" ")[-1].strip()
                    
                    continue
                    
                current_statement += line
                
                
                if line_strip.endswith(delimiter):
                    
                    statement_to_run = current_statement.rsplit(delimiter, 1)[0].strip()
                    
                    if statement_to_run: # Avoid empty statements
                        try:
                            with conn.cursor() as cursor:
                                cursor.execute(statement_to_run)
                        except Exception as e:
                            
                            if not statement_to_run.lower().startswith(("set ", "/*!")):
                                flash(f"Error executing statement: {statement_to_run[:50]}... ", "error")
                                
                                
                    current_statement = "" 
                    
        conn.commit()
        
    except FileNotFoundError:
        flash("SQL dump file not found. ", "error")
        raise
    except Exception as e:
        flash(f"Error during SQL import: {e}", "error")
        conn.rollback()
        raise
    finally:
        conn.close()



def get_connection():    

    # Check if database exists
    if not _database_exists():
        flash(f"Database '{DB_NAME}' creating.(Refresh this page)", "info")
        try:
            _import_sql_dump()
        except Exception as e:
            flash(f"Import failed. Cannot proceed. Error: {e}", "error")
            return None

    # Check if tables exist 
    elif _table_count() == 0:
        flash(f"Database '{DB_NAME}' has no tables. Importing...", "info")
        try:
            _import_sql_dump()
        except Exception as e:
            flash(f"Import failed. Cannot proceed. Error: {e}", "error")
            return None
    
    else:
        print("Database Exists with tables.")

    # Return working connection 
    print(f"Attempting to connect to '{DB_NAME}'...")
    final_conn = _connect_db()
    
    if final_conn:
        return final_conn
    else:
        flash(f"Failed to connect to database '{DB_NAME}'.", "error")
        return None

if __name__ == "__main__":
    
    flash("Running connection test...", "info")
    
    connection = get_connection()
    
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM `country`")
                results = cursor.fetchall()
                for row in results:
                    print(f"- ID: {row['id']}, Code: {row['code']}, Name: {row['name']}")
        except Exception as e:
            flash(f"Test query failed. Error: {e}", "error")
        finally:
            connection.close()
            flash("Connection closed.", "info")
    else:
        flash("Connection test failed. Could not establish database connection.", "error")
