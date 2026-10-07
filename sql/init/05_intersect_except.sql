-- Feature: INTERSECT and EXCEPT set operators (MariaDB 10.3+)
--
-- Task: find the intersection and difference of two sets of rows without JOIN boilerplate.
-- Problem: without INTERSECT/EXCEPT, set logic must be expressed through INNER JOIN and
-- LEFT JOIN + IS NULL. These produce correct results but hide the intent — a reader sees
-- join syntax and has to mentally decode it as a set operation. The code is also fragile:
-- if the join key changes, the NULL trick silently breaks.
--
-- SQL set operators treat two SELECT results as mathematical sets and combine them.
-- UNION     — all rows from A and B (duplicates removed).
-- INTERSECT — only rows that appear in both A and B (A ∩ B).
-- EXCEPT    — rows from A that do not appear in B (A \ B).
-- Both SELECTs must return the same number of columns with compatible types.

CREATE TABLE IF NOT EXISTS enrolled_python (
    student VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS enrolled_sql (
    student VARCHAR(100) NOT NULL
);

INSERT INTO enrolled_python (student) VALUES
    ('alice'), ('bob'), ('carol'), ('dave');

INSERT INTO enrolled_sql (student) VALUES
    ('bob'), ('carol'), ('eve'), ('frank');

-- OLD WAY: INTERSECT via JOIN
-- INNER JOIN returns rows where both tables have a match on the join condition.
-- This produces the correct result, but the intent (set intersection) is not obvious
-- from reading the query — it looks like a regular join, not a set operation.
SELECT p.student
FROM enrolled_python p
INNER JOIN enrolled_sql s ON p.student = s.student;

-- OLD WAY: EXCEPT via LEFT JOIN + IS NULL
-- LEFT JOIN keeps every row from the left table, filling right-side columns with NULL
-- when there is no match. WHERE s.student IS NULL isolates the unmatched left rows.
-- Again correct, but reads like a join trick rather than a set difference.
SELECT p.student
FROM enrolled_python p
LEFT JOIN enrolled_sql s ON p.student = s.student
WHERE s.student IS NULL;

-- NEW WAY: INTERSECT
-- Returns students who appear in both tables. Duplicate rows are removed automatically,
-- just like UNION — no DISTINCT needed.
SELECT student FROM enrolled_python
INTERSECT
SELECT student FROM enrolled_sql;

-- NEW WAY: EXCEPT
-- Returns students in the Python table that are not in the SQL table (Python \ SQL).
-- Order of the operands matters: swap them to get the opposite difference.
SELECT student FROM enrolled_python
EXCEPT
SELECT student FROM enrolled_sql;

-- EXCEPT: SQL \ Python
-- Reversing operands gives students in SQL but not in Python.
SELECT student FROM enrolled_sql
EXCEPT
SELECT student FROM enrolled_python;

-- chained: Python only, sorted
-- Operators can be chained; ORDER BY applies to the final combined result.
SELECT student FROM enrolled_python
EXCEPT
SELECT student FROM enrolled_sql
ORDER BY student;
