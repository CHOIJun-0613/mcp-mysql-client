import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8mb4', use_unicode=True, collation='utf8mb4_unicode_ci'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_db_schema():
    connection = get_db_connection()
    if connection is None: return "DB 연결 실패"
    
    cursor = connection.cursor()
    schema_info = ""
    try:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for (table_name,) in tables:
            schema_info += f"Table `{table_name}` (\n"
            cursor.execute(f"DESCRIBE `{table_name}`;")
            columns = cursor.fetchall()
            for col in columns:
                schema_info += f"  `{col[0]}` {col[1]},\n"
            schema_info += ");\n\n"
    except mysql.connector.Error as e:
        return f"스키마 조회 오류: {e}"
    finally:
        cursor.close()
        connection.close()
    return schema_info

def execute_query(query: str):
    connection = get_db_connection()
    if connection is None: return "DB 연결 실패", None

    cursor = connection.cursor(dictionary=True)
    result_data = None
    try:
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            result_data = cursor.fetchall()
            # Convert bytes to hex string for UUIDs
            for row in result_data:
                for key, value in row.items():
                    if isinstance(value, bytes):
                        row[key] = value.hex()
            print(f"Raw data from DB: {result_data}")
        else:
            connection.commit()
            result_data = f"{cursor.rowcount} rows affected."
    except mysql.connector.Error as e:
        return f"쿼리 실행 오류: {e}", None
    finally:
        cursor.close()
        connection.close()
    return "쿼리 성공", result_data