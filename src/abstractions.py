
from abc import ABC, abstractmethod

class APIClient(ABC):
    """
    Абстрактный класс для работы с API
    """
    @abstractmethod
    def get_vacancies(self, keyword, city=None, experience=None, count=None, order_by=None):
        """
        Метод для отправки запроса к API
        """
        pass

    @abstractmethod
    def parser_vacancies(self, data):
        """
        Метод для обработки ответа API
        """
        pass


class Saver(ABC):
    """
    Абстрактный класс для работы с сохранением результатов
    """
    @abstractmethod
    def load_from_file(self):
        """
        Загрузка данных о вакансиях из файла в программу
        """
        pass

    @abstractmethod
    def save_to_file(self):
        """
        Сохранения данных о вакансиях из программы в файл
        """
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        """
        Добавления вакансии в программу
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        """
        Поиска вакансии в программе по заданным критериям
        """
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy_id):
        """
        Удаления вакансии из программы по её номеру
        """
        pass
