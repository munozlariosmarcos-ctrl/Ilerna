'''Crea un programa que pida dos números al usuario e intente dividirlos.
Pasos:

Usa try y except para capturar divisiones por cero y errores de tipo (por ejemplo, si el usuario escribe texto).
Si la división es correcta, muestra el resultado dentro del bloque else.
Usa un bloque finally para mostrar un mensaje de cierre, independientemente del resultado.'''
try:
    num1 = float(input("Introduce el primer número: "))
    num2 = float(input("Introduce el segundo número: "))
    resultado = num1 / num2
except ZeroDivisionError as e:
    print("Error: No se puede dividir por cero.")
except ValueError as e:
    print(f"Error:no has introducido un numero {e.args}.")
else:
    print(f"El resultado de la división es: {resultado}")
finally:
    print("Gracias por usar el programa de división.")
