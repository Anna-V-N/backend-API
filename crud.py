from database import get_db

def create_user(username: str, email: str, full_name: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO users (username, email, full_name) VALUES (?, ?, ?)
    """, (username, email, full_name))
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user(user_id: int, username: str = None, email: str = None, full_name: str = None):
    conn = get_db()
    cursor = conn.cursor()
    user = get_user(user_id)
    if user:
        cursor.execute("""
        UPDATE users
        SET username = COALESCE(?, username),
            email = COALESCE(?, email),
            full_name = COALESCE(?, full_name)
        WHERE id = ?
        """, (username, email, full_name, user_id))
        conn.commit()
    conn.close()

def deactivate_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users SET is_active = 0 WHERE id = ?
    """, (user_id,))
    conn.commit()
    conn.close()
