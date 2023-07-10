import requests
from config import user_token


class Data:
    def __init__(self):
        self.user_token = user_token

    def get_cities(self, user_id):
        """Функция получения списка городов"""
        method = 'database.getCities'
        params = {'country_id': 1,
                  'need_all': 0,
                  'count': 1000,
                  'user_id': user_id,
                  'access_token': user_token,
                  'v': '5.131',
                  }
        url = f'https://api.vk.com/method/{method}'
        cities_list = requests.get(url, params=params).json()['response']['items']
        return cities_list

    def get_info_user(self, user_id):
        method = 'users.get'
        params = {'user_id': user_id,
                  'fields': 'sex, bdate, city, relation, last_seen',
                  'v': '5.131',
                  'access_token': user_token
                  }
        url = f'https://api.vk.com/method/{method}'
        res = requests.get(url, params=params).json()
        return res['response'][0]

    def get_photos_id(self, user_id):
        method = 'photos.get'
        params = {'user_id': user_id,
                  'access_token': user_token,
                  'album_id': 'profile',
                  'extended': 1,
                  'v': '5.131'}
        url = f'https://api.vk.com/method/{method}'
        res = requests.get(url, params=params).json()
        photo_pack = {}
        try:
            popular_pics = sorted(
                res['response']['items'],
                key=lambda k: k['likes']['count'] + k['comments']['count'],
                reverse=True
            )[0:3]
            for pic in popular_pics:
                if 'owner_id' not in photo_pack.keys():
                    photo_pack['owner_id'] = pic['owner_id']
                    photo_pack['pics_ids'] = []
                photo_pack['pics_ids'].append(pic['id'])

        except KeyError:
            pass

        finally:
            return photo_pack
