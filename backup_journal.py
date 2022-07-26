import os
import time
import datetime
import pandas
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

journalname = 'backup_journal.xlsx' #название для файла журнала

path_file = open('source_path.txt','r') #Отслеживаемые пути. Желательно не пересекать пути
types_file = open('file_types.txt','r') #Разрешённые типы файлов

#SOURCE_PATH - список путей (используется пока только 1)
SOURCE_PATH = [line.strip() for line in path_file.readlines()]

#FILE_TYPES - множество типов файлов, могут повторяться
FILE_TYPES = {line.strip() for line in types_file.readlines()}

path_file.close()   #Закрыли файл
types_file.close()  #Закрыли файл

#не забыть pip install openpyxl
datajournal = pandas.read_excel(journalname, sheet_name='log', engine="openpyxl",usecols=['Date','Time','Filename','Status'])

#Класс для слежки за файлами. Нужно только create
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):

        print("Создан файл:", event.src_path)
        #Проверяем расширение исходного файла и если совпадает с типами, то удаляем
        ext = event.src_path.split('.')[-1].lower()
        if ext in FILE_TYPES:
            while True:
                try:

                    bdate = str(datetime.datetime.today())[:10:]
                    btime = str(datetime.datetime.today())[11:19:]
                    datajournal.loc[len(datajournal.index)] = [bdate,btime,str(event.src_path),'Выполнен']
                    writer = pandas.ExcelWriter(journalname)
                    datajournal.to_excel(writer,'log')
                    writer.save()
                    print('Успешно сохранено')
                    break
                except PermissionError:
                    print(str(datetime.datetime.today())[:19:] + "\tзанят\t" + event.src_path)

        

print('Просмотр бэкапов в папках:\n',SOURCE_PATH, '\nБэкапы в форматах:\n', FILE_TYPES)

                
#Запускаем My_handler
event_handler = MyHandler()
observer = Observer()
for index in range(len(SOURCE_PATH)):
    observer.schedule(event_handler, path=SOURCE_PATH[index], recursive=True)
observer.start()

while True:
    try:
        pass
    except KeyboardInterrupt:
        observer.stop()
