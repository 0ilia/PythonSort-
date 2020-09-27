# Подключение всех модулей
from watchdog.observers import Observer
import os
import time
import json
from watchdog.events import FileSystemEventHandler

# Папка что отслеживается
folder_track = 'D:/Downloads'
# Папка куда перемещать будем
folder_dest = 'D:/Downloads'

with open('json.json') as f:
    templates = json.load(f)


def createDirectori():
    for i in templates["JSON"]:
        if not os.path.exists(folder_track + '/' + i["nameFolder"]):
            os.mkdir(folder_track + "/" + i["nameFolder"])


createDirectori()


def copyFile(filename):
    print("11")
    extension = filename.split(".")
    for i in templates["JSON"]:
        for j in i["file_extensions"]:
            if len(extension) > 1 and (extension[len(extension) - 1].lower() == j):
                file = folder_track + "/" + filename
                new_path = folder_dest + "/" + i["nameFolder"] + "/" + filename
                os.rename(file, new_path)


# Создаем класс наследник, через него может отслеживать изменения в папках
class Handler(FileSystemEventHandler):
    # При любых изменениях в папке, мы перемещаем файлы в ней

    def on_modified(self, event):
        # Перебираем все файлы в папке folder_track
        for filename in os.listdir(folder_track):
            # Проверяем расширенеи файла
            copyFile(filename)


# Запуск всего на отслеживание
handle = Handler()
observer = Observer()
observer.schedule(handle, folder_track, recursive=True)
observer.start()

# Программа будет срабатывать каждые 10 милисекунд
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()

observer.join()
