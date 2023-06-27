import requests
from selectel_config import ACCOUNT_ID, AUTH_KEY
import hmac
from hashlib import sha1
from time import time

url = "https://api.selcdn.ru/v1/SEL_{}/my_container".format(ACCOUNT_ID)

# Авторизация (получение токена для рабты с API)
resp = requests.get("https://api.selcdn.ru/auth/v1.0", headers={'X-Auth-User': ACCOUNT_ID, 'X-Auth-Key': AUTH_KEY})
token = resp.headers.get("X-Auth-Token")

# Получение списка объектов конкретного контейнера
objects = requests.get(url, headers={'X-Auth-Token': token})
print(objects.text)

# Скачивание файла
download_file = requests.get(url + "test_dir/test_file.txt", headers={'X-Auth-Token': token})
print(download_file.headers)

# Загрузка файла в хранилище
with open("Тестовый файл.txt", "rb") as new_file:
    send_file = requests.put(url + "/test_dir/new_folder/text.txt", headers={'X-Auth-Token': token}, files={'file':new_file})
    print(send_file.headers)



# Установка секретного ключа для контейнера, чтобы затем, используя его в ссылке, иметь доступ к файлу
secret_key = "container_key"
set_key = requests.post(url, headers={'X-Auth-Token': 'a7f640c10e821ad7b5c9d22fff98db8c', "X-Container-Meta-Temp-URL-Key": secret_key})

# Функция для создания ключа доступа, используемого в ссылке к файлу
def create_access_key(secret_key, file):
    method = "GET"
    # ссылка будет действительна 60 сек.
    expires = int(time()) + 60

    # путь к файлу в хранилище
    path = "/v1/SEL_{}/my_container/{}".format(ACCOUNT_ID, file)

    # секретный ключ контейнера
    link_secret_key = str.encode(secret_key)

    # генерируем ключ доступа к файлу
    hmac_body = str.encode('%s\n%s\n%s' % (method, expires, path))

    # итоговый ключ доступа
    sig = hmac.new(link_secret_key, hmac_body, sha1).hexdigest()

    return sig, expires

# Получение ключа доступа и срока его действия
sig, expires = create_access_key(secret_key, "/test_dir/new_folder/text.txt")

# После этого файл будет доступен по ссылке:
# https://api.selcdn.ru/v1/SEL_{}/my_container//test_dir/new_folder/text.txt?temp_url_sig={}&temp_url_expires={}".format(ACCOUNT_ID, sig, expires)


