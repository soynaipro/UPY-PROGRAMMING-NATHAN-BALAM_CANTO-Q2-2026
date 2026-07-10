import math

# INPUT
a = input("Write the left endpoint of the interval: ")
b = input("Write the right endpoint of the interval: ")

if a == "pi":
    a = math.pi
else:
    a = float(a)

if b == "pi":
    b = math.pi
else:
    b = float(b)

f_x = input("Write the function to integrate: ")
method = input("Select Integration Method (LRM/RRM/MPM/TRM): ").upper()

n = int(input("Write the number of subintervals: "))

exact = input("Write the exact value (or press Enter if unknown): ")

if exact != "":
    exact = float(exact)

# PROCESS
area = 0
h = (b - a) / n

if method == "TRM":
    area = eval(f_x.replace("x", str(a))) + eval(f_x.replace("x", str(b)))

    for i in range(1, n):
        xi = a + i * h
        area += 2 * eval(f_x.replace("x", str(xi)))

    area *= h / 2

else:
    shift = 0
    constant = 0

    if method == "RRM":
        shift = 1
    elif method == "MPM":
        constant = h / 2

    for i in range(0 + shift, n + shift):
        xi = a + i * h + constant
        area += eval(f_x.replace("x", str(xi))) * h

# OUTPUT
print(f"\nThe integration of {f_x} is {area:.6f}")

if exact != "":
    abs_error = abs(exact - area)
    rel_error = abs_error / abs(exact) * 100

    print(f"Exact value: {exact:.6f}")
    print(f"Absolute error: {abs_error:.6f}")
    print(f"Relative error: {rel_error:.4f}%")
    
