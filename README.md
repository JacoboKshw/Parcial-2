# Parcial-2

## Primer punto
- Diseño de gramatica que permita hacer las operaciones en CRUD en una base de datos

## Descripción de las reglas
 
| Regla | Descripción |
|---|---|
| `<programa>` | Secuencia de una o más sentencias separadas por `;` |
| `<sentencia>` | Una operación CRUD |
| `<insertar>` | Inserta un documento en una colección |
| `<buscar>` | Busca documentos en una colección, con filtro opcional |
| `<actualizar>` | Modifica un campo de documentos en una colección |
| `<eliminar>` | Elimina documentos de una colección con filtro opcional |
| `<documento>` | Estructura `{ clave: valor, ... }` |
| `<campo>` | Par `clave: valor` dentro de un documento |
| `<asignacion>` | Asignación `clave = valor` usada en UPDATE |
| `<filtro>` | Condición de comparación para WHERE |
| `<op>` | Operador de comparación: `==`, `!=`, `<`, `>` |
| `<valor>` | Tipos de datos soportados: cadena, número, booleano o nulo |
 
---
 
## Ejemplos de sentencias válidas
 
```
-- CREATE
INSERT INTO usuarios VALUES {"nombre": "Ana", "edad": 25};
 
-- READ
FIND IN usuarios WHERE "edad" > 18;
 
-- UPDATE
UPDATE usuarios SET "edad" = 26 WHERE "nombre" == "Ana";
 
-- DELETE
DELETE FROM usuarios WHERE "activo" == FALSE;
```

---

## Segundo Punto

 - Implementacion de la gramatica en ANTLR4 y muestra de las pruebas con arbol.

---

- Ejecucion:

Generar los analizadores a partir de la gramática:
  
```bash
antlr4 Punto1.g4
```

Compilar los archivos Java incluyendo la librería de ANTLR:
  
 ```bash
javac -cp antlr-4.13.1-complete.jar *.java
```
## Pruebas
- Para ver la jerarquía de la gramática de forma visual en una ventana:

```bash
grun Punto1 programa -gui < prueba.txt
```
- Para generar el árbol de derivación sintáctica directamente en la terminal:
```bash
grun Punto1 programa -tree < prueba.txt
```

---

## Resultado en consola:
- Arbol de derivacion de forma visual
 <img width="1858" height="386" alt="imagen" src="https://github.com/user-attachments/assets/aac7d1d5-aebd-438d-a382-7df36e2f6879" />

- Arbol de derivacion por consola
  <img width="1859" height="125" alt="imagen" src="https://github.com/user-attachments/assets/ca307016-167c-4b39-83df-4cd44419fba9" />


árbol de derivación sintáctica  generado por la herramienta ANTLR4 tras procesar un archivo de prueba con la gramática. En ella se observa cómo el analizador descompone jerárquicamente las sentencias CRUD —INSERT, FIND, UPDATE y DELETE— en sus componentes mínimos (tokens), validando que la estructura de los comandos, como los filtros WHERE y la definición de documentos {clave: valor}, cumple estrictamente con las reglas definidas en la gramática.

---

## Tercer Punto

- Desmostrar que la gramatica es LL(1).

  
```
S A a A b
S B b B a
A ε
B ε
```

- Primero una gramática es LL(1) si, para cualquier no terminal que tenga múltiples producciones (, los conjuntos de predicción de esas producciones son disjuntos (su intersección es vacía).

-sacamos los conjuntos First, Follow, y conjuntos de prediccion:

<img width="1186" height="550" alt="imagen" src="https://github.com/user-attachments/assets/9e6cb326-0fce-4c8e-a443-4dc9f26105dd" />

- Toca evaluar cada no terminal que tenga más de una regla o que produzca vacío (ϵ):

  No terminal S:

        S→AaAb tiene un conjunto de predicción {a}.

        S→BbBa tiene un conjunto de predicción {b}.

        Demostración: {a}∩{b}=∅. Como no hay elementos comunes, el parser puede decidir qué regla usar con solo ver el primer token.

  No terminales A y B:

        Aunque solo tienen una producción cada uno (A→ϵ y B→ϵ), sus conjuntos de predicción se calculan usando el FOLLOW de la variable cuando la regla deriva en vacío.

        Para A→ϵ, el conjunto de predicción es {a,b}.

        Para B→ϵ, el conjunto de predicción es {a,b}.

  ## Conclusion
  Dado que para cada no terminal X, las intersecciones de los conjuntos de predicción de sus producciones alternativas son vacías, se demuestra que la gramática es LL(1)

---
## Cuarto Punto

-Comparacion entre parser CYK y parser LL(1),midiendo los tiempos de ejecución para expresiones con diferentes cantidades de operadores. Los resultados, documentados en gráficas de escala lineal y logarítmica.

## Ejecucion
 - Parser CYK
```bash
python3 cyl_parser.py
```

-Parser LL(1)
```bash
python3 ll1_parser.py
```

## Resultados
Para evaluar el desempeño de ambos algoritmos, se hicieron pruebas automáticas que consistió en generar expresiones aritméticas, variando el número de operadores en un rango de 2 a 50, estos fueron los resultados:

- Parser CYK
  <img width="1205" height="408" alt="imagen" src="https://github.com/user-attachments/assets/856b3458-e2ee-424b-b799-1791e3df30c9" />

  <img width="1934" height="741" alt="benchmark_cyk" src="https://github.com/user-attachments/assets/bbe8c55e-d35e-4518-ba33-81873b6f13bf" />


- Parser LL(1)
  <img width="1154" height="653" alt="imagen" src="https://github.com/user-attachments/assets/e3acae6e-d344-44a4-b07f-2043f5ea5029" />

  <img width="1934" height="741" alt="benchmark_ll1" src="https://github.com/user-attachments/assets/9c48d48e-40af-44f7-a2cd-a03d2885da97" />

## Conclusion
Al comparar el rendimiento de ambos algoritmos, se evidencia que el parser LL(1) es drásticamente más eficiente que el CYK, ya que el primero presenta un crecimiento de tiempo lineal O(n) frente al crecimiento polinomial O(n3) del segundo. Los datos de las pruebas muestran que para una expresión de 50 operadores, el algoritmo CYK requiere 63.570 ms para procesar la cadena, mientras que el parser predictivo lo resuelve en apenas 0.0283 ms, siendo miles de veces más rápido y eficiente.


---
## Quinto Punto
- Calculadora booleana en YACC y expliclar como funciona el analizador sintactico.

La calculadora fue implementada utilizando un analizador de tipo LALR(1) a través de la librería PLY. Este enfoque permite que el programa evalúe las expresiones booleanas con una complejidad temporal de O(n), donde n es el número de tokens.

## Dependencias
Se necesita instalar PLY
```bash
pip install ply
```

## Ejecucion:
```bash
python3 CalculadoraBool.py
```

## Pruebas
<img width="1477" height="562" alt="imagen" src="https://github.com/user-attachments/assets/05dba2a1-0339-4fb7-931e-8042a53453f3" />


## Conclusion

El analizador sintáctico del punto 5 funciona bajo el algoritmo LALR(1), el cual procesa las expresiones booleanas de manera eficiente al realizar un solo recorrido de izquierda a derecha sobre la entrada. Este sistema utiliza una tabla de estados precalculada y almacenada en el archivo parsetab.py que le permite decidir instantáneamente si debe agrupar términos o avanzar al siguiente símbolo, garantizando que el tiempo de respuesta sea siempre proporcional a la longitud de la expresión.
