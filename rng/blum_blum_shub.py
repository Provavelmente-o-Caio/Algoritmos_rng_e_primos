from math import gcd


def blum_blum_shub(p, q, seed, iterations):
    # Garante que os números são congruentes com 3 mod 4
    assert p % 4 == 3 and q % 4 == 3
    m = p * q
    # Garante que m e seed são coprimos
    assert gcd(seed, m) == 1
    # n = seed**2 % m
    n = pow(seed, 2, m)
    numbers = [n]
    for _ in range(iterations - 1):
        # n = numbers[-1] ** 2 % m
        n = pow(numbers[-1], 2, m)
        numbers.append(n)
    return numbers


def blum_blum_shub_bits(p, q, seed, bits):
    # Garante que os números são congruentes com 3 mod 4
    assert p % 4 == 3 and q % 4 == 3
    m = p * q
    # Garante que m e seed são coprimos
    assert gcd(seed, m) == 1
    # n = seed**2 % m
    n = pow(seed, 2, m)
    result = 0
    for _ in range(bits):
        # n = n**2 % m
        n = pow(n, 2, m)
        result = (result << 1) | (n & 1)
    return result


def blum_blum_shub_randint(p, q, seed, n):
    if n < 1:
        raise ValueError("n must be a positive integer.")
    while True:
        value = blum_blum_shub_bits(p, q, seed, n.bit_length())
        if value < n:
            return value
