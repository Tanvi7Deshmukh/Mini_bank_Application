import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tad@123",
        database="online_banking_db",
        buffered=True
    )
