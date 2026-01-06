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
                onboarding_state TEXT
            )
        """)
        c.execute(
            "INSERT INTO users (email, hashed_password, role) VALUES (?, ?, ?)",
            (user.email, hashed, "user")
        )
        conn.commit()
        return c.lastrowid

def get_user_by_email(email: str):
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("SELECT id, email, hashed_password, role, onboarding_state FROM users WHERE email = ?", (email,))
            row = c.fetchone()
            if row:
                return {
                    "id": row[0],
                    "email": row[1],
                    "hashed_password": row[2],
                    "role": row[3],
                    "onboarding_state": row[4],
                }
            return None
    except sqlite3.OperationalError:
        # Table doesn't exist
        return None

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
