from requests import get  # Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
from _3_UserSet_Params import *  # мб так импортировать параметр Area из файла _4_?
import time


class GetPage_hh:
    """
    Класс GetPage_hh для работы со страницей.
    Позволяет обращаться к серверу и получать ответ.
    """

    def __init__(self, params, url='https://api.hh.ru/vacancies'):
        """
        Данный метод определяет свойства объектам этого класса (инициализация).
        :param params: объекту присваиваются параметры, которые являются результатом работы класса ParamsForInput
        :param url: объекту присваивается свой адрес, по умолчанию стоит https://api.hh.ru/vacancies.
        """
        self.params = params
        self.url = url

    def get_response(self):
        """
        Делаем запрос к серверу, получаем ответ от сервера.
        Метод возвращает json формат, с которым далее будет удобно работать и доставать данные.
        """
        response = get(self.url, params=self.params)
        return response.json()


class Parse:
    """Парсинг вакансий"""

    def __init__(self, apijson):
        self.apijson = apijson

    def get_vac_id(self):
        """Получение ID вакансии"""
        vac_id = [self.apijson[i]['id'] for i in range(len(self.apijson))]
        return vac_id

    def get_name_vac(self):
        """Названия вакансий"""
        name = [self.apijson[i]['name'] for i in range(len(self.apijson))]
        return name

    def get_date_created(self):
        """Дата размещения вакансии (мск)"""
        created = []
        for item in self.apijson:
            created.append(item['created_at'][:10] + ' ' + item['created_at'][11:19])
        return created

    def url_vac(self):
        """Сайты вакансий"""
        url = [item['alternate_url'] for item in self.apijson]
        return url

    def api_url_vac(self):
        """Сайты апи"""
        api_url = [item['url'] for item in self.apijson]
        return api_url

    # Возможно, в другой класс
    def get_city_vac(self):
        """Город размещения вакансии (мск)"""
        city = []
        for item in self.apijson:
            city.append(item['city']['name'])
        return city

    # Возможно, в другой класс
    def vac_metro(self):
        """
        Станции метро
        """
        metro = [self.apijson['metro_stations']['station_name'] for item in self.apijson['metro_stations']]
        return metro


class GetPage_vac:
    """
    Класс GetPage_vac для работы со страницей.
    Позволяет обращаться к серверу и получать ответ.
    """

    def __init__(self, api_url):
        self.api_url = api_url

    def get_response_vac(self):
        response_vac = get(self.api_url)
        return response_vac.json()


class ParseVac:

    def __init__(self, api_vac):
        self.api_vac = api_vac

    def get_experience(self):
        """Необходимый опыт работы в вакансии"""
        # ХЗ КАКОЙ ТИП ДАННЫХ ЛУЧШЕ ИСПОЛЬЗОВАТЬ ДЛЯ ТАБЛИЦ
        lst_experience1 = self.api_vac['experience']['name']
        return lst_experience1


txt = input('Какую вакансию вы ищите?\n')

start_time = time.process_time()

for i in range(20):

    print(f'Получение данных с {i+1} страницы с сайта hh.ru')

    """Сохраняем параметры в переменную"""
    obj_param = ParamsForInput(txt, i)  # создаем объект класса ParamsForInput
    user_params = obj_param.get_userparams()  # кладем словарь параметров в переменную user_params
    # print(user_params)

    """Создание переменной для json формата"""
    a = GetPage_hh(user_params)  # создаем объект класса GetPage_hh
    api_work = a.get_response()['items']  # в переменной api_work - json формат ответа от сервера
    # print(api_work)  # JSON вывод страниц api.hh.ru

    """Собственно отбор необходимых параметров"""
    parsing = Parse(api_work)  # создание объекта класса Parse
    # print(parsing.get_vac_id())  # список id вакансий (ПОЛЕ VAC_ID)
    # print(parsing.get_name_vac())  # список названий вакансий этой страницы (ПОЛЕ VAC_NAME)
    # print(parsing.get_date_created())  # список даты-времени создания вакансий (ПОЛЕ DATA_CREATED)
    # print(parsing.url_vac())  # список сайтов вакансий по запросу  (ПОЛЕ LINK_VAC)
    # print(parsing.vac_metro())  # список ближайшего метро в месту работы на вакансии

    """Получение данных уже непосредственно со страниц вакансий"""
    url_vac_for_parse = parsing.api_url_vac()  # список апи сайтов вакансий для дальнейшего парсинга
    exp = []
    for link in url_vac_for_parse:
        api_url_work = GetPage_vac(link)
        parse_api_vac = api_url_work.get_response_vac()
        # print(api_url_work.get_response_vac())
        vac_parse = ParseVac(parse_api_vac)
        vac_experience = vac_parse.get_experience()
        exp.append(vac_experience)
    print(exp, len(exp))

end_time = time.process_time()
print(end_time-start_time)
