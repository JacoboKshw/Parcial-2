"""
Parser Predictivo LL(1) para Calculadora
==========================================
Gramática (sin recursión izquierda, lista para LL(1)):

  E  -> T E'
  E' -> + T E' | - T E' | ε
  T  -> F T'
  T' -> * F T' | / F T' | ε
  F  -> ( E ) | NUMBER

El parser es recursivo descendente y evalúa la expresión
directamente mientras la analiza.
"""

import time
import re
import random
import matplotlib.pyplot as plt

#TOKENS

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


#  PARSER LL(1)

class LL1Parser:
    """
    Parser predictivo LL(1) con evaluación directa.
    Complejidad: O(n)
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ── utilidades ──────────────────────────

    def peek(self):
        """Retorna el tipo del token actual sin consumirlo."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        return 'EOF'

    def consume(self, expected=None):
        """Consume el token actual y retorna su valor."""
        if self.pos >= len(self.tokens):
            raise SyntaxError(f"Se esperaba {expected} pero se llegó al fin de la entrada")
        tipo, valor = self.tokens[self.pos]
        if expected and tipo != expected:
            raise SyntaxError(f"Se esperaba '{expected}' pero se obtuvo '{tipo}' (valor: {valor})")
        self.pos += 1
        return valor

    # reglas de la gramática

    def parse(self):
        """Punto de entrada. Retorna el valor de la expresión."""
        resultado = self.E()
        if self.peek() != 'EOF':
            raise SyntaxError(f"Token inesperado al final: {self.peek()}")
        return resultado

    def E(self):
        """E -> T E'"""
        val = self.T()
        return self.E_prima(val)

    def E_prima(self, izq):
        """E' -> + T E' | - T E' | ε"""
        if self.peek() == 'PLUS':
            self.consume('PLUS')
            der = self.T()
            return self.E_prima(izq + der)
        elif self.peek() == 'MINUS':
            self.consume('MINUS')
            der = self.T()
            return self.E_prima(izq - der)
        return izq   # ε

    def T(self):
        """T -> F T'"""
        val = self.F()
        return self.T_prima(val)

    def T_prima(self, izq):
        """T' -> * F T' | / F T' | ε"""
        if self.peek() == 'TIMES':
            self.consume('TIMES')
            der = self.F()
            return self.T_prima(izq * der)
        elif self.peek() == 'DIVIDE':
            self.consume('DIVIDE')
            der = self.F()
            if der == 0:
                raise ZeroDivisionError("División por cero")
            return self.T_prima(izq / der)
        return izq   # ε

    def F(self):
        """F -> ( E ) | NUMBER"""
        if self.peek() == 'LPAREN':
            self.consume('LPAREN')
            val = self.E()
            self.consume('RPAREN')
            return val
        elif self.peek() == 'NUMBER':
            return self.consume('NUMBER')
        else:
            raise SyntaxError(f"Token inesperado: '{self.peek()}'")


def ll1_parse(tokens):
    """Interfaz simple: parsea y evalúa los tokens."""
    parser = LL1Parser(tokens)
    return parser.parse()

#  TABLA LL(1) 

def mostrar_tabla():
    print("\n  Tabla de análisis LL(1):")
    print("  " + "-"*65)
    encabezado = f"  {'No-terminal':<10} {'NUMBER':>8} {'+':<8} {'-':<8} {'*':<8} {'/':<8} {'(':<8} {')':<6}"
    print(encabezado)
    print("  " + "-"*65)
    tabla = [
        ("E",   "T E'",  "",       "",       "",       "",       "T E'",  ""),
        ("E'",  "",      "+ T E'", "- T E'", "",       "",       "",      "ε"),
        ("T",   "F T'",  "",       "",       "",       "",       "F T'",  ""),
        ("T'",  "",      "ε",      "ε",      "* F T'", "/ F T'", "",     "ε"),
        ("F",   "NUM",   "",       "",       "",       "",       "( E )", ""),
    ]
    for fila in tabla:
        nt = fila[0]
        celdas = fila[1:]
        print(f"  {nt:<10} {celdas[0]:>8} {celdas[1]:<8} {celdas[2]:<8} "
              f"{celdas[3]:<8} {celdas[4]:<8} {celdas[5]:<8} {celdas[6]:<6}")
    print("  " + "-"*65)

#  DEMO 

def demo():
    mostrar_tabla()

    print("   PARSER LL(1) — Calculadora interactiva")
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
        try:
            resultado = ll1_parse(tokens)
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"  = {resultado:.6g}")
            print(f"  Tokens: {len(tokens)}  |  Tiempo LL(1): {elapsed:.4f} ms\n")
        except (SyntaxError, ZeroDivisionError) as e:
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"  Error: {e}")
            print(f"  Tiempo LL(1): {elapsed:.4f} ms\n")


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
            ll1_parse(tokens)
            total += time.perf_counter() - t0
        tiempos.append((total / repetitions) * 1000)
    return tiempos


def graficar(sizes, tiempos):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle('Parser LL(1) — Rendimiento', fontsize=14, fontweight='bold')
    color = '#2980b9'

    # Gráfica 1: tiempo absoluto
    ax = axes[0]
    ax.plot(sizes, tiempos, 's-', color=color, lw=2, ms=8)
    ax.set_xlabel('Número de operadores en la expresión')
    ax.set_ylabel('Tiempo promedio (ms)')
    ax.set_title('Tiempo de parsing (escala lineal)')
    ax.grid(True, alpha=0.3)
    for x, y in zip(sizes, tiempos):
        ax.annotate(f'{y:.4f}', (x, y), textcoords='offset points',
                    xytext=(0, 8), ha='center', fontsize=8)

    # Gráfica 2: crecimiento vs tamaño (linealidad)
    ax = axes[1]
    tokens_count = [2 * s + 1 for s in sizes]
    ax.plot(tokens_count, tiempos, 's-', color=color, lw=2, ms=8)
    ax.set_xlabel('Número de tokens en la expresión')
    ax.set_ylabel('Tiempo promedio (ms)')
    ax.set_title('Crecimiento lineal O(n)')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('benchmark_ll1.png', dpi=150, bbox_inches='tight')
    print("\n  ✓ Gráfica guardada como 'benchmark_ll1.png'")
    plt.show()


#  MAIN

if __name__ == '__main__':
    demo()

    print("  Ejecutando benchmark LL(1)...")

    sizes = [2, 4, 6, 8, 10, 15, 20, 30, 40, 50]
    tiempos = benchmark(sizes, repetitions=50)

    print(f"\n{'Operadores':>12} {'Tokens aprox':>14} {'Tiempo (ms)':>12}")
    print("-" * 42)
    for s, t in zip(sizes, tiempos):
        print(f"{s:>12} {2*s+1:>14} {t:>12.6f}")

    graficar(sizes, tiempos)
