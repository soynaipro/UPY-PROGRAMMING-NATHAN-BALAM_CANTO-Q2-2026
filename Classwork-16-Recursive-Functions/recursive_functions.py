def recursiva(n):
    # Caso base
    if n == 0:
        return "Done"
    else:
        print(n - 1)
        return recursiva(n - 1)


def fibonacci(n):
    # Caso base
    if n == 0 or n == 1:
        return n
    else:
        print((n - 1, n - 2))
        return fibonacci(n - 1) + fibonacci(n - 2)


def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return factorial(n - 1) * n


def multiplicacion_recursiva(n, m):
    total = 0
    if m == 0:
        return total
    else:
        return multiplicacion_recursiva(n, m - 1) + n


def division_entera(dividendo, divisor):
    if dividendo - divisor < 0:
        return 0
    else:
        return division_entera(dividendo - divisor, divisor) + 1


def serie_collatz(n):
    if n == 1:
        print('end')
        return 0
    else:
        if n % 2 == 0:
            print(n // 2)
            return serie_collatz(n // 2)
        else:
            print(3 * n + 1)
            return serie_collatz(3 * n + 1)

import json
with open("generated.json") as file:
    data = json.load(file)

def aplanar_json(estructura, clave_padre='', separador='.'):
    elementos = []
    # Normalizamos: si es lista usamos el indice como llave
    if isinstance(estructura, list):
        items = enumerate(estructura)
    else:
        items = estructura.items()
    for key, value in items:
        nueva_llave = f"{clave_padre}{separador}{key}" if clave_padre != '' else str(key)
        if isinstance(value, (dict, list)):
            # Recursividad si el valor es otro diccionario o lista
            elementos.extend(aplanar_json(value, nueva_llave, separador).items())
        else:
            elementos.append((nueva_llave, value))

    return dict(elementos)

json_prueba = {
    'alumnos': [
        {"Roman": "Hola"},
        {"Emiliano": "Hola Mundo"},
        {"Nathan": "ok"},
        {"Stephan": "Adios"}
    ],
    'Materias': {
        "programacion": {"Unidad 1": 9, "Unidad 2": 8, "Unidad 3": 10},
        "mate discretas": {"Unidad 1": 9, "Unidad 2": 9, "Unidad 3": 7}
    }
}
print(aplanar_json(data))