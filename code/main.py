from EllipticCurve import EllipticCurve
from Entity import Entity
from tools import table
from Point import Point
import sys

# p = int(sys.argv[1])
# a = int(sys.argv[2])
# b = int(sys.argv[3])


alf = 'abcdefghijklmnopqrstuvwxyz '
# Curva que soporta 256 caracteres
eli = EllipticCurve(23, 1, 17)
g = eli.points[-1]
# print(g)
# print(len(eli.points))
# print(eli.order(g))
# print(eli.cofactor(g))

print("Puntos de la curva:\n")

print(eli.get_points())

print("Codificacion para cada letra del alfabeto:\n")

code = table(eli,alf)
print(code)

a = Entity("Allice", eli, g, code)
msg_a = "quiero vacaciones"
b = Entity("Bob", eli, g, code)
msg_b = "The fears we don't face, become our limits."
pub_k_a = a.genera_llaves_publicas()
pub_k_b = b.genera_llaves_publicas()
a.recibe_llaves_publicas(pub_k_b)
b.recibe_llaves_publicas(pub_k_a)

pub_k_a = a.final_keys()
pub_k_b = b.final_keys()
a.recibe_llaves_publicas(pub_k_b)
b.recibe_llaves_publicas(pub_k_a)

print()
print("Mensaje a cifrar: ", msg_a)
enc = a.cifrar(msg_a)
print("Mensaje cifrado:", enc)
denc = b.descifrar(enc)
print("Mensaje descifrado:", denc)

"""
Este es el resultado final:
(11, 5)
(6, 20)
(18, 18)
(18, 18)
Puntos de la curva:

[None, (2, 2), (2, 21), (3, 1), (3, 22), (4, 4), (4, 19), (5, 3), (5, 20), (6, 3), (6, 20), 
(8, 10), (8, 13), (11, 5), (11, 18), (12, 3), (12, 20), (15, 7), (15, 16), (16, 9), (16, 14),
 (17, 5), (17, 18), (18, 5), (18, 18), (19, 8), (19, 15)]
Codificacion para cada letra del alfabeto:

{'a': None, 'b': (2, 2), 'c': (2, 21), 'd': (3, 1), 'e': (3, 22), 'f': (4, 4), 'g': (4, 19), 
'h': (5, 3), 'i': (5, 20), 'j': (6, 3), 'k': (6, 20), 'l': (8, 10), 'm': (8, 13), 'n': (11, 5), 
'o': (11, 18), 'p': (12, 3), 'q': (12, 20), 'r': (15, 7), 's': (15, 16), 't': (16, 9), 'u': (16, 14),
 'v': (17, 5), 'w': (17, 18), 'x': (18, 5), 'y': (18, 18), 'z': (19, 8), ' ': (19, 15)}

Mensaje a cifrar:  quiero vacaciones
Mensaje cifrado: [('m', 'n'), ('m', 'q'), ('m', 'w'), ('m', 'y'), ('m', 'v'), ('m', 'p'), ('m', 'm'), ('m', 'h'), ('m', 'f'), ('m', 'e'), ('m', 'f'), ('m', 'e'), ('m', 'w'), ('m', 'p'), ('m', 'u'), ('m', 'y'), ('m', 'i')]
Mensaje descifrado: quiero vacaciones
"""