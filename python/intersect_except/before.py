"""
before.py — set operations via JOIN and subqueries

Finding common/unique students without INTERSECT/EXCEPT requires
JOIN constructs that obscure the intent.
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
            cur.execute(  #intersection via INNER JOIN
                "SELECT p.student FROM demo_enrolled_python p"
                " INNER JOIN demo_enrolled_sql s ON p.student = s.student"
                " ORDER BY p.student"
            )
            both = [r[0] for r in cur.fetchall()]
            cur.execute(  #difference via LEFT JOIN + IS NULL
                "SELECT p.student FROM demo_enrolled_python p"
                " LEFT JOIN demo_enrolled_sql s ON p.student = s.student"
                " WHERE s.student IS NULL ORDER BY p.student"
            )
            only_python = [r[0] for r in cur.fetchall()]
        print("[before.py] In both courses (INNER JOIN):", both)
        print("[before.py] Python only  (LEFT JOIN+NULL):", only_python)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
