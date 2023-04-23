import datetime
import logging
from typing import Union
import re
import os


# TODO В дальнейшем перевести в базу данных
sample_r = {
    0: r"CC\s+(IX[\+\-0-9.]+)*\s+(IY[\+\-0-9.]+)*",
    1: r"BEGIN\s*PGM\s*(([0-9]*))\s*MM",
    2: r"^\s*(([0-9])*)\s*M140\s*MB\s*MAX",
    3: r"^\s*(([0-9])*)\s*CALL\s*PGM\s*TNC:\\otmena.h",
    4: r"^\s*([0-9]*)\s*TOOL\s+CALL\s+([0-9]+)\s+[XYZ]*\s+S([0-9]+)",
    5: r"^\s*([0-9]*)\s*L\s+([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*"
       r"\s*([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*\s*([R0|RL|RR]*)\s+FMAX\s*(M[0-9]+)*\s*$",
    6: r"^\s*([0-9]*)\s*L\s+([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}([\+\-.0-9]+))*\s*([XYZBC]{1}[\+\-.0-9]+)*"
       r"\s*([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*\s*([R0|RL|RR]*)\s*(F[ZU0-9.]+)*\s*(M[0-9]+)*\s*$",
    7: r"^\s*([0-9]*)\s*C\s+([XYZCB]{1}[\+\-.0-9]+)*\s*([XYZCB]{1}[\+\-.0-9]+)\s*([XYZCB]{1}[\+\-.0-9]+)*"
       r"\s*([XYZCB]{1}[\+\-.0-9]+)*\s*([XYZCB]{1}[\+\-.0-9]+)*\s*DR\+\s*(F[ZU0-9.]+)*$",
    8: r"^\s*([0-9]*)\s*C\s+([XYZCB]{1}[\+\-.0-9]+)*\s*([XYZCB]{1}[\+\-.0-9]+)\s*([XYZCB]{1}[\+\-.0-9]+)*"
       r"\s*([XYZCB]{1}[\+\-.0-9]+)*\s*([XYZCB]{1}[\+\-.0-9]+)*\s*DR\-\s*(F[ZU0-9.]+)*$",
    9: r"^\s*(([0-9]*))\s*CYCL\s*DEF\s*247",
    10: r"^\s*([0-9]*)\s*(M[0-9]*)+\s*(M[0-9]*)*\s*(M[0-9]*)*",
    2000: r"^\s*([0-9]+)\s*(Q[0-9]+)+\s*=\s*(Q?[\+\-.0-9]+)",
    2001: r"^\s*([0-9]*)\s*(Q[0-9]+)+\s*=\s*(Q[\+\-.0-9]+)\s*([\+\-\*\\])\s*(Q[\+\-.0-9]+)",
    2002: r"^\s*([0-9]*)\s+L\s+([XYZBC]{1}[\+\-]{1}Q?[0-9]+)*\s*([XYZBC]{1}[\+\-]Q?[0-9]+)*\s*([XYZBC]{1}[\+\-]Q?[0-9]+)*"
          r"\s*([XYZBC]{1}[\+\-]Q?[0-9]+)*\s*([XYZBC]{1}[\+\-]Q?[0-9]+)*\s*([R0|RL|RR]*)\s+FMAX\s*$",
    2003: r"^([0-9]+)\sFN\s+9:\s+IF\s*([\+|\-]Q[0-9]+)\s+EQU\s+([\+|\-]Q[0-9]+)\s+GOTO\s+LBL\s+([0-9]+)\s*$",
    2004: r"^([0-9]+)\sFN\s+12:\s+IF\s*([\+|\-]Q[0-9]+)\s+LT\s+([\+|\-]Q[0-9]+)\s+GOTO\s+LBL\s+([0-9]+)\s*$",
    2005: r"^([0-9]+)\sFN\s+11:\s+IF\s*([\+|\-]Q[0-9]+)\s+GT\s+([\+|\-]Q[0-9]+)\s+GOTO\s+LBL\s+([0-9]+)\s*$",
    2006: r"^\s*([0-9]*)\s*CALL\s+LBL\s+([0-9]+)\s*$",
    2007: r"^([0-9]+)\s+LBL\s+([0-9]+)\s*.*$",
    2008: r"^\s*([0-9]*)\s+L\s+([XYZBC]{1}[\+\-]{1}Q?[0-9]+)*\s*([XYZBC]{1}[\+\-]Q?[0-9]+)*\s*([XYZBC]{1}[\+\-]Q?[0-9]+)*"
          r"\s*([XYZBC]{1}[\+\-]Q?[0-9]+)*\s*([XYZBC]{1}[\+\-]Q?[0-9]+)*\s*([R0|RL|RR]*)\s+(F[Z|V]?Q?[0-9]+)\s*$",

}

sample_f = {
    0: "{0}{1}",                                # Вспомагательная позиции: центр окружности
    1: "%\nO{0}",                               # Номер программы
    2: "N{0} G91G30Z0.",                        # Возврат в референтную точку
    3: "N{0} G00G90G80G40G49",                  # Строка безопасности
    4: "N{0} T{1}M06\nG90\nS{2}",               # Вызов режущий инструмент
    5: "N{0} G00{1}{2}{3}{4}{5}{6}",            # Линейная интерполяция (быстрый ход)
    6: "N{0} G01{1}{2}{3}{4}{5}{6}{7}",         # Линейная интерполяция (рабочая подача)
    7: "N{0} G02{1}{2}{3}{4}{5}",               # Круговая интерполяция (по часовой стрелке)
    8: "N{0} G03{1}{2}{3}{4}{5}",               # Круговая интерполяция (против часвой стрелке)
    9: "N{0} G90G54",                           # Система координат
    10: "N{0} {1} {2} {3}",                     # Вспомогательные M-функции
    2000: "N{0} {1}={2}",                       # Макро: присваивание значений регистру
    2001: "N{0} {1}={2}{3}{4}",                 # Макро: действие с регистрами
    2002: "N{0} G00{1}{2}{3}{4}{5}",            # Макро: использование регистров в интерполяции
    2003: "N{0} IF[{1}EQ{2}]GOTO{3}0000",       # Макро: условие сравнения (=)
    2004: "N{0} IF[{1}LT{2}]GOTO{3}0000",       # Макро: условие сравнения (<)
    2005: "N{0} IF[{1}GT{2}]GOTO{3}0000",       # Макро: условие сравнения (>)
    2006: "N{0} GOTO{1}0000",                   # Макро: переход на определнный кадр
    2007: "N{1}0000",                           # Макро: определенный кадр
    2008: "N{0} G01{1}{2}{3}{4}{5}{6}{7}",
    9000: "G43H{0}"                             # Включение коррекции на длину
}

sub_sample = {
    5:  [["R0", "G40"], ["RL", "G41"], ["RR", "G42"]],
    6: [["R0", "G40"], ["RL", "G41"], ["RR", "G42"]],
    0: [["IX", "I"], ["IY", "J"]],
    10: [["M13", "M3M8"]],
    2000: [["Q", "#"]],
    2001: [["Q", "#"]],
    2002: [["Q", "#"]],
    2003: [["Q", "#"]],
    2004: [["Q", "#"]],
    2008: [["Q", "#"]]
}

sub_data = {
    "tool_number": 0,
    "length compensation": False,
    "radius compensation": False
}


def update_sub_data(function):
    def wrapper(*args, **kwargs):
        new_str = function(*args, **kwargs)
        if re.search(r"\d+G4[12]{1}(?:$|\D+)", new_str):
            tmp = re.findall(r"\d+G4[12]{1}(?:$|\D+)", new_str)[0]
            new_str = new_str.replace(tmp, f"{tmp}D{sub_data['tool_number']}")
        return new_str
    return wrapper

@update_sub_data
def get_new_str(positions: list, sub_positions: list) -> str:
    """
    Функция составления новой строки.
    :param positions: Список значений.
    :param sub_positions: Список вспомагательных.
    :return: Новая строка.
    """
    new_str = sample_f[positions[-1]].format(*positions[0])
    if positions[-1] in [7, 8]:
        new_str += sample_f[sub_positions[-1]].format(*sub_positions[0])
    if positions[-1] in [4, 5, 6, 7, 8, 9]:
        if check_save_data(positions):
            new_str += sample_f[9000].format(sub_data["tool_number"])
    return new_str


def get_position(str_text: str) -> Union[list, None]:
    """
     Функция поиска совпадений по шаблону.
    :param str_text: Строка управляющей программы.
    :return: Список совпадений по шаблону.
    """
    lst_coincidence = []
    for number, sample in sample_r.items():
        if re.search(sample, str_text):
            lst_coincidence = re.compile(sample).findall(str_text)
            lst_coincidence.append(number)
            break
    return lst_coincidence if len(lst_coincidence) > 1 else None


def get_sub_positions(positions: list) -> tuple:
    """
    Функция которая редактирует вспомогательные позиции.
    :param positions: Список значений, который нужно изменить.
    :return: Кортеж измененых значений.
    """

    def get_replace(position, val):
        """Замена в позиций в строке"""
        lst_pos = list(position[0])
        for v in val:
            for pos in range(len(lst_pos)):
                lst_pos[pos] = lst_pos[pos].replace(*v)
        return tuple(lst_pos)

    lst = []
    lst_pos_to_change = [0, 5, 6, 10, 2000, 2001, 2002, 2003, 2008]

    if positions[-1] in lst_pos_to_change:
        lst = get_replace(positions, sub_sample[positions[-1]])
    return tuple(lst) if lst else positions[0]


def check_save_data(positions: list) -> bool:
    """Проверка включены ли определенные параметры, если нет то включить и наоборот"""

    if positions[-1] == 4:
        sub_data["tool_number"] = positions[0][1]
    elif positions[-1] == 9:
        sub_data["length compensation"] = False
    elif sub_data["length compensation"] is False and positions[-1] in [5, 6, 7, 8]:
        if check_availability("Z", positions[0]):
            sub_data["length compensation"] = True
            return True
        else:
            return False


def check_availability(pos: str, lst: tuple) -> bool:
    """Проверка наличие опеределенных позиций в строчке"""
    for p in lst:
        if re.search(fr"{pos}[0-9\\+\-.]+", p):
            return True
    return False


def get_cnc_program() -> Union[list, None]:
    """Функция открывает файл с УП и возвращает список строк"""
    try:
        with open("originalCNCprog", "r", encoding="utf-8") as file:
            list_strng = file.read().split("\n")
    except FileNotFoundError:
        logging.error(f"File not exists.")

    return list_strng if list_strng else None


def save_new_cnc_program(new_list_strng: list):
    """Функция сохраняет новую управляющу программу"""
    with open("NewCNCprog.nc", "w", encoding="utf-8") as fl:
        fl.write("\n".join(new_list_strng))


def create_logfile():
    """Создание нового логфайла"""

    timestring = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    path = "logfile\\"

    if not os.path.exists(path):
        os.makedirs(path)

    logfile = f"{path}basic_{timestring}.log"
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s_%(levelname)s: %(message)s')


def main():
    """Преобразует управляющую программу на новую стойку ЧПУ"""

    new_list_strng = []
    sub_positions = []

    create_logfile()
    list_strng = get_cnc_program()

    if list_strng is None:
        return

    for str_text in list_strng:
        positions = get_position(str_text)

        if positions is not None:
            if positions[-1] in [0]:
                positions[0] = get_sub_positions(positions)
                sub_positions = positions
                continue
            elif positions[-1] in [5, 6, 10, 2000, 2001, 2002, 2003, 2008]:
                positions[0] = get_sub_positions(positions)

            new_strng = get_new_str(positions, sub_positions)
            new_list_strng.append(new_strng)
        else:
            logging.warning(f"No matches found: {str_text}")
            print(f"Совпадений не найдено, строка: {str_text}")

    save_new_cnc_program(new_list_strng)


if __name__ == "__main__":
    main()
