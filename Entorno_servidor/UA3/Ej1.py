class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        print(f"Punto creado en ({self.x}, {self.y})")

    def __del__(self):
        print(f"Punto en ({self.x}, {self.y}) eliminado")
        
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __eq__(self, otro):
        if isinstance(otro, Punto):
            return self.x==otro.x and self.y==otro.y
        return False
    
    def __add__(self, otro):
        if isinstance(otro, Punto):
            return Punto(self.x + otro.x, self.y + otro.y)
        return NotImplemented
    
if __name__ == "__main__":
    p1 = Punto(2, 3)
    p2 = Punto(2, 3)
    p3=p1+p2
    print(f"Suma de puntos: {p3}")
    print(f"p1 es igual a p2? {p1==p2}")