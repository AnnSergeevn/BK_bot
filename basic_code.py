from random import randrange
from config import comm_token, photo_token, GROUP_ID, API_VERSION

import vk_api
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import datetime
import bs4
import time
import json


class VKBot:
    def __init__(self):
        print("\nСоздан объект бота!")
        self.vk = vk_api.VkApi(token=comm_token)  # АВТОРИЗАЦИЯ СООБЩЕСТВА
        self.longpoll = VkLongPoll(self.vk)  # РАБОТА С СООБЩЕНИЯМИ

    def write_msg(self, user_id, message):
        """МЕТОД ДЛЯ ОТПРАВКИ СООБЩЕНИЙ"""
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def get_user_id(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message['text'] != '':
                if event.from_user:
                    #print(f'USER_ID {event.obj.message["from_id"]} ')
                    user_id = event.obj.message["from_id"]
                    return user_id

    def get_user(self, user_id):
        """Получение имени пользователя, который написал боту, пола, возраста, города, в котором он проживает.
        Получение нижней границы возраста для поиска людей"""

        print("\nПолучено имя пользователя!")
        list_date_user = {}
        url = f'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id,
                  'access_token': comm_token,
                  'fields': 'sex, bdate, city',
                  'v': '5.199'}
        repl = requests.get(url, params=params)
        #print(repl.url)
        response = repl.json()
        #print(response)
        try:
             information_dict = response['response']
             for i in information_dict:
                 first_name = i.get('first_name')
                 find_sex = i.get('sex')
                 date = i.get('bdate')
                 list_date_user['first_name'] = first_name
                 list_date_user['find_sex'] = find_sex
                 if 'city' in i:
                     city = i.get('city')
                     id = str(city.get('id'))
                     #title = str(city.get('title'))
                     list_date_user['id_city'] = id
                 elif 'city' not in i:
                     self.write_msg(user_id, 'Введите название вашего города: ')
                     for event in self.longpoll.listen():
                         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                             city_name = event.text
                             #print(city_name)
                             list_date_user[city_name] = city_name
                 date_list = date.split('.')
                 print(date_list)
                 list_date_user['date_list'] = date_list
                 if len(date_list) == 3:
                     year = int(date_list[2])
                     year_now = int(datetime.date.today().year)
                     age_now = year_now - year
                     list_date_user['age_now'] = age_now
                     for event in self.longpoll.listen():
                         print(self.longpoll.listen())
                         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                             event.text != ""
                             self.write_msg(user_id, 'Введите нижний порог возраста: ')
                             for event in self.longpoll.listen():
                                 print(self.longpoll.listen())
                                 if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    print(event.text, "Тест события")
                                    age_low = event.text
                                    print(age_low)
                                    list_date_user['age_low'] = age_low
                                    #print(list_date_user)
                                    return list_date_user
                 elif len(date_list) == 2 or date not in information_dict:
                     for event in self.longpoll.listen():
                         print(self.longpoll.listen())
                         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                             event.text != ""
                             self.write_msg(user_id, 'Введите нижний порог возраста для поиска: ')
                             for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    age_low = event.text
                                    list_date_user[age_low] = age_low
                                    return list_date_user
        except KeyError:
             self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    def get_age_high(self, user_id):
        """Верхняя ганица возраста для поиска пользователей"""
        self.write_msg(user_id, 'Введите верхний порог возраста: ')
        for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        high_age = event.text
                        print(high_age)
                        return high_age

    def cities(self, user_id, city_name):
        """ПОЛУЧЕНИЕ ID ГОРОДА ПОЛЬЗОВАТЕЛЯ ПО НАЗВАНИЮ"""
        url = url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': photo_token,
                  'country_id': 1,
                  'q': f'{city_name}',
                  'need_all': 0,
                  'count': 1000,
                  'v': '5.199'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            list_cities = information_list['items']
            for i in list_cities:
                found_city_name = i.get('title')
                if found_city_name == city_name:
                    found_city_id = i.get('id')
                    return int(found_city_id)
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_city(self, user_id):
        """ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ГОРОДЕ ПОЛЬЗОВАТЕЛЯ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': photo_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': '5.199'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for i in information_dict:
                if 'city' in i:
                    city = i.get('city')
                    id = str(city.get('id'))
                    return id
                elif 'city' not in i:
                    self.write_msg(user_id, 'Введите название вашего города: ')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city_name = event.text
                            id_city = self.cities(user_id, city_name)
                            if id_city != '' or id_city != None:
                                return str(id_city)
                            else:
                                break
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_user(self, user_id):
        """ПОИСК ЧЕЛОВЕКА ПО ПОЛУЧЕННЫМ ДАННЫМ"""
        #global city_name
        list_users_id = []
        list_users_params = []
        params_user = self.get_user(user_id)
        sex = params_user['find_sex']
        id_city = params_user['id_city']
        age_low = params_user['age_low']
        age_high = self.get_age_high(user_id)
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': photo_token,
                  'v': '5.199',
                  'sex': sex,
                  'age_from': age_low,
                  'age_to': age_high,
                  'city': self.find_city(user_id),
                  'fields': 'is_closed, id, first_name, last_name',
                  'status': '1' or '6',
                  'count': 500}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        try:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
            for person_dict in list_1:
                if person_dict.get('is_closed') == False:
                    first_name = person_dict.get('first_name')
                    last_name = person_dict.get('last_name')
                    vk_id = str(person_dict.get('id'))
                    vk_link = 'vk.com/id' + str(person_dict.get('id'))
                    insert_data_users(first_name, last_name, vk_id, vk_link)   # вызов функции для занесения параметров в БД

            if list_1 == []:
                self.write_msg(user_id, 'Партнеров не найдено')
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photos_id(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИЙ С РАНЖИРОВАНИЕМ В ОБРАТНОМ ПОРЯДКЕ"""
        #print(user_id)
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': photo_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.199'}
        resp = requests.get(url, params=params)
        #print(resp.url)
        dict_photos = dict()
        resp_json = resp.json()
        #print(resp_json)
        try:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
            for i in list_1:
                photo_id = str(i.get('id'))
                i_likes = i.get('likes')
                if i_likes.get('count'):
                    likes = i_likes.get('count')
                    dict_photos[likes] = photo_id
            list_of_ids = sorted(dict_photos.items(), reverse=True)
            #print(list_of_ids)
            return list_of_ids
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photo_1(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ № 1"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 1:
                return i[1]

    def get_photo_2(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ № 2"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 2:
                return i[1]

    def get_photo_3(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ № 3"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 3:
                return i[1]

    def send_photo_1(self, user_id, message):
        """ОТПРАВКА ПЕРВОЙ ФОТОГРАФИИ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': photo_token,
                                         'message': message,
                                         'attachment': f'photo{73680897}_{self.get_photo_1(73680897)}',
                                         'random_id': 0})

    def send_photo_2(self, user_id, message):
        """ОТПРАВКА ВТОРОЙ ФОТОГРАФИИ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': photo_token,
                                         'message': message,
                                         'attachment': f'photo{73680897}_{self.get_photo_2(73680897)}',
                                         'random_id': 0})

    def send_photo_3(self, user_id, message):
        """ОТПРАВКА ТРЕТЬЕЙ ФОТОГРАФИИ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': photo_token,
                                         'message': message,
                                         'attachment': f'photo{73680897}_{self.get_photo_3(73680897)}',
                                         'random_id': 0})

    def find_persons(self, user_id):
        #self.write_msg(user_id, self.found_person_info(id_bd))    # вывод в бот информации о найденном пользователе
        self.write_msg(user_id, "Информация о пользователе")
        #self.find_user(user_id) # id того кто ищет
        #self.person_id(id_bd)
        self.get_photos_id(73680897) # id чьи фото ищем
        self.send_photo_1(user_id, 'Фото номер 1')
        if self.get_photo_2(73680897) != None:
            self.send_photo_2(user_id, 'Фото номер 2')
        if self.get_photo_3(73680897) != None:
            self.send_photo_3(user_id, 'Фото номер 3')
        else:
            self.write_msg(user_id, f'Больше фотографий нет')

    def found_person_info(self, id_bd):
        """ВЫВОД ИНФОРМАЦИИ О НАЙДЕННОМ ПОЛЬЗОВАТЕЛИ ИЗ БД"""
        pass

    def person_id(self, id_bd):
        """ВЫВОД ID НАЙДЕННОГО ПОЛЬЗОВАТЕЛЯ ИЗ БД"""
        pass



if __name__ == '__main__':
    
    # создание сессии и начало работы с API
    vk_session = VkApi(token=comm_token, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    bot = VKBot()
    user_id = []
    i = 0
    for ind, event in enumerate(longpoll.listen()):
            # обработка входящих сообщений
            bot.get_user_id(event)
            user_id.append(bot.get_user_id(event))
            if ind == 1:
                break
    bot.find_persons(user_id[1])
    #bot.find_user(user_id[1])

    