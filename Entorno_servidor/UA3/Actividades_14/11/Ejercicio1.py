'''Ejercicio 1'''
class Producto:
    def __init__(self, nombre, precio, stock):
        self.__nombre = nombre
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = precio
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.__stock = stock
    '' 'getters'''
    @property
    def precio(self):
        return self.__precio
    @property
    def stock(self):
        return self.__stock
    @property
    def nombre(self):
        return self.__nombre
    '' 'setters'''
    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = valor
    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.__stock = valor

def mostrar_inventario(inventario):
    for producto in inventario:
        try:
            valor_total = producto.precio * producto.stock
            print(f"Producto: {producto.nombre}, valor total: {valor_total}")
        except Exception as e:
            print(f"No se puede acceder a los atributos del producto {producto.nombre}: {e}")
        

    
