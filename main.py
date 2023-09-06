
from src.utils import *
from src.headhunter import *
from src.superjob import *

#В хороших программах принято здороваться со всяк туда входящим
print('''Доброго времени суток!
Сегодня мы поможем подобрать Вам список подходящих вакансий :)''')

#Старт программы
while True:

    user_answer = input('''Выберете необходимое Вам действие:
    1. Поиск вакансий
    2. Вывод вакансий из сохраненного списка
    3. Сравнение двух вакансий
    4. Удалить вакансию из списка JSON
    5. Вывести вакансии по ключевому слову
    0. выход
    Ответ: ''')

    if user_answer == '1':
        #Получение начальных вводных для работы программы
        site = get_a_site()
        keyword = get_a_keyword()
        city = get_a_city()
        experience = get_experience()
        count_vacancies = get_count_vacancies()
        sort_option = get_sort_option()

        #Обработка города в зависимости от выбранного сайта
        if isinstance(site, HeadHunterAPI):
            city = HHController.get_city_id(city)
        elif isinstance(site, SuperJobAPI):
            city = SJController.validate_city(city)

        #Обработка параметра запроса в зависимости от выбранного сайта
        if isinstance(site, HeadHunterAPI):
            sort_option = HHController.order_by(sort_option)
        elif isinstance(site, SuperJobAPI):
            sort_option = SJController.order_field(sort_option)

        #Отправка запроса к сайту с выбранными параметрами запроса
        if isinstance(site, HeadHunterAPI):
            response = site.get_vacancies(keyword, city, experience, count_vacancies, sort_option)
        elif isinstance(site, SuperJobAPI):
            response = site.get_vacancies(keyword, city, experience, count_vacancies, sort_option)

        #Сохранение вакансий в файле JSON
        vacancy_list = []
        for el in response:
            vacancy_list.append(el.to_dict())
        save_to_json('vacancies', vacancy_list)

    elif user_answer == '2':
        #Получение списка вакансий из файла JSON
        result = vacancies_list()
        for el in result:
            print(el)
            print('=' * 50)

    elif user_answer == '3':
        #Сравнение 2х вакансий
        print(vacancies_comparison())

    elif user_answer == '4':
        #Удаление вакансии из списка JSON
        remove_vacancy()

    elif user_answer == '5':
        #Поиск вакансий по ключевым словам
        print(search_by_criterion())

    elif user_answer == '0':
        #Прощание с пользователем и выход
        print('\nСпасибо что воспользовались моей программой.'
        '\nP.S. Поддержать разработчика можно переводом на сбер +791696407**'
        '\nP.S.S. Добавление новых функций и оптимизация запланированы на конец сентября 2023 г.')
        break
