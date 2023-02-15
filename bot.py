from Vkinder import *

for event in bot.longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()

        if request == 'нажми, чтобы узнать что я умею \N{smiling face with sunglasses}':
            bot.write_msg(user_id,
                          f'Приветствую, {bot.name(user_id)}! Я - чат-бот VKinder, и я помогу Вам найти пару. Для этого я буду использовать следующие критерии: возраст, пол, город, семейное положение. Я отправлю Вам топ-3 самых популярных фото профиля, сквозь которые Вы сможете составить первое впечатление о возможном партнере. Можно воспользоваться как автоматическим поиском так и поиском по индивидуальным параметрам. Если не понравится жми "Еще варианты", у меня в запасе их много!')

        elif request == 'начать автоматический поиск':
            creating_database()
            bot.write_msg(user_id, f'Хорошо, {bot.name(user_id)} приступим')
            bot.send_info_about_users(user_id)

        elif request == 'начать поиск по заданным параметрам':
            creating_database()
            bot.write_msg(user_id, f'Хорошо, {bot.name(user_id)} приступим')
            bot.send_info_about_users_individual_parameters(user_id)

        else:
            bot.write_msg(event.user_id, 'Я не понимаю вас, повторите запрос')
