import mysql.connector

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",        # your MySQL username
            password="saad1223",        # your MySQL password
            database="employee_transport"
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        return None