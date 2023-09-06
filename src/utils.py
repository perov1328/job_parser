
from src.headhunter import HeadHunterAPI
from src.superjob import SuperJobAPI
from src.saver import *

def get_a_site():
    """
    Выбор сайта для поиска вакансий
    """
    answer = input('С какого сайта Вы желаете получить список вакансий: \n'
                   '1. HeadHunter\n'
                   '2. SuperJob\n'
                   'Выбранный вариант: ')
    if answer == '1':
        return HeadHunterAPI()
    elif answer == '2':
        return SuperJobAPI()
    else:
        print('Введите номер варианта из предложенного списка')

def get_a_keyword():
    """
    Получение запроса для поискать вакансий
    """
    return input('Введите запрос для поиска вакансий: ')

def get_a_city():
    """
    Получение города для поиска вакансий
    """
    city = input('В каком городе Вас интересуют вакансии?\n'
                 'Ваш ответ (оставьте поле пустым для глобального поиска): ')
    if '-' in city:
        parts = city.split('-')
        parts = [word.lower().title().strip() for word in parts]
        city = "-".join(parts)
    else:
        city = city.lower().title()
    return city

def get_experience():
    """
    Получение информации о необходимом опыте
    """
    ex = input('Укажите опыт работы: \n'
                       '1.Без опыта\n'
                       '2.От 1-3\n'
                       '3.От 3-6\n'
                       '4.Более 6\n'
                       '5.Не указывать\n'
                       'Ответ: ')
    if ex == '1':
        return 'noExperience'
    elif ex == '2':
        return 'between1And3'
    elif ex == '3':
        return 'between3And6'
    elif ex == '4':
        return 'moreThan6'
    elif ex == '5':
        return None
    else:
        print('Введите номер варианта из предложенного списка')

def get_count_vacancies():
    """
    Возвращает необходимое количество вакансий для вывода пользователю
    """
    try:
        count = int(input(
            'Какое минимальное количество вакансий вы хотите вывести на экран?\n'
            '(Нажмите Enter если хотите вывести все): '))
    except ValueError:
        count = None
    return count

def get_sort_option():
    """
    Выбор параметра для сортировки вакансий
    """
    option = input('Отсортировать вакансии по:\n'
                  ' 1.По времени публикации\n'
                  ' 2.По зарплате\n'
                  ' Если сортировка не требуется - нажмите Enter\n'
                  'Ответ:')
    return option

def save_to_json(filename: str, vacancies_list: list):
    """
    Сохранение списка вакансий в JSON файл
    """
    json_saver = JSONSaver(filename + '.json', vacancies_list)
    json_saver.save_to_file()
    return json_saver

def vacancies_list():
    """
    Получение листа вакансий
    """
    json_loader = JSONSaver('vacancies.json')
    json_loader.load_from_file()
    if len(json_loader.instance_vacancies) == 0:
        return []
    else:
        return json_loader.instance_vacancies

def vacancies_comparison():
    """
    Сравнение двух вакансий по их ID.
    """
    list_instance = vacancies_list()
    list_vac_dict = [el.to_dict() for el in list_instance]
    first_id = int(input("\nВведите id первой вакансии: "))
    second_id = int(input("Введите id второй вакансии: "))
    vacancy1 = None
    vacancy2 = None

    for item in list_vac_dict:
        if first_id == item.get("id_num"):
            vacancy1 = Vacancy(
                int(item.get('id_num', "Нет данных")),
                str(item.get('vacancy_name', "Нет данных")),
                str(item.get('company_name')),
                str(item.get('description', "Нет данных")),
                float(item.get('salary_from')),
                float(item.get('salary_to')),
                str(item.get('salary_currency')),
                str(item.get('area', "Нет данных")),
                str(item.get('url', "Нет данных")),
            )

        if second_id == item.get("id_num"):
            vacancy2 = Vacancy(
                int(item.get('id_num', "Нет данных")),
                str(item.get('vacancy_name', "Нет данных")),
                str(item.get('company_name')),
                str(item.get('description', "Нет данных")),
                float(item.get('salary_from')),
                float(item.get('salary_to')),
                str(item.get('salary_currency')),
                str(item.get('area', "Нет данных")),
                str(item.get('url', "Нет данных")),
            )

    if vacancy1 is None:
        return "Не удалось найти первую вакансию"
    elif vacancy2 is None:
        return "Не удалось найти вторую вакансию"
    elif vacancy1 is None and vacancy2 is None:
        return "Не удалось найти обе вакансии."

    if vacancy1 == vacancy2:
        return "Обе вакансии имеют одинаковые зарплаты."
    elif vacancy1 > vacancy2:
        return "Зарплата в первой вакансии больше."
    elif vacancy1 < vacancy2:
        return "Зарплата во второй вакансии больше."

def remove_vacancy():
    """
    Удалить вакансию из JSON по её номеру.
    """
    user_answer = input("Введите ID вакансии, которую хотите удалить: ")
    result = JSONSaver(path="vacancies.json")
    result.remove_vacancy(vacancy_id=user_answer)

def search_by_criterion():
    """
    Поиск вакансий по ключевому слову в описании.
    """
    criterion = input('Введите ключевое слово для поиска: ')
    doc = JSONSaver(path='vacancies.json')
    matched = doc.get_vacancies(criterion)

    if len(matched) == 0:
        print("К сожалению ничего не найдено")
    else:
        for vacancy in matched:
            print(vacancy)
            print("=" * 50)