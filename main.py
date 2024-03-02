from work_bd import drop_create_table, add_VK_Partners, add_VK_Photos, select_count_partners, check_ban_partner
from work_bd import add_ban_partner, check_favorite_partner, add_favorite_partner, select_partner, get_photo
from work_bd import select_partner_fn_ln_link, select_partner_id
# from basic_code import VKBot








if __name__ == '__main__':
    # 1.Вызов функции DROP удаления (если есть) и создания (без данных) таблиц VK_Partners, VK_Photos, VK_Settings
    # drop_create_table()

    # Создаем экземпляр класса VKBot
    # vkbot = VKBot()
    # vkbot.find_user(716450769)
    # print(data1)

    # 10.Вызов функции получения данных о партнере (имя, фамилия, линк) по id из таблицы VK_Partners
    data2 = select_partner_fn_ln_link(1)
    print(data2)

    # 11.Вызов функции получения данных о партнере (partner_id) по id из таблицы VK_Partners
    data3 = select_partner_id(3)
    print(data3)









    # # Получаем список партнеров с данными (имя, фамилия, id) из get-запроса
    # list_VK_Partners = [['Петя', 'Пупкин', '111111'], ['Вова', 'Тяпкин', '2222222'], ['Саня', 'Ляпкин', '3333333']]
    # # Записываем каждый элемент списка (каждого партнера по очереди) в таблицу VK_Partners
    # for partner in list_VK_Partners:
    #     add_VK_Partners(*partner)
    #     # print(add_VK_Partners(*partner))
    #
    #
    # # Получаем список фото (id, link) из get-запроса
    # list_VK_Photos = [['111111', 'photo_1'], ['111111', 'photo_2'], ['111111', 'photo_3'], ['2222222', 'photo_1'],
    #                   ['2222222', 'photo_2'], ['2222222', 'photo_3'], ['3333333', 'photo_1'], ['3333333', 'photo_2'],
    #                   ['3333333', 'photo_3']]
    # # Записываем каждый элемент списка (каждое фото по очереди) в таблицу VK_Photos
    # for photo in list_VK_Photos:
    #     add_VK_Photos(*photo)
    #
    #
    # # Получаем количество партнеров в таблице VK_Partners
    # count_partners = select_count_partners()
    # print('Количество партнеров', *count_partners)
    #
    # # Проверка, что партнер (partner_id) в бане (True, False)
    # partner_id = '111111'
    # check_ban = check_ban_partner(partner_id)
    # print('Партнер в бане', *check_ban)
    #
    #
    # # Добавление партнера (partner_id) в бан (ban = True)
    # # И запрос , что партнер (partner_id) в бане (True, False)
    # partner_id = '3333333'
    # add_ban = add_ban_partner(partner_id)
    # check_ban = check_ban_partner(partner_id)
    # print('Партнер в бане', *check_ban)
    #
    #
    # # Проверка, что партнер (partner_id) в избранном (True, False)
    # partner_id = '111111'
    # check_favorite = check_favorite_partner(partner_id)
    # print('Партнер в избранном', *check_favorite)
    #
    #
    # # Добавление партнера (partner_id) в избранное (favorite = True)
    # # И запрос , что партнер (partner_id) в избранном (True, False)
    # partner_id = '111111'
    # add_favorite = add_favorite_partner(partner_id)
    # check_favorite = check_favorite_partner(partner_id)
    # print('Партнер в избранном', *check_favorite)
    #
    #
    # # Получение всех данных о партнере (имя, фамилия, id, фото)
    # partner_id = '111111'
    # partner = select_partner(partner_id)
    # print(partner)
    #
    #
    # # Получаем фото из таблицы VK_Photos по partner_id (id партнера)
    # partner_id = '111111'
    # photo = get_photo(partner_id)
    # print(photo)



