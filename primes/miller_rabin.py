from rng.lagged_fibonacci_generator import LaggedFibonacciGenerator


def miller_rabin(n, iterations=20, bits=32) -> bool:
    # casos triviais de não primalidade
    if n < 2:
        return False
    if n != 2 and n % 2 == 0:
        return False

    # definindo valores de k e m tal que n - 1 = 2^k * m
    k = 0
    m = n - 1
    while m % 2 == 0:
        m //= 2
        k += 1

    generator = LaggedFibonacciGenerator(m=bits)
    # fazendo o teste de Miller-Rabin no nível de precisão definido pelo usuário (padrão 20)
    for _ in range(iterations):
        # gerando um valor aleatório entre 2 e n-2
        a = generator.generate_randint(n - 4) + 2
        # x = a ** m % n
        x = pow(a, m, n)

        for _ in range(k):
            # y = x ** 2 % n
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n - 1:
                return False  # composto
            x = y
        if y != 1:
            return False  # composto

    return True  # Provavelmente primo
