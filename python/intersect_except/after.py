"""
after.py — set operations via INTERSECT and EXCEPT (MariaDB 10.3+)

Intent is immediately clear from the operator name.
No JOIN boilerplate needed.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db import get_connection

PYTHON_STUDENTS = ["alice", "bob", "carol", "dave"]
SQL_STUDENTS    = ["bob", "carol", "eve", "frank"]


def setup(cur):
    cur.execute("DROP TABLE IF EXISTS demo_enrolled_python")
    cur.execute("DROP TABLE IF EXISTS demo_enrolled_sql")
    cur.execute("CREATE TABLE demo_enrolled_python (student VARCHAR(100) NOT NULL)")
    cur.execute("CREATE TABLE demo_enrolled_sql    (student VARCHAR(100) NOT NULL)")
    for s in PYTHON_STUDENTS:
        cur.execute("INSERT INTO demo_enrolled_python VALUES (%s)", (s,))
    for s in SQL_STUDENTS:
        cur.execute("INSERT INTO demo_enrolled_sql VALUES (%s)", (s,))


def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            setup(cur)
            cur.execute(  #INTERSECT — students in both courses
                "SELECT student FROM demo_enrolled_python"
                " INTERSECT"
                " SELECT student FROM demo_enrolled_sql"
                " ORDER BY student"
            )
            both = [r[0] for r in cur.fetchall()]
            cur.execute(  #EXCEPT — in Python but not SQL
                "SELECT student FROM demo_enrolled_python"
                " EXCEPT"
                " SELECT student FROM demo_enrolled_sql"
                " ORDER BY student"
            )
            only_python = [r[0] for r in cur.fetchall()]
            cur.execute(  #EXCEPT reversed — in SQL but not Python
                "SELECT student FROM demo_enrolled_sql"
                " EXCEPT"
                " SELECT student FROM demo_enrolled_python"
                " ORDER BY student"
            )
            only_sql = [r[0] for r in cur.fetchall()]
        print("[after.py] INTERSECT (both courses):", both)
        print("[after.py] EXCEPT    (Python only): ", only_python)
        print("[after.py] EXCEPT    (SQL only):    ", only_sql)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
