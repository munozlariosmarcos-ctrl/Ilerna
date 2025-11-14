'''Ejercicio 2'''
class Alumno:
    def __init__(self, nombre, notas=None):
        self.__nombre = nombre
        if notas is None:
            self.__notas = []
        else:
            self.__notas = notas

    def agregar_nota(self, nota):
        if nota < 0 or nota > 10:
            raise ValueError("La nota debe estar entre 0 y 10.")
        self.__notas.append(nota)

    def media(self):
        if not self.__notas:
            raise ValueError("No hay notas para calcular la media.")
        return sum(self.__notas) / len(self.__notas)

    @property
    def nombre(self):
        return self.__nombre
def mostrar_media_alumno(alumno):
    try:
        media = alumno.media()
        print(f"Alumno: {alumno.nombre}, Media: {media}")
    except Exception as e:
        print(f"No se puede calcular la media del alumno {alumno.nombre}: {e}")




alumno1 = Alumno("Pablo")
alumno2 = Alumno("Antonio El futbolista", [8, 9, 10])
alumno3 = Alumno("Nicolas")
alumno4 = Alumno("Manolin", [5, 6, 7])
try:
    alumno1.agregar_nota(7)
    alumno1.agregar_nota(11)  
except Exception as e:
    print(f"Error al agregar nota a {alumno1.nombre}: {e}")
mostrar_media_alumno(alumno1)
mostrar_media_alumno(alumno2)
