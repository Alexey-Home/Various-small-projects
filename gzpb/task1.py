# имеется текстовый файл file.csv, в котром разделитель полей с данными: | (верт. черта)
# пример ниже содержит небольшую часть этого файла(начальные 3 строки, включая строку заголовков полей)

"""
lastname|name|patronymic|date_of_birth|id
Фамилия1|Имя1|Отчество1 |21.11.1998   |312040348-3048
Фамилия2|Имя2|Отчество2 |11.01.1972   |457865234-3431
...
"""

# Задание
# 1. Реализовать сбор уникальных записей
# 2. Случается, что под одиннаковым id присутствуют разные данные - собрать отдельно такие записи

import csv

def add_data(data, new_data, col):
    """Добавляет данные с одинаковыми id"""
    data.append(get_new_data(new_data, col))
    return data


def check_uniq(data_info, data, name_col):
    """Проверка на уникальность данных"""
    flag = True
    new_data = get_new_data(data, name_col)
    for id, old_data in data_info.items():
        for od in old_data:
            if od == new_data:
                print("done")
                return False

    return flag

def get_new_data(data, col):
    """Распределяет новые данные по колонкам."""
    d_temp = {}
    for title, index in col.items():
        if title in "id":
            continue
        d_temp[title] = data[index]
    return d_temp


with open("test.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)
name_col = {}
titles = rows[0][0].split("|")
for title in titles:
    name_col[title] = titles.index(title)

data_info = {}

for i in range(1, len(rows)):
    data = rows[i][0].split("|")

    if check_uniq(data_info, data, name_col):
        if data[name_col["id"]] not in data_info:
            data_info[data[name_col["id"]]] = [get_new_data(data, name_col)]
        else:
            data_info[data[name_col["id"]]] = add_data(data_info[data[name_col["id"]]], data, name_col)


print(data_info)
