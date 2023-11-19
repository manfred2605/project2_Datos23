import AnalizadorSemantico as AS


# import Identifier_method


def main(nom_archivo, analizador):
    """
    _summary_

    Args:
        nom_archivo (_type_): _description_
        :param nom_archivo:
        :param analizador:
    """
    with open(nom_archivo, 'r') as file:
        codigo_fuente = file.read()

    analizador.analizar_codigo(codigo_fuente)


def imprimir_tabla(tabla_simb):
    """
    _summary_

    Args:
        tabla_simb (_type_): _description_
    """
    print("Tabla de simbolos:")
    for entrada in tabla_simb.tabla:
        if entrada is not None:
            for simbolo in entrada:
                print(simbolo['llave'], simbolo['valores'])


if __name__ == "__main__":
    analizador = AS.AnalizadorSemantico()

    main('code1.txt', analizador)

    print("\n")

    imprimir_tabla(analizador.tabla_simbolos)