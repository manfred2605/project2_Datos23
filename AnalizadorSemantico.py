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
    
    def _analizar_codigo(self, linea, num_linea):
        """
        Funcion para analizar una linea de codigo

        Args:
            linea (_type_): _description_
            num_linea (_type_): _description_
        """
        tokens = linea.split()

        if tokens:
            palabra_clave = tokens[0]

            if (palabra_clave in tipos_validos + ["void"]) and (
                    "(" and ")" and "{"
            ) in linea:
                self.analizar_funcion(tokens, num_linea)

            elif palabra_clave in ["if", "while"] and ("(" and ")" and "{") in linea:
                self.tabla_simbolos.insertar(
                    palabra_clave, {"tipo": "condicion/ciclo", "linea": num_linea}
                )
                self.analizar_condicion(
                    tokens[tokens.index("(") + 1: tokens.index(")")], num_linea
                )

            elif palabra_clave in tipos_validos and not "=" in linea:
                self.analizar_declaracion(tokens, num_linea)

            elif "=" in linea:
                self.analizar_asignacion(tokens, num_linea)

            elif palabra_clave == "return":
                self.analizar_llamada(tokens, num_linea)

            else:
                self.analizar_linea(tokens, num_linea)
    
    def analizar_asignacion(self, tokens, num_linea):
        """
        Funcion para analizar una asignacion en linea de codigo

        Args:
            tokens (_type_): _description_
            num_linea (_type_): _description_
        """
        identificador = tokens[1]
        if self.tabla_simbolos.buscar(identificador):
            self.errores.append(
                f"Error – Línea {num_linea}: '{identificador}' ya está declarado."
            )
        else:
            tipo_identificador = tokens[0]

            # Verifica los tipos de datos dentro de la asignacion
            if tokens[2] == "=":
                valor = tokens[3]

                if tipo_identificador == "int" and not valor.isdigit():
                    self.errores.append(
                        f"Error – Línea {num_linea}: Asignación inválida para '{identificador}'."
                    )
                    return

                elif (
                        tipo_identificador == "float"
                        and not valor.replace(".", "", 1).isdigit()
                ):
                    self.errores.append(
                        f"Error – Línea {num_linea}: Asignación inválida para '{identificador}'."
                    )
                    return

                elif tipo_identificador == "string" and not (
                        valor.startswith('"') and valor.endswith('"')
                ):
                    self.errores.append(
                        f"Error – Línea {num_linea}: Asignación inválida para '{identificador}'."
                    )
                    return

                self.tabla_simbolos.insertar(
                    identificador,
                    {"tipo": tokens[0], "valor": valor, "linea": num_linea},
                )
    
    def analizar_condicion(self, tokens_condicion, num_linea):
        """
        Funcion para analizar una condicion dentro de linea de codigo

        Args:
            tokens (_type_): _description_
            num_linea (_type_): _description_
            :param num_linea:
            :param tokens_condicion:
        """
        tipo_actual = None

        for token in tokens_condicion:
            if token.isalnum():
                if self.validar_identificador(token) == "string":
                    if self.tabla_simbolos.buscar(token):
                        pass
                    else:
                        self.tabla_simbolos.insertar(
                            token,
                            {"tipo": "string", "valor": f"{token}", "linea": num_linea},
                        )

                if self.validar_identificador(token) == "int":
                    if self.tabla_simbolos.buscar(token):
                        pass
                    else:
                        self.tabla_simbolos.insertar(
                            token, {"tipo": "int", "valor": token, "linea": num_linea}
                        )

                if self.validar_identificador(token) == "float":
                    if self.tabla_simbolos.buscar(token):
                        pass
                    else:
                        self.tabla_simbolos.insertar(
                            token, {"tipo": "float", "valor": token, "linea": num_linea}
                        )

                elif self.validar_identificador(token) is None:
                    self.errores.append(
                        f"Error – Línea {num_linea}: '{token}' no es argumento válido."
                    )
                    return

                # Verifica si el identificador ya esta declarado
                if not self.tabla_simbolos.buscar(token):
                    self.errores.append(
                        f"Error – Línea {num_linea}: '{token}' no está declarado."
                    )
                    return
                else:
                    # Obtiene el tipo del identificador de la tabla de simbolos
                    tipo_identificador = self.tabla_simbolos.buscar(token)["tipo"]

                if tipo_actual is None:
                    tipo_actual = tipo_identificador

                # Realiza verificacion de tipos
                elif tipo_actual != tipo_identificador:
                    self.errores.append(
                        f"Error – Línea {num_linea}: Tipos incompatibles en la condición."
                    )
                    return

            if token in comp_ops:
                # Se verifica si se utilizan operadores de comparacion
                if not self.tabla_simbolos.buscar(token):
                    self.tabla_simbolos.insertar(
                        token, {"tipo operador": "comparacion", "linea": num_linea}
                    )

                if tipo_actual not in tipos_validos:
                    self.errores.append(
                        f"Error – Línea {num_linea}: Operador de comparación '{token}' no válido para el tipo de dato."
                    )
                    return

            if token in arit_ops:
                # Se verifica si se utilizan operadores aritmeticos
                if not self.tabla_simbolos.buscar(token):
                    self.tabla_simbolos.insertar(
                        token, {"tipo operador": "aritmetico", "linea": num_linea}
                    )

                if tipo_actual not in ["int", "float"]:
                    self.errores.append(
                        f"Error – Línea {num_linea}: Operador aritmético '{token}' no válido para el tipo de dato."
                    )
                    return

            if token in logic_ops:
                # Se verifica si se utilizan operadores logicos
                if not self.tabla_simbolos.buscar(token):
                    self.tabla_simbolos.insertar(
                        token, {"tipo operador": "logico", "linea": num_linea}
                    )
            else:
                # Se verifican otros casos de ser necesarios
                pass

        # Verifica si el tipo es valido en la condicion
        if tipo_actual not in tipos_validos:
            self.errores.append(
                f"Error – Línea {num_linea}: Tipo no permitido en la condición."
            )
        else:
            pass

    def analizar_declaracion(self, tokens, num_linea):
        """
        Funcion para analizar una declaracion dentro de linea de codigo

        Args:
            tokens (_type_): _description_
            num_linea (_type_): _description_
        """
        identificador = tokens[1]
        if self.tabla_simbolos.buscar(identificador):
            self.errores.append(
                f"Error – Línea {num_linea}: '{identificador}' ya está declarado."
            )
        else:
            # Verifica si el tipo de datos es valido (solo se verifican 'int', 'float', y 'string')
            if tokens[0] not in tipos_validos:
                self.errores.append(
                    f"Error – Línea {num_linea}: Tipo de dato no válido."
                )
            else:
                self.tabla_simbolos.insertar(
                    identificador, {"tipo": tokens[0], "linea": num_linea}
                )

    def analizar_funcion(self, tokens, num_linea):
        """
        Funcion para analizar una funcion en linea de codigo

        Args:
            tokens (_type_): _description_
            num_linea (_type_): _description_
        """
        identificador = tokens[1]
        if self.tabla_simbolos.buscar(identificador):
            self.errores.append(
                f"Error – Línea {num_linea}: '{identificador}' ya está declarado."
            )
        else:
            self.tabla_simbolos.insertar(
                identificador, {"tipo": tokens[0], "funcion": True, "linea": num_linea}
            )

            # Manejo de parametros
            params_inicio = tokens.index("(")
            params_fin = tokens.index(")")
            if "," in tokens:
                params_separador = tokens.index(",")
                parametros = (
                        tokens[params_inicio + 1: params_separador]
                        + tokens[params_separador + 1: params_fin]
                )
            else:
                parametros = tokens[params_inicio + 1: params_fin]

            for i in range(0, len(parametros) - 1, 2):
                tipo_param = parametros[i]
                param = parametros[i + 1]
                if param.isalnum():
                    self.tabla_simbolos.insertar(
                        param,
                        {"tipo": tipo_param, "parametro": True, "linea": num_linea},
                    )
                else:
                    self.errores.append(
                        f"Error – Línea {num_linea}: Nombre de parámetro inválido."
                    )

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
