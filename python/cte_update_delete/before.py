"""
before.py — UPDATE/DELETE with nested subqueries

The filtering logic is buried inside WHERE IN (SELECT ...).
MariaDB requires double nesting for UPDATE/DELETE subqueries
that reference the same table being modified.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db import get_connection

ORDERS = [
    ("alice",  250.00),
    ("bob",    50.00),
    ("carol",  1500.00),
    ("dave",   30.00),
    ("eve",    900.00),
]


def setup(cur):
    cur.execute("DROP TABLE IF EXISTS demo_orders")
    cur.execute(
        "CREATE TABLE demo_orders ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  customer VARCHAR(100) NOT NULL,"
        "  amount DECIMAL(10,2) NOT NULL,"
        "  status VARCHAR(20) NOT NULL DEFAULT 'pending'"
        ")"
    )
    for customer, amount in ORDERS:
        cur.execute(
            "INSERT INTO demo_orders (customer, amount) VALUES (%s, %s)",
            (customer, amount),
        )


def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            setup(cur)
            cur.execute(  #subquery nested twice — MariaDB limitation
                "UPDATE demo_orders SET status = 'approved'"
                " WHERE id IN ("
                "   SELECT id FROM ("
                "     SELECT id FROM demo_orders WHERE amount >= 100.00"
                "   ) AS sub"
                " )"
            )
            cur.execute(
                "DELETE FROM demo_orders"
                " WHERE id IN ("
                "   SELECT id FROM ("
                "     SELECT id FROM demo_orders WHERE amount < 100.00"
                "   ) AS sub"
                " )"
            )
            cur.execute("SELECT customer, amount, status FROM demo_orders ORDER BY amount")
            rows = cur.fetchall()
        print("[before.py] After UPDATE+DELETE via subquery:")
        for customer, amount, status in rows:
            print(f"  {customer:<8} {amount:>8.2f}  {status}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
