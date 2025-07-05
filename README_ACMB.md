# Análisis de Complejidad Computacional – Ancestro Común Más Bajo (ACMB)

Resolución de preguntas.
---

## d. ¿Cuál es la diferencia en el código?

###  Memoización (Top-Down)

Este enfoque parte desde la raíz y desciende en el árbol, guardando resultados ya calculados en un diccionario para evitar recalcularlos en futuras llamadas.

```python
clave = (id(nodo), min(p, q), max(p, q))
if clave in self.dict_memo:
    return self.dict_memo[clave]
```

**Clave del rendimiento**: El uso de `dict_memo` evita búsquedas duplicadas y mejora el rendimiento cuando se hacen múltiples consultas.

---

###  Enfoque Constructivo (Bottom-Up)

Este método no se basa en las propiedades del BST. Recorre todo el árbol desde las hojas, y detecta el ACMB en el momento en que un nodo contiene uno de los valores en su subárbol izquierdo y el otro en el derecho.

```python
izquierda = self.encontrar_amcb(nodo.izquierda, p, q)
derecha = self.encontrar_amcb(nodo.derecha, p, q)
```

**Clave del rendimiento**: No reutiliza ningún resultado. Se ejecuta una búsqueda completa para cada consulta, sin optimización.

---

###  Fuerza Bruta

Este método primero encuentra el camino completo desde la raíz hasta cada uno de los dos nodos, y luego compara ambos caminos para identificar el último nodo en común.

```python
ruta_p = self.encontrar_camino(raiz, p)
ruta_q = self.encontrar_camino(raiz, q)

for a, b in zip(ruta_p, ruta_q):
    if a.valor == b.valor:
        nodo_comun = a
```

**Clave del rendimiento**: Recorre el árbol dos veces completamente, y usa memoria adicional para guardar ambos caminos.

---
## Análisis Detallado de Complejidad y Recomendación

### d. Diferencias en el Código

Cada algoritmo presenta estructuras distintas según la forma en que se recorre el árbol o se almacenan resultados:

#### Fuerza Bruta
Se basa en recorrer el árbol completo dos veces para hallar el camino a cada nodo. Luego compara ambos caminos:

```python
ruta_p = self.encontrar_camino(raiz, p)
ruta_q = self.encontrar_camino(raiz, q)
```
Este doble recorrido afecta su costo computacional.

#### Constructivo (Bottom-Up)
Usa recursión postorden para explorar ambos lados del árbol simultáneamente y decidir el nodo más bajo que tenga a ambos descendientes:

```python
izquierda = self.encontrar_amcb(nodo.izquierda, p, q)
derecha = self.encontrar_amcb(nodo.derecha, p, q)
```

#### Memoización (Top-Down)
Evita cálculos repetidos almacenando soluciones previamente computadas para subárboles específicos:

```python
clave = (id(nodo), min(p, q), max(p, q))
if clave in self.dict_memo:
    return self.dict_memo[clave]
```

Esto marca una diferencia importante al mejorar el rendimiento sobre árboles muy grandes o consultas repetidas.

---

### e. Diferencias en la Ejecución

| Estrategia       | Estilo de Recorrido      | Consultas repetidas | Caminos duplicados | Memoria extra |
|------------------|--------------------------|----------------------|--------------------|---------------|
| Fuerza Bruta     | Desde la raíz 2 veces    | Lento                | Sí                 | No            |
| Constructivo     | Desde hojas hacia arriba | Razonable            | No                 | No            |
| Memoización      | De arriba hacia abajo    | Rápido               | No                 | Sí (diccionario)|

---

### f. Costos Computacionales

A continuación, se exponen las fórmulas de complejidad para cada estrategia usando notación Big-O:

#### Fuerza Bruta

- Recorre dos caminos independientes: $$ O(h) + O(h) $$, donde $$ h $$ es la altura del árbol.
- Comparación de caminos: $$ O(h) $$
- **Complejidad total**:

$$
T(n) = O(h) + O(h) + O(h) = 3 \cdot O(h) = O(h)
$$

#### Constructivo

- Cada nodo del árbol se visita una sola vez en el peor caso.
- No hay comparación explícita de caminos.

$$
T(n) = O(n)
$$

#### Memoización

- Cada nodo se visita una sola vez, y los resultados se almacenan.
- La búsqueda evita repetir trabajo.

$$
T(n) = O(n) 
$$

con mejor rendimiento en múltiples consultas gracias al cache, con resultados ya almacenados en **dict_memo**


En términos de espacio:

- **Fuerza Bruta**: $$O(h)$$ por cada camino
- **Constructivo**: $$O(h)$$ por la pila de recursión
- **Memoización**: $$O(n)$$ por el diccionario `dict_memo`

---

### g. Recomendación para una Empresa de Software

La estrategia de **Memoización (Top-Down)** es altamente recomendable para entornos de producción por estas razones:

- **Escalabilidad**: Soporta árboles grandes con múltiples consultas sin recalcular.
- **Eficiencia**: La mejora de rendimiento es evidente en árboles dinámicos donde se consulta varias veces.
- **Facilidad de mantenimiento**: Es modular, limpia y fácil de entender.

Si el árbol solo se consulta una vez y es relativamente pequeño, **Constructivo** también es una opción muy eficiente y sin memoria adicional.  
**Fuerza Bruta**, aunque funcional, es la menos eficiente y no recomendado para entornos productivos donde se busca una buena relación coste/simplicidad/eficacia.

##  Análisis matemático complementario de complejidad

###  Memoización (Top-Down)

Este enfoque realiza una exploración descendente (de la raíz hacia las hojas), aprovechando la naturaleza del árbol binario de búsqueda para evitar recorrer ramas innecesarias. Pero lo más relevante es que guarda en cache (`dict_memo`) los resultados ya calculados, evitando recarlcular si se repiten.

#### Fragmento clave del código:
```python
clave = (id(nodo), min(p, q), max(p, q))
if clave in self.dict_memo:
    return self.dict_memo[clave]
```

Este fragmento engloba el ahorro computacional. Se accede al resultado ya almacenado en el diccionario sin repetir el cálculo.

#### Complejidad:

En el mejor caso (si es un BST balanceado):
$$
T(n) = O(\log n)
$$

En el peor caso (BST completamente desbalanceado):
$$
T(n) = O(n)
$$

La mejora se da especialmente cuando hay múltiples consultas. Por ejemplo, si ya se resolvió la búsqueda entre (2, 8), esa solución ya está lista para ser reutilizada.

---

###  Enfoque Constructivo (Bottom-Up)

Aquí no se almacenan resultados ni se usan propiedades especiales del árbol binario de búsqueda. Se recorre todo el árbol desde las hojas hacia arriba y se detecta el nodo en el que los caminos hacia los nodos buscados se separan.

#### Fragmento clave:
```python
izquierda = self.encontrar_amcb(nodo.izquierda, p, q)
derecha = self.encontrar_amcb(nodo.derecha, p, q)
```

Ambas ramas se exploran completamente de forma independiente.

#### Complejidad:

Cada nodo se puede visitar una vez como máximo:
$$
T(n) = O(n)
$$

Este método tiene una ejecución predecible, aunque no tan eficiente si el árbol es muy grande y se hacen múltiples consultas.

---

###  Fuerza Bruta

Este enfoque busca el camino completo desde la raíz hasta los dos nodos por separado, y luego compara ambos caminos para encontrar el último nodo en común.

#### Fragmento clave:
```python
ruta_p = self.encontrar_camino(raiz, p)
ruta_q = self.encontrar_camino(raiz, q)
```

Esto implica dos recorridos completos más una comparación paso a paso.

#### Complejidad:

Si el árbol tiene altura `h` (profundidad del nodo más profundo), entonces:

- Camino desde raíz hasta p: $$ O(h) $$
- Camino desde raíz hasta q: $$ O(h) $$
- Comparación de caminos: $$ O(h) $$

Por lo tanto:

$$
T(n) = O(h) + O(h) + O(h) = 3 \cdot O(h) = O(h)
$$

En árboles balanceados $$ h = \log n $$

Pero en el peor caso puede ser $$ O(n) $$.