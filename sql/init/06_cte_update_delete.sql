-- Feature: UPDATE / DELETE with CTEs (MariaDB 10.2+)

CREATE TABLE IF NOT EXISTS orders (
    id         INT          AUTO_INCREMENT PRIMARY KEY,
    customer   VARCHAR(100) NOT NULL,
    amount     DECIMAL(10,2) NOT NULL,
    status     VARCHAR(20)  NOT NULL DEFAULT 'pending'
);

INSERT INTO orders (customer, amount, status) VALUES
    ('alice',  250.00, 'pending'),
    ('bob',    50.00,  'pending'),
    ('carol',  1500.00,'pending'),
    ('dave',   30.00,  'pending'),
    ('eve',    900.00, 'pending');

-- OLD WAY: UPDATE with a subquery — logic buried inside WHERE

UPDATE orders
SET status = 'approved'
WHERE id IN (
    SELECT id FROM (
        SELECT id FROM orders WHERE amount >= 100.00
    ) AS sub
);

SELECT * FROM orders;

-- Reset

UPDATE orders SET status = 'pending';

-- NEW WAY: WITH clause makes the selection logic readable on its own

WITH high_value AS (
    SELECT id FROM orders WHERE amount >= 100.00
)
UPDATE orders
SET status = 'approved'
WHERE id IN (SELECT id FROM high_value);

SELECT * FROM orders;

-- DELETE with CTE — remove small orders

WITH small_orders AS (
    SELECT id FROM orders WHERE amount < 100.00
)
DELETE FROM orders
WHERE id IN (SELECT id FROM small_orders);

SELECT * FROM orders;

-- CTE can reference multiple conditions — still readable

WITH vip_customers AS (
    SELECT customer FROM orders WHERE amount > 500.00
),
pending_vip AS (
    SELECT o.id
    FROM orders o
    INNER JOIN vip_customers v ON o.customer = v.customer
    WHERE o.status = 'pending'
)
UPDATE orders
SET status = 'priority'
WHERE id IN (SELECT id FROM pending_vip);

SELECT * FROM orders;
