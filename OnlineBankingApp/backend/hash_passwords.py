from werkzeug.security import generate_password_hash
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tad@123",
    database="online_banking_db"
)

cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT user_id, password_hash FROM users")
users = cursor.fetchall()

for user in users:
    hashed = generate_password_hash(user["password_hash"])
    cursor.execute(
        "UPDATE users SET password_hash=%s WHERE user_id=%s",
        (hashed, user["user_id"])
    )

conn.commit()
cursor.close()
conn.close()
