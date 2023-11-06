from src.website_work import Vacancies, SuperJobVacancies, HeadHunterVacancies


def get_data_from_user():
    """
    Запрашивает данные у пользователя для дальнейшей сортировки/фильтрации
    """
    print("Приветствуем, Пользователь.\nВам придётся ввести данные для того, чтобы продолжить.\n")

    vacancy = get_vacancy_name()
    platform = get_platform_name()
    city = get_location()
    salary = get_salary()
    quantity = get_quantity()

    print("Идёт обработка и загрузка данных.\nДля вашего удобства результат будет выведен в файл 'results.txt'")
    return vacancy, platform, city, salary, quantity


def get_vacancy_name():
    """
    Запрашивает и возвращает имя вакансии/ключевое слово
    """
    while True:
        vacancy = input("Введите название вакансии:\n")
        if vacancy.isdigit():
            print("Введите вакансию корректно.\n")
            continue
        else:
            break
    return vacancy


def get_platform_name():
    """
    Запрашивает и возвращает платформу для поиска
    """
    while True:
        platform = input("Выберите площадку:\nHeadHunter\nSuperJob\nВсе/All\n")
        if platform == "HeadHunter" or platform == "SuperJob" or platform == "Все" or platform == "All":
            break
        else:
            print("Введите корректное название.\n")
            continue
    return platform


def get_location():
    """
    Запрашивает и возвращает местоположение
    """
    while True:
        city = input("Введите город/населённый пункт:\n")
        if city.isalpha():
            break
        else:
            print("Введите корректное название.\n")
            continue
    return city


def get_salary():
    """
    Запрашивает и возвращает минимальный оклад
    """
    while True:
        salary = input("Введите минимальный желаемый оклад:\n")
        if salary.isalpha():
            print("Введите корректное значение з/п.\n")
            continue
        else:
            break
    return salary


def get_quantity():
    """
    Запрашивает и возвращает кол-во вакансий для отображения
    """
    while True:
        quantity = input("Введите желаемое количество вакансий для отображения (макс. 50): ")
        if quantity.isalpha() or int(quantity) > 50 or int(quantity) < 1:
            print("Введите корректное значение.\n")
        else:
            break
    return quantity


def output_data(list_of_vacancies: list[dict], quantity: str):
    """
    Выводит вакансии в консоль
    """
    print("Список подходящих вакансий:\n")
    for vacancy in list_of_vacancies[:int(quantity)]:
        print(f"Название: {vacancy['name']}\n"
              f"Минимальная зарплата: {vacancy['salary']}{vacancy['salary_currency']}\n"
              f"Опыт работы: {vacancy['experience']}\n"
              f"Ссылка: {vacancy['url']}\n")


def get_platforms_data(platform: str, keyword: str) -> list[Vacancies]:
    """
    Возвращает вакансии в созданных экземплярах класса
    """
    platforms = [(HeadHunterVacancies,), (SuperJobVacancies,), (HeadHunterVacancies, SuperJobVacancies)]
    required_platforms_data = []
    if platform == "HeadHunter":
        required_platforms = platforms[0]
    elif platform == "SuperJob":
        required_platforms = platforms[1]
    else:
        required_platforms = platforms[2]

    for platform in required_platforms:
        required_platforms_data.extend(platform().load_vacancies(keyword))

    return required_platforms_data
