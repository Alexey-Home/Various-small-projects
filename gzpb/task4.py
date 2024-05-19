import os
from datetime import datetime
# Имеется папка с файлами
# Реализовать удаление файлов старше N дней

path = "C:/Users/domahin_a/Desktop/test"
delta_time = int(input())

l_name = os.listdir(path)


for filename in l_name:
    stat = os.stat(path + "/" + filename)
    s_time = stat.st_ctime
    create_time = datetime.fromtimestamp(s_time)

    time_now = datetime.now()
    if time_now.day - create_time.day >= delta_time:
        os.remove(path + "/" + filename)


