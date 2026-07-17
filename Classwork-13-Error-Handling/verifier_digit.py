rol = input("Ingrese rol sin digito verificador: ")

# Validamos que el rol ingresado contenga el guion para cumplir con el formato
if "-" not in rol:
    print("Rol inválido: No tiene el formato XXXXXXXXX-X")
else:
    # Separamos la parte numérica del dígito verificador
    rol_base, verificador_ingresado = rol.split("-", 1)
    
    suma = 0
    multiplicador = 2

    for digito in reversed(rol_base):
        suma += int(digito) * multiplicador
        multiplicador += 1
        
        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    digito_verificador = 11 - resto
    
    # Manejo de los casos especiales del dígito verificador (11 -> 0, 10 -> K)
    if digito_verificador == 11:
        digito_verificador = "0"
    elif digito_verificador == 10:
        digito_verificador = "K"
    else:
        digito_verificador = str(digito_verificador)

    # Aquí puedes imprimir el rol con su dígito calculado o hacer la comparación final
    print(f"{rol_base}-{digito_verificador}")