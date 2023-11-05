import json
import requests
from abc import ABC, abstractmethod


class Website(ABC):
    @abstractmethod
    def get_vacancies_data(self, page, keyword):
        pass


class HeadHunter(Website):
    def get_vacancies_data(self, page: int, keyword: str):
        params = {
            "text": keyword,
            "page": page,
            "per_page": 100
        }
        response = requests.get("https://api.hh.ru/vacancies", params=params)
        response.close()
        return response.content

    def vacancies_to_json(self, keyword: str):
        js_list = []

        for page in range(0, 20):
            js_obj = json.loads(self.get_vacancies_data(page, keyword))
            js_list.extend(js_obj['items'])
            if js_obj['pages'] - page <= 1:
                break
        return js_list


class SuperJob(Website):

    API = "v3.r.137937370.924277268373661c326e2d86d1509666810c1dfc.f5bfa2098a0696b48d0d8d646e960dd6c4973aab"

    def __init__(self):
        pass

    def get_vacancies_data(self, page: int, keyword: str):
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
        js_list = []

        for page in range(0, 20):
            js_obj = json.loads(self.get_vacancies_data(page, keyword))
            js_list.extend(js_obj["objects"])
        return js_list
