import os
import sqlite3
import hashlib

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "healthcare.db"
)

print("DB Path:", DB_PATH)

def make_hash(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def create_user(
    username,
    email,
    password,
    role="Patient"
):

    conn = sqlite3.connect("database/healthcare.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username,email,password,role)
            VALUES (?,?,?,?)
            """,
            (
                username,
                email,
                make_hash(password),
                role
            )
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(username, password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Debug
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    print("Tables:", cursor.fetchall())

    cursor.execute(
        """
        SELECT id,
               username,
               email,
               role
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            make_hash(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


def get_all_users():

    conn = sqlite3.connect("database/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,
               username,
               email,
               role
        FROM users
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users