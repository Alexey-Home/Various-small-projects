import csv
import pandas as pd


# # считывание данных из файла
# with open("D:\\python\\books\\demo\\orderdata_sample.csv") as file:
#     reader = csv.reader(file, quoting=csv.QUOTE_ALL)
#     rows = list(reader)
#
# # Добавление еще одного столбца
# rows[0].append("Total")
# for i in range(1, len(rows)):
#     rows[i].append(round(float(rows[i][3]) * float(rows[i][4]) + float(rows[i][5]), 2))
#
# # Вывод определнного столбца с условием
# index = rows[0].index("Total")
# for i in range(1, len(rows)):
#     if float(rows[i][index]) < 100:
#         print(rows[i][index])
#
# # Сохранение таблицы в файл
# with open("orderdata_sample.csv", "w", encoding="utf-8") as file:
#     writer = csv.writer(file, quoting=csv.QUOTE_ALL)
#     writer.writerows(rows)



