import time


class LaggedFibonacciGenerator:
    def __init__(
            self,
            j=24,
            k=55,
            m=32,
            seed = None
    ):
        # 0 < j < k
        if j < 0 or k < 0:
            raise ValueError("j and k must be non-negative integers.")
        if j >= k:
            raise ValueError("j must be less than k.")

        self.j = j
        self.k = k
        # self.m = 2**m
        self.m = pow(2, m)
        # apenas define o tamanho dos estados
        self.state = [0] * k
        self.index = 0
        # preenche o estado inicial utilizando um gerador linear congruencial
        self.seed(seed = seed)

    def seed(self, seed=None, a=1664525, c=1013904223):
        """
        Gerador Linear Congruencial para definir os valores iniciais do gerador
        """
        # se não for passada explicitamente uma seed usa o tempo atual
        if seed is None:
            seed = int(time.time())
        if seed < 0:
            raise ValueError("Seed must be a non-negative integer.")
        # iniciando o gerador
        self.state[0] = int(seed) % self.m
        for i in range(1, self.k):
            self.state[i] = (a * self.state[i - 1] + c) % self.m

    def generate(self, n=1, mode="addition"):
        """
        Gera n valores pseudo-aleatórios
        """
        # garantindo uma entrada correta
        if mode not in ["addition", "multiplication", "subtraction", "xor"]:
            raise ValueError(
                "Invalid mode. Choose from 'addition', 'multiplication', 'subtraction', or 'xor'."
            )

        if n < 1:
            raise ValueError("n must be a positive integer.")

        values = []
        for _ in range(n):
            # Additive Lagged Fibonacci Generator (ALFG)
            if mode == "addition":
                self.state[self.index] = (
                                                 self.state[(self.index - self.j) % self.k]
                                                 + self.state[(self.index - self.k) % self.k]
                                         ) % self.m
            # Multiplicative Lagged Fibonacci Generator (MLFG)
            elif mode == "multiplication":
                self.state[self.index] = (
                                                 self.state[(self.index - self.j) % self.k]
                                                 * self.state[(self.index - self.k) % self.k]
                                         ) % self.m
            # Subtractive Lagged Fibonacci Generator (SLFG)
            elif mode == "subtraction":
                self.state[self.index] = (
                                                 self.state[(self.index - self.j) % self.k]
                                                 - self.state[(self.index - self.k) % self.k]
                                         ) % self.m
            # Two-tap generalised feedback shift register (GFSR)
            elif mode == "xor":
                self.state[self.index] = (
                                                 self.state[(self.index - self.j) % self.k]
                                                 ^ self.state[(self.index - self.k) % self.k]
                                         ) % self.m
            values.append(self.state[self.index])
            self.index = (self.index + 1) % self.k

        return values

    def generate_bits(self, bits, mode="addition"):
        """
        Gera um número pseudo-aleatório de n bits
        """
        # Gerantindo entrada válida de bits
        if bits < 1:
            raise ValueError("bits must be a positive integer.")
        if bits > self.m.bit_length():
            raise ValueError("bits must be less than or equal to the bit length of m.")

        result = 0
        counter = 0
        # Gera números e pega o seus bits menos significativos
        while counter < bits:
            # Gera um novo valor
            value = self.generate(1, mode)[0]
            # Gerante que o número de bits gerado não ultrapassa o limite
            remaining_bits = bits - counter
            bits_to_take = min(remaining_bits, self.m.bit_length() - 1)
            # Move todos os bits do resultado bits_to_take vezes para a esquerda e coloca os bits menos significativos no resultado
            result = (result << bits_to_take) | (value & ((1 << bits_to_take) - 1))
            counter += bits_to_take

        return result

    def generate_randint(self, n, mode="addition"):
        """
        Gera um número aleatório de entre 0 e n-1
        """
        # gerantindo entradas válidas
        if n < 1:
            raise ValueError("n must be a positive integer.")

        # Gera números com mesmo tamanho de bits até que um seja menor do que o valor estipulado
        while True:
            value = self.generate_bits(n.bit_length())
            if value < n:
                return value
