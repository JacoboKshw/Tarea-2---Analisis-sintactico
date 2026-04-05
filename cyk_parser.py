import time

# ══════════════════════════════════════════════════════════
#  CYK — O(n³ · |G|)
#  Gramática en Forma Normal de Chomsky (CNF)
#  Reconoce: { a^n b^n | n >= 1 }
#
#  Producción original:   S → a b | a S b
#  Conversión a CNF:
#    S → A B | A T
#    T → S B
#    A → a
#    B → b
# ══════════════════════════════════════════════════════════

GRAMMAR = {
    'S': [('A', 'B'), ('A', 'T')],
    'T': [('S', 'B')],
    'A': ['a'],
    'B': ['b'],
}
START = 'S'

def cyk_parse(grammar, start, word):
    n = len(word)
    if n == 0:
        return False

    # tabla[i][j] = conjunto de no-terminales que derivan word[i..j]
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Paso 1 — diagonal: substrings de longitud 1
    for i, ch in enumerate(word):
        for lhs, prods in grammar.items():
            for p in prods:
                if p == ch:
                    table[i][i].add(lhs)

    # Paso 2 — longitudes 2..n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):                      # punto de corte
                for lhs, prods in grammar.items():
                    for p in prods:
                        if isinstance(p, tuple) and len(p) == 2:
                            B, C = p
                            if B in table[i][k] and C in table[k+1][j]:
                                table[i][j].add(lhs)

    return start in table[0][n - 1]


# ══════════════════════════════════════════════════════════
#  BENCHMARK
# ══════════════════════════════════════════════════════════
REPS = 200

def measure(word):
    t0 = time.perf_counter()
    for _ in range(REPS):
        result = cyk_parse(GRAMMAR, START, word)
    t1 = time.perf_counter()
    return result, (t1 - t0) / REPS * 1000   # ms promedio

if __name__ == '__main__':
    sizes = list(range(1, 18))
    words = ['a' * n + 'b' * n for n in sizes]

    print(f"{'n':>4}  {'palabra (preview)':>20}  {'acepta':>6}  {'tiempo (ms)':>12}")
    print("=" * 52)

    for n, word in zip(sizes, words):
        ok, t = measure(word)
        preview = word if len(word) <= 20 else word[:17] + '...'
        print(f"{n:>4}  {preview:>20}  {str(ok):>6}  {t:>12.6f}")
