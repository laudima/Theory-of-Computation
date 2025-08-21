#Cifrado des 

# references: https://medium.com/@ziaullahrajpoot/data-encryption-standard-des-dc8610aafdb3


# Tabla de permutacion inicial
import hashlib


IP = [  
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

# Permuta la llave de 64 bits a 56 bits
PC1 = [
        57, 49, 41, 33, 25, 17, 9, 1,
        58, 50, 42, 34, 26, 18, 10, 2,
        59, 51, 43, 35, 27, 19, 11, 3,
        60, 52, 44, 36, 63, 55, 47, 39,
        31, 23, 15, 7, 62, 54, 46, 38,
        30, 22, 14, 6, 61, 53, 45, 37,
        29, 21, 13, 5, 28, 20, 12, 4
]

# Recorrimiento a la izquierda 
desplazamiento_izq = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
]

# Permutacion de la llave de 56 bits a 48 bits
PC2 = [
        14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32
    ]

# Tabla de expansion E-box, la tabla de 32 bits se expande a 48 bits
EBOX = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

#Tablas S - estas cajas toman 6 bits como entrada y producen 4 bits como salida
# Con ellas garantizamos no linealidad en el cifrado
S_cajas = [
    # S-box 1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S-box 2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S-box 3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S-box 4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S-box 5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S-box 6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S-box 7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S-box 8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

#Tabla P, esta tabla se ocupa para permutar los bits despues de 
# han pasado por las cajas S, aqui estan su propocito
P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

# Tabla de inversion IP 
IP_inversa = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]


#Funcion para convertir un string en binario de 64 bits 
def string_to_bin(texto):
    texto_bin = ""

    for i in texto:
        texto_char = format(ord(i), '08b')
        texto_bin += texto_char
        texto_bin = texto_bin[:64]

    # Toma los primeros 64 bits de la representacion binaria, 
    # si es menor a 64 bits, se rellena con ceros (ljust 64) 
    texto_bin = texto_bin[:64].ljust(64, '0')

    print("Texto en binario: ", texto_bin) # Para probar

    return texto_bin

#Funcion para convertir un binario en string
def bin_to_string(texto_bin):
    ascii_str = ''.join([chr(int(texto_bin[i:i+8], 2)) for i in range(0, len(texto_bin), 8)])
    return ascii_str
#Funcion para implementar la permutacion inicial en la string en binario 
def permutacion_inicial_binario(texto):
    texto_permutado = [None] * 64 # Se crea una lista de 64 elementos
    for i in range(64):
        texto_permutado[i] = texto[IP[i]-1]
    texto_permutado_str = ''.join(texto_permutado)
    return texto_permutado_str

# Representacion de la llave en binario
def llave_binaria():
    llave_original = "abcdefgh" # Llave de 8 caracteres
    llave_bin = ""

    for i in llave_original:
        llave_char = format(ord(i), '08b')
        llave_bin += llave_char
    return llave_bin

# Funcion para generar las subllaves cada ronda 
def generar_subllaves():
    llave = llave_binaria()

    pc1_llave_string = ''.join(llave[bit-1] for bit in PC1) # Permutacion de la llave de 64 bits a 56 bits

    # Dividimos los 56 bits en dos mitades
    c0 = pc1_llave_string[:28]
    d0 = pc1_llave_string[28:]
    llaves_ronda = []
    # Generamos las 16 subllaves, para cada ronda, dezplazando los bits a la izquierda
    for i in range(16):
        c0 = c0[desplazamiento_izq[i]:] + c0[:desplazamiento_izq[i]]
        d0 = d0[desplazamiento_izq[i]:] + d0[:desplazamiento_izq[i]]
        cd = c0 + d0 # Concatenamos las dos mitades

        llave_ronda = ''.join(cd[bit-1] for bit in PC2) # Permutacion de la llave de 56 bits a 48 bits

        llaves_ronda.append(llave_ronda)
    return llaves_ronda

def encriptacion(input):

    mensaje_bin = string_to_bin(input) # Convertimos el mensaje a binario

    # Inicializamos las subllaves
    subllaves = generar_subllaves()

    primera_permutacion_str = permutacion_inicial_binario(mensaje_bin) # Permutacion inicial

    # La permutacion inicial se divide en dos mitades
    l_mitad = primera_permutacion_str[:32] # L = 32 bits
    r_mitad = primera_permutacion_str[32:] # R = 32 bits

    for ronda in range(16):

        # Expandimos los 32 bits a 48 bits
        r_expandido = [r_mitad[i-1] for i in EBOX]

        r_expandido_str = ''.join(r_expandido)

        # Aplicamos la llave a la ronda actual

        llave_ronda_str = subllaves[ronda]

        # Hacemos un XOR entre la llave de la ronda y el resultado de la expansion
        # Notemos que ambas son de 48 bits
        xor_result_str = ""
        for i in range(48):
            xor_result_str += str(int(r_expandido_str[i]) ^ int(llave_ronda_str[i]))


        # Dividimos el resultado del XOR en 8 bloques de 6 bits
        bloques_seis = [xor_result_str[i:i+6] for i in range(0, 48, 6)]

        cajas_s_sustituidas = ''

        # Aplicamos las cajas S
        for i in range(8):

            # Obtenemos la fila y columna de la caja S
            fila = int(bloques_seis[i][0] + bloques_seis[i][-1], 2)
            columna = int(bloques_seis[i][1:-1], 2)

            # Buscamos el valor en la caja S
            valor_caja_s = S_cajas[i][fila][columna]

            # Convertimos el valor de la caja S a binario de 4 bits
            cajas_s_sustituidas += format(valor_caja_s, '04b')

        # Permutamos los bits despues de pasar por las cajas S
        p_result = [cajas_s_sustituidas[i-1] for i in P]

        # Convertimos la primera mitad a una lista 
        l_mitad_lista = list(l_mitad)

        # Hacemos un XOR entre la primera mitad y el resultado de la permutacion
        xor_result = [str(int(l_mitad_lista[i]) ^ int(p_result[i])) for i in range(32)]

        # Convertimos el resultado del XOR a string
        xor_result_str = ''.join(xor_result)

        # Actualizamos las mitades
        l_mitad = r_mitad
        r_mitad = xor_result_str


        # Termina la ronda
        # Aqui tenemos que las dos mitades ya tienen los resultados de las 16 rondas
        # Ahora las concatenamos y aplicamos la permutacion inversa

    mensaje_cifrado = r_mitad + l_mitad

    # Aplicamos la permutacion inversa
    mensaje_cifrado_permutado = [mensaje_cifrado[IP_inversa[i]-1] for i in range(64)]

    # Convertimos el mensaje cifrado a string
    mensaje_cifrado_str = ''.join(mensaje_cifrado_permutado)

    print("Mensaje cifrado: ", mensaje_cifrado_str, len(mensaje_cifrado_str))

    # Convertimos el mensaje cifrado a ASCII
    mensaje_cifrado_ascii = bin_to_string(mensaje_cifrado_str)

    print("Mensaje cifrado en ASCII: ", mensaje_cifrado_ascii)

    return mensaje_cifrado_ascii
    
def desencriptacion(mensaje_cifrado):

    # Inicializamos las subllaves
    subllaves = generar_subllaves()

    # Aplicamos la permutacion inicial
    ip_result_str = permutacion_inicial_binario(mensaje_cifrado)

    # Dividimos el resultado de la permutacion inicial en dos mitades
    l_mitad = ip_result_str[:32]
    r_mitad = ip_result_str[32:]

    for ronda in range(16):
            
        # Expandimos los 32 bits a 48 bits
        r_expandido = [r_mitad[i-1] for i in EBOX]

        r_expandido_str = ''.join(r_expandido) # Convertimos a string

        # Aplicamos la llave a la ronda actual
        llave_ronda_str = subllaves[15 - ronda]

        # Hacemos un XOR entre la llave de la ronda y el resultado de la expansion
        # Notemos que ambas son de 48 bits
        xor_result_str = ""
        for i in range(48):
            xor_result_str += str(int(r_expandido_str[i]) ^ int(llave_ronda_str[i]))

        # Dividimos el resultado del XOR en 8 bloques de 6 bits
        bloques_seis = [xor_result_str[i:i+6] for i in range(0, 48, 6)]

        cajas_s_sustituidas = ''

        # Aplicamos las cajas S
        for i in range(8):

            # Obtenemos la fila y columna de la caja S
            fila = int(bloques_seis[i][0] + bloques_seis[i][-1], 2)
            columna = int(bloques_seis[i][1:-1], 2)

            # Buscamos el valor en la caja S
            valor_caja_s = S_cajas[i][fila][columna]

            # Convertimos el valor de la caja S a binario de 4 bits
            cajas_s_sustituidas += format(valor_caja_s, '04b')

        p_result = [cajas_s_sustituidas[i-1] for i in P]

        # Permutamos los bits despues de pasar por las cajas S
        p_result_str = ''.join(p_result)

        # Convertimos la primera mitad a una lista 
        l_mitad_lista = list(l_mitad)

        # Hacemos un XOR entre la primera mitad y el resultado de la permutacion
        xor_result = [str(int(l_mitad_lista[i]) ^ int(p_result_str[i])) for i in range(32)]

        # Convertimos el resultado del XOR a string
        xor_result_str = ''.join(xor_result)

        # Actualizamos las mitades 
        l_mitad = r_mitad
        r_mitad = xor_result_str

    # Aqui tenemos que las dos mitades ya tienen los resultados de las 16 rondas
    # Ahora las concatenamos y aplicamos la permutacion inversa

    mensaje_descifrado = r_mitad + l_mitad

    # Aplicamos la permutacion inversa

    mensaje_descifrado_permutado = [mensaje_descifrado[IP_inversa[i]-1] for i in range(64)]

    # Convertimos el mensaje descifrado a string

    mensaje_descifrado_str = ''.join(mensaje_descifrado_permutado)

    mensaje_descifrado_ascii = bin_to_string(mensaje_descifrado_str)

    print("Mensaje descifrado: ", mensaje_descifrado_ascii)

    return mensaje_descifrado_ascii

# Pruebas

mensaje = "lunes"

mensaje_cifrado = encriptacion(mensaje)

mensaje_cifrado_bin = string_to_bin(mensaje_cifrado)

mensaje_descifrado = desencriptacion(mensaje_cifrado_bin)

#Output
# Texto en binario:  0110110001110101011011100110010101110011000000000000000000000000
# Mensaje cifrado:  1111101100011000011111111001001101101000001010111011010001010111 64
# Mensaje cifrado en ASCII:  û↑h+´W
# Texto en binario:  1111101100011000011111111001001101101000001010111011010001010111
# Mensaje descifrado:  lunes


# Crea la llave de esta manera 

"""
Una manera de usar la curva eliptica para cifrar el mensaje es utilizando el punto $P = (x, y)$. Despues 
se toman las coordenadas $( x )$ e $( y )$ y se concatenan para formar una cadena binaria. Luego, podemos aplicar
una función hash (como $SHA-256$) para obtener una llave de longitud adecuada para DES ($56$ bits).
"""

def llave_binaria_punto(x, y):
    x_str = format(x, '08b')
    y_str = format(y, '08b')
    llave = x_str + y_str
    return llave
def hash_llave(llave):
    llave_hash = hashlib.sha256(llave.encode()).digest()
    # Toma los primeros 56 bits de la llave hash
    llave_hash = llave_hash[:7]
    return llave_hash

# Pruebas
llave_binaria = llave_binaria_punto(2, 21)
llave_hash = hash_llave(llave_binaria)
print("Llave binaria: ", llave_binaria)
print("Llave hash: ", llave_hash)
