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

def get_facts_about_user(about_user_id: str) -> list:
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        """SELECT fact FROM global_memory
           WHERE about_user_id = %s
           ORDER BY ts DESC LIMIT 20""",
        (about_user_id,)
    )
    rows = cur.fetchall()
    cur.close()
    con.close()
    return [r[0] for r in rows]

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