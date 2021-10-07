import random
import os

encode_letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                 "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E",
                 "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
                 "Z"]
decode_cara = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', ' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '/', '&', '"', "'", '(',
               '-', '_', ')', '=', '+', 'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Q', 'S', 'D', 'F', 'G', 'H',
               'J', 'K', 'L', 'M', 'W', 'X', 'C', 'V', 'B', 'N', ':', '!', ';', ',', '?', '.', '/', '\\', '<', '>', '[',
               ']', "@"]


def create_encode(nb_ec, table_file):
    super_list = []
    for x in decode_cara:
        sup = []
        for i in range(nb_ec):
            sup.append(encode_letter[random.randint(1, len(encode_letter)) - 1])
        super_list.append([x, "".join(sup)])
    random.shuffle(super_list)
    sup = []
    for i in range(nb_ec):
        sup.append(encode_letter[random.randint(1, len(encode_letter)) - 1])
    super_list.append("".join(sup))
    super_list[0], super_list[-1] = super_list[-1], super_list[0]
    finish = []
    for i in super_list:
        if i == super_list[0]:
            finish.append(i)
        else:
            finish.append(super_list[0].join(i))
    with open(table_file, "w") as f:
        f.write("\n".join(finish))


class Encoder:
    def __init__(self, table):
        if os.path.isfile(table):
            self.table = table
            self.read_table()
        else:
            raise FileNotFoundError("table not found")

    def read_table(self):
        tmp = open(self.table).read().split("\n")
        self.separator = tmp[0]
        self.table_reader = {}
        self.reader_table = {}
        self.table_size = len(list(self.separator))
        del tmp[0]
        for i in tmp:
            self.table_reader[i.split(self.separator)[0]] = i.split(self.separator)[1]
            self.reader_table[i.split(self.separator)[1]] = i.split(self.separator)[0]

    def encode_str(self, string):
        return "".join([self.table_reader[i] for i in list(string)])

    def decode_str(self, string):
        return "".join([self.reader_table[i] for i in
                        [string[i:i + self.table_size] for i in range(0, len(string), self.table_size)]])

    def encode_join(self, *decode):
        return self.separator.join(decode)

    def encode_split(self, string):
        return string.split(self.separator)
