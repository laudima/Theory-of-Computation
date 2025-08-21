import random as r
from EllipticCurve import *


class Entity:
    '''Clase que modela una entidad como Alice o Bob.'''

    def __init__(self, name, curve, generator_point, table):
        '''Construye un nuevo personaje con un mensaje para compartir
        Una entidad tiene:
        1. name: Nombre de la entidad
        2. curve: Una curva eliptica a compartir
        3. generator_point: Un punto generador a compartir
        4. table: Una codificacion de caracteres a puntos de la curva.

        Ademas, debe inicializar sus llaves, publicas y privadas:
        5. private_key: Un entero aleatorio entre 1 y el orden del punto generador-1
        6. private_point: Un punto aleatorio de la curva que no sea el punto al infinito
        ## 3 llaves publicas de esta entidad
        7. public_key_1, public_key_2, public_key_3 = None
        ## 3 llaves publicas de la otra entidad
        8. another_entity_public_key_1, another_entity_public_key_2, another_entity_public_key_3 = None'''
        self.name = name
        self.curve = curve
        self.generator_point = generator_point
        self.order = curve.order(self.generator_point)
        ## Cosas privadas
        self.private_key = r.randint(1,self.order-1)
        # self.private_point = curve.mult(self.private_key,self.generator_point)

        # Generamos el punto privado: punto aleatorio que no sea infinito ni -G
        while True:
            points = self.curve.points[1:]  # Excluimos el punto infinito
            self.private_point = r.choice(points)
            # Verificamos que no sea el inverso de G
            if self.curve.sum(generator_point, self.private_point) is not None:
                break

        # Cosas publicas
        self.public_key_1 = None #Public key using private point
        self.public_key_2 = None #Public key using only private key
        self.public_key_3 = None

        #Public keys from another entity
        self.another_entity_public_key_1 = None
        self.another_entity_public_key_2 = None
        self.another_entity_public_key_3 = None

        self.table = table

    def __str__(self):
        '''Representacion en cadena de la entidad'''
        s = f'''{self.name}:
EC: {self.curve}
G: {self.generator_point}
Private Key: {self.private_key}
Private Point: {self.private_point}
'''
        return s

    def descifrar(self, ciphered_msg):
        '''Descifra un conjunto de parejas de puntos (e1, e2) de una curva eliptica a un texto
        plano legible humanamente'''

        if not ciphered_msg:
            return ""

        pt = ""
        for e1_char, e2_char in ciphered_msg:
            e1 = self.table[e1_char]
            e2 = self.table[e2_char]

            # P = e2 - (alpha(e1) + alpha(B1) + Be)
            temp1 = self.curve.mult(self.private_key, e1)
            temp2 = self.curve.mult(self.private_key, self.another_entity_public_key_1)
            sum_temp = self.curve.sum(temp1, temp2)
            sum_temp = self.curve.sum(sum_temp, self.another_entity_public_key_3)
            sum_temp = self.curve.inv(sum_temp)

            P = self.curve.sum(e2, sum_temp)

            # Buscamos n la tabla el caracter asociado al punto P
            found = False
            for k, v in self.table.items():
                if v == P:
                    pt += k
                    found = True
                    break

            if not found:
                # en caso de que no se encuentre, sabemos por nuestra regla impuesta que es el ultimo caracter de la tabla
                pt += list(self.table.keys())[-1]

        return pt

    def cifrar(self, message):
        '''Cifra el mensaje (self.message) a puntos de la curva eliptica. Cada caracter es 
        mapeado a una pareja de puntos (e1, e2) con e1, e2 en EC.'''
        # Se usa un random para cada simbolo
        if not message:
            return []

        cipher = []
        for char in message:
            # Verificamos si el caracter esta en la tabla
            if char not in self.table:
                print("not in table")
                # Usamos un caracter fijo de la tabla para mantener consistencia
                char = list(self.table.keys())[-1]

            M = self.table[char]

            # Usamos un valor r fijo lo suficientemente grande
            r = 7654321

            # e1 = r(G)
            e1 = self.curve.mult(r, self.generator_point)

            # e2 = M + (beta + r)A1 - r(A2) + Ae
            temp1 = self.curve.mult(self.private_key + r, self.another_entity_public_key_1)
            temp2 = self.curve.mult(r, self.another_entity_public_key_2)
            temp2 = self.curve.inv(temp2)

            e2 = self.curve.sum(M, temp1)
            e2 = self.curve.sum(e2, temp2)
            e2 = self.curve.sum(e2, self.another_entity_public_key_3)

            # Buscamos en la tabla los caracteres asociados a e1 y e2
            e1C = None
            e2C = None
            for k, v in self.table.items():
                if e1C and e2C:
                    break
                if v == e1:
                    e1C = k
                if v == e2:
                    e2C = k


            if e1C is not None and e2C is not None:
                cipher.append((e1C, e2C))
            elif e1C is None and e2C is not None:
                last_char = list(self.table.keys())[-1]
                cipher.append((last_char,e2C))
            elif e1C is not None and e2C is None:
                last_char = list(self.table.keys())[-1]
                cipher.append((e1C,last_char))
            else:
                # en caso de que no se haya encontrado, para consistencia en el cifrado y descifrado, optamos por usar el ultimo caracter de la tabla para aquellos caracteres no encontrados.
                last_char = list(self.table.keys())[-1]
                cipher.append((last_char, last_char))

        return cipher


    def genera_llaves_publicas(self):
        '''Hace las operaciones correspondientes para generar la primera ronda de llaves
        publicas de esta entidad PK1 y PK2.'''

        # A1 = alpha(G + A)
        self.public_key_1 = self.curve.mult(self.private_key,self.curve.sum(self.generator_point,self.private_point))

        # A1 = alpha(A)
        self.public_key_2 = self.curve.mult(self.private_key,self.private_point)
        # print(f'{self.name} genera sus llaves publicas como \npk1{self.public_key_1}\tpk2{self.public_key_2}')

        # Aseguramos que ambas llaves existan
        if self.public_key_1 is None or self.public_key_2 is None:
            raise ValueError("Error al generar llaves publicas")

        return (self.public_key_1, self.public_key_2)

    def recibe_llaves_publicas(self, public_keys):
        '''Recibe la llave publica de otra entidad y las guarda. (primera ronda solo guarda 2)
        o si ya es la segunda ronda, guarda la ultima llave (pk1, pk2 y pk3 != None)'''
        # print(public_keys) puede ser que alguna llave sea None, pero lo evitaremos por
        # motivos didacticos, pero no pasa nada, sigue funcionando

        if len(public_keys) < 3:
            self.another_entity_public_key_1 = public_keys[0]
            self.another_entity_public_key_2 = public_keys[1]
            # self.another_entity_public_key_1, self.another_entity_public_key_2 = public_keys[:2]
        else:
            self.another_entity_public_key_3 = public_keys[2]

    def final_keys(self):
        '''Genera la ultima llave publica, en combinacion con otra llave publica de otra entidad
        Regresa las 3 llaves publicas de esta entidad.'''

        if self.another_entity_public_key_2 is None:
            raise ValueError("Se necesita que Bob te haya pasado la llave publica B2")

        self.public_key_3 = self.curve.mult(self.private_key,self.another_entity_public_key_2)
        # print(f'{self.name} crea su llave final como {self.public_key_3}')
        # print(f'Todas las llaves publicas de {self.name} son: {public_keys}\n')
        return (self.public_key_1,self.public_key_2,self.public_key_3)

