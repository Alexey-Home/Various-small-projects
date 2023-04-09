import re
sample_r = {
    0: r"CC\s+(IX[\+\-0-9.]+)*\s+(IY[\+\-0-9.]+)*",
    1: r"BEGIN\s*PGM\s*(([0-9]*))\s*MM",
    2: r"^\s*(([0-9])*)\s*M140\s*MB\s*MAX",
    3: r"^\s*(([0-9])*)\s*CALL\s*PGM\s*TNC:\\otmena.h",
    4: r"^\s*([0-9]*)\s*TOOL\s+CALL\s+([0-9]+)\s+[XYZ]*\s+S([0-9]+)",
    5: r"^\s*([0-9]*)\s*L\s+([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*"
       r"\s*([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*\s*[R0]*\s+FMAX",
    6: r"^\s*([0-9]*)\s*L\s+([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*"
       r"\s*([XYZBC]{1}[\+\-.0-9]+)*\s*([XYZBC]{1}[\+\-.0-9]+)*\s*[R0]*",
    7: r"^\s*([0-9]*)\s*C\s+([XYZCB]{1}[\+\-.0-9]+)*\s*([XYZCB]{1}[\+\-.0-9]+)\s*([XYZCB]{1}[\+\-.0-9]+)*"
       r"\s*([XYZCB]{1}[\+\-.0-9]+)*\s*([XYZCB]{1}[\+\-.0-9]+)*\s*[R0]*\s*DR\+",
    8: r"^\s*([0-9]*)\s*C\s+([XYZCB]{1}[\+\-.0-9]+)*\s*([XYZCB]{1}[\+\-.0-9]+)\s*([XYZCB]{1}[\+\-.0-9]+)*"
       r"\s*([XYZCB]{1}[\+\-.0-9]+)*\s*([XYZCB]{1}[\+\-.0-9]+)*\s*[R0]*\s*DR\-",
    9: r"^\s*(([0-9]*))\s*CYCL\s*DEF\s*247",
    10: r"^\s*([0-9]*)\s*(M[0-9]*)+\s*(M[0-9]*)*\s*(M[0-9]*)*"

}

sample_f = {
    0: "{0}{1}",
    1: "%\nO{0}",
    2: "N{0} G91G30Z0.",
    3: "N{0} G00G90G80G40G49",
    4: "N{0} T{1}M06\nG90\nS{2}",
    5: "N{0} G00{1}{2}{3}{4}{5}",
    6: "N{0} G01{1}{2}{3}{4}{5}",
    7: "N{0} G02{1}{2}{3}{4}{5}",
    8: "N{0} G03{1}{2}{3}{4}{5}",
    9: "N{0} G90G54",
    10: "N{0} {1} {2} {3}",
    9000: "G43H{0}"
}

sub_data = {
    "tool_number": 0,
    "length compensation": False
}


def main():
    with open("originalCNCprog", "r", encoding="utf-8") as file:
        list_strng = file.read().split("\n")

    new_list_strng = []
    sub_positions = []

    for str_text in list_strng:
        positions = get_position(str_text)
        if positions is not None:
            if positions[-1] in [0]:
                positions[0] = get_sub_positions(positions)
                sub_positions = positions
                continue
            elif positions[-1] in [10]:
                positions[0] = get_sub_positions(positions)
            new_strng = get_new_str(positions, sub_positions)
            new_list_strng.append(new_strng)

    with open("NewCNCprog.nc", "w", encoding="utf-8") as fl:
        fl.write("\n".join(new_list_strng))


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


def get_position(str_text: str) -> list:
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

    def get_replace(positions, val):
        tmp = []
        for pos in positions[0]:
            for rep in val:
                pos = pos.replace(*rep)
                tmp.append(pos)
        return tmp

    lst = []
    if positions[-1] == 0:
        lst = get_replace(positions, [["IX", "I"], ["IY", "J"]])
    elif positions[-1] == 10:
        lst = get_replace(positions, [["M13", "M3M8"]])
    return tuple(lst)


def check_save_data(positions: list) -> bool:
    """Проверка включены ли определенные параметры, если нет включить или наоборот"""

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
        if re.search(fr"{pos}[0-9\+\-.]+", p):
            return True
    return False


if __name__ == "__main__":
    main()



