from server.database import get_connection


def ensure_player(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO players (username)
        VALUES (?)
    """, (username,))

    conn.commit()
    conn.close()


def record_match_result(winner_username, loser_username):
    ensure_player(winner_username)
    ensure_player(loser_username)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE players
        SET total_match = total_match + 1,
            win = win + 1
        WHERE username = ?
    """, (winner_username,))

    cursor.execute("""
        UPDATE players
        SET total_match = total_match + 1,
            lose = lose + 1
        WHERE username = ?
    """, (loser_username,))

    conn.commit()
    conn.close()


def record_shot(username, result):
    ensure_player(username)

    conn = get_connection()
    cursor = conn.cursor()

    if result == "HIT":
        cursor.execute("""
            UPDATE players
            SET hit_count = hit_count + 1
            WHERE username = ?
        """, (username,))
    elif result == "MISS":
        cursor.execute("""
            UPDATE players
            SET miss_count = miss_count + 1
            WHERE username = ?
        """, (username,))

    conn.commit()
    conn.close()


def get_leaderboard(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, total_match, win, lose, hit_count, miss_count
        FROM players
        ORDER BY win DESC, hit_count DESC, total_match DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    leaderboard = []

    for row in rows:
        username, total_match, win, lose, hit_count, miss_count = row
        win_rate = 0

        if total_match > 0:
            win_rate = round((win / total_match) * 100, 2)

        leaderboard.append({
            "username": username,
            "total_match": total_match,
            "win": win,
            "lose": lose,
            "hit_count": hit_count,
            "miss_count": miss_count,
            "win_rate": win_rate
        })

    return leaderboard