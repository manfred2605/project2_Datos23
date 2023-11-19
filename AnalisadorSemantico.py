import TablaSimbolos as TB

arit_ops = ["+", "-", "*", "**", "/", "//", "%"]
comp_ops = [">", "<", ">=", "<=", "==", "!="]
logic_ops = ["&&", "||"]
tipos_validos = ["int", "float", "string"]


class AnalizadorSemantico:

    def __init__(self):
        """
        Constructor
        """
        self.tabla_simbolos = TB.TablaSimbolos()
        self.errores = []

    def analizar_codigo(self, codigo):
        """
        Wrapper para funcion _analizar_codigo

        Args:
            codigo (_type_): _description_
        """
        lineas = codigo.split("\n")

        for num_linea, linea in enumerate(lineas, 1):
            self._analizar_codigo(linea, num_linea)

        if not self.errores:
            print("El código fuente es correcto.")
        else:
            for error in self.errores:
                print(error)

    def analizar_llamada(self, tokens, num_linea):
        self.tabla_simbolos.insertar(
            "statement", {"tipo": "call", "valor": tokens[0], "linea": num_linea}
        )

        if self.analizar_linea(tokens[1:], num_linea) != None:
            self.errores.append(
                f"Error – Línea {num_linea}: Argumentos inválidos en llamada {tokens[0]}."
            )

    def validar_identificador(self, identificador):
        """
        _summary_

        Args:
            identificador (_type_): _description_

        Returns:
            _type_: _description_
        """
        if identificador.isalpha():
            return "string"
        elif identificador.isnumeric():
            return "int"
        elif identificador.isalnum() and identificador.replace(".", "", 1).isdigit():
            return "float"
        else:
            return None