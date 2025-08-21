import random
from math import gcd, isqrt
from typing import List, Optional, Tuple

# Función que encuentra una base de factores para el logaritmo discreto
def find_factor_base(p: int) -> List[int]:
    # Función auxiliar para verificar si un número es primo
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, isqrt(n) + 1):
            if n % i == 0:
                return False
        return True

    # Establecemos un límite para la base de factores usando la longitud en bits de p
    limit = int(pow(p.bit_length() * 0.693, 1.414))  # Aproximación de la raíz de la función logarítmica
    limit = max(limit, 20)  # Aseguramos que el límite sea al menos 20
    factor_base = [n for n in range(2, limit + 1) if is_prime(n)]  # Lista de números primos hasta el límite
    max_base_size = min(20, p.bit_length() // 2)  # Tamaño máximo de la base
    return factor_base[:max_base_size]  # Limitar la base a un tamaño razonable

# Función para factorizar un número n usando la base de factores
def factorize(n: int, factor_base: List[int]) -> Optional[List[int]]:
    result = [0] * len(factor_base)  # Inicializamos el contador de exponentes para cada primo de la base
    temp = n  # Copia de n para realizar la factorización

    # Intentamos dividir n entre cada primo en la base de factores
    for i, prime in enumerate(factor_base):
        while temp % prime == 0:
            result[i] += 1  # Aumentamos el exponente del primo
            temp //= prime  # Reducimos n dividiendo por el primo

    if temp == 1:  # Si hemos llegado a 1, hemos factorado completamente n
        return result
    return None  # Si no hemos podido factorizar completamente, devolvemos None

# Función para calcular el inverso multiplicativo de un número a módulo m
def mod_inverse(a: int, m: int) -> int:
    # Algoritmo extendido de Euclides para calcular el inverso multiplicativo
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("El inverso multiplicativo no existe")  # Si no hay inverso, lanzamos una excepción
    return (x % m + m) % m  # Devolvemos el inverso multiplicativo de a módulo m

# Función para resolver un sistema de ecuaciones lineales mod p-1
def solve_linear_system(relations: List[Tuple[List[int], int]], p: int) -> Optional[List[int]]:
    n = len(relations[0][0])  # Número de incógnitas
    m = len(relations)  # Número de ecuaciones
    matrix = [[x for x in eq[0]] + [eq[1]] for eq in relations]  # Construimos la matriz aumentada

    # Realizamos una eliminación gaussiana para resolver el sistema
    for i in range(n):
        pivot_row = -1
        min_val = float('inf')
        for j in range(i, m):
            if 0 < abs(matrix[j][i]) < min_val:
                min_val = abs(matrix[j][i])
                pivot_row = j

        if pivot_row == -1:
            continue  # Si no hay pivote, continuamos con la siguiente columna

        # Intercambiamos filas si es necesario
        if pivot_row != i:
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]

        pivot = matrix[i][i]
        try:
            pivot_inv = mod_inverse(pivot, p-1)  # Calculamos el inverso del pivote mod (p-1)
            # Hacemos una eliminación hacia atrás
            for j in range(i, n + 1):
                matrix[i][j] = (matrix[i][j] * pivot_inv) % (p-1)

            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n + 1):
                        matrix[k][j] = (matrix[k][j] - factor * matrix[i][j]) % (p-1)
        except ValueError:
            continue

    # Comprobamos si el sistema tiene una solución única
    rank = sum(1 for row in matrix[:n] if any(x != 0 for x in row[:-1]))
    if rank < n:
        return None  # Si el rango es menor que el número de incógnitas, el sistema no tiene solución única

    return [row[-1] for row in matrix[:n]]  # Devolvemos la solución del sistema

# Función principal para resolver el logaritmo discreto usando cálculo de índices
def index_calculus(p: int, alpha: int, beta: int, verbose: bool = True) -> Optional[int]:
    # Comprobamos si p es primo y si alpha es un generador del grupo multiplicativo de Z_p
    if not all(p % i != 0 for i in range(2, isqrt(p) + 1)):
        raise ValueError("p debe ser primo")

    if pow(alpha, p-1, p) != 1:
        raise ValueError("alpha debe ser un generador")

    # Obtenemos la base de factores
    factor_base = find_factor_base(p)
    t = len(factor_base)  # El tamaño de la base

    if verbose:
        print(f"Base de factores S = {factor_base}")
        print(f"Tamaño de la base: {t}")

    relations = []
    exponents_used = set()  # Para evitar usar los mismos exponentes repetidamente

    if verbose:
        print("\nBuscando relaciones...")

    # Intentamos encontrar relaciones entre alpha^k y la base de factores
    max_attempts = 5000
    attempts = 0

    while len(relations) < t + 5 and attempts < max_attempts:
        k = random.randrange(1, p.bit_length() * 100)  # Elegimos un exponente aleatorio
        if k in exponents_used:
            continue  # Si ya hemos usado este exponente, lo omitimos

        exponents_used.add(k)
        power = pow(alpha, k, p)  # Calculamos alpha^k mod p

        # Intentamos factorizar power usando la base de factores
        exponents = factorize(power, factor_base)
        if exponents is not None:
            relations.append((exponents, k))  # Guardamos la relación
            if verbose:
                factorization = ' * '.join([f"{factor_base[i]}^{e}" for i, e in enumerate(exponents) if e > 0])
                print(f"Relación {len(relations)}:")
                print(f"{alpha}^{k} mod {p} = {power}")
                print(f"{factorization}")

        attempts += 1

    if len(relations) < t + 1:
        if verbose:
            print(f"\nNo se encontraron suficientes relaciones después de {max_attempts} intentos.")
        return None

    if verbose:
        print("\nResolviendo sistema de ecuaciones...")

    discrete_logs = None
    # Intentamos resolver el sistema de ecuaciones lineales
    for i in range(min(5, len(relations) - t)):
        try:
            candidate_logs = solve_linear_system(relations[i:t+i], p)
            if candidate_logs is not None:
                discrete_logs = candidate_logs
                break
        except Exception:
            continue

    if discrete_logs is None:
        if verbose:
            print("No se pudo resolver el sistema de ecuaciones")
        return None

    if verbose:
        print("\nLogaritmos discretos encontrados:")
        for i, log in enumerate(discrete_logs):
            print(f"log_{alpha}({factor_base[i]}) = {log}")

    if verbose:
        print("\nCalculando logaritmo discreto final...")

    attempts = 0
    # Ahora calculamos el logaritmo discreto de beta
    while attempts < max_attempts:
        k = random.randrange(1, p.bit_length() * 100)  # Elegimos un exponente aleatorio
        gamma = (beta * pow(alpha, k, p)) % p  # Calculamos gamma = beta * alpha^k mod p

        # Intentamos factorizar gamma usando la base de factores
        exponents = factorize(gamma, factor_base)
        if exponents is not None:
            log_sum = sum(e * l for e, l in zip(exponents, discrete_logs)) % (p-1)  # Suma ponderada de los logaritmos
            result = (log_sum - k) % (p-1)  # Calculamos el logaritmo discreto

            if pow(alpha, result, p) == beta:
                if verbose:
                    print(f"\nSolución encontrada con k = {k}")
                    print(f"β · α^{k} mod {p} = {gamma}")
                    print(f"Factorización de {gamma} = {' · '.join([f'{factor_base[i]}^{e}' for i, e in enumerate(exponents) if e > 0])}")
                    print(f"log_{alpha}({beta}) = ({' + '.join([f'{e} log_{alpha}({factor_base[i]})' for i, e in enumerate(exponents) if e > 0])} - {k}) mod {p-1} = {result}")
                return result

        attempts += 1

    if verbose:
        print(f"\nNo se encontró solución después de {max_attempts} intentos.")
    return None

# Función de prueba que se encarga de mostrar el resultado del logaritmo discreto
def test_index_calculus(p: int, alpha: int, beta: int) -> None:
    print(f"\nCalculando log_{alpha}({beta}) mod {p}")

    try:
        result = index_calculus(p, alpha, beta)

        if result is not None:
            print(f"\nResultado: log_{alpha}({beta}) ≡ {result} (mod {p-1})")
            verification = pow(alpha, result, p)
            print(f"Verificación: {alpha}^{result} mod {p} = {verification}")
            print(f"¿Es correcto? {verification == beta}")
        else:
            print("\nNo se pudo encontrar una solución.")

    except ValueError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")

# Bloque principal para ejecutar el código
if __name__ == "__main__":
    p = int(input("Ingrese el valor de p: "))  # Valor primo p
    alpha = int(input("Ingrese el valor de alpha: "))  # Generador alpha
    beta = int(input("Ingrese el valor de beta: "))  # Número cuyo logaritmo queremos calcular
    test_index_calculus(p, alpha, beta)  # Ejecutar el cálculo del logaritmo discreto