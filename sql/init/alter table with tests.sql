SELECT * FROM employees;

ALTER TABLE employees
ADD COLUMN email VARCHAR(150);

ALTER TABLE employees
ADD COLUMN joining_date DATE;

UPDATE employees
SET email = 'rahul@gmail.com',
    joining_date = '2024-01-15'
WHERE emp_id = 101;

UPDATE employees
SET email = 'john@gmail.com',
    joining_date = '2023-06-20'
WHERE emp_id = 102;

ALTER TABLE employees
ADD COLUMN email VARCHAR(150);