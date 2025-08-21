import random
from math import gcd, isqrt
from typing import List, Optional, Tuple

# Function to factorize a number n using the factor base
def factorize(n: int, factor_base: List[int]) -> Optional[List[int]]:
    result = [0] * len(factor_base)  # Initialize exponents counter for each prime in the base
    temp = n  # Copy of n to factorize

    for i, prime in enumerate(factor_base):
        while temp % prime == 0:
            result[i] += 1  # Increment the exponent for the prime
            temp //= prime  # Divide n by the prime

    if temp == 1:  # If we've completely factorized n
        return result
    return None  # If not fully factorizable, return None

# Function to calculate the modular inverse of a number a modulo m
def mod_inverse(a: int, m: int) -> int:
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
# Step 1: Find a factor base
def find_factor_base(p: int) -> List[int]:
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, isqrt(n) + 1):
            if n % i == 0:
                return False
        return True

    limit = max(int(pow(p.bit_length() * 0.693, 1.414)), 20)
    factor_base = [n for n in range(2, limit + 1) if is_prime(n)]
    max_base_size = min(20, p.bit_length() // 2)
    return factor_base[:max_base_size]

# Step 2: Find relations
def find_relations(alpha: int, p: int, factor_base: List[int], verbose: bool = True) -> List[Tuple[List[int], int]]:
    relations = []
    exponents_used = set()
    max_attempts = 5000
    attempts = 0

    while len(relations) < len(factor_base) + 5 and attempts < max_attempts:
        k = random.randrange(1, p.bit_length() * 100)
        if k in exponents_used:
            continue
        exponents_used.add(k)

        power = pow(alpha, k, p)
        exponents = factorize(power, factor_base)

        if exponents is not None:
            relations.append((exponents, k))
            if verbose:
                factorization = ' * '.join([f"{factor_base[i]}^{e}" for i, e in enumerate(exponents) if e > 0])
                print(f"Relation {len(relations)}: {alpha}^{k} mod {p} = {power}, {factorization}")

        attempts += 1

    if len(relations) < len(factor_base) + 1:
        raise ValueError(f"Insufficient relations found after {max_attempts} attempts.")

    return relations

# Funcion para resolver un sistema de ecuaciones lineales mod p-1
def solve_linear_system(relations: List[Tuple[List[int], int]], p: int) -> Optional[List[int]]:
    n = len(relations[0][0])  # Numero de incognitas
    m = len(relations)  # Numero de ecuaciones
    matrix = [[x for x in eq[0]] + [eq[1]] for eq in relations]  # Construimos la matriz aumentada

    # Realizamos una eliminacion gaussiana para resolver el sistema
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
            # Hacemos una eliminacion hacia atras
            for j in range(i, n + 1):
                matrix[i][j] = (matrix[i][j] * pivot_inv) % (p-1)

            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n + 1):
                        matrix[k][j] = (matrix[k][j] - factor * matrix[i][j]) % (p-1)
        except ValueError:
            continue

    # Comprobamos si el sistema tiene una solucion unica
    rank = sum(1 for row in matrix[:n] if any(x != 0 for x in row[:-1]))
    if rank < n:
        return None  # Si el rango es menor que el numero de incognitas, el sistema no tiene solucion unica

    return [row[-1] for row in matrix[:n]]  # Devolvemos la solucion del sistema

#Step 3: Compute the discrete logs 
def compute_discrete_log(p: int, alpha: int, beta: int, factor_base: List[int],relations) -> Optional[int]:
    discrete_logs = None
    # Intentamos resolver el sistema de ecuaciones lineales
    for i in range(min(5, len(relations) - len(factor_base))):
        try:
            candidate_logs = solve_linear_system(relations[i:t+i], p)
            if candidate_logs is not None:
                discrete_logs = candidate_logs
                break
        except Exception:
            continue

    return discrete_logs


# Step 4: Compute the discrete logarithm
def calculate(p: int, alpha: int, beta: int, factor_base: List[int], discrete_logs: List[int]) -> Optional[int]:
    max_attempts = 5000
    attempts = 0

    while attempts < max_attempts:
        k = random.randrange(1, p.bit_length() * 100)
        gamma = (beta * pow(alpha, k, p)) % p
        exponents = factorize(gamma, factor_base)

        if exponents is not None:
            log_sum = sum(e * l for e, l in zip(exponents, discrete_logs)) % (p - 1)
            result = (log_sum - k) % (p - 1)

            if pow(alpha, result, p) == beta:
                return result

        attempts += 1

    raise ValueError("Failed to compute discrete logarithm.")

# Main function
def index_calculus(p: int, alpha: int, beta: int, verbose: bool = True) -> Optional[int]:
    factor_base = find_factor_base(p)
    relations = find_relations(alpha, p, factor_base, verbose)
    discrete_logs = compute_discrete_log(p, alpha, beta, factor_base, relations)
    return calculate(p, alpha, beta, factor_base, discrete_logs)

# Testing block
if __name__ == "__main__":
    p = 1217
    alpha = 3
    beta = 37
    try:
        result = index_calculus(p, alpha, beta)
        print(f"\nResult: log_{alpha}({beta}) = {result} (mod {p-1})")
    except Exception as e:
        print(f"\nError: {e}")

# Resultado: log_3(37) = 588 (mod 1216) 
