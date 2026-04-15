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
 
```sql
-- CREATE: insertar un documento
INSERT INTO usuarios VALUES {"nombre": "Ana", "edad": 25};
 
-- READ: buscar con filtro
FIND IN usuarios WHERE "edad" > 18;
 
-- UPDATE: modificar un campo con condición
UPDATE usuarios SET "edad" = 26 WHERE "nombre" == "Ana";
 
-- DELETE: eliminar con condición
DELETE FROM usuarios WHERE "activo" == FALSE;
```

---

## Segundo Punto

 - Implementacion de la gramatica en ANTLR4 y muestra de las pruebas con arbol.

---

- Ejecucion:

Generar los analizadores a partir de la gramática:
  
```bash
antlr4 NoSQL.g4
```

Compilar los archivos Java incluyendo la librería de ANTLR:
  
 ```bash
javac -cp antlr-4.13.1-complete.jar *.java
```
## Pruebas
- Para ver la jerarquía de la gramática de forma visual en una ventana:

```bash
grun NoSQL programa -gui < prueba.txt
```
- Para generar el árbol de derivación sintáctica directamente en la terminal:
```bash
grun NoSQL programa -tree < prueba.txt
```

---

## Resultado en consola:
- Arbol de derivacion

<img width="1851" height="404" alt="imagen" src="https://github.com/user-attachments/assets/41a2b28d-f216-456b-9239-e1251b1ab6f3" />

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

- Primero una gramática es LL(1) si, para cualquier no terminal que tenga múltiples producciones (como S, A o B en tu caso), los conjuntos de predicción de esas producciones son disjuntos (su intersección es vacía).

-sacamos los conjuntos First, Follow, y conjuntos de prediccion:

<img width="1186" height="550" alt="imagen" src="https://github.com/user-attachments/assets/9e6cb326-0fce-4c8e-a443-4dc9f26105dd" />

- Debes evaluar cada no terminal que tenga más de una regla o que produzca vacío (ϵ):

  No terminal S:

        S→AaAb tiene un conjunto de predicción {a}.

        S→BbBa tiene un conjunto de predicción {b}.

        Demostración: {a}∩{b}=∅. Como no hay elementos comunes, el parser puede decidir qué regla usar con solo ver el primer token.

  No terminales A y B:

        Aunque solo tienen una producción cada uno (A→ϵ y B→ϵ), sus conjuntos de predicción se calculan usando el FOLLOW de la variable cuando la regla deriva en vacío.

        Para A→ϵ, el conjunto de predicción es {a,b}.

        Para B→ϵ, el conjunto de predicción es {a,b}.

  ## Conclusion
  Dado que para cada no terminal X, las intersecciones de los conjuntos de predicción de sus producciones alternativas son vacías, se demuestra matemáticamente que la gramática es LL(1)

