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

    def analizar_llamada(self, tokens, num_linea):
        self.tabla_simbolos.insertar(
            "statement", {"tipo": "call", "valor": tokens[0], "linea": num_linea}
        )

        if self.analizar_linea(tokens[1:], num_linea) != None:
            self.errores.append(
                f"Error – Línea {num_linea}: Argumentos inválidos en llamada {tokens[0]}."
            )
