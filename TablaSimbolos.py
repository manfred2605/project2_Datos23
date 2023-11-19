class TablaSimbolos:
    """
    Clase TablaSimbolos

    Atributos:
        -> tamano => indica el tamano maximo para la tabla
        -> tabla => almacena la tabla como estructura
    """

    def __init__(self, tamano=100):
        """
        Constructor

        Args:
            tamano (int, optional): Indica el tamano deseado para la tabla. El valor inicial es 100 en caso de no indicar.
        """
        self.tamano = tamano
        self.tabla = [None] * self.tamano

    def _funcion_hash(self, llave):
        """
        Funcion para realizar hashing

        Args:
            llave (_tipo_): _description_

        Returns:
            _type_: _description_
        """
        return hash(llave) % self.tamano

    def insertar(self, llave, valores):
        """
        Funcion para insertar en tabla

        Args:
            llave (_type_): _description_
            valores (_type_): _description_
        """
        llave_hash = self._funcion_hash(llave)
        if self.tabla[llave_hash] is None:
            self.tabla[llave_hash] = [{"llave": llave, "valores": valores}]
        else:
            self.tabla[llave_hash].append({"llave": llave, "valores": valores})

    def buscar(self, llave):
        """
        Funcion para buscar en tabla

        Args:
            llave (_type_): _description_

        Returns:
            _type_: _description_
        """
        llave_hash = self._funcion_hash(llave)
        entradas = self.tabla[llave_hash]
        if entradas is not None:
            for entrada in entradas:
                if entrada["llave"] == llave:
                    return entrada["valores"]
        return None

    def modificar(self, llave, nuevos_valores):
        """
        Funcion para modificar valores en tabla

        Args:
            llave (_type_): _description_
            nuevos_valores (_type_): _description_

        Returns:
            _type_: _description_
        """
        llave_hash = self._funcion_hash(llave)
        entradas = self.tabla[llave_hash]
        if entradas is not None:
            for entrada in entradas:
                if entrada["llave"] == llave:
                    entrada["valores"] = nuevos_valores
                    return True
        return False

    def eliminar(self, llave):
        """
        Funcion para eliminar valor en tabla

        Args:
            llave (_type_): _description_

        Returns:
            _type_: _description_
        """
        llave_hash = self._funcion_hash(llave)
        entradas = self.tabla[llave_hash]
        if entradas is not None:
            for i, entrada in enumerate(entradas):
                if entrada["llave"] == llave:
                    del entradas[i]
                    return True
        return False
