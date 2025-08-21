class Point:
    '''Clase que representa un punto en un plano 2D'''

    #Punto al infinito
    infinite_point = None

    def __init__(self, x = 0, y = 0):
        '''Constructor: Construye un punto en un plano 2D con coordenadas (x,y)'''
        self.x = x
        self.y = y

    def __str__(self):
        '''Representación en cadena. Usamos str(p)'''
        return f'({self.x}, {self.y})'


    def __repr__(self):
        '''Representación en cadena x2. Usamos print(p)'''
        s = f'({self.x}, {self.y})'
        # return ("(", self.x, ", ", self.y, ")")
        return s

    def __eq__(self, another_point):
        '''Comparación entre 2 puntos. Usamos ==
        another_point debe ser instancia de Point'''
        if not isinstance(another_point,Point):
            return False
        
        return (self.x == another_point.x) and (self.y == another_point.y)



    def set(self, x, y):
        '''Reescribe los valores de x y y a este punto.
        @raise ValueError si x o y no son números enteros'''
        if not isinstance(x, (int)) or not isinstance(y,int):
            # raise ValueError("Las coordenadas de los puntos deben ser enteras")
            return
        
        self.x = x
        self.y = y

