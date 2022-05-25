"""
ВЫБОР ЛОКАЦИИ САМИМ ПОЛЬЗОВАТЕЛЕМ В КОНСОЛИ
(МОЖНО СТРАНУ ЦЕЛИКОМ, МОЖНО ОБЛАСТЬ, РЕГИОН, ГОРОД ИЛИ ЛЮБОЙ ДРУГОЙ НАСЕЛЕННЫЙ ПУНКТ)
"""

from requests import get
from pprint import pprint


def get_areas():
    """Получаем набор всех доступных локаций для поиска: название и id.
    Функция возвращает кортеж (или словарь) из всех доступных для поиска локаций"""
    url = 'https://api.hh.ru/areas'
    response = get(url)
    data = response.json()
    return data


class Area:
    """
    Класс Area позволяет определить id нужной для пользователя локации, которой он интересуется и
    вводит в консоль.
    Имеет несколько дочерних классов: Country, Region, City.
    """
    datas = get_areas()  # кладем в переменную datas json, где подробно приведены все локации
    user_area = []

    def __init__(self):
        pass

    def get_area(self):
        """Метод позволяет получить id нужной локации"""
        pass


class Country(Area):
    """
    Пользователь выбирает страну, в которой его интересует вакансия.
    """

    def __init__(self, usr_country=None):
        super().__init__()
        if usr_country is None:
            usr_country = {}
        self.usr_country = usr_country

    def get_countries(self):
        """
        Формируем словарь из стран как результат парсинга API hh.ru.
        Перебираем списки со странами, вытаскиваем оттуда name и id, и кладем в словарь.
        Функция возвращает переменную countries, в которой находится словарь, состоящий из ключа
        (название страны) и значения (id страны).
        """
        countries = {}  # создаем пустой словарь
        for i in range(len(self.datas)):  # в цикле перебираем списки со странами
            countries[self.datas[i]['name']] = self.datas[i]['id']  # сохраняем название страны и его айди
        return countries  # возвращаем словарь со странами

    def get_other_countries(self):
        """
        Формируем словарь остальных стран, если пользователю интересна другая страна, отличная от списка
        этих стран: Россия, Украина, Казахстан, Азербайджан, Беларусь, Грузия, Кыргызстан, Узбекистан.
        Перебираем списки со странами, вытаскиваем оттуда name и id, и кладем в словарь.
        Функция возвращает переменную other_countries, в которой находится словарь, состоящий из ключа
        (название страны) и значения (id страны).
        """
        other_countries = {}  # создаем пустой словарь
        for i in range(len(self.datas)):  # в цикле перебираем списки со странами
            if self.datas[i]['name'] == 'Другие регионы':
                for j in range(len(self.datas[i]['areas'])):
                    other_countries[self.datas[i]['areas'][j]['name']] = self.datas[i]['areas'][j][
                        'id']  # сохраняем название страны и его айди
        return other_countries  # возвращаем словарь со странами

    """Разобраться с декоратором"""
    def str(self):
        countries = Country().get_countries()  # сохраняем в словарь со странами в переменную countries
        lst_countries = list(countries.keys())  # создаем список стран + "Другие регионы"
        print(', '.join(lst_countries), end='.\n')  # выводим на печать этот список
        while True:  # создаем проверку ввода страны
            try:
                user_country = input('Введите название страны: ')  # пользователь вводит страну
                if isinstance(user_country, str):  # проверка типа ввода данных на то, что это строка
                    user_country = user_country.capitalize()  # преобразуем первую букву слова в верхний регистр
                    if user_country != 'Другие регионы':  # проверяем, что в переменной user_country не находится строчка
                        # "Другие страны"
                        self.usr_country = countries[user_country]
                        return countries[user_country]  # возвращаем код страны
            except KeyError:
                print('Данной страны нет в вышеперечисленных вариантах, повторите ввод')
            else:
                """проделываем то же самое с другими регионами, но здесь используем другую функцию для вывода стран"""
                othercountries = Country().get_other_countries()
                print('Остальные страны:')
                print(*othercountries.keys(), sep=', ')
                try:
                    user_othercountry = input('Введите название страны из предложенного списка: ')
                    user_othercountry = user_othercountry.lower()  # сначала преобразуем строку в нижний регистр, потому что некоторые страны имеют аббревиатуру (верхний регистр)
                    if isinstance(user_othercountry, str):
                        if user_othercountry in ('оаэ', 'сша', 'юар'):
                            user_othercountry = user_othercountry.upper()
                        else:
                            user_othercountry = user_othercountry.title()  # преобразуем первую букву каждого слова в верхний регистр
                        self.usr_country = othercountries[user_othercountry]
                        return othercountries[user_othercountry]
                except KeyError:
                    print('Данной страны нет в вышеперечисленных вариантах, повторите ввод')



class Region(Area):
    """
    Метод применяется к странам - Россия, Беларусь, Украина, Узбекистан, Азербайджан, Кыргызстан, Казахстан, Грузия
    (все, кроме "Другие регионы").
    Пользователь вводит название региона, программа находит этот регион в списке и находит его id.
    Россия, Беларусь, Украина - результат - id региона (область/край/республика/АО).
    Узбекистан, Азербайджан, Кыргызстан, Казахстан, Грузия - только id региона
    :return: код региона
    """

    def get_region(self):
        """
        Формируем словарь из регионов как результат парсинга API hh.ru.
        Перебираем списки со странами, вытаскиваем оттуда name и id, и кладем в словарь.
        :return: переменную countries, в которой находится словарь, состоящий из ключа
        (название страны) и значения (id страны).
        """
        regions = {}
        for i in range(len(self.datas)):
            if self.datas[i]['id'] == Country().usr_country:
                for j in range(len(self.datas[i]['areas'])):
                    name = self.datas[i]['areas'][j]['name']
                    id = self.datas[i]['areas'][j]['id']
                    regions[name] = id
        return regions


class City(Area):
    pass


n = Country()
print(n.str())
print(n.usr_country)
print(Region().get_region())

# 0 - Россия
# 1 - Украина
# 2 - Казахстан
# 3 - Азербайджан
# 4 - Беларусь
# 5 - Грузия
# 6 - Другие регионы (другие страны) ()
# 7 - Кыргызстан
# 8 - Узбекистан
