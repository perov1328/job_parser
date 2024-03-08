
from src.config import *
from src.database import *

def save_to_database(data: list, database_name: str, params: dict):
    """
    Функция для сохранения данных в базу данных
    """

    conn = psycopg2.connect(dbname = database_name, **params)

    with conn.cursor() as cur:

        vacancies_delete = "TRUNCATE TABLE vacancies;"
        companies_delete = "TRUNCATE TABLE companies CASCADE;"

        cur.execute(vacancies_delete)
        cur.execute(companies_delete)

        for company in data:

            cur.execute(
                '''
                INSERT INTO companies (id_num, company_name, vacancy_name, url)
                VALUES (%s, %s, %s, %s)
                ''',
                (company['id_num'], company['company_name'], company['vacancy_name'], company['url'])
            )

        for vacancy in data:

            cur.execute(
                '''
                INSERT INTO vacancies (id_num, vacancy_name, company_name, description, salary_from,
                salary_to, salary_currency, area, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (vacancy['id_num'], vacancy['vacancy_name'], vacancy['company_name'], vacancy['description'],
                 vacancy['salary_from'], vacancy['salary_to'], vacancy['salary_currency'],
                 vacancy['area'], vacancy['url'])
            )

    conn.commit()
    conn.close()

def db_interface():
    """
    Интерфейс для пользователя при работе с БД
    """
    db = DBManager()
    params = config('database.ini', 'postgresql')

    flag = True

    while flag:

        user_answer = input("""
        Выберите что Вам необходимо получить:
        1. Получить список всех компаний и количество вакансий в них
        2. Получить список вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки
        3. Получить среднюю зарплату по полученным вакансиям
        4. Получить список вакансий у которых зарплата выше средней
        5. Получить список вакансии в названии которых присутствует заданное слово
        0. Выход
        Ответ: """)

        match user_answer:

            case '1':
                """
                Получение списка всех компаний и количество вакансий в каждой
                """
                db.get_companies_and_vacancies_count('vacancies', params)

            case '2':
                """
                Получение списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
                """
                db.get_all_vacancies('vacancies', params)

            case '3':
                """
                Получение средней зарплаты по вакансиям
                """
                db.get_avg_salary('vacancies', params)

            case '4':
                """
                Получение списка вакансий у которых зарплата выше средней по всем полученным вакансиям
                """
                db.get_vacancies_with_higher_salary('vacancies', params)

            case '5':
                """
                Получение списка всех вакансий , в названии которых содержатся переданные слова
                """
                keyword = input("Введите ключевое слово: ")
                db.get_vacancies_with_keyword('vacancies', params, keyword)

            case '6':
                flag = False
                return None



