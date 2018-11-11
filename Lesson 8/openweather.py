"""
== OpenWeatherMap ==
OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.
Необходимо решить следующие задачи:
== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.

    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID,
    используя дополнительную библиотеку GRAB (pip install grab)
        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up
        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in
        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys

        Ключ имеет смысл сохранить в локальный файл, например, "app.id"

== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz

    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка
     (воспользоваться модулем gzip
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)

    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}


== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a
    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a
    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a
    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}
== Сохранение данных в локальную БД ==
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):
    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных
2. Выводить список стран из файла и предлагать пользователю выбрать страну
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))
3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.
При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.
При работе с XML-файлами:
Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>
Чтобы работать с пространствами имен удобно пользоваться такими функциями:
    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''
    tree = ET.parse(f)
    root = tree.getroot()
    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}
    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...
"""
from interface import clear, interface

import os
import urllib.request
import urllib.parse
import gzip
import json

import sqlite3
from sqlite3 import Error

BASE_PATH = 'data'
LIST_NAME = 'city.list'
LIST_URL = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
SOURCE_LINK = 'http://api.openweathermap.org/data/2.5/weather'
APPID_FILE = 'app.id'


interface.selected_city = None


def url_request(url, params, method="GET"):
    if method == "POST":
        return urllib.request.urlopen(url, data=urllib.parse.urlencode(params))
    else:
        return urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params))


def appid():
    # Получение App ID из файла
    with open(APPID_FILE, encoding="utf-8") as appid:
        result = appid.read()
        return result


def init_citylist():
    # Проверка наличия рабочей директории
    if not os.path.exists(BASE_PATH):
        os.mkdir(BASE_PATH)

    # Проверка наличия списка городов
    if not os.path.isfile(os.path.join(BASE_PATH, LIST_NAME+'.json')):
        print('Список городов подготавливается...')

        # Загрузка архива
        if not os.path.isfile(os.path.join(BASE_PATH, LIST_NAME + '.json.gz')):
            print('Загрузка файла из интернета...')
            try:
                urllib.request.urlretrieve(LIST_URL, os.path.join(BASE_PATH, LIST_NAME+'.json.gz'))
            except urllib.error.URLError:
                print('Ошибка: не удалось загрузить базу данных')
            else:
                print('База городов успешно загружена')

        # Распаковка архива
        if not os.path.isdir(os.path.join(BASE_PATH, LIST_NAME+'.json.gz')):
            with gzip.open(os.path.join(BASE_PATH, LIST_NAME+'.json.gz'), 'rb') as in_file:
                s = in_file.read()
            open(os.path.join(BASE_PATH, LIST_NAME+'.json'), 'wb').write(s)
            print('База городов успешно распакована')

    # Преобразование списка городов из JSON в словарь
    with open(os.path.join(BASE_PATH, LIST_NAME+'.json'), encoding="utf-8") as file:
        city_list = json.load(file)

    return city_list


def check_inter():
    print(init_citylist())

def city_select():
    city_list = init_citylist()
    country_list = []
    for city in city_list:
        if city['country'] not in country_list and city['country'] != '':
            country_list.append(city['country'])
    country_list.sort()

    clear()
    print('Список стран:')
    for key in range(len(country_list)//20+1):
        print(str(country_list[key*20:key*20+20]))
    input_country = input('\nУкажите страну: ')

    filtred_city_list = []
    for city in city_list:
        if city['country'] == input_country:
            filtred_city_list.append(city['name'])
    filtred_city_list.sort()

    if filtred_city_list == []:
        interface.selected_city = None
        clear()
        print('Указанная страна не найдена\n')
        return

    clear()
    print('Список городов:')
    for key in range(len(filtred_city_list)//5+1):
        print(str(filtred_city_list[key*5:key*5+5]))
    input_city = input('\nУкажите город: ')

    for city in city_list:
        if city['name'] == input_city:
            interface.selected_city = city
            clear()
            print(f'Выбранный город: {interface.selected_city}\n')
            break
        else:
            interface.selected_city = None

    if interface.selected_city is None:
        interface.selected_city = None
        clear()
        print('Такого города нет в списке\n')


def print_selected_city():
    clear()
    print(f'Выбранный город: {interface.selected_city}\n')


def print_weather():
    if interface.selected_city is not None:
        params = dict(
            id=interface.selected_city['id'],
            units='metric',
            appid=appid()
        )
        try:
            data = json.load(url_request(SOURCE_LINK, params))
        except urllib.error.URLError:
            print('Ошибка соединения\n')
        else:
            print(f'Погода в городе: {interface.selected_city["name"]}\nСтрана: {interface.selected_city["country"]}')
            print(f'Основная информация: {data["weather"][0]["main"]} - {data["weather"][0]["description"]}')
            print(f'Температура: {data["main"]["temp"]} градусов по Цельсию')
            print()


clear()
tasks = {'0': (city_select, 'Выбрать город', []),
         '1': (print_selected_city, 'Вывести на экран выбранный город', []),
         '2': (print_weather, 'Какая погода в выбранном городе')}

interface(tasks)

