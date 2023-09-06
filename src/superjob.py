
import os
import requests
from src.vacancy import Vacancy
from src.abstractions import APIClient

APY_KEY = 'v3.r.137770957.0146b11e6252f209964f1b28cc99740f066efaab.4341ca9ded679f88804bd4bfefcfbd53fdf9b271'

class SuperJobAPI(APIClient):
    """
    Класс для взаимодействия с API SuperJob
    """
    def __init__(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self, keyword: str, city=None, experience=None, count=None, order_by=None):
        """
        Отправляет запрос к API
        :param keyword: ключевые слова для запроса
        :param city: город для запроса
        :param experience: необходимый стаж для запроса
        :param count: количество результатов для запроса
        :param order_field: параметр сортировки
        """
        params = {
            'keyword': keyword,
            "town": city,
            "experience": experience,
            "count": count,
            "order_field": order_by
        }
        headers = {
            'X-Api-App-Id': APY_KEY,
        }
        try:
            response = requests.get('https://api.superjob.ru/2.0/vacancies/', params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if len(data) == 0:
                    return []
                else:
                    return SuperJobAPI.parser_vacancies(data)
        except requests.exceptions.RequestException:
            return []

    def parser_vacancies(data: dict):
        """
        Парсинг ответа в формате JSON
        """
        result =[]
        for el in data.get('objects'):
            from_salary = float(el.get('payment_from')) if el.get('payment_from') != 0 else None
            to_salary = float(el.get('payment_to')) if el.get('payment_to') != 0 else None
            currency = str(el.get('currency'))

            vacancy = Vacancy(
                int(el.get('id', "Нет данных")),
                str(el.get('profession', "Нет данных")),
                str(el.get('employer', {}).get('name', "Нет данных")),
                str(el.get('candidat', "Нет данных")),
                from_salary,
                to_salary,
                currency,
                str(el.get('town', {}).get('title', "Нет данных")),
                str(el.get('link', "Нет данных"))
            )
            result.append(vacancy)

        return result

class SJController:
    """
    Контролер для управления параметрами запроса к API SuperJob
    """
    @staticmethod
    def order_field(param: str):
        """
        Получение параметра сортировки для запросов.
        """
        if param == '1':
            return 'date'
        elif param == '2':
            return 'payment_desc'
        else:
            return 'relevance'

    @staticmethod
    def validate_city(city: str):
        """
        Проверка наличия города в API SuperJob
        """
        if len(city) == 0:
            return None
        else:
            url = 'https://api.superjob.ru/2.0/towns/'
            headers = {
                'X-Api-App-Id': APY_KEY,
            }
            response = requests.get(url, headers=headers).json()
            for el in response['objects']:
                if el['title'] == city:
                    return city
        return None