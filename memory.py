import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DB_URL)

def init_db():
    con = get_conn()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_update_log (
            user_id TEXT NOT NULL,
            version TEXT NOT NULL,
            PRIMARY KEY (user_id, version)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS slash_command_log (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            command TEXT NOT NULL,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    cur.close()
    con.close()

def get_history(user_id: str, limit: int = 15) -> list:
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        """SELECT role, content FROM history
           WHERE user_id = %s
           ORDER BY ts DESC LIMIT %s""",
        (user_id, limit)
    )
    rows = cur.fetchall()
    cur.close()
    con.close()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

def save_message(user_id: str, role: str, content: str):
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO history (user_id, role, content) VALUES (%s, %s, %s)",
        (user_id, role, content)
    )
    con.commit()
    cur.close()
    con.close()

def clear_history(user_id: str):
    con = get_conn()
    cur = con.cursor()
    cur.execute("DELETE FROM history WHERE user_id = %s", (user_id,))
    cur.execute("DELETE FROM global_memory WHERE about_user_id = %s", (user_id,))
    cur.execute("DELETE FROM user_profiles WHERE user_id = %s", (user_id,))
    con.commit()
    cur.close()
    con.close()

def save_global_fact(about_user_id: str, about_user_name: str, fact: str):
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        """INSERT INTO global_memory (about_user_id, about_user_name, fact)
           VALUES (%s, %s, %s)""",
        (about_user_id, about_user_name, fact)
    )
    con.commit()
    cur.close()
    con.close()

def get_global_memory(limit: int = 30) -> list:
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        """SELECT about_user_name, fact, ts
           FROM global_memory
           ORDER BY ts DESC LIMIT %s""",
        (limit,)
    )
    rows = cur.fetchall()
    cur.close()
    con.close()
    return [{"name": r[0], "fact": r[1], "ts": str(r[2])} for r in rows]

def save_user_profile(user_id: str, display_name: str, known_as: str = None):
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        """INSERT INTO user_profiles (user_id, display_name, known_as, updated_at)
           VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
           ON CONFLICT (user_id) DO UPDATE
           SET display_name = EXCLUDED.display_name,
               known_as = COALESCE(EXCLUDED.known_as, user_profiles.known_as),
               updated_at = CURRENT_TIMESTAMP""",
        (user_id, display_name, known_as)
    )
    con.commit()
    cur.close()
    con.close()

def get_user_profile(user_id: str) -> dict:
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        "SELECT display_name, known_as FROM user_profiles WHERE user_id = %s",
        (user_id,)
    )
    row = cur.fetchone()
    cur.close()
    con.close()
    if row:
        return {"display_name": row[0], "known_as": row[1]}
    return None

def get_active_users(minutes: int = 10) -> list:
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        """SELECT DISTINCT up.known_as, gm.fact
           FROM user_profiles up
           LEFT JOIN global_memory gm ON gm.about_user_id = up.user_id
           WHERE up.known_as IS NOT NULL
           AND up.user_id IN (
               SELECT DISTINCT user_id FROM history
               WHERE ts >= NOW() - (INTERVAL '1 minute' * %s)
           )
           ORDER BY up.known_as""",
        (minutes,)
    )
    rows = cur.fetchall()
    cur.close()
    con.close()
    return [{"name": r[0], "fact": r[1]} for r in rows]

def has_seen_update(user_id: str, version: str) -> bool:
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        "SELECT 1 FROM user_update_log WHERE user_id = %s AND version = %s",
        (user_id, version)
    )
    result = cur.fetchone()
    cur.close()
    con.close()
    return result is not None

def mark_update_seen(user_id: str, version: str):
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO user_update_log (user_id, version) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        (user_id, version)
    )
    con.commit()
    cur.close()
    con.close()

def log_slash_command(user_id: str, command: str):
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO slash_command_log (user_id, command) VALUES (%s, %s)",
        (user_id, command)
    )
    con.commit()
    cur.close()
    con.close()