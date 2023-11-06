from src.file_work import JSONOperation
import src.functions


def main():
    user_data = list(src.functions.get_data_from_user())
    all_vacancies = list(src.functions.get_platforms_data(user_data[1], user_data[0]))
    vacancies_data = JSONOperation.json_exemplars(all_vacancies)
    JSONOperation.operate_file(vacancies_data)
    JSONOperation.get_vacancies_by_town(user_data[2])
    final_data = JSONOperation.get_vacancies_by_salary(user_data[3])
    src.functions.output_data(JSONOperation.get_sorted_vacancies_by_salary(final_data), user_data[4])
    data_to_print = JSONOperation.get_sorted_vacancies_by_salary(final_data)
    JSONOperation.result_to_file(data_to_print, user_data[4])


if __name__ == '__main__':
    main()
