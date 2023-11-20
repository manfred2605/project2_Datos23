import unittest
import AnalizadorSemantico
from main import main


class Testing_method(unittest.TestCase):

    def main(nom_archivo, analizador):
        with open(nom_archivo, 'r') as file:
            codigo_fuente = file.read()

        analizador.analizar_codigo(codigo_fuente)

    def Main_test(self):
        analizador = AnalizadorSemantico.AnalizadorSemantico()

        self.assertEquals(main("code1.txt", analizador), "El código fuente es correcto.")
