"""
ЧЕРНОВИК, ЧТО СДЕЛАТЬ ТАК, ЧТОБЫ
ПАРАМЕТРЫ МЫ МОГЛИ ЗАПРАШИВАТЬ У ПОЛЬЗОВАТЕЛЯ
"""
from requests import get
import json


class ParamsForInput:
    """Параметры, задаваемые пользователь. Пользователь сам вводит параметры отбора для интересующейся
    вакансии. Функция возвращает дополненный словарь с нужными для пользователя параметрами"""
    usr_params = {}
    page = 0
    per_page = 100

    def __init__(self, usr_text, page, params=None):
        if params is None:
            params = {'page': 0, 'per_page': 100}
        self.usr_params = params
        self.usr_text = usr_text
        self.page = page

    def get_userparams(self):
        """Пользователь вводит в консоли интересующую его вакансию,
        например 'junior python developer', также можно ввести ключевые слова.
        Метод возвращает введенный тест"""
        self.usr_params['text'] = self.usr_text
        self.usr_params['page'] = self.page
        self.usr_params['per_page'] = self.per_page
        return self.usr_params

    def add_area(self):
        """Пользователь вводит в консоли населенный пункт, в котором производится поиск интересующих его
        вакансий"""
        pass

