
class Vacancy:
    """
    Класс с информацией о вакансии
    """
    def __init__(self, id_num, vacancy_name, company_name, description, salary_from,
                 salary_to, salary_currency, area, url):
        self.id_num = id_num
        self.vacancy_name = vacancy_name
        self.company_name = company_name
        self.description = description
        self.salary_from = salary_from if salary_from is not None else 0
        self.salary_to = salary_to if salary_from is not None else 0
        self.salary_currency = salary_currency if salary_from is not None else "Данные отсутствуют"
        self.area = area
        self.url = url

    def __str__(self):
        """
        Возвращает объект в понятном для пользователя виде
        """
        if self.salary_to == 0 and self.salary_from == 0:
            salary_range = 'Информация отсутствует'
        else:
            from_part = f'От {self.salary_from} ' if self.salary_from != 0 else ''
            to_part = f'До {self.salary_to} ' if self.salary_to != 0 else ''
            salary_range = f'{from_part}{to_part}{self.salary_currency}'

        return f'ID: {self.id_num}\n' \
               f'Название вакансии: {self.vacancy_name}\n' \
               f'Название компании: {self.company_name}\n' \
               f'Описание: {self.description}\n' \
               f'Зарплата: {salary_range}\n' \
               f'Местоположение: {self.area}\n' \
               f'URL: {self.url}'

    def __ge__(self, other):
        return int(self.salary_from) >= int(other.salary_from)

    def __le__(self, other):
        return int(self.salary_from) <= int(other.salary_from)

    def __gt__(self, other):
        return int(self.salary_from) > int(other.salary_from)

    def __lt__(self, other):
        return int(self.salary_from) < int(other.salary_from)

    def __eq__(self, other):
        return (self.salary_currency == other.salary_currency and self.salary_to == other.salary_to and self.salary_from == other.salary_from)

    def to_dict(self):
        """
        Возвращает словарь для последующей работы с вакансией
        """
        return {
            "id_num": self.id_num,
            "vacancy_name": self.vacancy_name,
            "company_name": self.company_name,
            "description": self.description,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "salary_currency": self.salary_currency,
            "area": self.area,
            "url": self.url
        }
