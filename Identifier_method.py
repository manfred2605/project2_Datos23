

def __equal_brackets_count(text):
    pass


class Identifier_method:
    def __init__(self):
        self.__current_line = None
        self.hash_table = {}

    def read_file(self, path):

        file = open(path, "r", encoding="utf-8")  # abre el archivo de texto con codificacion UTF-8
        hash_table = file.readlines()             # lea las lineas y las guarda en una lista hash_table
        file.seek(0)                        # se coloca al inico del archivo para siempre leerlo desde el principio
        text = file.read().strip()
        file.close()
        for line in hash_table:
            self.__current_line += 1
            new_line = line.strip()
            if new_line == "":
                continue
            if new_line[-1] != "{" and new_line[-1] != "}" and new_line[-1] != "(" and new_line[-1] != ";":
                new_line += ";"
            self.__process_line(
                new_line, self.__equal_brackets_count(text))

    def __equal_brackets_count(self, text):
        """Verifica que la cantidad de llaves que abren, cierran
      
               """
        return text.count("{") - text.count("}") == 0

    def __process_line(self, new_line, param):
        pass
