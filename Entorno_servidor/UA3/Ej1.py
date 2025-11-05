class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        print(f"Punto creado en ({self.x}, {self.y})")

    def __del__(self):
        print(f"Punto en ({self.x}, {self.y}) eliminado")
        
    def __str__(self):
        return "Punto con x=" + str(self.x) + " e y=" + str(self.y)   
    
    def __eq__(self, otro):
        return self.x==otro.x and self.y==otro.y
    
    def __add__(self, otro):    
        return Punto(self.x + otro.x, self.y + otro.y)
        

# código de prueba
    p1 = Punto(2, 3)
    p2 = Punto(1, 4)
    
    print(p1)      
    print(p2)         
    print(p1 == p2)