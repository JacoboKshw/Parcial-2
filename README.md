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
