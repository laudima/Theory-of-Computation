# Default alphabet
alphabet = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def isPrime(n):
    '''Nos dice si un número n es primo'''
    # Los números menores que 2 no son primos
    if n <= 1:
        return False
    # Los números 2 y 3 son primos
    if n <= 3:
        return True
    # Eliminar los múltiplos de 2 y 3 para optimización
    if n % 2 == 0 or n % 3 == 0:
        return False
    # Comprobar desde 5 hasta la raíz cuadrada de n
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
    

def inv_add(a, mod):
    '''Nos da el inverso aditivo tal que a + i == 0 modulo n'''
    return (-a) % mod


def inv_mult(a, mod):
    '''Nos da el inverso multiplicativo modulo n'''
    # Utilizamos el algoritmo extendido de Euclides para hallar el inverso multiplicativo
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    gcd, x, _ = extended_gcd(a, mod)
    # El inverso multiplicativo existe solo si a y mod son coprimos
    if gcd != 1:
        raise ValueError(f'El inverso multiplicativo de {a} módulo {mod} no existe')
    else:
        # Nos aseguramos de que el resultado esté en el rango [0, mod-1]
        return x % mod


def table(elliptic_curve, alphabet = alphabet):
    '''Regesa una tabla de un abecedario mapeado a puntos de la curva elíptica e'''
    pts = elliptic_curve.points
    if len(pts) < len(alphabet):
        print("Las letras mapeadas no caben en la definición de la curva. Se recortará el alfabeto...\n")
        l = alphabet[:len(pts)]
    else:
        l = alphabet

    table = {}

    for i in range(len(l)):
        if i < len(pts):
            table[l[i]] = pts[i]
    return table
