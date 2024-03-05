from random import randrange

import vk_api
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import datetime
import bs4
import time
import json
import psycopg2
import configparser

# импорт класса для работы с клавитурой чата ВК
from VK_bot_keyboard import *
# импорт класса для взаимодествия с БД
from work_bd import *

class VKBot:
    def __init__(self, vk_session, botLongpoll, longpoll):
        print("\nСоздан объект бота!")

        self.vk = vk_session  # АВТОРИЗАЦИЯ СООБЩЕСТВА
        self.longpoll = longpoll  # РАБОТА С СООБЩЕНИЯМИ

        self.vk_bot = self.vk.get_api()
        self.botLongpoll = botLongpoll  # РАБОТА С СООБЩЕНИЯМИ


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

        list_date_user = {}
        url = f'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id,
                  'access_token': get_VK_Settings_conf_value('comm_token'),
                  'fields': 'sex, bdate, city',
                  'v': '5.199'}
        repl = requests.get(url, params=params)
        response = repl.json()
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
                     list_date_user['id_city'] = id
                 elif 'city' not in i:
                     self.write_msg(user_id, 'Введите название вашего города: ', 'send')
                     for event in self.longpoll.listen():
                         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                             city_name = event.text
                             list_date_user[city_name] = city_name
                 date_list = date.split('.')
                 list_date_user['date_list'] = date_list
                 if len(date_list) == 3:
                     year = int(date_list[2])
                     year_now = int(datetime.date.today().year)
                     age_now = year_now - year
                     list_date_user['age_now'] = age_now
                     for event in self.longpoll.listen():
                         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                             event.text != ""
                             self.write_msg(user_id, 'Введите нижний порог возраста: ', 'send')
                             for event in self.longpoll.listen():
                                 if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    age_low = event.text
                                    list_date_user['age_low'] = age_low
                                    return list_date_user
                 elif len(date_list) == 2 or date not in information_dict:
                     for event in self.longpoll.listen():
                         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                             event.text != ""
                             self.write_msg(user_id, 'Введите нижний порог возраста для поиска: ', 'send')
                             for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    age_low = event.text
                                    list_date_user['age_low'] = age_low
                                    return list_date_user
        except KeyError:
             self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - comm_token', 'error')

    def get_age_high(self, user_id):
        """Верхняя ганица возраста для поиска пользователей"""
        self.write_msg(user_id, 'Введите верхний порог возраста: ', 'send')
        for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        high_age = event.text       
                        return high_age

    def cities(self, user_id, city_name):
        """ПОЛУЧЕНИЕ ID ГОРОДА ПОЛЬЗОВАТЕЛЯ ПО НАЗВАНИЮ"""
        url = url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': get_VK_Settings_conf_value('user_token'),
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
            self.write_msg(user_id, 'Ошибка получения токена (в методе cities())', 'error')

    def find_city(self, user_id):
        """ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ГОРОДЕ ПОЛЬЗОВАТЕЛЯ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': get_VK_Settings_conf_value('user_token'),
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
                    self.write_msg(user_id, 'Введите название вашего города: ', 'send')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city_name = event.text
                            id_city = self.cities(user_id, city_name)
                            if id_city != '' or id_city != None:
                                return str(id_city)
                            else:
                                break # БОТ ЗАКАНЧИВАЕТ РАБОТУ ЕСЛИ НЕ ВВЕДЕН ГОРОД?
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена (в методе find_city())', 'error')

    def find_partners(self, user_id):
        """ПОИСК ЧЕЛОВЕКА ПО ПОЛУЧЕННЫМ ДАННЫМ"""
        #global city_name
        list_users_id = []
        list_users_params = []
        params_user = self.get_user(user_id)
        if params_user['find_sex'] == 1:
            sex = 2
        else:
            sex = 1
        id_city = params_user['id_city']
        age_low = params_user['age_low']
        age_high = self.get_age_high(user_id)
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': get_VK_Settings_conf_value('user_token'),
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
                    print(first_name)
                    add_VK_Partners(first_name, last_name, vk_id, vk_link)  # вызов функции для занесения параметров в БД

            if list_1 == []:
                self.write_msg(user_id, 'Партнеров не найдено', 'error')
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена (в методе find_partners())', 'error')

    def get_photos_id(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИЙ С РАНЖИРОВАНИЕМ В ОБРАТНОМ ПОРЯДКЕ"""
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': get_VK_Settings_conf_value('user_token'),
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.199'}
        resp = requests.get(url, params=params)
        dict_photos = dict()
        resp_json = resp.json()
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
            return list_of_ids
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена (в методе get_photos_id())', 'error')

    # метод сохранения фотографий в БД        
    def save_photo(self, msg_id):
        # для каждой записи (партнеров) в таблице VK_Partners
        # вызываем метод get.photos_id, если количество фотографий, возвращенных методом, больше или равно 3 шт,
        # то выполняем только запись 3 шт, если меньше 3 шт, то записываем все что есть
        share = 100/select_count_partners()
        for i in range(select_count_partners()): 
            partner_id = select_partner_id(i+1)
            all_partners_photos = self.get_photos_id(partner_id)
            if len(all_partners_photos) >= 3:
                for j in range(3):
                    add_VK_Photos(partner_id, f'photo{partner_id[0]}_{all_partners_photos[j][1]}')
            else:
                for j in range(len(all_partners_photos)):
                    add_VK_Photos(partner_id, f'photo{partner_id[0]}_{all_partners_photos[j][1]}')
            # вывод значений прогресса сохранения фотографий в БД в чат 
            # чтобы исключить ошибку vk_api.exceptions.ApiError: [9] Flood control: too much messages sent to user
            # бот отправляет сообщение о прогрессе 1 раз в 10 пользователей (значение i цикла for)
            if (i+1) % 10 == 0:
                progress = float('{:.1f}'.format(share * i))
                bot.write_msg(active_user, f'Бот собирает фотографии пользователей, это может занять несколько больше секунд...\n Выполнено {progress}%', 'edit', False, msg_id)
        # по окончанию выводим финальное значение 100%
        bot.write_msg(active_user, f'Бот собирает фотографии пользователей, это может занять несколько больше секунд...\n Выполнено 100.0%', 'edit', False, msg_id)
                

    # метод формирования "базового ответа" в чате - представление результатов работы Бота
    def chat_respond(self, user_id, msg_id, msg_type, partner_id):
            partner_info = f'Вот что нашел Бот (пользователей - {select_count_partners()}): \n\n  {select_partner_fn_ln_link(partner_id)}'
            self.write_msg(user_id, partner_info, msg_type, True, msg_id, get_photo(partner_id))


    # метод работы с исходящими от Бота сообщениями
    # метод может выполнять как отправку новых сообщений, так и редактировать существующие
    # также в метод включен "базовый" ответ на запрос "Показать избранных"              
    def write_msg(self, user_id, message, msg_type='send', keys=False, msg_id=None, attachment=None):
        """МЕТОД ДЛЯ ОТПРАВКИ СООБЩЕНИЙ"""
        # тип сообщения - отправка нового сообщения
        if msg_type == 'send':
            # проверка на необходимость клавиатуры в сообщении
            if keys: 
                last_id = self.vk_bot.messages.send(
                    user_id=user_id,
                    random_id=get_random_id(),
                    peer_id=user_id,
                    attachment=attachment,
                    keyboard=vk_keys.keyboard().get_keyboard(),
                    message=message)
                return last_id
            else:
                last_id = self.vk_bot.messages.send(
                    user_id=user_id,
                    random_id=get_random_id(),
                    peer_id=user_id,
                    attachment=attachment,
                    message=message)
                return last_id
        # тип сообщения - редактирование существующего сообщения
        elif msg_type == 'edit':
            # проверка на необходимость клавиатуры в сообщении
            if keys:
                self.vk_bot.messages.edit(
                    peer_id=user_id,
                    message=message,
                    message_id=msg_id,
                    attachment=attachment,
                    keyboard=vk_keys.keyboard().get_keyboard()
                    )
            else:
                self.vk_bot.messages.edit(
                    peer_id=user_id,
                    message=message,
                    message_id=msg_id,
                    attachment=attachment
                    )
        # тип сообщения - ошибка
        elif msg_type == 'error':
            last_id = self.vk_bot.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                peer_id=user_id,
                message=message                
                )
            return last_id
        # тип сообщения - выход
        elif msg_type == 'exit':
            self.vk_bot.messages.edit(
                peer_id=user_id,
                message=message,
                message_id=msg_id,
                keyboard=vk_keys.exit_keys().get_keyboard()
                )
        
        # тип сообщения - показать список избранных
        elif msg_type == 'show_favorite':
            # выборка информации о партнерах из числа добавленных в избранное
            for id in range(select_count_partners()):
                if check_favorite_partner(select_partner_id(id+1))[0]:
                    message += f'\n{select_partner_fn_ln_link(select_partner_id(id+1))}'

            
            self.vk_bot.messages.edit(
                peer_id=user_id,
                message=message,
                message_id=msg_id,
                keyboard=vk_keys.aux_keys().get_keyboard()
                )

    # счетчик значения ID записи в таблице VK_Partners при 
    # осуществлениии навигации среди результатов поиска партнеров
    # в чате ("Следующий пользователь", "Предыдущий пользователь")
    # 
    # принимает значение текущего ID и направление отсчета ("Forward", "Backward")
    # возвращает ID следующего пользователя
    def id_calculator(self, id, type_):
        
        if type_ == 'forward':
            if id == select_count_partners():
                next_id = 1
            else:
                next_id = id + 1
        elif type_ == 'backward':
            if id == 1:
                next_id = select_count_partners()
            else:
                next_id = id - 1
        else:
            next_id = 1

    # проверка не находится ли следующий пользователь в "Черном списке"
        if check_ban_partner(select_partner_id(next_id))[0] == True:
            return self.id_calculator(next_id, type_)

        elif next_id != None :
            return next_id

# метод для первичной настройки работы Бота
def bot_app_init():

    cmd = input('Обновить данные Бота (VK_Settings)? y/n ')

    if cmd == 'y' or cmd == 'Y':
        del_VK_Settings_conf_value('group_id')
        del_VK_Settings_conf_value('comm_token')
        del_VK_Settings_conf_value('user_token')

        add_VK_Settings('group_id', input('Введите ID сообщества - '))
        add_VK_Settings('comm_token', input('Введите токен группы - '))
        add_VK_Settings('user_token', input('Введите токен пользователя - '))
    
    elif cmd == 'n' or cmd == 'N':
        print('ОК')
    
    else:
        print('Ошибка ввода...')
        return bot_app_init()



    
if __name__ == '__main__':

    # работа с БД
    get_password()
    
    # очитска таблиц
    drop_create_table()
     
    # запрос данных для работы с VK API
    bot_app_init()


    # создание сессии и начало работы с API
    vk_session = VkApi(token=get_VK_Settings_conf_value('comm_token'))
    vk = vk_session.get_api()
    botLongpoll = VkBotLongPoll(vk_session, group_id=get_VK_Settings_conf_value('group_id'))
    longpoll = VkLongPoll(vk_session)

    # создание объекта класса для работы с клавиатурой
    vk_keys = VK_chat_keys(vk_session, vk, botLongpoll)

    # переменные для работы Бота
    # 
    # active_user - ID пользователя с которым Бот в настоящее время ведет беседу
    # в соответствии с логикой работы Бота одновременно он может беседовать только с одним пользователем
    # после начала беседы с пользователем, присваевается значени active_user
    active_user = ''

    # переменная current_id определяет значение ID записи в таблице VK_Partners 
    # для отображения в чате и последующей навагиции
    current_id = 1
    
    # создание объекта класса VKBot
    bot = VKBot(vk_session, botLongpoll, longpoll)

    # цикл прослушивания сервера через botLongPoll API
    for event in botLongpoll.listen():
        
        # если событие является новым сообщением от пользователя
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message['text'] != '':
                if bot.get_user_id(event) != None:
                    # если с Ботом еще никто не начал беседу
                    if active_user == '':
                        # присвоить значение active_user
                        active_user = bot.get_user_id(event)

                        # поиск и запись подходящих партнеров в БД
                        msg_id = bot.write_msg(active_user, 'Бот ищет подходящих пользователей, это может занять несколько секунд...', 'send')
                        bot.find_partners(active_user)

                        # поиск и запись фотографий партнеров в БД
                        msg_id = bot.write_msg(active_user, 'Бот собирает фотографии пользователей, это может занять несколько больше секунд...\n Выполнено 0.0%', 'send')
                        bot.save_photo(msg_id)

                        # сообщение о том, что Бот закончил поиск необходима для определения ID (msg_id) последнего сообщения
                        # в псоледующем никаких новых сообщений Бот отправлять не будет - только редактирования сообщения с ID
                        msg_id = bot.write_msg(active_user, 'Бот закончил поиски.', 'send')


                        if select_count_partners() != 0:
                            bot.chat_respond(active_user, msg_id, 'edit', select_partner_id(current_id))
                        else:
                            bot.write_msg(active_user, 'Пользователей с указанными параметрами не найдено.', 'exit', True, msg_id)
                        
                    # если с Ботом уже кто-то беседует
                    if active_user != '':
                        # если к Боту образщается пользователь с user_id отличным от acive_user
                        if active_user != bot.get_user_id(event):
                            # направляем стандартный ответ
                            bot.write_msg(bot.get_user_id(event), 'Ваше обращение очень важно для нас, к сожалению, все Боты заняты, попробуйте написать позже.', 'send', False)

        # если событие явлется событием чата
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            
            # если событие - нажатие кнопки "Следующий пользователь"
            if event.object.payload.get('type') == 'forward':
                
                # присваеваем следующее значение current_id через метод id_calculator()
                current_id = bot.id_calculator(current_id, event.object.payload.get('type'))
                
                # вызов "базового ответа" Бота со следующим current_id партнера (ID таблицы VK_partners)
                bot.chat_respond(active_user, msg_id, 'edit', select_partner_id(current_id))

            # если событие - нажатие кнопки "Предыдущий пользователь"
            elif event.object.payload.get('type') == 'backward':

                # присваеваем следующее значение current_id через метод id_calculator()
                current_id = bot.id_calculator(current_id, event.object.payload.get('type'))
                
                # вызов "базового ответа" Бота со следующим current_id партнера (ID таблицы VK_partners)
                bot.chat_respond(active_user, msg_id, 'edit', select_partner_id(current_id))

            # если событие - нажатие кнопки "Добавить в избранное"
            elif event.object.payload.get('type') == 'like':
                # если партнер не в списке избранного
                if not check_favorite_partner(select_partner_id(current_id))[0]:
                    # устанавливаем значение True в поле 'favorite' для партнера
                    add_favorite_partner(select_partner_id(current_id))
                    
                    # вызываем pop-up уведомление о том, что партнер добавлен в избранное
                    vk_keys.pop_up(active_user, event.object.event_id, 'Добавлено в избранное')
                # если партнер в списке избранного
                else:

                    # вызываем pop-up уведомление о том, что партнер УЖЕ добавлен в избранное
                    vk_keys.pop_up(active_user, event.object.event_id, 'Уже в избранных!')
                
            # если событие - нажатие кнопки "Добавить в черный список"
            elif event.object.payload.get('type') == 'ban':
                # устанавливаем значение True в поле 'ban' для партнера
                add_ban_partner(select_partner_id(current_id))  
                
                # выводим информацию о том. что партнер добавлен в избранное
                bot.write_msg(active_user, f'Пользователь {select_partner_fn_ln_link(select_partner_id(current_id))} отправлен в бан. \n\n Надо двигаться дальше', 'edit', True, msg_id)
                
            # если событие - нажатие кнопки "Показать избранных"
            elif event.object.payload.get('type') == 'show_favorite':

                # выводим список избранных                
                bot.write_msg(active_user, 'Список избранных:', 'show_favorite', False, msg_id)

            # если событие - нажатие кнопки "Вернуться к поиску партнеров" - события выхода из показа спика избранных
            elif event.object.payload.get('type') == 'return':
                # вызов "базового ответа" Бота
                bot.chat_respond(active_user, msg_id, 'edit', select_partner_id(current_id))

            # если событие - нажатие кнопки "Закрыть" (закончить диалог с Ботом)
            elif event.object.payload.get('type') == 'quit':                               
                # выводим информацию о том, как начать диалог с Ботом заново
                bot.write_msg(active_user, 'Для начала работы Бота, обратитесь к нему: "О Великий разум!"', 'edit', False, msg_id)

                # устанавливаем базовые значения переменных
                active_user = ''
                current_id = 1

                # сбрасываем таблицы
                drop_create_table()


                

                
