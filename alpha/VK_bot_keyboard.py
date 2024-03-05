from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

class VK_chat_keys:
    def __init__(self, vk_session, vk, longpoll):        

        self.vk_session = vk_session
        self.vk = vk
        self.longpoll = longpoll

    #описание и создание клавиатуры
    def keyboard(self):
        #определяем тип кнопок
        settings = dict(one_time=False, inline=True) 
        keyboard = VkKeyboard(**settings) 

        #создаем кнопки
        keyboard.add_callback_button(label="Следующий пользователь", color=VkKeyboardColor.PRIMARY, payload={"type": "forward"})
        keyboard.add_line()
        keyboard.add_callback_button(label="Предыдущий пользователь", color=VkKeyboardColor.PRIMARY, payload={"type": "backward"})
        keyboard.add_line()
        keyboard.add_callback_button(label="Добавить в избранное", color=VkKeyboardColor.POSITIVE, payload={"type": "like"})
        keyboard.add_line()
        keyboard.add_callback_button(label="Добавить в черный список", color=VkKeyboardColor.NEGATIVE, payload={"type": "ban"})
        keyboard.add_line()
        keyboard.add_callback_button(label="Показать избранных", color=VkKeyboardColor.POSITIVE, payload={"type": "show_favorite"})
        keyboard.add_line()
        keyboard.add_callback_button(label="Закрыть", color=VkKeyboardColor.NEGATIVE, payload={"type": "quit"})

        #возвращаем созданный объект
        return keyboard

    def aux_keys(self):
        # определяем тип кнопок для вспомогательного меню - возврат из списка избранных
        settings = dict(one_time=False, inline=True) 
        aux_keyboard = VkKeyboard(**settings) 

        # создаем кнопку
        aux_keyboard.add_callback_button(label="Вернуться к поиску партнеров", color=VkKeyboardColor.PRIMARY, payload={"type": "return"})

        return aux_keyboard

    def exit_keys(self):
        # определяем тип кнопки - закрыть
        settings = dict(one_time=False, inline=True) 
        exit_keyboard = VkKeyboard(**settings) 

        # создаем кнопку
        exit_keyboard.add_callback_button(label="Закрыть", color=VkKeyboardColor.NEGATIVE, payload={"type": "quit"})

        return exit_keyboard

    def pop_up(self, user_id, event_id, msg):
        payload = {
            'type': 'show_snackbar',
            'text': msg
        }

        resp = self.vk.messages.sendMessageEventAnswer(
            event_id=event_id,
            user_id=user_id,
            peer_id=user_id,                                                   
            event_data=json.dumps(payload))


