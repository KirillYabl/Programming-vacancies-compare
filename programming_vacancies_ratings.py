import itertools
import logging
import os

import requests
import dotenv

from common_functions import get_stream_logger
from common_functions import calc_salary
from common_functions import get_pretty_table_from_dict


def predict_rub_salary_sj(vacancy):
    """Calc salary by vacancy for superjob.ru.

    :param vacancy: dict, item of vacancy from superjob.ru
    :return: int or None, salary of vacancy
    """
    if vacancy['currency'] != 'rub':
        return None

    if vacancy['payment_from'] == 0:
        vacancy['payment_from'] = None

    if vacancy['payment_to'] == 0:
        vacancy['payment_to'] = None

    salary = calc_salary(vacancy['payment_from'], vacancy['payment_to'])

    return salary


def predict_rub_salary_hh(vacancy):
    """Calc salary by vacancy for hh.ru.

    :param vacancy: dict, item of vacancy from hh.ru
    :return: int or None, salary of vacancy
    """
    salary = vacancy['salary']
    # if employer dont set salary, hh gives None, else dict
    if salary is None:
        return None

    if salary['currency'] != 'RUR':
        return None

    if salary is None:
        salary = {'from': None, 'to': None}

    salary = calc_salary(salary['from'], salary['to'])

    return salary


def predict_rub_salary(vacancy, site_name):
    """Predict salary in rub depends of API site name.

    :param vacancy: dict, object of API with vacancy info
    :param site_name: name of site with API, for every site this function needs new logic
    :return: int or None, size of salary, None means that employer dont write salary or non RUR salary
    """

    if site_name == 'SuperJob':
        return predict_rub_salary_sj(vacancy)

    if site_name == 'HeadHunter':
        return predict_rub_salary_hh(vacancy)

    raise AttributeError('unknown site name')


def calc_salary_by_lang(list_of_salaries):
    """Calc salary for lang with list of salaries by lang.

    :param list_of_salaryes: list of float or None
    :return: dict with count of vacancies, count of vacancies with salary and average salary
    """
    vacancies_found = len(list_of_salaries)
    not_none_salaries = [salary for salary in list_of_salaries if salary is not None]
    vacancies_processed = len(not_none_salaries)
    average_salary = int(sum(not_none_salaries) / vacancies_processed)

    salary_by_lang = {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary
    }

    return salary_by_lang


def get_lang_salaries_rating(api_url, api_params, api_headers, spec_params, site_name, logger, languages):
    """Calc rating of salary for API some site.

    :param api_url: str, url of api
    :param api_params: dict, params to get request
    :param api_headers: dict, headers to get request
    :param spec_params: dict, specific by site API params
    :param site_name: str, name of site
    :param logger: logger object
    :param languages: list, list of languages keywords
    :return: dict, dictionary with keys as keywords nad values too dicts with parameters
    vacancies_found - count of vacancies
    vacancies_processed - count of vacancies with salary
    average_salary - average salary for vacancies with salary
    """

    logger.info(f'Starts calc rating')
    logger.debug(f'Languages list have lenght={len(languages)}')
    logger.debug(f'API url = {api_url}')

    salaries_rating = {}
    for lang in languages:
        logger.debug(f'start calculate {lang} salary')
        api_params[spec_params['keyword_for_search']] = lang

        vacancies = []
        write_found_already = False
        vacancies_proceeded = 0
        for page in itertools.count():
            api_params['page'] = page
            response = requests.get(api_url, headers=api_headers, params=api_params)

            # check HTTPError
            response.raise_for_status()
            # some sites can return 200 and write error in body
            if 'error' in response:
                raise requests.exceptions.HTTPError(response['error'])

            found = response.json()[spec_params['total_vacancies_param']]
            if not write_found_already:
                logger.debug(f'lang {lang}, {found} vacancies found')
                write_found_already = True

            page_vacancies = [vacancy for vacancy in response.json()[spec_params['name_of_items_key']]]
            vacancies += page_vacancies

            vacancies_proceeded += len(page_vacancies)

            if vacancies_proceeded >= found:
                logger.debug(f'max vacancies proceeded for {lang}, break')
                break

            if (page + 1) * spec_params['page_vacancies_count'] >= spec_params['limit_vacancies']:
                logger.debug(f'limit of site vacancies count achieved, break')
                break

        list_of_salaries = [predict_rub_salary(vacancy, site_name) for vacancy in vacancies]
        logger.debug(f'lang {lang}, finish calculate salary')
        if len(list_of_salaries) > spec_params['min_count_vacancies']:
            salaries_rating[lang] = calc_salary_by_lang(list_of_salaries)
            logger.info(f'lang {lang}, add lang in rating')

    return salaries_rating


def get_sj_params():
    """Wired params for SuperJob.

    :return: list of params
    """
    sj_api_url = 'https://api.superjob.ru/2.0/vacancies/'
    sj_api_params = {
        'catalogues': 48,
        'town': 4,
    }
    sj_api_headers = {
        'X-Api-App-Id': os.getenv('SJ_SECRET_KEY')
    }
    sj_spec_params = {
        'keyword_for_search': 'keyword',
        'total_vacancies_param': 'total',
        'name_of_items_key': 'objects',
        'page_vacancies_count': 20,
        'limit_vacancies': 500,
        'min_count_vacancies': 5
    }
    sj_site_name = 'SuperJob'
    sj_logger = get_stream_logger(sj_site_name, logging.INFO, '%(asctime)s  %(name)s  %(levelname)s  %(message)s')

    return [sj_api_url, sj_api_params, sj_api_headers, sj_spec_params, sj_site_name, sj_logger]


def get_hh_params():
    """Wired params for HeadHunter.

        :return: list of params
        """
    hh_api_url = 'https://api.hh.ru/vacancies'
    hh_api_params = {
        'area': 1,
        'period': 30,
        'specialization': '1.221'
    }
    hh_api_headers = None
    hh_spec_params = {
        'keyword_for_search': 'text',
        'total_vacancies_param': 'found',
        'name_of_items_key': 'items',
        'page_vacancies_count': 20,
        'limit_vacancies': 2000,
        'min_count_vacancies': 100
    }
    hh_site_name = 'HeadHunter'
    hh_logger = get_stream_logger(hh_site_name, logging.INFO, '%(asctime)s  %(name)s  %(levelname)s  %(message)s')

    return [hh_api_url, hh_api_params, hh_api_headers, hh_spec_params, hh_site_name, hh_logger]


if __name__ == '__main__':
    dotenv.load_dotenv()
    languages = ['1C', 'Assembler', 'C', 'C#', 'C++', 'Clojure', 'CoffeeScript', 'Cuda', 'Delphi', 'Erlang', 'Fortran',
                 'Groovy', 'Haskell', 'Java', 'JavaScript', 'Kotlin', 'Lisp', 'Lua', 'Matlab ', 'Objective-C',
                 'OpenGL', 'Pascal', 'Perl', 'PHP', 'PL/SQL', 'Python', 'R', 'Ruby', 'Rust', 'Scala', 'Solidity',
                 'Swift', 'Visual Basic', 'Visual Basic.NET', 'Bash', 'ECMAScript', 'F#', 'Octave', 'Go', 'Julia',
                 'Maple', 'Mathematica', 'PowerShell', 'Shell', 'Tcl', 'TypeScript']
    header = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    keys_rules = ['vacancies_found', 'vacancies_processed', 'average_salary']

    ###################SuperJob################################

    sj_in_params = get_sj_params() + [languages]
    sj_salaries_rating = get_lang_salaries_rating(*sj_in_params)

    sj_title = 'SuperJob Moscow'
    sj_table = get_pretty_table_from_dict(header, sj_salaries_rating, sj_title, keys_rules)

    ###################HeadHunter################################

    hh_in_params = get_hh_params() + [languages]
    hh_salaries_rating = get_lang_salaries_rating(*hh_in_params)

    hh_title = 'HeadHunter Moscow'
    hh_table = get_pretty_table_from_dict(header, hh_salaries_rating, hh_title, keys_rules)

    ###################Print Tables################################

    print(sj_table)
    print()
    print(hh_table)
