grammar NoSQL;

programa : sentencia (';' sentencia)* ';'? EOF ;

sentencia : insertar | buscar | actualizar | eliminar ;

// CRUD
insertar   : 'INSERT' 'INTO' ID 'VALUES' documento ;
buscar     : 'FIND' 'IN' ID ('WHERE' filtro)? ;
actualizar : 'UPDATE' ID 'SET' asignacion ('WHERE' filtro)? ;
eliminar   : 'DELETE' 'FROM' ID ('WHERE' filtro)? ;

documento : '{' campo (',' campo)* '}' ;
campo     : CADENA ':' valor ;

asignacion : CADENA '=' valor ;

filtro    : CADENA op valor ;
op        : '==' | '!=' | '<' | '>' ;

valor : CADENA | NUMERO | 'TRUE' | 'FALSE' | 'NULL' ;

// Tokens
ID     : [a-zA-Z_][a-zA-Z0-9_]* ;
CADENA : '"' (~["\r\n])* '"' ;
NUMERO : '-'? [0-9]+ ('.' [0-9]+)? ;
WS     : [ \t\r\n]+ -> skip ;
