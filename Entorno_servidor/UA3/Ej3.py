'''Crea un programa que pida al usuario su edad y valide que sea un número positivo.'''
try:
    edad=int(input("Introduce tu edad : "))
    if edad < 0:
        raise ValueError("La edad debe de ser un numero positivo.") 
except ValueError as e:
    print(f"Error: {e}")
else:
    print(f"Tienes {edad} años.")
finally:
    print("Gracias por usar el programa.")

