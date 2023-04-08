products = ["Хлеб", "Колбаса", "Фрукты", "Сок", "Консервы", "Конфеты", "Сыр", "Молоко", "Мыло", "Масло"]
price = [23, 145, 44, 110, 45, 30, 256, 59, 25, 80]
code_employee = [323, 456, 232, 767, 234, 657, 232, 435, 111, 345]

justlist = [i for i in zip(products, price, code_employee)]
print(justlist)
