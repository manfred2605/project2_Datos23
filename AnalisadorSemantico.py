# import TablaSimbolos as TB

arit_ops = ["+", "-", "*", "**", "/", "//", "%"]
comp_ops = [">", "<", ">=", "<=", "==", "!="]
logic_ops = ["&&", "||"]
tipos_validos = ["int", "float", "string"]


class AnalizadorSemantico:
    """
    _summary_
    """

    def __init__(self):
        """
        Constructor
        """
        #self.tabla_simbolos = TB.TablaSimbolos()
        self.errores = []
