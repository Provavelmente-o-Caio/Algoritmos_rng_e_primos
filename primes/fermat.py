from math import gcd

from rng.lagged_fibonacci_generator import LaggedFibonacciGenerator


def fermat(n, k=20, bits=32):
    # tratando dos casos triviais
    if n < 2:
        return False
    if n == 2:
        return True
    if n != 2 and n % 2 == 0:
        return False

    # criando o gerador de números
    lfg = LaggedFibonacciGenerator(m=bits)

    # realizando o teste de Fermat repetidamente para aumentar a confiança
    for _ in range(k):
        a = lfg.generate_randint(n - 4) + 2
        while gcd(a, n) != 1:
            a = lfg.generate_randint(n - 4) + 2

        # a ** (n-1) % n
        if pow(a, n - 1, n) != 1:
            return False

    return True
