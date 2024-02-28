from random import randrange
from config import comm_token, user_token, photo_token

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import datetime
import bs4
import time

class VKBot:
    def __init__(self):
        print("\nСоздан объект бота!")
        self.vk = vk_api.VkApi(token=comm_token)  # АВТОРИЗАЦИЯ СООБЩЕСТВА
        self.longpoll = VkLongPoll(self.vk)  # РАБОТА С СООБЩЕНИЯМИ

    def write_msg(self, user_id, message):
        """МЕТОД ДЛЯ ОТПРАВКИ СООБЩЕНИЙ"""
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

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
        print(repl.url)
        response = repl.json()
        print(response)
        try:
             information_dict = response['response']
             for i in information_dict:
                 first_name = i.get('first_name')
                 find_sex = i.get('sex')
                 date = i.get('bdate')
                 print(date)
                 print(find_sex)
                 print(first_name)
                 list_date_user['first_name'] = first_name
                 list_date_user['find_sex'] = find_sex

                 if 'city' in i:
                     city = i.get('city')
                     id = str(city.get('id'))
                     title = str(city.get('title'))
                     print(city)
                     list_date_user['id_city'] = id
                 elif 'city' not in i:
                     self.write_msg(user_id, 'Введите название вашего города: ')
                     for event in self.longpoll.listen():
                         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                             city_name = event.text
                             print(city_name)
                             list_date_user[city_name] = city_name
                 date_list = date.split('.')
                 print(date_list)
                 list_date_user['date_list'] = date_list
                 if len(date_list) == 3:
                     year = int(date_list[2])
                     year_now = int(datetime.date.today().year)
                     age_now = year_now - year
                     list_date_user['age_now'] = age_now
                     self.write_msg(user_id, 'Введите нижний порог возраста: ')
                     for event in self.longpoll.listen():
                         print(self.longpoll.listen())
                         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                             print(event.type)
                             age_low = event.text
                             print(age_low)
                             list_date_user['age_low'] = age_low
                             print(list_date_user)
                             return list_date_user
                 elif len(date_list) == 2 or date not in information_list:
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
        global city_name
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
            #print(list_1)
            for person_dict in list_1:
                if person_dict.get('is_closed') == False:
                    dict_users_params = {}
                    first_name = person_dict.get('first_name')
                    last_name = person_dict.get('last_name')
                    vk_id = str(person_dict.get('id'))
                    list_users_id.append(vk_id)
                    vk_link = 'vk.com/id' + str(person_dict.get('id'))
                    list_users_id.append(vk_id)
                    dict_users_params["first_name"] = first_name
                    dict_users_params["last_name"] = last_name
                    dict_users_params["vk_id"] = vk_id
                    dict_users_params["vk_link"] = vk_link
                    list_users_params.append(dict_users_params)
            if list_1 == []:
                self.write_msg(user_id, 'Партнеров не найдено')
            print(list_users_params)
            return list_users_params                              # занести пользователей в БД
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photos_id(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИЙ С РАНЖИРОВАНИЕМ В ОБРАТНОМ ПОРЯДКЕ"""
        print(user_id)
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
            print(list_of_ids)
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
    bot = VKBot()
    bot.find_persons(423567)

