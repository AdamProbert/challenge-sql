-- Solution for advanced subquery & aggregation challenge
SELECT
    d.department_name AS department,
    COUNT(e.employee_id) AS employee_count,
    ROUND(AVG(e.salary), 2) AS avg_salary
FROM
    departments d
    JOIN employees e ON d.department_id = e.department_id
GROUP BY
    d.department_name
HAVING
    AVG(e.salary) > (
        SELECT
            AVG(salary)
        FROM
            employees
    )
ORDER BY
    avg_salary DESC;
