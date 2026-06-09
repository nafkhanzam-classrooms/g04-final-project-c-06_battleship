import hashlib

from server.database import get_connection
from server.ranking_service import ensure_player


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(username, password):
    username = username.strip()

    if not username:
        return False, "Username wajib diisi"

    if not password:
        return False, "Password wajib diisi"

    if len(username) < 3:
        return False, "Username minimal 3 karakter"

    if len(password) < 4:
        return False, "Password minimal 4 karakter"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username FROM users
        WHERE username = ?
    """, (username,))

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False, "Username sudah dipakai"

    cursor.execute("""
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
    """, (username, hash_password(password)))

    conn.commit()
    conn.close()

    ensure_player(username)

    return True, "Register berhasil"


def login_user(username, password):
    username = username.strip()

    if not username:
        return False, "Username wajib diisi"

    if not password:
        return False, "Password wajib diisi"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT password_hash FROM users
        WHERE username = ?
    """, (username,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "Username tidak ditemukan"

    stored_password_hash = row[0]

    if stored_password_hash != hash_password(password):
        return False, "Password salah"

    ensure_player(username)

    return True, "Login berhasil"