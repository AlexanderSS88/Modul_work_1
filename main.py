import os
import requests
import time
import json
from tqdm import tqdm
from pprint import pprint
from datetime import datetime
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive


class YaDiLoader:
    def __init__(self, token_vk: str, token_yadi: str, ver_apivk: str):
        self.token_vk = token_vk
        self.token_yadi = token_yadi
        self.ver_apivk = ver_apivk
        self.id_vk = int(input('Введите ID Вконтакте: '))


    def get_headers_yadi(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {token_yadi}'}


    def file_writer_json(self, result_date: list):
        with open('photo.json', mode='wt') as file:
            json_str = json.dumps(result_date)
            file.write(json_str)


    def get_photo(self):
        dict_f = {}
        photo_params = {}
        result_date = []
        url = f"https://api.vk.com/method/photos.get?owner_id={self.id_vk}&album_id=profile&extended=1&" \
              f"access_token={self.token_vk}&v={self.ver_apivk}"
        photos = requests.get(url).json()['response']['items']
        for id, photo in enumerate(photos):
            if id > 4:
                break
            else:
                if photo['likes']['count'] in dict_f:
                    time.sleep(0.35)
                    dict_f[f"{photo['likes']['count']}_{datetime.fromtimestamp(photo['date']).date()}"] = photo['sizes'][-1]['url']
                    name = f"{photo['likes']['count']}_{datetime.fromtimestamp(photo['date']).date()}.jpg"
                    size = photo['sizes'][-1]['type']
                    photo_params = {'file_name': name, 'size': size}
                else:
                    time.sleep(0.35)
                    dict_f[photo['likes']['count']] = photo['sizes'][-1]['url']
                    name = f"{photo['likes']['count']}.jpg"
                    size = photo['sizes'][-1]['type']
                    photo_params = {'file_name': name, 'size': size}
                result_date.append(photo_params)
        self.file_writer_json(result_date)
        pprint(result_date)
        print()
        return dict_f


    def create_catalog(self, path_on_yadisk_catalog: str):
        create_cat = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = self.get_headers_yadi()
        parameters = {"path": path_on_yadisk_catalog}
        create = requests.put(create_cat, headers=headers, params=parameters)
        create.raise_for_status()
        if create.status_code == 201:
            print(f'Папка "{path_on_yadisk_catalog}" успешно создана на Yandex Disk \n')


    def upload_foto(self, path_on_yadisk: str):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers_yadi()
        vk_dict = self.get_photo()
        for name, url_vk in tqdm((vk_dict.items()), desc='Photos load', dynamic_ncols=True):
            time.sleep(0.35)
            path_on_ya = f'{path_on_yadisk}{name}.jpg'
            parameters = {"path": path_on_ya, "url": url_vk}
            requests.post(upload_url, headers=headers, params=parameters)
        return


if __name__ == '__main__':
    token_vk = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    token_yadi = 'AQAAAAA5Ju1YAADLW-ELZgMfgEo6l_OWPBRKflo'
    ver_apivk = '5.131'

    path_on_yadisk_catalog = 'foto'
    path_on_yadisk = 'foto/'

    loaderY = YaDiLoader(token_vk=token_vk, token_yadi=token_yadi, ver_apivk=ver_apivk)
    loaderY.create_catalog(path_on_yadisk_catalog=path_on_yadisk_catalog)
    loaderY.upload_foto(path_on_yadisk=path_on_yadisk)



    # loaderG = GoogleDrive()
    # loaderG.upload_foto_google()

    # 466624282  # begemot_korovin
    # kon: 504529382274 tip: 79099338

    # def get_photo_ok(self):
    #     dict_f = {}
    #     photo_params = {}
    #     result_date = []
    #     url = "https://api.ok.ru/api/photos/getUserPhotos"
    #     parameters = {'fid':79099338}
    #     photos = requests.get(url)
    #     pprint(photos.json())

# class GoogleDrive:
#     def upload_foto_google(self):
#         GoogleAuth.LocalWebserverAuth(self)
#
#         dict_f = loaderY.get_photo()
#         file = GoogleDrive.CreateFile({'title':f'requirements.txt'})
#         file.Upload()
#             # for photo, url in dict_f.items():
#             #     GoogleDrive.CreateFile()
#             #     file_metadata = {'name': photo}
#             #     media = MediaFileUpload(url, mimetype='image/jpeg')
#             #     file = drive_service.files().create(body=file_metadata,
#             #                             media_body=media,
#             #                             fields='id').execute()
#             #      print'File ID: %s' % file.get('id')


