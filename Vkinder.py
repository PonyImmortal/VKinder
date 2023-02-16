import datetime
import time
from random import randrange

import requests
import vk_api
from tqdm import tqdm
from vk_api.longpoll import VkEventType, VkLongPoll

from database import *
from keyboard import keyboard1, keyboard2
from method import Data

params_count = 0  # параметр для загрузки анкет


def increment():
    """Счетчик для загрузки анкет"""
    global params_count
    params_count += 20
    return params_count


class VKBotSearch:
    def __init__(self):
        print('Бот запущен')
        self.vk = vk_api.VkApi(token=comm_token)
        self.longpoll = VkLongPoll(self.vk)
        self.data = Data()

    def loop_bot(self):
        for this_event in self.longpoll.listen():
            if this_event.type == VkEventType.MESSAGE_NEW and this_event.to_me:
                message_text = this_event.text
                return message_text, this_event.user_id

    def write_msg(self, user_id, message, keyboard=None, attachment=None):
        """SendMessage"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7),
                                         'attachment': attachment,
                                         'keyboard': keyboard
                                         })

    def name(self, user_id):
        """Функция получения имени пользователя"""
        first_name = self.data.get_info_user(user_id)['first_name']
        return first_name

    def get_sex(self, user_id):
        """Функция получения пола пользователя для автоматического подбора"""
        sex = self.data.get_info_user(user_id)['sex']
        if sex == 2:
            sex = 1
            return sex
        elif sex == 1:
            sex = 2
            return sex

    def get_sex_individual_parameters(self, user_id):
        """Функция получения пола для поиска по индивидуальным параметрам"""
        self.write_msg(user_id, 'Введите пол для поиска (мужской/женский): ')
        msg_text, user_id = self.loop_bot()
        if msg_text == 'мужской':
            msg_text = 2
            return msg_text
        elif msg_text == 'женский':
            msg_text = 1
            return msg_text
        else:
            self.write_msg(user_id, 'Некорректный ввод')
            return self.get_sex_individual_parameters(user_id)

    def get_age(self, user_id):
        """Функция получения возраста для автоматического подбора"""
        bdate = self.data.get_info_user(user_id)['bdate'].split('.')
        if len(bdate) == 3:
            age = int(datetime.date.today().year) - int(bdate[2])
            age_from = str(age - 1)
            age_to = str(age + 1)
            return {'age_from': age_from, 'age_to': age_to}

        elif len(bdate) == 2:
            age_from = self.get_age_low(user_id)
            age_to = self.get_age_high(user_id)
            return {'age_from': age_from, 'age_to': age_to}

    def get_age_low(self, user_id):
        """Функция получения возраста по нижней границе для индивидуального подбора"""
        self.write_msg(user_id, 'Введите минимальный порог возраста (min - 18): ')
        msg_text, user_id = self.loop_bot()
        age_from = int(msg_text)
        if age_from < 18:
            self.write_msg(user_id, 'Некорректный ввод')
            self.get_age_low(user_id)
            return age_from
        else:
            return age_from

    def get_age_high(self, user_id):
        """Функция получения возраста по верхней границе для индивидуального подбора"""
        self.write_msg(user_id, 'Введите верхний порог возраста (max - 99): ')
        msg_text, user_id = self.loop_bot()
        age_to = int(msg_text)
        if age_to > 99:
            self.write_msg(user_id, 'Некорректный ввод')
            self.get_age_high(user_id)
            return age_to
        else:
            return age_to

    def find_city(self, user_id):
        """Функция получения информации о городе"""
        if 'city' not in self.data.get_info_user(user_id):
            return self.find_city_individual_parameters(user_id)
        else:
            hometown = self.data.get_info_user(user_id)['city']['title']
            return hometown

    """Функция получения города для индивидуального подбора"""

    def find_city_individual_parameters(self, user_id):
        self.write_msg(user_id, 'Введите название города для поиска: ')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                hometown = event.text
                for city in self.data.get_cities(user_id):
                    if city['title'] == hometown.title():
                        self.write_msg(user_id, f'Ищу в городе {hometown.title()}')
                        return hometown.title()
                    else:
                        pass

    def find_user_params(self, user_id):
        """Поиск людей по полученным данным для автоматического поиска"""
        fields = 'id, sex, bdate, city, relation'
        params = {'access_token': user_token,
                  'v': '5.131',
                  'sex': self.get_sex(user_id),
                  'age_from': self.get_age(user_id)['age_from'],
                  'age_to': self.get_age(user_id)['age_to'],
                  'country_id': '1',
                  'hometown': self.find_city(user_id),
                  'fields': fields,
                  'status': '1' or '6',
                  'count': increment(),
                  'has_photo': '1',
                  'is_closed': False
                  }
        return params

    def find_user_individual_parameters(self, user_id):
        fields = 'id, sex, bdate, city, relation'
        params = {'access_token': user_token,
                  'v': '5.131',
                  'sex': self.get_sex_individual_parameters(user_id),
                  'age_from': self.get_age_low(user_id),
                  'age_to': self.get_age_high(user_id),
                  'country_id': '1',
                  'hometown': self.find_city_individual_parameters(user_id),
                  'fields': fields,
                  'status': '1' or '6',
                  'count': increment(),
                  'has_photo': '1',
                  'is_closed': False
                  }
        return params

    def search_users(self, user_id):
        method = 'users.search'
        all_persons = []
        url = f'https://api.vk.com/method/{method}'
        res = requests.get(url, self.find_user_params(user_id)).json()
        user_url = f'https://vk.com/id'
        count = res['response']['count']
        count_list = []
        for element in tqdm(res['response'].get('items'), desc="Loading: ", ncols=100, colour='green'):

            profile_pics = self.data.get_photos_id(element['id'])
            if profile_pics:
                attach = ''
                for pic in profile_pics['pics_ids']:
                    attach += f'photo{profile_pics["owner_id"]}_{pic},'
                person = [
                    element['first_name'],
                    element['last_name'],
                    user_url + str(element['id']),
                    element['id'],
                    attach
                ]
                all_persons.append(person)
                count_list = len(all_persons)
        print(
            f'Поиск пользователей закончен,всего найдено {count} пользователей. Загружаю для просмотра {count_list} пользователей')
        if count == 0:
            self.write_msg(user_id, f"К сожалению нет подходящих кандидатов")
            print('Нет подходящих кандидатов')
        else:
            self.write_msg(user_id,
                           f'Нашел для Вас несколько вариантов, проверяю есть ли фотографии и открыт ли профиль...')
        return all_persons

    def search_users_individual_parameters(self, user_id):
        method = 'users.search'
        all_persons = []
        url = f'https://api.vk.com/method/{method}'
        res = requests.get(url, self.find_user_individual_parameters(user_id)).json()
        user_url = f'https://vk.com/id'
        count = res['response']['count']
        count_list = []
        for element in tqdm(res['response'].get('items'), desc="Loading: ", ncols=100, colour='green'):
            profile_pics = self.data.get_photos_id(element['id'])
            if profile_pics:
                attach = ''
                for pic in profile_pics['pics_ids']:
                    attach += f'photo{profile_pics["owner_id"]}_{pic},'
                person = [
                    element['first_name'],
                    element['last_name'],
                    user_url + str(element['id']),
                    element['id'],
                    attach
                ]
                all_persons.append(person)
                count_list = int(len(all_persons))
        print(
            f'Поиск пользователей закончен,всего найдено {count} пользователей. Загружаю для просмотра {count_list} пользователей')
        if count == 0:
            self.write_msg(user_id, f"К сожалению нет подходящих кандидатов")
            print('Нет подходящих кандидатов')
        else:
            self.write_msg(user_id,
                           f'Нашел для Вас несколько вариантов, проверяю есть ли фотографии и открыт ли профиль...')
        return all_persons

    def send_info_about_users(self, user_id):
        res_li = self.search_users(user_id)
        for u in range(len(res_li)):
            if select(user_id, res_li[u][3]) is None:
                insert_data_seen_users(user_id, res_li[u][3])
                self.write_msg(user_id,
                               f'\n{res_li[u][0]}  {res_li[u][1]}  {res_li[u][2]}',
                               attachment={res_li[u][4]})

                self.write_msg(user_id, f'Посмотрите, как Вам этот кандидат? Не нравится, жми "Еще варианты!"',
                               keyboard1.get_keyboard())
                self.write_msg(user_id,
                               f'Чтобы начать новый поиск, или просмотреть, что я умею нажми "Закончить просмотр"',
                               keyboard2.get_keyboard())
                msg_text, user_id = self.loop_bot()
                if msg_text == 'Еще варианты':
                    if u >= len(res_li) - 1:
                        self.write_msg(user_id,
                                       f'Секунду, подготавливаю к просмотру анкеты...')
                        self.send_info_about_users(user_id)
                    else:
                        continue
                elif msg_text == 'Закончить просмотр':
                    self.write_msg(user_id,
                                   f'Жду дальнейших распоряжений!')
                    break
            if u >= len(res_li) - 1:
                self.write_msg(user_id,
                               f'Секунду, отсортировываю уже просмотренные вами анкеты...\n'
                               f'\nВсе анкеты просмотрены... ')
                print('Все анкеты просмотрены')
                break

    def send_info_about_users_individual_parameters(self, user_id):
        res_li = self.search_users_individual_parameters(user_id)
        for u in range(len(res_li)):
            if select(user_id, res_li[u][3]) is None:
                insert_data_seen_users(user_id, res_li[u][3])
                self.write_msg(user_id,
                               f'\n{res_li[u][0]}  {res_li[u][1]}  {res_li[u][2]}',
                               attachment={res_li[u][4]})
                self.write_msg(user_id, f'Посмотрите, как Вам этот кандидат? Не нравится, жми "Еще варианты!"',
                               keyboard1.get_keyboard())
                self.write_msg(user_id,
                               f'Чтобы начать новый поиск, или просмотреть, что я умею нажми "Закончить просмотр"',
                               keyboard2.get_keyboard())
                msg_text, user_id = self.loop_bot()
                if msg_text == 'Еще варианты':
                    if u >= len(res_li) - 1:
                        self.write_msg(user_id,
                                       f"Загруженные в мою память анкеты закончились.\n"
                                       f"К сожалению меня не научили запоминать введенные Вами параметры для загрузки следующих анкет.\n"
                                       f"Будьте так любезны введите заново желаемые параметры и я загружу еще варианты для просмотра!")
                        self.send_info_about_users_individual_parameters(user_id)
                    else:
                        continue
                elif msg_text == 'Закончить просмотр':
                    self.write_msg(user_id,
                                   f'Жду дальнейших распоряжений!')
                    break
            if u >= len(res_li) - 1:
                self.write_msg(user_id,
                               f"Секунду, отсортировываю уже просмотренные вами анкеты...\n"
                               f"\nПохоже вы уже просмотрели все анкеты...\n"
                               )
                print('Все анкеты просмотрены')
                break

    # def last_seen(self, user_id):
    #     last_seen = self.data.get_info_user(user_id)['last_seen']
    #     while True:
    #         if last_seen['time'] + 1 < int(time.time()):
    #             self.write_msg(user_id, 'До свидания')
    #             break


bot = VKBotSearch()
