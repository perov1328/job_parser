
import psycopg2

class DBManager:
    """
    Класс отвечающий за работу с базой данных 
    """

    def get_companies_and_vacancies_count(self, database_name: str, params: dict):
        """
        Получение списка всех компаний и количество вакансий в каждой
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                            SELECT companies.company_name, COUNT(vacancies.id_num) AS vacancy_count
                            FROM companies
                            LEFT JOIN vacancies ON companies.id_num = vacancies.id_num
                            GROUP BY companies.company_name;
                    """)

            result = cur.fetchall()

        conn.commit()
        conn.close()

        return result

    def get_all_vacancies(self, database_name: str, params: dict):
        """
        Получение списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT companies.company_name, vacancy_name AS vacancy_vacancy_name, vacancy_url, salary_from,
                    salary_to,salary_currency FROM vacancies
                    LEFT JOIN companies USING(id_num);
                    """)

            result = cur.fetchall()

        conn.commit()
        conn.close()

        return result

    def get_avg_salary(self, database_name: str, params: dict):
        """
        Получение средней зарплаты по вакансиям
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT AVG(salary_from) AS average_salary_from FROM vacancies
                    WHERE salary_from IS NOT NULL;
                    """)

            result = cur.fetchall()

        conn.commit()
        conn.close()

        return result

    def get_vacancies_with_higher_salary(self, database_name: str, params: dict):
        """
        Получение списка вакансий у которых зарплата выше средней по всем полученным вакансиям
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT companies.company_name AS company_name, vacancies.url, salary_from
                    FROM vacancies
                    INNER JOIN companies USING(id_num)
                    WHERE salary_from > (
                        SELECT AVG(salary_from)
                        FROM vacancies
                        WHERE salary_from IS NOT NULL
                    );
                    """)

            result = cur.fetchall()

        conn.commit()
        conn.close()

        return result

    def get_vacancies_with_keyword(self, database_name: str, params: dict, keyword: str):
        """
        Получение списка всех вакансий , в названии которых содержатся переданные слова
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT companies.company_name AS company_name, vacancies.url, vacancies.salary_from, vacancies.salary_to
                    FROM vacancies
                    LEFT JOIN companies USING(id_num)
                    WHERE title LIKE %s
            """, ('%' + keyword + '%',))

            result = cur.fetchall()

        conn.commit()
        conn.close()

        return result
