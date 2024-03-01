# Описание

## Базы данных:
1. По 1 этапу разработана структура БД:
- VK_bot_db_structure.drawio
- VK_bot_structure.pdf
2. По 2 этапу разработан скрипт создания таблиц БД:
- VK_bot_create_sql_script.sql - Создание таблиц VK_Partners, VK_Photos, VK_settings
- VK_bot_drop_sql_script.sql - Сборс таблиц VK_Partners, VK_Photos

## Чат-бот:
1. По 3 этапу разработаны модули:
- VK_chat_keyboard.pу - модуль клавиатуры для чат-бота
- VK_token_get.py - модуль получения токена пользователя 

## Класс и методы класса `VK_keys` модуля `VK_chat_keyboard.pу`:
1. Основной класс `VK_keys` содержит два метода:
    - `keybord()` - создание и описание объекта клавиатуры.
    - `message_handler()` - обработка входящих сообщений и  событий в чате, принимает параметр `event` от метода `VkBotLongPoll.listen()` (Long Poll API <https://vk-api.readthedocs.io/en/latest/longpoll.html>)

## Модуль `VK_token_get.py`:
1. После исполнения модуль выводит `access_token` в терминал
2. Если веб-сессия VK была закрыта - потребуется указать логин и пароль VK в теле модуля
