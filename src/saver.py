
import json
from src.abstractions import Saver
from json import JSONDecodeError
from src.vacancy import Vacancy

class JSONSaver(Saver):
    """
    Класс для сохранения результатов в json формате
    """
    def __init__(self, path, vacancies = None):
        self.path = path
        self.dict_vacancies = vacancies
        self.instance_vacancies = []

    def load_from_file(self):
        """
        Загрузка данных о вакансии из файла
        """
        try:

            try:
                with open(self.path, "r", encoding="utf-8") as file:
                    data = json.load(file)
            except JSONDecodeError:
                print("Файл пуст")
                return

            for el in data:
                vacancy = Vacancy(
                    int(el.get('id_num', "Нет данных")),
                    str(el.get('vacancy_name', "Нет данных")),
                    str(el.get('company_name')),
                    str(el.get('description', "Нет данных")),
                    int(el.get('salary_from')) if el.get('salary_from') is not None else None,
                    int(el.get('salary_to')) if el.get('salary_to') is not None else None,
                    str(el.get('salary_currency')),
                    str(el.get('area', "Нет данных")),
                    str(el.get('url', "Нет данных")),
                )
                self.instance_vacancies.append(vacancy)
            self.dict_vacancies = [vacancy.to_dict() for vacancy in self.instance_vacancies]
        except FileNotFoundError:
            self.dict_vacancies = []
            raise FileNotFoundError("File not found")

    def save_to_file(self):
        """
        Сохранение файла
        """
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.dict_vacancies, file, indent=4)

    def add_vacancy(self, vacancy):
        """
        Добавление вакансии
        """
        self.load_from_file()
        self.dict_vacancies.append(vacancy)
        self.save_to_file()

    def get_vacancies(self, criteria):
        """
        Поиск и получение вакансии
        """
        self.load_from_file()
        result = []
        for vacancy in self.instance_vacancies:
            dict_vacancy = vacancy.to_dict()
            if criteria in dict_vacancy['vacancy_name'] or criteria in dict_vacancy['description']:
                result.append(vacancy)
        return result

    def remove_vacancy(self, vacancy_id):
        """
        Удаление вакансии
        """
        self.load_from_file()
        try:
            self.dict_vacancies = [vacancy for vacancy in self.dict_vacancies if vacancy['id_num'] != int(vacancy_id)]
            self.save_to_file()
            print("Вакансия удалена!")
        except ValueError:
            print("Вакансии с таким номером не существует.")
