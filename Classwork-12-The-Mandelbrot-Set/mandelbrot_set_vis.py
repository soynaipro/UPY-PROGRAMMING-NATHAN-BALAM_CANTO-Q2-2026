from PIL import Image


config = {}

file = open("config.txt", "r")
lines = file.readlines()
for line in lines:
    parameter, value = line.strip().split("=")
    config[parameter] = float(value) if "." in value else int(value)
file.close()

print(config)

archivo = open("mandelbrot.csv", "r")
lineas = archivo.readlines()
archivo.close()

#NO OLVIDAR QUITAR ENCABEZASDOS
lineas.pop(0)

#DESEMPAQUETAR VARIABLES
max_iter= config["max_iter"]
ancho, alto = config["ancho"], config["alto"]


img = Image.new("HSV", (ancho,alto))

for linea in lineas:
    row, column, iterations = linea.strip().split(",")
    iterations = int(iterations)
    row = int(row)
    column = int(column)
    
    if iterations == max_iter:
        brillo = 40
    else:
        brillo = int((iterations/ max_iter) * 255)
        
    img.putpixel((column,row), (brillo,255,255))
    
img_rgb = img.convert("RGB")
img_rgb.save("mandelbrot.png")
print("DONE")