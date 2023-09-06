
import requests
from src.vacancy import Vacancy
from src.abstractions import APIClient

class HeadHunterAPI(APIClient):
    """
    Класс для взаимодействия с API HeadHunter
    """
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, keyword: str, city=None, experience=None, count=None, order_by=None):
        """
        Отправляет запрос к API
        :param keyword: ключевые слова для запроса
        :param city: город для запроса
        :param experience: необходимый стаж для запроса
        :param count: количество результатов для запроса
        :param order_by: параметр сортировки
        """
        params = {
            'text': {keyword},
            'area': {city},
            'experience': {experience},
            'per_page': {count},
            'order_by': {order_by}
        }
        try:
            response = requests.get('https://api.hh.ru/vacancies', params=params)
            if response.status_code == 200:
                data = response.json()
                if data['found'] == 0:
                    return []
                else:
                    return HeadHunterAPI.parser_vacancies(data)
        except requests.exceptions.RequestException:
            return []


    def parser_vacancies(data: dict):
        """
        Парсинг ответа в формате JSON
        """
        result = []
        for el in data.get('items'):
            salary = el.get('salary', {})
            if salary:
                from_salary = float(salary.get('from')) if salary.get('from') is not None else None
                to_salary = float(salary.get('to')) if salary.get('to') is not None else None
                currency = str(salary.get('currency')) if salary.get('currency') is not None else None
            else:
                from_salary = to_salary = currency = None
            vacancy = Vacancy(
                int(el.get('id', "Нет данных")),
                str(el.get('name', "Нет данных")),
                str(el.get('employer', {}).get('name', "Нет данных")),
                str(el.get('snippet', "Нет данных").get('requirement', "Нет данных")),
                from_salary,
                to_salary,
                currency,
                str(el.get('area', {}).get('name', "Нет данных")),
                str(el.get('alternate_url', "Нет данных"))
            )
            result.append(vacancy)
        return result

class HHController:
    """
    Контролер для управления параметрами запроса к API HeadHunter
    """
    @staticmethod
    def order_by(param: str):
        """
        Получение параметра сортировки для запросов.
        """
        if param == '1':
            return 'publication_time'
        elif param == '2':
            return 'salary_desc'
        else:
            return None

    @staticmethod
    def get_city_id(city: str):
        """
        Получение id города по его названию
        """
        response = requests.get("https://api.hh.ru/areas").json()
        for el in response:
            for country in el["areas"]:
                if "areas" in country:
                    for reg in country["areas"]:
                        if reg["name"] == city:
                            return reg["id"]
                elif country["name"] == city:
                    return country["id"]

test = HeadHunterAPI()
keyword = 'python'
city = None
experience = 'between1And3'
count_vacancies = None
sort_option = None

print(test.get_vacancies(keyword, city, experience, count_vacancies, sort_option))