import random

#Creamos el archivo
file = open("test.cvs", 'w')

#Hacer encabezados
file.write("X,Y,COLOR\n")

#Generar puntos aleatorios
for _ in range(100):
    ''' En python, Si la variable auxiliar NO SE OCUPA en el bloque de codigo, se coloca _'''
    x = random.uniform(-10,10)
    y = random.uniform(-10,10)

    #Calcular si se escapa o no
    punto = (x * x + y * y) ** 0.5 #Formula distancia
    iteraciones = 0
    color = 0

    while (punto < 1) and (iteraciones > 100):
        punto = punto * punto
        interaciones += 1
    color = 255 if punto > 1 else ( punto * 255)

    file.write(f"{x},{y},{color}\n")

file.close()

print("DONE")