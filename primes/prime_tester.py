import os
import time

from primes.fermat import fermat
from primes.miller_rabin import miller_rabin
from rng.lagged_fibonacci_generator import LaggedFibonacciGenerator


def measure_time_fermat(bits):
    """
    Mede o tempo de execução do teste de primalidade de Fermat
    """
    result = False
    start = time.perf_counter()
    # iniciando cada gerador com seed diferente
    seed = int.from_bytes(os.urandom(16), "big")
    generator = LaggedFibonacciGenerator(m=bits, seed=seed)
    while not result:
        number = generator.generate_bits(bits)
        number |= 1 << (bits - 1)  # Garante o tamanho
        result = fermat(number, bits=bits)
    end = time.perf_counter()
    return end - start, number


def measure_time_miller_rabin(bits):
    """
    Mede o tempo de execução do teste de primalidade de Miller-Rabin
    """
    result = False
    start = time.perf_counter()
    # iniciando cada gerador com seed diferente
    seed = int.from_bytes(os.urandom(16), "big")
    generator = LaggedFibonacciGenerator(m=bits, seed=seed)
    while not result:
        number = generator.generate_bits(bits)
        number |= 1 << (bits - 1)  # Garante o tamanho
        result = miller_rabin(number, bits=bits)
    end = time.perf_counter()
    return end - start, number


def prime_tester():
    bit_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

    # valores sendo gerados pelo lfg para maior eficiência
    print(
        "Algoritmo    |   Tamanho do Número   | Número Primo Gerado  | Tempo para gerar"
    )
    print(
        "-------------|-----------------------|----------------------|-----------------"
    )
    for bits in bit_sizes:
        fermat_time, fermat_num = measure_time_fermat(bits)
        miller_rabin_time, miller_rabin_num = measure_time_miller_rabin(bits)
        print(
            f"Fermat       | {bits:4} bits             | {fermat_num} | {fermat_time * 1000} ms"
        )
        print(
            f"Miller-Rabin | {bits:4} bits             | {miller_rabin_num} | {miller_rabin_time * 1000} ms"
        )


def pseudoprimes():
    pseudoprimes = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341]
    print("Algoritmo    |   Número     |   Resposta")
    print("-------------|--------------|-----------")
    for pseudoprime in pseudoprimes:
        print(
            f"Fermat       |    {pseudoprime:5}     |   {fermat(pseudoprime, bits=pseudoprime.bit_length())}"
        )
        print(
            f"Miller-Rabin |    {pseudoprime:5}     |   {miller_rabin(pseudoprime, bits=pseudoprime.bit_length())}"
        )
