from random import randrange
from config import comm_token

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import datetime
import bs4

class VKBot:
    def __init__(self):
        print("\nСоздан объект бота!")
        self.vk = vk_api.VkApi(token=comm_token)  # АВТОРИЗАЦИЯ СООБЩЕСТВА
        self.longpoll = VkLongPoll(self.vk)  # РАБОТА С СООБЩЕНИЯМИ

    def write_msg(self, user_id, message):
        """МЕТОД ДЛЯ ОТПРАВКИ СООБЩЕНИЙ"""
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def get_name_sex(self, user_id):
        """ПОЛУЧЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ НАПИСАЛ БОТУ"""
        print("\nПолучено имя пользователя!")
        url = f'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id,
                  'access_token': comm_token,
                  'fields': 'sex',
                  #'fields': ['sex', "bdate", 'city'],
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
                 print(find_sex)
                 print(first_name)
                 return first_name, find_sex
        except KeyError:
             self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    def get_age(self, user_id):
        """ПОЛУЧЕНИЕ ВОЗРАСТА ПОЛЬЗОВАТЕЛЯ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id,
                  'access_token': comm_token,
                  'fields': 'bdate',
                  'v': '5.199'}
        repl = requests.get(url, params=params)
        response = repl.json()
        print(response)
        information_list = response['response']
        for i in information_list:
            date = i.get('bdate')
        date_list = date.split('.')
        print(date_list)
        if len(date_list) == 3:
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            age_now = year_now-year
            self.write_msg(user_id, 'Введите нижний порог возраста: ')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age_low = event.text
            self.write_msg(user_id, 'Введите верхний порог возраста: ')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age_high = event.text
        elif len(date_list) == 2 or date not in information_list:
            self.write_msg(user_id, 'Введите нижний порог возраста: ')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age_low = event.text
            self.write_msg(user_id, 'Введите верхний порог возраста: ')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age_high = event.text
        return age_now, age_low, age_high

    def find_city(self, user_id):
        """ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ГОРОДЕ ПОЛЬЗОВАТЕЛЯ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id,
                  'access_token': comm_token,
                  'fields': 'city',
                  'v': '5.199'}
        repl = requests.get(url, params=params)
        response = repl.json()
        information_dict = response['response']
        for i in information_dict:
            if 'city' in i:
                city = i.get('city')
                id = str(city.get('id'))
                print(id)
                return id
            elif 'city' not in i:
                self.write_msg(user_id, 'Введите название вашего города: ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        city_name = event.text
                        return city_name


if __name__ == '__main__':
    bot = VKBot()
    bot.get_name_sex(423567)
    bot.get_age(423567)
    bot.find_city(423567)
