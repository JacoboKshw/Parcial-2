"""
Parser CYK para Calculadora

Gramática en Forma Normal de Chomsky (CNF):

  E   -> ET1 | ET2 | T
  ET1 -> E A1        (representa E + T)
  ET2 -> E A2        (representa E - T)
  A1  -> PLUS T
  A2  -> MINUS T
  T   -> TF1 | TF2 | F
  TF1 -> T B1        (representa T * F)
  TF2 -> T B2        (representa T / F)
  B1  -> TIMES F
  B2  -> DIVIDE F
  F   -> LP EP       (representa ( E ))
  EP  -> E RP
  F   -> NUMBER
"""

import time
import re
import random
import matplotlib.pyplot as plt



#  TOKENs


def tokenize(expr):
    token_re = re.compile(r'\s*(\d+\.?\d*|[+\-*/()])\s*')
    tokens = []
    for m in token_re.finditer(expr):
        tok = m.group(1)
        if re.match(r'\d', tok):
            tokens.append(('NUMBER', float(tok)))
        elif tok == '+':
            tokens.append(('PLUS', '+'))
        elif tok == '-':
            tokens.append(('MINUS', '-'))
        elif tok == '*':
            tokens.append(('TIMES', '*'))
        elif tok == '/':
            tokens.append(('DIVIDE', '/'))
        elif tok == '(':
            tokens.append(('LPAREN', '('))
        elif tok == ')':
            tokens.append(('RPAREN', ')'))
    return tokens



#  GRAMÁTICA 

# Producciones binarias: (hijo_izq, hijo_der) -> [padres posibles]
BINARY = {
    ('E',     'A1'): ['ET1'],
    ('E',     'A2'): ['ET2'],
    ('PLUS',  'T' ): ['A1'],
    ('MINUS', 'T' ): ['A2'],
    ('T',     'B1'): ['TF1'],
    ('T',     'B2'): ['TF2'],
    ('TIMES',  'F'): ['B1'],
    ('DIVIDE', 'F'): ['B2'],
    ('LP',    'EP'): ['F'],
    ('E',     'RP'): ['EP'],
}

# Producciones terminales: tipo_token -> [no-terminales que lo generan]
TERMINAL = {
    'NUMBER':  ['F', 'T', 'E'],   # F->NUMBER, T->F, E->T
    'PLUS':    ['PLUS'],
    'MINUS':   ['MINUS'],
    'TIMES':   ['TIMES'],
    'DIVIDE':  ['DIVIDE'],
    'LPAREN':  ['LP'],
    'RPAREN':  ['RP'],
}



#  ALGORITMO CYK

def cyk_parse(tokens):
    n = len(tokens)
    if n == 0:
        return False

    # tabla[i][j] = conjunto de no-terminales que derivan tokens[i..j]
    tabla = [[set() for _ in range(n)] for _ in range(n)]

    # Paso 1: inicializar diagonal con terminales
    for i, (tipo, _) in enumerate(tokens):
        tabla[i][i] = set(TERMINAL.get(tipo, []))

    # Cierre manual de unitarias
    if 'F' in tabla[i][i]:
        tabla[i][i].add('T')
        tabla[i][i].add('E')

    # Paso 2: llenar por longitudes crecientes del span
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):                   # punto de corte
                for (A, B), padres in BINARY.items():
                    if A in tabla[i][k] and B in tabla[k + 1][j]:
                        tabla[i][j].update(padres)

    return 'E' in tabla[0][n - 1]


# DEMo

def demo():
    print("   PARSER CYK — Validador de expresiones")
    print("   (escribe 'salir' para terminar)")


    while True:
        try:
            expr = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if expr.lower() in ('salir', 'exit', 'quit', ''):
            break

        tokens = tokenize(expr)
        if not tokens:
            print("  Expresión vacía.\n")
            continue

        t0 = time.perf_counter()
        valida = cyk_parse(tokens)
        elapsed = (time.perf_counter() - t0) * 1000

        print(f"  Tokens: {len(tokens)}  |  Tiempo CYK: {elapsed:.4f} ms\n")


#  BENCHMARK Y GRÁFICAS

def gen_expr(num_ops):
    """Genera una expresión aritmética con num_ops operadores."""
    ops = ['+', '-', '*']
    nums = [str(random.randint(1, 9)) for _ in range(num_ops + 1)]
    op_list = [random.choice(ops) for _ in range(num_ops)]
    parts = [nums[0]]
    for i, op in enumerate(op_list):
        parts.append(op)
        parts.append(nums[i + 1])
    return ' '.join(parts)


def benchmark(sizes, repetitions=50):
    tiempos = []
    for n_ops in sizes:
        total = 0.0
        for _ in range(repetitions):
            expr = gen_expr(n_ops)
            tokens = tokenize(expr)
            t0 = time.perf_counter()
            cyk_parse(tokens)
            total += time.perf_counter() - t0
        tiempos.append((total / repetitions) * 1000)
    return tiempos


def graficar(sizes, tiempos):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle('Parser CYK — Rendimiento', fontsize=14, fontweight='bold')
    color = '#e74c3c'

    # Gráfica 1: tiempo absoluto
    ax = axes[0]
    ax.plot(sizes, tiempos, 'o-', color=color, lw=2, ms=8)
    ax.set_xlabel('Número de operadores en la expresión')
    ax.set_ylabel('Tiempo promedio (ms)')
    ax.set_title('Tiempo de parsing (escala lineal)')
    ax.grid(True, alpha=0.3)
    for x, y in zip(sizes, tiempos):
        ax.annotate(f'{y:.3f}', (x, y), textcoords='offset points',
                    xytext=(0, 8), ha='center', fontsize=8)

    # Gráfica 2: escala logarítmica
    ax = axes[1]
    ax.semilogy(sizes, tiempos, 'o-', color=color, lw=2, ms=8)
    ax.set_xlabel('Número de operadores en la expresión')
    ax.set_ylabel('Tiempo promedio (ms) — escala log')
    ax.set_title('Tiempo de parsing (escala logarítmica)')
    ax.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('benchmark_cyk.png', dpi=150, bbox_inches='tight')
    print("\n  ✓ Gráfica guardada como 'benchmark_cyk.png'")
    plt.show()


#  MAIN

if __name__ == '__main__':
    demo()

    print("  Ejecutando benchmark CYK...")

    sizes = [2, 4, 6, 8, 10, 15, 20, 30, 40, 50]
    tiempos = benchmark(sizes, repetitions=50)

    print(f"\n{'Operadores':>12} {'Tokens aprox':>14} {'Tiempo (ms)':>12}")
    print("-" * 42)
    for s, t in zip(sizes, tiempos):
        print(f"{s:>12} {2*s+1:>14} {t:>12.4f}")

    graficar(sizes, tiempos)
