import hashlib

# Referencia: https://pt.w3d.community/jennyt/arbol-de-merkle-todo-lo-que-necesitas-saber-5ak5
# Funcion para calcular el hash de un dato
def calcular_hash(dato):
    return hashlib.sha256(dato.encode()).hexdigest()

# Funcion para construir el arbol de Merkle
def construir_arbol_merkle(datos):
    # Calculamos los hashes de las hojas
    hojas = [calcular_hash(dato) for dato in datos]

    # Construimos el arbol de manera recursiva
    while len(hojas) > 1:
        # Agrupamos los hashes en pares y los combinamos
        hojas = [calcular_hash(hojas[i] + hojas[i+1]) for i in range(0, len(hojas), 2)]

    # Devolvemos la raiz del arbol
    return hojas[0]

# Verificar la integridad de los datos
def verificar_integridad(datos, raiz_merkle, dato_modificado):
    # Calculamos el hash del dato modificado
    hash_modificado = calcular_hash(dato_modificado)

    # Si el hash del dato modificado es igual a la raiz del arbol de Merkle, los datos estan integros
    if hash_modificado == raiz_merkle:
        print("Los datos estan integros.")
    else:
        print("Los datos han sido modificados.")

# Ejemplo de uso
datos = ["Bitcoin", "Ethereum", "Litecoin", "Monero", "Hyperledger", "Corda", "Multichain"]
raiz_merkle = construir_arbol_merkle(datos)

print("Raiz del arbol de Merkle:", raiz_merkle)

# Supongamos que modificamos un dato
dato_modificado = "Bitcoin"
verificar_integridad(datos, raiz_merkle, dato_modificado)
