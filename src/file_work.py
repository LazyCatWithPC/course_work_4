import json
from abc import ABC, abstractmethod
from src.website_work import Vacancies


class FileOperation(ABC):
    @staticmethod
    @abstractmethod
    def operate_file(keyword):
        pass


class JSONOperation(FileOperation):
    @staticmethod
    def json_exemplars(united_list: list[Vacancies]) -> list[dict]:
        list_dicts = []
        for a in united_list:
            list_dicts.append(a.__dict__)
        return list_dicts

    @staticmethod
    def operate_file(list_dict):
        with open("data.json", "w+", encoding="utf-8") as file:
            json.dump(list_dict, file, ensure_ascii=False)

    @staticmethod
    def get_vacancies_by_town(town: str):
        with open("data.json", "r", encoding="utf-8") as file:
            read_file = json.load(file)
            filtered_list = []
            for string in read_file:
                if string["town"] == town:
                    filtered_list.append(string)
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(filtered_list, file, ensure_ascii=False)

    @staticmethod
    def get_vacancies_by_salary(salary: str) -> list[dict]:
        with open("data.json", "r", encoding="utf-8") as file:
            read_file = json.load(file)
            filtered_list = []
            for string in read_file:
                if string["salary"] is None:
                    continue
                elif string["salary"] >= int(salary):
                    filtered_list.append(string)
        return filtered_list

    @staticmethod
    def get_sorted_vacancies_by_salary(filtered_list: list[dict]) -> list[dict]:
        sorted_list = sorted(filtered_list, key=lambda x: x["salary"], reverse=True)
        return sorted_list

    @staticmethod
    def result_to_file(result: list[dict], quantity: str):
        with open("results.txt", "w", encoding="utf-8") as file:
            for index in result[:int(quantity)]:
                for k, v in index.items():
                    file.write(f"{k}: {v} \n")
                file.write("\n")
