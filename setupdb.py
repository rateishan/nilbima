import pymysql
import bcrypt

# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "#@19is16Pro"
DB_NAME = "nilbima"

def create_first_user():
    try:
        # 1. Connect to MySQL
        con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        cur = con.cursor()

        # 2. Define your first credentials
        first_username = "admin"
        first_password = "admin123" # Change this to whatever you want

        # 3. Encrypt the password using bcrypt
        hashed_password = bcrypt.hashpw(first_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 4. Insert into the login table
        # Make sure the table name and column names match your DB exactly
        query = "INSERT INTO mainlog (username, password) VALUES (%s, %s)"
        cur.execute(query, (first_username, hashed_password))

        con.commit()
        print(f"Successfully created first user: {first_username}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'con' in locals():
            con.close()

if __name__ == "__main__":
    create_first_user()