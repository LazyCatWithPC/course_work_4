import json
import requests
from abc import ABC, abstractmethod


class Website(ABC):
    """
    Абстрактный класс для работы с API
    """
    @abstractmethod
    def get_vacancies_data(self, page, keyword):
        pass


class HeadHunter(Website):
    """
    Класс для работы с данными и API с HeadHunter
    """
    def get_vacancies_data(self, page: int, keyword: str):
        """
        Возвращает данные вакансий, полученные с сайта
        """
        params = {
            "text": keyword,
            "page": page,
            "per_page": 100
        }
        response = requests.get("https://api.hh.ru/vacancies", params=params)
        response.close()
        return response.content

    def vacancies_to_json(self, keyword: str):
        """
        Преобразовывает и возвращает данные вакансий в список JSON
        """
        js_list = []

        for page in range(0, 20):
            js_obj = json.loads(self.get_vacancies_data(page, keyword))
            js_list.extend(js_obj['items'])
            if js_obj['pages'] - page <= 1:
                break
        return js_list


class SuperJob(Website):
    """
    Класс для работы с данными и API с SuperJob
    """
    API = "v3.r.137937370.924277268373661c326e2d86d1509666810c1dfc.f5bfa2098a0696b48d0d8d646e960dd6c4973aab"

    def __init__(self):
        pass

    def get_vacancies_data(self, page: int, keyword: str):
        """
        Возвращает данные вакансий, полученные с сайта
        """
        header = {
            "Host": "api.superjob.ru",
            "X-Api-App-Id": SuperJob.API,
            "Authorization": "Bearer r.000000010000001.example.access_token",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
            "keyword": keyword,
            "town ": "",
            "count": "100",
            "period": "3",
            "page": page
        }
        response = requests.get("https://api.superjob.ru/2.0/vacancies/", params=params, headers=header)
        response.close()
        return response.content

    def vacancies_to_json(self, keyword: str):
        """
        Преобразовывает и возвращает данные вакансий в список JSON
        """
        js_list = []

        for page in range(0, 20):
            js_obj = json.loads(self.get_vacancies_data(page, keyword))
            js_list.extend(js_obj["objects"])
        return js_list


class Vacancies:
    """
    Общий класс для работы с вакансиями
    """
    def __init__(self, name=None, salary=None, salary_to=None, salary_currency=None,
                 town=None, experience=None, url=None):
        self.name = name
        self.salary = salary
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.town = town
        self.experience = experience
        self.url = url

    def __repr__(self):
        return (f"Vacancy(name={self.name}, salary={self.salary}, salary_to={self.salary_to}, "
                f"salary_currency={self.salary_currency}, town={self.town},"
                f"experience={self.experience}, url={self.url}")

    def __str__(self):
        return (f"Вакансия: {self.name}. Зарплата {self.salary}-{self.salary_to} {self.salary_currency}. "
                f"Город: {self.town}"
                f"Ссылка: {self.url}"
                f"Опыт работы:{self.experience}")

    def __le__(self, other):
        return int(self.salary) <= int(other.salary)

    def __lt__(self, other):
        return int(self.salary) < int(other.salary)

    def __ge__(self, other):
        return int(self.salary) >= int(other.salary)

    def __gt__(self, other):
        return int(self.salary) > int(other.salary)

    def __eq__(self, other):
        return int(self.salary) == int(other.salary)


class SuperJobVacancies(Vacancies, SuperJob):
    """
    Класс для работы с вакансиями SuperJob
    """
    def load_vacancies(self, keyword: str):
        """
        Возвращает список вакансий
        """
        list_vacancies = []
        for vacancy in SuperJob.vacancies_to_json(self, keyword):
            new_vacancy = SuperJobVacancies(name=vacancy["profession"],
                                            salary=vacancy["payment_from"],
                                            salary_to=vacancy["payment_to"],
                                            salary_currency=vacancy["currency"],
                                            town=vacancy["town"]["title"],
                                            experience=vacancy["experience"]["title"],
                                            url=vacancy["link"])
            list_vacancies.append(new_vacancy)

        return list_vacancies


class HeadHunterVacancies(Vacancies, HeadHunter):
    """
    Класс для работы с вакансиями HH
    """
    def load_vacancies(self, keyword: str):
        """
        Возвращает список вакансий
        """
        list_of_vacancies = []
        for vacancy in HeadHunter.vacancies_to_json(self, keyword):
            try:
                new_vacancy = HeadHunterVacancies(name=vacancy["name"],
                                                  salary=vacancy["salary"]["from"],
                                                  salary_to=vacancy["salary"]["to"],
                                                  salary_currency=vacancy["salary"]["currency"],
                                                  town=vacancy["area"]["name"],
                                                  experience=vacancy["experience"]["name"],
                                                  url=vacancy["alternate_url"])
                list_of_vacancies.append(new_vacancy)
            except TypeError:
                new_vacancy = HeadHunterVacancies(name=vacancy["name"],
                                                  salary=None,
                                                  town=vacancy["area"]["name"],
                                                  experience=vacancy["experience"]["name"],
                                                  url=vacancy["alternate_url"])
                list_of_vacancies.append(new_vacancy)

        return list_of_vacancies
