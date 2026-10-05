"""
before.py — session IDs stored as CHAR(36)

No validation: any string is accepted. Sort order is lexicographic,
not time-based. Storage: 36 bytes per value.
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db import get_connection


def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS demo_sessions_old")
            cur.execute(
                "CREATE TABLE demo_sessions_old ("
                "  id INT AUTO_INCREMENT PRIMARY KEY,"
                "  session_id CHAR(36) NOT NULL,"
                "  user_name  VARCHAR(100) NOT NULL"
                ")"
            )
            for name in ("alice", "bob", "carol"):
                cur.execute(
                    "INSERT INTO demo_sessions_old (session_id, user_name) VALUES (%s, %s)",
                    (str(uuid.uuid4()), name),
                )
            cur.execute(
                "INSERT INTO demo_sessions_old (session_id, user_name) VALUES (%s, %s)",
                ("not-a-uuid-at-all", "mallory"),  #accepted silently
            )
            cur.execute("SELECT session_id, user_name FROM demo_sessions_old")
            rows = cur.fetchall()
        print("[before.py] CHAR(36) — invalid UUID accepted silently:")
        for session_id, name in rows:
            valid = len(session_id) == 36 and session_id.count("-") == 4
            flag = "OK" if valid else "INVALID"
            print(f"  [{flag}] {session_id}  {name}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
