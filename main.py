import requests
import json
from tqdm import tqdm
from pprint import pprint

class VK:
    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token
        self.url = 'https://api.vk.com/method/'
        self.params = {
            'owner_id': user_id,
            'access_token': access_token,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1
                }
    def get_photos(self):
        response = requests.get(self.url + "photos.get", params=self.params)
        return response.json()
                
    def get_maxphoto_url(self, photo):
        for size in photo['sizes']:
            if size['type'] == 'w':
                return size['url']

class YandexDisk:
    def __init__(self, token):
        self.token = token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def create_folder(self, folder_name):
        url_create_dir = self.url + folder_name
        params = {
                'path': folder_name
                        }
        headers = {
                'Authorization': 'OAuth '+ self.token
                }
        response = requests.put(url_create_dir, params = params, headers = headers)
        return response.status_code

    def upload_photo(self, photo_url, file_name, folder_name):
        url_upload_photo = self.url + folder_name + '/' + file_name
        params = {
                'path': folder_name,
                'url': photo_url
                        }
        headers = {
                'Authorisation': 'OAuth '+ self.token
                        }
        response = requests.post (url_upload_photo, params = params, headers = headers)
        response.raise_for_status()

        with open(folder_name + '/' + file_name, "wb") as f:
            pbar = tqdm(total=int(response.headers['Content-Length']), desc = 'Загрузка')
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
            pbar.close()
        return response.status_code
        