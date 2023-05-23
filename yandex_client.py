import yadisk
import requests
import config

y = yadisk.YaDisk(token=config.TOKEN)
# или
# y = yadisk.YaDisk(config.CLIENTID, config.SECRET, config.TOKEN)

# Проверяем, валиден ли токен
print(y.check_token())

# Получаем общую информацию о диске
print(y.get_disk_info())

# Создаём новую папку "/test-dir"
print(y.mkdir("/test-dir"))

# Выводим содержимое папки
print(list(y.listdir("/test-dir")))
#
# Безвозвратно удаляем "/test-dir/Запросы2.txt"
y.remove("/test-dir/Запросы2.txt", permanently=True)

# Загружаем "Тестовый файл.txt" в "/test-dir/Тестовый файл" и получаем атрибут "href" объекта ссылки на ресурс
link=y.upload("Тестовый файл.txt", "/test-dir/Тестовый файл.txt").href
#
# Скачиваем "/test-dir/Тестовый файл.txt" в "downloaded.txt"
y.download("/test-dir/Тестовый файл.txt", "downloaded.txt")
#
# Получаем ссылку на сам файл
file_link = requests.get(link, headers={'Authorization': 'OAuth ' + config.TOKEN}).json()['file']
# Выводим содержимое файла
file_content=requests.get(file_link).text
print(file_content)
