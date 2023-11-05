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


