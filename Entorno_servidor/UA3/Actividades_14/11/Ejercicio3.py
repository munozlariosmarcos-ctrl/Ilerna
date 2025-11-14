'''Ejercicio 3'''

class Libro:
    def __init__(self, titulo, autor):
        self.__titulo = titulo
        self.__autor = autor
        self.__prestado = False

    def prestar(self):
        if self.__prestado:
            raise Exception(f"El libro '{self.__titulo}' ya está prestado.")
        self.__prestado = True

    def devolver(self):
        if not self.__prestado:
            raise Exception(f"El libro '{self.__titulo}' no está prestado.")
        self.__prestado = False

    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def prestado(self):
        return self.__prestado
    
class Biblioteca:
    def __init__(self):
        self.__libros = []

    def agregar_libro(self, libro):
        self.__libros.append(libro)

    def buscar_por_titulo(self, titulo):
        for libro in self.__libros:
            if libro.titulo == titulo:
                return libro
        return None

    def mostrar_libros(self):
        for libro in self.__libros:
            estado = "Prestado" if libro.prestado else "Disponible"
            print(f"Título: {libro.titulo}, Autor: {libro.autor}, Estado: {estado}")



biblioteca = Biblioteca()

libro1 = Libro("1984", "Pblo Orti")
libro2 = Libro("Quijote", "Antonio Molina")
libro3 = Libro("Blancanieves", "Manolin")

biblioteca.agregar_libro(libro1)
biblioteca.agregar_libro(libro2)
biblioteca.agregar_libro(libro3)

biblioteca.mostrar_libros()

try:
    libro_a_prestar = biblioteca.buscar_por_titulo("1984")
    if libro_a_prestar:
        libro_a_prestar.prestar()
        print(f"Se ha prestado el libro: {libro_a_prestar.titulo}")
    else:
        print("Libro no encontrado.")
except Exception as e:
    print(e)

try:
    libro_a_devolver = biblioteca.buscar_por_titulo("1984")
    if libro_a_devolver:
        libro_a_devolver.devolver()
        print(f"Has devuelto el libro: {libro_a_devolver.titulo}")
    else:
        print("Libro no encontrado.")
except Exception as e:
    print(e)

biblioteca.mostrar_libros()
