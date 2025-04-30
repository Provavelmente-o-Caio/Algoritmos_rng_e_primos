import random
import time

from sympy import nextprime

from rng import blum_blum_shub
from rng.lagged_fibonacci_generator import LaggedFibonacciGenerator


def measure_time_lfg(bits):
    start = time.perf_counter()
    fib = LaggedFibonacciGenerator(m=bits)
    result = fib.generate_bits(bits)
    end = time.perf_counter()
    return end - start


def measure_time_bbs(bits):
    while True:
        p = nextprime(random.getrandbits(bits // 2))
        if p % 4 == 3:
            break
    while True:
        q = nextprime(random.getrandbits(bits // 2))
        if q % 4 == 3 and q != p:
            break
    seed = random.randrange(2, p * q)
    start = time.perf_counter()
    result = blum_blum_shub.blum_blum_shub_bits(p, q, seed, bits)
    end = time.perf_counter()
    return end - start


def rng_tester():
    bit_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

    print("Algoritmo | Tamanho do Número | Tempo para gerar")
    print("----------|-------------------|-----------------")
    for bits in bit_sizes:
        lfg_time = 0
        bbs_time = 0
        for _ in range(3):
            lfg_time += measure_time_lfg(bits)
            bbs_time += measure_time_bbs(bits)
        lfg_time /= 3
        bbs_time /= 3
        print(f"LFG       | {bits:4} bits         | {lfg_time * 1000} ms")
        print(f"BBS       | {bits:4} bits         | {bbs_time * 1000} ms")
