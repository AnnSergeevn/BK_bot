from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

class VK_chat_keys:

    #описание и создание клавиатуры
    def keyboard(self):
        #определяем тип кнопок
        settings = dict(one_time=False, inline=True) 
        keyboard_1 = VkKeyboard(**settings) 

        #создаем кнопки
        keyboard_1.add_callback_button(label="Следующий пользователь", color=VkKeyboardColor.PRIMARY, payload={"type": "next_photo"})
        keyboard_1.add_line()
        keyboard_1.add_callback_button(label="Предыдущий пользователь", color=VkKeyboardColor.PRIMARY, payload={"type": "previous_photo"})
        keyboard_1.add_line()
        keyboard_1.add_callback_button(label="Добавить в избранное", color=VkKeyboardColor.POSITIVE, payload={"type": "like"})
        keyboard_1.add_line()
        keyboard_1.add_callback_button(label="Добавить в черный список", color=VkKeyboardColor.NEGATIVE, payload={"type": "ban"})
        keyboard_1.add_line()
        keyboard_1.add_callback_button(label="Показать избранных", color=VkKeyboardColor.POSITIVE, payload={"type": "show_favorite"})
        keyboard_1.add_line()
        keyboard_1.add_callback_button(label="Изменить диапазон возраста для поиска", color=VkKeyboardColor.PRIMARY, payload={"type": "change_age_gap"})

        #возвращаем созданный объект
        return keyboard_1

    #обработка событий в сообщениях
    def message_handler(self, event, active_peer):
        #если пришло сообщение от пользователя (начало переписки), то отправить клавиатуру
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message['text'] != '':
                if event.from_user:
                    if 'callback' not in event.obj.client_info['button_actions']:
                        print(f'Клиент {event.obj.message["from_id"]} не поддерж. callback')
                    #проверка id собеседника (активный собеседеник или новый собеседник)
                    if active_peer == event.obj.message['from_id'] or active_peer == '':
                        vk.messages.send(
                                user_id=event.obj.message['from_id'],
                                random_id=get_random_id(),
                                peer_id=event.obj.message['from_id'],
                                keyboard=self.keyboard().get_keyboard(),
                                message=event.obj.message['text'])
                    #если в чат подключается посторонний - отправлять сообщение "Я занят"
                    else:
                        vk.messages.send(
                                user_id=event.obj.message['from_id'],
                                random_id=get_random_id(),
                                peer_id=event.obj.message['from_id'],
                                message="Я занят")


        #если пришло событие нажатие кнопки, то обработать это событие и вернуть значение
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            #следующий пользователь
            if event.object.payload.get('type') == 'next_photo':
                return 'forward'
            #предыдущий пользователь
            elif event.object.payload.get('type') == 'previous_photo':
                return 'backward'
            #изменить диапазон поиска по возрасту
            elif event.object.payload.get('type') == 'change_age_gap':
                return 'change_age_gap'
            #добавить пользователя в избранное
            elif event.object.payload.get('type') == 'like':
                return 'like'
            #добавить ползователя в черный список
            elif event.object.payload.get('type') == 'ban':
                return 'ban'
            #вывести список всех избранных
            elif event.object.payload.get('type') == 'show_favorite':
                return 'show_favorite'




if __name__ == '__main__':
    #описание параметров работы с API
    #id сообщества
    GROUP_ID = '224805178'
    #токен сообщества
    GROUP_TOKEN = 'vk1.a.U9H9VPRMeR1gkIruwCdtkJoVbhtdI3oZuj5J_ey9_v698SyEwM1JWXLaHWDF1pWxZeUM0Bd3kRL0Qe-jEQoN17Tw32Nw4PyIJw_m53vzvpp_3BkEstHL2wGo_8jr3wxZRSCkNXZ3Zfgfha4OGtXeEa0oCLOsQEDwqDnQMfkpBoG2hPSexTOVh75LvLuQeClSulbfF24akpCdxWOjoRfeuw'

    API_VERSION = '5.120'
    #создание сессии и начало работы с API
    vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    #создание объекта vk_keys 
    vk_keys = VK_chat_keys()

    #ожидание сообщений от сервера по Long Poll Api
    for event in longpoll.listen():
        #обработка входящих сообщений
        print(vk_keys.message_handler(event< active_peer))