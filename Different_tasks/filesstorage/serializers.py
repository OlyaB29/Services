from rest_framework import serializers
from .models import MyFiles
from .config import TOKEN
import yadisk
from .selectel_config import ACCOUNT_ID, AUTH_TOKEN, URL, CONTAINER_KEY
import hmac
from hashlib import sha1
from time import time


class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyFiles
        fields = ('id', 'myfile')


class FileGetSerializer(serializers.ModelSerializer):
    myfile = serializers.SerializerMethodField(method_name='get_file_link')

    class Meta:
        model = MyFiles
        fields = "__all__"

    def get_file_link(self, obj):
        y = yadisk.YaDisk(token=TOKEN)
        link = y.get_download_link(str(obj.myfile))
        return link


# Функция для создания ключа доступа, используемого в ссылке к файлу (в хранилище Selectel)
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


class SelectelFileGetSerializer(serializers.ModelSerializer):
    myfile = serializers.SerializerMethodField(method_name='get_file_link')

    class Meta:
        model = MyFiles
        fields = "__all__"

    def get_file_link(self, obj):
        # Получение ключа доступа и срока его действия
        sig, expires = create_access_key(CONTAINER_KEY, str(obj.myfile))
        link = URL + str(obj.myfile) + "?temp_url_sig={}&temp_url_expires={}".format(sig, expires)
        return link
