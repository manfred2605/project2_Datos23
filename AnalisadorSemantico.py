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

    def analizar_llamada(self, tokens, line_number):
        self.tabla_simbolos.insertar(
            "statement", {"tipo": "call", "valor": tokens[0], "linea": line_number}
        )

        if self.analizar_linea(tokens[1:], line_number) is not None:
            self.errores.append(
                f"Error – Línea {line_number}: Argumentos inválidos en llamada {tokens[0]}."
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

    def analizar_linea(self, tokens, line_number):

        for token in tokens:
            if token.isalnum():
                if self.validar_identificador(token) == "string":  # analiza si el token es de tipo string
                    if self.tabla_simbolos.buscar(token):
                        pass
                    else:
                        self.tabla_simbolos.insertar(
                            token,
                            {"tipo": "string", "valor": f"{token}", "linea": line_number},
                        )

                if self.validar_identificador(token) == "int":  # analiza si el token es de tipo int
                    if self.tabla_simbolos.buscar(token):
                        pass
                    else:
                        self.tabla_simbolos.insertar(
                            token, {"tipo": "int", "valor": token, "linea": line_number}
                        )

                if self.validar_identificador(token) == "float":  # analiza si el token es de tipo float
                    if self.tabla_simbolos.buscar(token):
                        pass
                    else:
                        self.tabla_simbolos.insertar(
                            token, {"tipo": "float", "valor": token, "linea": line_number}
                        )

                elif self.validar_identificador(token) is None: # analiza si el es o no identificador valido sino
                    # genera un error
                    self.errores.append(
                        f"Error – Línea {line_number}: '{token}' no es argumento válido."
                    )
                    return

            if token in arit_ops: # analiza si el token es o no, operador aritmetico
                if self.tabla_simbolos.buscar(token):
                    pass
                else:
                    self.tabla_simbolos.insertar(
                        token, {"tipo operador": "aritmetico", "linea": line_number}
                    )

            if token in comp_ops:  # analiza si el token es o no, un operador de comparacion
                if self.tabla_simbolos.buscar(token):
                    pass
                else:
                    self.tabla_simbolos.insertar(
                        token, {"tipo operador": "comparacion", "linea": line_number}
                    )

            if token in logic_ops:  # analiza si el token es o no, un operador logico
                if self.tabla_simbolos.buscar(token):
                    pass
                else:
                    self.tabla_simbolos.insertar(
                        token, {"tipo operador": "logico", "linea": line_number}
                    )

            elif token in [";", "}"]: # si el token es ";", "}" no hace nada
                pass

            elif not self.tabla_simbolos.buscar(token): # analiza si el token no esta en la tabla, genera un error
                self.errores.append(
                    f"Error – Línea {line_number}: '{token}' es argumento inválido."
                )
                return
