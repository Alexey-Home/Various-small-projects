# -*- coding: utf8 -*-
import itertools
from string import digits, punctuation, ascii_letters
import win32com.client as client
from datetime import datetime
import time

def quessing_password():

    try:
        pas_len = input("Приблизительная длина пароля?, например 4 - 8: ")
        pas_len = [int(item) for item in pas_len.split("-")]
    except:
        print("Не правильно введены данные.")

    print("Введите 1, если пароль состоит только из цифры\n"
          "Введите 2, если пароль содержит только буквы\n"
          "ВВедите 3, если пароль содержит буквы и цифры\n"
          "Введите 4, если пароль содержит цифры, буквы и спецсимволы\n"
          "Введите 0, если хотите ввести приблизительные символы")

    try:
        number = int(input(":"))
        if number == 1:
            symbols = digits
        elif number == 2:
            symbols = ascii_letters
        elif number == 3:
            symbols = digits + ascii_letters
        elif number == 4:
            symbols = digits + ascii_letters + punctuation
        elif number == 0:
            symbols = input("Введите приблизительные символы: ")
        else:
            print("Не правильно введены данные.")
    except:
        print("Не правильно введены данные.")

    start_timestamp = time.time()
    print(f"Время начала: {datetime.utcfromtimestamp(time.time()).strftime('%H:%M:%S')}")

    for pas_len in range(pas_len[0], pas_len[1] + 1):
        for pas in itertools.product(symbols, repeat=pas_len):
            pas = "".join(pas)

            opened_doc = client.Dispatch("Excel.Application")

            try:
                opened_doc.Workbooks.Open(
                    r"C:\Ptyhon3\password\Книга1.xlsx",
                    False,
                    True,
                    None,
                    pas
                )

                time.sleep(0.1)
                print(f"Время конца: {datetime.utcfromtimestamp(time.time()).strftime('%H:%M:%S')}")
                print(f"Время подбора - {time.time() - start_timestamp}")
                print(f"Пароль: {pas}")
                return
            except:
                print(f"Не правильный: {pas}")
                pass

def main():
    quessing_password()


if __name__ == '__main__':
    main()
