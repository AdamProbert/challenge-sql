-- Setup for advanced subquery & aggregation challenge
-- Create a more detailed employees database
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES departments (department_id),
    position VARCHAR(100),
    salary DECIMAL(10, 2) NOT NULL,
    hire_date DATE NOT NULL
);

-- Insert department data
INSERT INTO
    departments (department_name, location)
VALUES
    ('Engineering', 'Building A'),
    ('Marketing', 'Building B'),
    ('Finance', 'Building C'),
    ('Human Resources', 'Building B'),
    ('Sales', 'Building D'),
    ('Research', 'Building A');

-- Insert employee data with varied salaries
INSERT INTO
    employees (
        first_name,
        last_name,
        email,
        department_id,
        position,
        salary,
        hire_date
    )
VALUES
    -- Engineering
    (
        'John',
        'Smith',
        'john.smith@company.com',
        1,
        'Senior Developer',
        95000.00,
        '2018-06-15'
    ),
    (
        'Emily',
        'Johnson',
        'emily.johnson@company.com',
        1,
        'Software Architect',
        115000.00,
        '2017-04-20'
    ),
    (
        'Michael',
        'Lee',
        'michael.lee@company.com',
        1,
        'Developer',
        82000.00,
        '2020-01-10'
    ),
    (
        'Lisa',
        'Wong',
        'lisa.wong@company.com',
        1,
        'QA Engineer',
        78000.00,
        '2019-10-05'
    ),
    (
        'David',
        'Chen',
        'david.chen@company.com',
        1,
        'DevOps Engineer',
        88000.00,
        '2019-03-22'
    ),
    (
        'Sarah',
        'Davis',
        'sarah.davis@company.com',
        1,
        'Junior Developer',
        65000.00,
        '2021-02-15'
    ),
    -- Marketing
    (
        'Jessica',
        'Wilson',
        'jessica.wilson@company.com',
        2,
        'Marketing Manager',
        92000.00,
        '2018-07-12'
    ),
    (
        'Daniel',
        'Miller',
        'daniel.miller@company.com',
        2,
        'Content Specialist',
        72000.00,
        '2020-05-03'
    ),
    (
        'Emma',
        'Brown',
        'emma.brown@company.com',
        2,
        'SEO Specialist',
        68000.00,
        '2021-01-20'
    ),
    (
        'Ryan',
        'Taylor',
        'ryan.taylor@company.com',
        2,
        'Social Media Coordinator',
        58000.00,
        '2021-06-10'
    ),
    -- Finance
    (
        'Robert',
        'Anderson',
        'robert.anderson@company.com',
        3,
        'Finance Director',
        125000.00,
        '2016-08-10'
    ),
    (
        'Mary',
        'Thomas',
        'mary.thomas@company.com',
        3,
        'Senior Accountant',
        95000.00,
        '2018-11-05'
    ),
    (
        'Christopher',
        'Jackson',
        'christopher.jackson@company.com',
        3,
        'Financial Analyst',
        85000.00,
        '2019-09-15'
    ),
    (
        'Amanda',
        'White',
        'amanda.white@company.com',
        3,
        'Accountant',
        72000.00,
        '2020-07-22'
    ),
    (
        'James',
        'Harris',
        'james.harris@company.com',
        3,
        'Payroll Specialist',
        68000.00,
        '2020-10-18'
    ),
    -- Human Resources
    (
        'Patricia',
        'Martin',
        'patricia.martin@company.com',
        4,
        'HR Manager',
        90000.00,
        '2018-03-01'
    ),
    (
        'Jennifer',
        'Thompson',
        'jennifer.thompson@company.com',
        4,
        'Recruiter',
        65000.00,
        '2020-06-08'
    ),
    (
        'Kevin',
        'Garcia',
        'kevin.garcia@company.com',
        4,
        'HR Specialist',
        62000.00,
        '2021-05-15'
    ),
    -- Sales
    (
        'Thomas',
        'Rodriguez',
        'thomas.rodriguez@company.com',
        5,
        'Sales Director',
        110000.00,
        '2017-05-20'
    ),
    (
        'Elizabeth',
        'Lewis',
        'elizabeth.lewis@company.com',
        5,
        'Sales Manager',
        95000.00,
        '2018-09-12'
    ),
    (
        'Steven',
        'Walker',
        'steven.walker@company.com',
        5,
        'Account Executive',
        85000.00,
        '2019-02-28'
    ),
    (
        'Nicole',
        'Allen',
        'nicole.allen@company.com',
        5,
        'Sales Representative',
        72000.00,
        '2020-08-03'
    ),
    (
        'Brian',
        'Young',
        'brian.young@company.com',
        5,
        'Sales Representative',
        71000.00,
        '2020-08-15'
    ),
    (
        'Michelle',
        'King',
        'michelle.king@company.com',
        5,
        'Sales Representative',
        70000.00,
        '2020-10-05'
    ),
    -- Research
    (
        'William',
        'Scott',
        'william.scott@company.com',
        6,
        'Research Director',
        130000.00,
        '2016-04-15'
    ),
    (
        'Karen',
        'Green',
        'karen.green@company.com',
        6,
        'Senior Researcher',
        105000.00,
        '2017-09-10'
    ),
    (
        'Mark',
        'Baker',
        'mark.baker@company.com',
        6,
        'Research Scientist',
        95000.00,
        '2019-01-25'
    ),
    (
        'Laura',
        'Adams',
        'laura.adams@company.com',
        6,
        'Research Analyst',
        80000.00,
        '2020-03-18'
    );
