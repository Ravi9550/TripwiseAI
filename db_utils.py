import os

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set. Add it to your deployment environment variables.")
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def init_auth_db():
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trips (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                thread_id TEXT NOT NULL,
                trip_name TEXT NOT NULL,
                user_query TEXT NOT NULL,
                file_content TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("ALTER TABLE trips ADD COLUMN IF NOT EXISTS file_content TEXT")
        conn.commit()


def create_user(username: str, password_hash: str):
    with get_db_connection() as conn:
        try:
            row = conn.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (%s, %s)
                RETURNING id, username
                """,
                (username, password_hash),
            ).fetchone()
            conn.commit()
            return row
        except psycopg.errors.UniqueViolation:
            conn.rollback()
            return None


def get_user_by_username(username: str):
    with get_db_connection() as conn:
        return conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = %s",
            (username,),
        ).fetchone()


def save_user_trip(user_id: int, thread_id: str, trip_name: str, user_query: str, file_content: str):
    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO trips (user_id, thread_id, trip_name, user_query, file_content)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, thread_id, trip_name, user_query, file_content),
        )
        conn.commit()


def get_user_trips(user_id: int):
    with get_db_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, thread_id, trip_name, user_query, file_content, created_at
            FROM trips
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def rename_user_trip(user_id: int, trip_id: int, new_name: str) -> bool:
    new_name = new_name.strip()
    if not new_name:
        return False

    with get_db_connection() as conn:
        result = conn.execute(
            "UPDATE trips SET trip_name = %s WHERE id = %s AND user_id = %s",
            (new_name, trip_id, user_id),
        )
        conn.commit()
        return result.rowcount > 0


def delete_user_trip(user_id: int, trip_id: int) -> bool:
    with get_db_connection() as conn:
        result = conn.execute(
            "DELETE FROM trips WHERE id = %s AND user_id = %s",
            (trip_id, user_id),
        )
        conn.commit()
        return result.rowcount > 0
