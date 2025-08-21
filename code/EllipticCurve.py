from Point import Point
from tools import *

class EllipticCurve:
    '''Clase que crea una curva elíptica usando un campo finito modulo p > 3'''

    # Punto al infinito siempre será None. Ignorar esta prueba unitaria
    inf_p = None

    
    def __init__(self, prime = 23, a = 1, b = 17):
        '''Construimos la curva elíptica a partir de los parámetros a, b modulo p'''
        if not isPrime(prime):
            raise ValueError("El campo debe estar definido sobre un número primo.")


        self.prime = prime
        self.a = a
        self.b = b
        self.points = self.calculate_points()

    def __str__(self):
        '''La curva debe ser representada como: y^2 = x^3 + ax + b mod p'''
        return f"y^2 = x^3 + {self.a}x + {self.b} mod {self.prime}"

    def isInCurve(self, point):
        '''Nos dice si un punto "point" pertenece a esta curva'''

        if point == self.inf_p:
            return True

        if not isinstance(point,Point):
            return False

        if point == self.inf_p:
            return True

        # los puntos (y^2=x3+ax+b)%p estan en la curva, por lo que si se cumpla la igualdad, lo va estar

        x,y = point.x, point.y
        l = (y**2)%self.prime
        r = (x**3 + (self.a*x) + self.b)%self.prime

        return l == r

    def get_points(self):
        '''Nos da todos los puntos que pertenecen a la curva elíptica'''
        return self.points
    
    def calculate_points(self):
        points = []
        points.append(None)        
        for x in range(self.prime):
            for y in range(self.prime):
                point = Point(x,y)

                if self.isInCurve(point):
                    points.append(point)

        return points

    def sum(self, p, q):
        '''Suma p + q  regresando un nuevo punto modulo prime
        como está definido en las curvas elípticas. Recuerda que el punto al
        infinito funciona como neutro aditivo'''

        if p == self.inf_p:
            return q 
        
        if q == self.inf_p:
            return p
        
        if p.x == q.x and (p.y != q.y or p.y == 0):
            return self.inf_p
        
        if p == q: 
            m = ((3*(p.x)**2 + self.a )*inv_mult(2*p.y,self.prime))%self.prime
        else:
             m = ((q.y - p.y) * inv_mult(q.x - p.x, self.prime)) % self.prime

        rx = (m ** 2 - p.x - q.x) % self.prime
        ry = (m * (p.x - rx) - p.y) % self.prime

        return Point(rx,ry)


    def mult(self, k, p):
        '''Suma  k veces el punto p (o k(P)).
        Si k < 0 entonces se suma el inverso de P k veces'''
        if k == 0 or p == self.inf_p:
            return self.inf_p
        if k < 0:
            return self.mult(-k, self.inv(p))
        
        result = self.inf_p
        addend = p

        while k > 0:
            # Si k es impar, añadimos el punto 'addend' a 'result'
            if k % 2 != 0:
                result = self.sum(result, addend)
            
            # Duplicamos el punto 'addend' en cada iteración
            addend = self.sum(addend, addend)
            
            # Reducimos k a la mitad (división entera)
            k = k // 2
            
        return result

    def order(self, p):
        '''Dado el punto p que pertenece a la curva elíptica, nos regresa el mínimo entero k 
        tal que  k(P) = punto al infinito.'''
        if not self.isInCurve(p):
            raise ValueError("El punto debe estar en la curva")
            
        k = 1
        current = p
        while current is not self.inf_p:
            k += 1
            current = self.sum(current, p)
        return k
   

    def cofactor(self, p):
        '''Dado el punto p de la curva, regresa el total de puntos de la curva entre el orden
        de ese punto'''
        if not self.isInCurve(p):
            raise ValueError("Point must be on the curve")
            
        point_order = self.order(p)
        curve_order = len(self.points)
        
        # The cofactor is the number of times the point order divides the curve order
        return curve_order // point_order
      

    def inv(self, p):
        '''Regresa el inverso aditivo de este punto. Recuerda que es el mismo punto reflejado
        en el eje x'''
        if p == self.inf_p:
            return self.inf_p
        return Point(p.x, (-p.y) % self.prime)

# Definimos la curva
curve = EllipticCurve(23, 1, 17)
# Definimos el punto
p = Point(2, 2)
# Calculamos 5P
result = curve.mult(5, p)
print(result) # (11,5)

# Definimos la curva
curve = EllipticCurve(23, 1, 17)
# Definimos el punto
p = Point(2, 2)
# Calculamos 7P
result = curve.mult(7, p)
print(result) #(6,20)

# Definimos la curva
curve = EllipticCurve(23, 1, 17)
# Definimos el punto
p = Point(6, 20)
# Calculamos 7P
result = curve.mult(5, p)
print(result)

# Quiero saber cual es el resultado de multiplicar 5 veces el punto (20 ,20)
# en la curva y^2 = x^3 + 1x + 17 mod 23

# Definimos la curva
curve = EllipticCurve(23, 1, 17)
# Definimos el punto
p = Point(11, 5)
# Calculamos 5P
result = curve.mult(7, p)
print(result)
