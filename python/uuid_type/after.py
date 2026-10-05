"""
after.py — session IDs stored as UUID (MariaDB 10.7+)

16 bytes instead of 36. Invalid values rejected at INSERT time.
DEFAULT UUID() generates a valid v1 UUID automatically.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db import get_connection


def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS demo_sessions_new")
            cur.execute(
                "CREATE TABLE demo_sessions_new ("
                "  id INT AUTO_INCREMENT PRIMARY KEY,"
                "  session_id UUID NOT NULL DEFAULT UUID(),"
                "  user_name  VARCHAR(100) NOT NULL"
                ")"
            )
            for name in ("alice", "bob", "carol"):
                cur.execute(
                    "INSERT INTO demo_sessions_new (user_name) VALUES (%s)", (name,)
                )  #UUID() called automatically
            cur.execute("SELECT session_id, user_name FROM demo_sessions_new")
            rows = cur.fetchall()
        print("[after.py] UUID — auto-generated, 16 bytes, validated:")
        for session_id, name in rows:
            print(f"  {session_id}  {name}")
        print()
        print("Storage: UUID=16 bytes vs CHAR(36)=36 bytes (2.25x smaller)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
