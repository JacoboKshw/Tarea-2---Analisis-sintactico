import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ══════════════════════════════════════════════════════════
#  Tiempos reales de Bison (tomados de ./bison_parser)
# ══════════════════════════════════════════════════════════
bison_times = [
    0.000049,  # n=1  ab
    0.000067,  # n=2  aabb
    0.000062,  # n=3  aaabbb
    0.000050,  # n=4  aaaabbbb
    0.000054,  # n=5  aaaaabbbbb
    0.000070,  # n=6  aaaaaabbbbbb
    0.000097,  # n=7  aaaaaaabbbbbbb
    0.000125,  # n=8  aaaaaaaabbbbbbbb
    0.000142,  # n=9  aaaaaaaaabbbbbbbbb
    0.000156,  # n=10
    0.000171,  # n=11
    0.000190,  # n=12
    0.000201,  # n=13
    0.000215,  # n=14
    0.000221,  # n=15
    0.000245,  # n=16
    0.000256,  # n=17
]

# ══════════════════════════════════════════════════════════
#  CYK — O(n³ · |G|)
# ══════════════════════════════════════════════════════════
GRAMMAR = {
    'S': [('A', 'B'), ('A', 'T')],
    'T': [('S', 'B')],
    'A': ['a'],
    'B': ['b'],
}
START = 'S'
REPS  = 200

def cyk_parse(grammar, start, word):
    n = len(word)
    if n == 0:
        return False
    table = [[set() for _ in range(n)] for _ in range(n)]
    for i, ch in enumerate(word):
        for lhs, prods in grammar.items():
            for p in prods:
                if p == ch:
                    table[i][i].add(lhs)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for lhs, prods in grammar.items():
                    for p in prods:
                        if isinstance(p, tuple) and len(p) == 2:
                            B, C = p
                            if B in table[i][k] and C in table[k+1][j]:
                                table[i][j].add(lhs)
    return start in table[0][n - 1]

# ══════════════════════════════════════════════════════════
#  BENCHMARK CYK
# ══════════════════════════════════════════════════════════
sizes = list(range(1, 18))
words = ['a'*n + 'b'*n for n in sizes]
cyk_times = []

print(f"\n{'n':>4}  {'|w|':>4}  {'CYK ok':>6}  {'CYK (ms)':>12}  {'Bison (ms)':>12}  {'Ratio':>8}")
print("=" * 62)

for n, word in zip(sizes, words):
    t0 = time.perf_counter()
    for _ in range(REPS):
        ok = cyk_parse(GRAMMAR, START, word)
    t1 = time.perf_counter()
    t_ms = (t1 - t0) / REPS * 1000
    cyk_times.append(t_ms)

    b_ms  = bison_times[n - 1]
    ratio = t_ms / b_ms if b_ms > 0 else 0
    print(f"{n:>4}  {len(word):>4}  {str(ok):>6}  {t_ms:>12.6f}  {b_ms:>12.6f}  {ratio:>8.1f}x")

print("=" * 62)
print(f"\nPromedio CYK   : {sum(cyk_times)/len(cyk_times):.6f} ms")
print(f"Promedio Bison : {sum(bison_times)/len(bison_times):.6f} ms")
print(f"CYK es ~{sum(cyk_times)/sum(bison_times):.1f}x más lento que Bison en promedio")

# ══════════════════════════════════════════════════════════
#  GRÁFICAS
# ══════════════════════════════════════════════════════════
lens = [len(w) for w in words]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("CYK  vs  Bison LALR(1) — Comparación de Rendimiento",
             fontsize=14, fontweight='bold')

# Gráfica 1 — tiempos absolutos
ax = axes[0]
ax.plot(lens, cyk_times,   'o-', color='#e74c3c', lw=2,
        markersize=6, label='CYK  O(n³·|G|)  [Python]')
ax.plot(lens, bison_times, 's-', color='#2980b9', lw=2,
        markersize=6, label='Bison LALR(1)  O(n)  [C]')
ax.set_xlabel('Longitud de la palabra |w|')
ax.set_ylabel('Tiempo promedio (ms)')
ax.set_title('Tiempo de ejecución')
ax.legend()
ax.grid(True, alpha=0.3)

# Gráfica 2 — ratio CYK / Bison
ax2 = axes[1]
ratios = [c / b for c, b in zip(cyk_times, bison_times)]
ax2.bar(lens, ratios, color='#8e44ad', alpha=0.8, edgecolor='white')
ax2.set_xlabel('Longitud de la palabra |w|')
ax2.set_ylabel('CYK / Bison (veces más lento)')
ax2.set_title('Ratio de lentitud CYK respecto a Bison')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('cyk_vs_bison.png', dpi=150, bbox_inches='tight')
print("\nGráfica guardada: cyk_vs_bison.png")
