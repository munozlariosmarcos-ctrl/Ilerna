'''Crea una lista con cinco números y pide al usuario un índice para mostrar un elemento.'''
numeros = [10, 20, 30, 40, 50]
try:
    indice = int(input("Introduce un indice entre 0 y 4: "))
except IndexError as e:
    print("Error: Indice fuera de rango.")
except ValueError as e:
    print("Error: Debes introducir un numero")
else:
    print(f"El numero en el indice {indice} es: {numeros[indice]}")
finally:
    print("Lista de numeros : " , numeros)

