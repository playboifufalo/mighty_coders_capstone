-- Feature: INTERSECT and EXCEPT set operators (MariaDB 10.3+)

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

SELECT p.student
FROM enrolled_python p
INNER JOIN enrolled_sql s ON p.student = s.student;

-- OLD WAY: EXCEPT via LEFT JOIN + IS NULL

SELECT p.student
FROM enrolled_python p
LEFT JOIN enrolled_sql s ON p.student = s.student
WHERE s.student IS NULL;

-- NEW WAY: INTERSECT — students enrolled in both courses

SELECT student FROM enrolled_python
INTERSECT
SELECT student FROM enrolled_sql;

-- NEW WAY: EXCEPT — students in Python but not SQL

SELECT student FROM enrolled_python
EXCEPT
SELECT student FROM enrolled_sql;

-- EXCEPT the other way: in SQL but not Python

SELECT student FROM enrolled_sql
EXCEPT
SELECT student FROM enrolled_python;

-- Operators can be chained: students only in Python, sorted
SELECT student FROM enrolled_python
EXCEPT
SELECT student FROM enrolled_sql
ORDER BY student;
