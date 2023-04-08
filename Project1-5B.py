# 1 задание.
def middle_temp(ls_t: list) -> float:
    """
    :param ls_t: Список температурных изменений в течение дня.
    :return Среднее значение списка, окгруглив до двух знаков после запятой. :
    """
    ls_justint = [i for i in ls_t if isinstance(i, int)]
    return round(sum(ls_justint)/len(ls_justint), 2)


print(middle_temp([12, 15, 14, 16, None, 11, 14, None, 17, 10, 16, 11, None]))


# 2 задание
def get_list(lst: list) -> tuple:
    """
    :param lst: Список числовых аргументов.
    :return: Возвращает кортеж из двух списков: отрицательных значений (отсортирован по убыванию);
    неотрицательных значений (отсортирован по возрастанию).
    """
    first_list, second_list = [], []
    for i in lst:
        if isinstance(i, (int, float)):
            first_list.append(i) if i < 0 else second_list.append(i)
    return sorted(first_list, reverse=True), sorted(second_list)


print(get_list([0, 1, -5, 3, -3, -2, 7, -7, -1, -9, 3, 10]))


# 3 задание
def func01(n, s):
    """
    Функция возведение в степень.
    :param n: Число возводимое в степень.
    :param s: Степень числа.
    :return: Число возведенное в степень
    """
    return n**s


print(func01(3, 3))


def func02(n, s, x=1):
    """
    Рекурсивная функция возведение в степень.
    :param n: Число возводимое в степень.
    :param s: Степень числа.
    :param x: Результат возведения.
    :return: Число возведенное в степень
    """
    return x if s == 0 else func02(n, s - 1, x * n)


print(func02(3, 4))
