#Задание №1
from random import randint
min_int = 0
max_int = 100
lst = [randint(min_int, max_int) for i in range(10)]
flag = int(input(f"Введите значение порога(от {min_int} до {max_int}): "))
new_lst = ["High" if flag > i else "Low" for i in lst]


# Задание №2
import randomname

lst = [randomname.generate("names/surnames/english", 'names/people/computing', sep=" ").title() for i in range(100)]
first_list, second_list = [], []
for i in lst:
    first_list.append(i) if 65 <= ord(i[0]) <= 77 else second_list.append(i)

# Задание №3
words = []
while True:
    word = input("Введите слово: ")
    if len(word) == 0:
        break
    words.append(word)
create_word = "".join([w[0] for w in words])
print(create_word)


