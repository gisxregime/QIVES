import hashlib, secrets
import sqlite3
from datetime import datetime

from database import get_db_conn


def hash_password(password, salt_hex):
    h = hashlib.sha256()
    h.update(bytes.fromhex(salt_hex) + password.encode("utf-8"))
    return h.hexdigest()

def create_user(username, password):
    conn = get_db_conn()
    c = conn.cursor()
    salt = secrets.token_bytes(16)
    salt_hex = salt.hex()
    pw_hash = hash_password(password, salt_hex)
    try:
        c.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                  (username, pw_hash, salt_hex))
        uid = c.lastrowid
        c.execute("INSERT INTO progress (user_id, chapter) VALUES (?, ?)", (uid, 1))
        conn.commit()
        return uid
    except sqlite3.IntegrityError:
        print("Username already exists.")
        return None
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    if hash_password(password, row["salt"]) == row["password_hash"]:
        return row["id"]
    return None

def get_user_progress(user_id):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT chapter FROM progress WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row["chapter"] if row else 1

def set_user_progress(user_id, chapter):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("UPDATE progress SET chapter = ? WHERE user_id = ?", (chapter, user_id))
    conn.commit()
    conn.close()

def log_action(user_id, action):
    conn = get_db_conn()
    c = conn.cursor()
    ts = datetime.utcnow().isoformat() + "Z"
    c.execute("INSERT INTO forensic_logs (user_id, action, timestamp) VALUES (?, ?, ?)",
              (user_id, action, ts))
    conn.commit()
    conn.close()

def save_seed(user_id, chapter, seed):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO seeds (user_id, chapter, seed) VALUES (?, ?, ?)",
              (user_id, chapter, seed))
    conn.commit()
    conn.close()

def get_seed(user_id, chapter):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT seed FROM seeds WHERE user_id = ? AND chapter = ?", (user_id, chapter))
    row = c.fetchone()
    conn.close()
    return row["seed"] if row else None

def register_evidence(user_id, chapter, path):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("INSERT INTO evidence_registry (user_id, chapter, file_path, description) VALUES (?, ?, ?, ?)",
              (user_id, chapter, path, "Correct next file"))
    conn.commit()
    conn.close()