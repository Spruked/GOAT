import sqlite3
from passlib.context import CryptContext
from app.models.user import UserCreate, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DB_PATH = "../skg_goat.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def create_user(user: UserCreate):
    hashed = pwd_context.hash(user.password)
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                role TEXT NOT NULL,
                onboarding_state TEXT,
                blocked INTEGER DEFAULT 0
            )
        """)
        c.execute(
            "INSERT INTO users (email, hashed_password, role, blocked) VALUES (?, ?, ?, ?)",
            (user.email, hashed, "user", 0)
        )
        conn.commit()
        return c.lastrowid

def get_user_by_email(email: str):
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("SELECT id, email, hashed_password, role, onboarding_state, blocked FROM users WHERE email = ?", (email,))
            row = c.fetchone()
            if row:
                return {
                    "id": row[0],
                    "email": row[1],
                    "hashed_password": row[2],
                    "role": row[3],
                    "onboarding_state": row[4],
                    "blocked": bool(row[5]),
                }
            return None
    except sqlite3.OperationalError:
        # Table doesn't exist
        return None

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_all_users():
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("SELECT id, email, role, onboarding_state, created_at, blocked FROM users")
            rows = c.fetchall()
            return [
                {
                    "id": row[0],
                    "email": row[1],
                    "role": row[2],
                    "onboarding_state": row[3],
                    "created_at": row[4],
                    "blocked": bool(row[5]),
                }
                for row in rows
            ]
    except sqlite3.OperationalError:
        return []

def delete_user(user_id: int):
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return c.rowcount > 0
    except sqlite3.OperationalError:
        return False

def block_user(user_id: int):
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET blocked = 1 WHERE id = ?", (user_id,))
            conn.commit()
            return c.rowcount > 0
    except sqlite3.OperationalError:
        return False

def unblock_user(user_id: int):
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET blocked = 0 WHERE id = ?", (user_id,))
            conn.commit()
            return c.rowcount > 0
    except sqlite3.OperationalError:
        return False
