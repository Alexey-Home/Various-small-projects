person = input("Введите имя и фамилию(через пробел и в указанной последовательности): ")
ls = [i.title() for i in person.lower().split()]
login = ls[1][:4] + ls[0][0]
print(f"{ls[0]} {ls[1]}: {login}")
