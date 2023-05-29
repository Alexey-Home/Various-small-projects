import random
from typing import Union, List


def main(volume, number, amount_dif, side, price_min, price_max):
    if check_valid_data(volume, number, amount_dif, side, price_min, price_max):
        orders = create_orders(volume, number, amount_dif, price_min, price_max)
        orders = division_of_remainder(orders, volume)
        return orders
    else:
        return None


def division_of_remainder(orders: List[dict], volume: Union[int, float]) -> List[dict]:
    """Распределение остатка по ордерам"""
    remainder = get_volume_remainder(orders, volume)
    if check_without_remainder(orders, remainder):
        return orders
    return check_with_remainder(orders, remainder)


def check_with_remainder(orders: List[dict], remainder: Union[float, int]) -> List[dict]:
    """Добавляет максимальное количество лотов, получившееся от деления остатка полного объема на цену """

    def foo(i):
        return i["price"]

    orders.sort(key=foo, reverse=True)
    div_lots = [remainder // order["price"] for order in orders]
    max_lots = max(div_lots)
    if max_lots == 0:
        return orders
    index = div_lots.index(max_lots)
    lots = int(orders[index]["lots"] + div_lots[index])
    price = orders[index]["price"]
    orders[index] = get_dict_order(lots, price)
    return orders


def check_without_remainder(orders:  List[dict], remainder: Union[float, int]) -> bool:
    """Добавляет в ордер лот если остаток обьема делится нацело"""
    for order in orders:
        if remainder % order["price"] == 0:
            order["lots"] += remainder / order["price"]
            order["volume"] = order["lots"] * order["price"]
            return True
    return False


def get_volume_remainder(orders: List[dict], volume: Union[float, int]) -> Union[float, int]:
    """Возвращает остаток от полного объема в долларах и суммы объемов ордеров"""
    volume_orders = 0
    for order in orders:
        volume_orders += order["volume"]
    return volume - volume_orders


def create_orders(volume: Union[float, int],
                  number: int,
                  amount_dif: Union[float, int],
                  price_min: Union[float, int],
                  price_max: Union[float, int]) -> List[dict]:
    """Создает и возвращает список ордеров"""
    approximate_price_of_one = volume / number
    orders = []
    for num in range(number):
        price = random.randrange(price_min, price_max + amount_dif, amount_dif)
        lots = int(approximate_price_of_one // price)
        orders.append(get_dict_order(lots, price))
    return orders


def get_dict_order(lots: int, price: Union[float, int]) -> dict:
    """Возвращает оредер в виде словаря"""
    order = {
        "lots": lots,
        "price": price,
        "volume": lots * price
    }
    return order


def check_valid_data(volume, number, amount_dif, side, price_min, price_max):
    """Проверяет правлиность данных"""
    if price_min > price_max:
        print("Не корректно введены данные - Минимальная цена больше Максимальная цена")
        return False
    elif price_min < amount_dif:
        print("Не корректно введены данные - Минимальная цена меньше 'amount_dif'")
        return False
    elif price_max < amount_dif:
        print("Не корректно введены данные - Максимальная цена меньше 'amount_dif'")
        return False
    elif volume < price_max:
        print("Не корректно введены данные - Объем меньше Максимальная цена")
        return False
    elif volume == 0:
        print("Не корректно введены данные - Объем равен 0")
        return False
    elif number == 0:
        print("Не корректно введены данные - Число ордеров равно 0")
        return False
    elif price_max == 0:
        print("Не корректно введены данные - Максимальная цена равно 0")
        return False
    elif number * price_min > volume:
        print(f"Не корректно введены данные -  Не возможно создать {number} лотов")
        return False
    elif number * price_max > volume:
        print(f"Внимание!!! Возможно лотов будет не {number}")
        return False
    return True


def chech_volume_orders(result):
    """Проверка данных"""
    for res in result:
        print(res)


if "__main__" == __name__:
    while True:
        try:
            volume = float(input("Введите объем в долларах: "))
            number = int(input("На сколько ордеров нужно разбить этот объем?: "))
            amount_dif = float(input("Введите разброс в доллраха: "))
            price_min = float(input("Введите нижнюю цену: "))
            price_max = float(input("Введите нижнюю цену: "))

            result = main(volume, number, amount_dif, "SELL", price_min, price_max)

            if result:
                chech_volume_orders(result)
        except TypeError:
            print("Не корректно введены данные")

        answer = input("Продолжить?(Д/Н): ")
        if answer.upper() != "Д":
            break



