
-- Создание базы данных
CREATE DATABASE database_name;

-- Создание таблицы компаний
CREATE TABLE companies (
	id_num INT UNIQUE,
	company_name VARCHAR,
	vacancy_name VARCHAR,
	url VARCHAR);

-- Создание таблицы вакансий
CREATE TABLE vacancies (
	id_num INT REFERENCES companies(id_num),
	vacancy_name VARCHAR,
	company_name VARCHAR,
	description TEXT,
	salary_from INT,
	salary_to INT,
	salary_currency VARCHAR,
	area VARCHAR,
	url VARCHAR);

--Получение списка всех компаний и количество вакансий в каждой
SELECT companies.company_name, COUNT(vacancies.id_num) AS vacancy_count
FROM companies
LEFT JOIN vacancies ON companies.id_num = vacancies.id_num
GROUP BY companies.company_name;

--Получение списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
SELECT companies.company_name AS company_name, vacancies.vacancy_name, vacancies.url, salary_from, salary_to,salary_currency FROM vacancies
LEFT JOIN companies USING(id_num);

--Получение средней зарплаты по вакансиям
SELECT AVG(salary_from) AS average_salary_from FROM vacancies
WHERE salary_from IS NOT NULL;

--Получение списка вакансий у которых зарплата выше средней по всем полученным вакансиям
SELECT companies.company_name AS company_name, vacancies.url, salary_from
FROM vacancies
INNER JOIN companies USING(id_num)
WHERE salary_from > (
    SELECT AVG(salary_from)
    FROM vacancies
    WHERE salary_from IS NOT NULL
);

--Получение списка всех вакансий , в названии которых содержатся переданные слова
SELECT companies.company_name AS company_name, vacancies.url, vacancies.salary_from, vacancies.salary_to
FROM vacancies
LEFT JOIN companies USING(id_num)
WHERE vacancies.company_name LIKE '%keyword%';
