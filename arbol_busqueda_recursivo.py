from typing import Optional, List


class Nodo:
    def __init__(self, valor: int):
        """
        Crea un nodo del árbol binario con un valor entero (valor).
        El nodo puede tener hijos izquierdo y derecho.
        """
        self.valor = valor
        self.izquierda: Optional[Nodo] = None
        self.derecha: Optional[Nodo] = None


class ArbolBusqueda:
    """
    Árbol binario de búsqueda (BST) construido a partir de una lista.
    Este árbol se puede usar para hallar el ancestro común más bajo (amcb) entre dos nodos.
    """

    def __init__(self, lista: List[Optional[int]]):
        """
        Construye el árbol binario utilizando el método recursivo construir_arbol.
        La lista debe representar el árbol en orden por niveles (level-order), y los
        valores 'None' indican ausencia de nodo en esa posición.
        """
        self.lista = lista
        self.raiz = self.construir_arbol_con_lista(0)

    def construir_arbol_con_lista(self, indice: int) -> Optional[Nodo]:
        """
        Construye el árbol binario de forma recursiva a partir de una lista que contiene
        los valores de cada nodo, siguiendo el orden por niveles.

        Este método funciona gracias a una regla muy útil:
        - Si un nodo está en la posición i de la lista:
          - Su hijo izquierdo está en la posición 2*i + 1
          - Su hijo derecho está en la posición 2*i + 2

        Esto permite que, sin usar estructuras adicionales como colas o pilas, podamos construir el árbol directamente recorriendo la lista (como pide el ejercicio) como si fuese un árbol completo.

        Args:
            indice (int): Posición actual en la lista desde donde se construye el nodo.

        Returns:
            Nodo: Nodo raíz del subárbol correspondiente a ese índice, o None si la posición está fuera de la lista o representa un nodo vacío.
        """
        # Si nos pasamos del final de la lista o encontramos un None, no hay nodo que insertar
        if indice >= len(self.lista) or self.lista[indice] is None:
            return None

        # Creamos el nodo con el valor actual
        nodo = Nodo(self.lista[indice])

        # Aplicamos la regla de índice: hijo izquierdo está en 2*i+1, derecho en 2*i+2
        nodo.izquierda = self.construir_arbol_con_lista(2 * indice + 1)
        nodo.derecha = self.construir_arbol_con_lista(2 * indice + 2)

        return nodo


# Nótemos: AMCB -> Ancestro Común Más Bajo


class ACMB_dict_memoizacion:
    """
    Estrategia de dict_memoización (Top-Down) para encontrar el Ancestro Común Más Bajo (ACMB).

    Este enfoque se basa en recorrer el árbol desde la raíz hacia abajo (de arriba hacia abajo).
    Se va dividiendo el problema en subproblemas y se guardan los resultados parciales en un
    diccionario (dict_memo) para evitar recalcularlos si se vuelven a necesitar.
    """

    def __init__(self):
        """
        Inicializa el diccionario dict_memo, que se usará para guardar resultados de subproblemas.
        La clave es una tupla que identifica un nodo y los dos valores de búsqueda.
        """
        self.dict_memo = {}

    def encontrar_amcb(self, nodo: Optional[Nodo], p: int, q: int) -> Optional[Nodo]:
        """
        Encuentra el Ancestro Común Más Bajo (ACMB) de los valores p y q utilizando dict_memoización.

        Se explora el árbol desde la raíz tomando decisiones basadas en las propiedades de un
        Árbol Binario de Búsqueda (ABB). Si ambos valores están por debajo del nodo actual,
        se baja por la izquierda. Si están por encima, se baja por la derecha. Si se dividen,
        el nodo actual es el ACMB.

        Si ya se resolvió el problema para una combinación específica de nodo y valores, se
        recupera de dict_memo en lugar de repetir la búsqueda.

        Args:
            nodo (Optional[Nodo]): nodo actual donde se inicia o continúa la búsqueda
            p (int): valor del primer nodo a buscar
            q (int): valor del segundo nodo a buscar

        Returns:
            Optional[Nodo]: el nodo que representa el ancestro común más bajo, o None si no se encuentra
        """
        # Creamos una clave única con la dirección del nodo actual y los valores ordenados
        clave = (id(nodo), min(p, q), max(p, q))

        # Si esta búsqueda ya se hizo antes, devolvemos el resultado guardado
        if clave in self.dict_memo:
            return self.dict_memo[clave]

        # Si el nodo actual no existe, no hay ACMB en esta rama
        if nodo is None:
            return None

        # Si ambos valores son menores, debemos buscar en el subárbol izquierdo
        if p < nodo.valor and q < nodo.valor:
            resultado = self.encontrar_amcb(nodo.izquierda, p, q)

        # Si ambos valores son mayores, debemos buscar en el subárbol derecho
        elif p > nodo.valor and q > nodo.valor:
            resultado = self.encontrar_amcb(nodo.derecha, p, q)

        # Si uno está a la izquierda y otro a la derecha (o uno es igual al actual), este nodo es el ACMB
        else:
            resultado = nodo

        # Guardamos el resultado en dict_memo antes de retornarlo
        self.dict_memo[clave] = resultado
        return resultado


# Nótemos: AMCB -> Ancestro Común Más Bajo


class ACMB_Constructivo:
    """
    Este método se basa en recorrer todo el árbol desde las hojas hasta la raíz.
    Busca por separado cada uno de los nodos y cuando encuentra que uno está en un lado
    y el otro en el otro, determina que ese nodo es el ancestro común más bajo.
    """

    def encontrar_amcb(self, nodo: Optional[Nodo], p: int, q: int) -> Optional[Nodo]:
        """
        Recorre el árbol completo buscando ambos nodos. Al encontrar que están en
        ramas distintas, retorna el nodo actual como el ancestro común más bajo.
        """
        if nodo is None:
            return None

        if nodo.valor == p or nodo.valor == q:
            return nodo

        izquierda = self.encontrar_amcb(nodo.izquierda, p, q)
        derecha = self.encontrar_amcb(nodo.derecha, p, q)

        if izquierda and derecha:
            return nodo

        return izquierda if izquierda else derecha


class ACMB_FuerzaBruta:
    """
    Esta solución obtiene el camino desde la raíz hasta cada nodo
    y luego compara los caminos para encontrar el último punto en común.
    """

    def encontrar_camino(self, nodo: Optional[Nodo], valor: int) -> List[Nodo]:
        """
        Devuelve el camino desde la raíz hasta el nodo que contiene el valor indicado.
        Si no se encuentra el valor, retorna una lista vacía.
        """
        if nodo is None:
            return []

        if nodo.valor == valor:
            return [nodo]

        # Decidimos por cuál rama bajar
        rama = (
            self.encontrar_camino(nodo.izquierda, valor)
            if valor < nodo.valor
            else self.encontrar_camino(nodo.derecha, valor)
        )

        # Si lo encontramos más abajo, lo agregamos al inicio del camino
        if rama:
            return [nodo] + rama

        return []

    def encontrar_amcb(self, raiz: Nodo, p: int, q: int) -> Optional[Nodo]:
        """
        Busca el camino desde la raíz hasta cada uno de los valores,
        y devuelve el último nodo donde los caminos coinciden.
        """
        ruta_p = self.encontrar_camino(raiz, p)
        ruta_q = self.encontrar_camino(raiz, q)

        nodo_comun = None

        # Recorremos ambos caminos a la vez, paso por paso
        for a, b in zip(ruta_p, ruta_q):
            if a.valor == b.valor:
                nodo_comun = a  # seguimos actualizando mientras coincidan
            else:
                break  # en cuanto difieren, nos detenemos

        return nodo_comun


# Ejemplo de prueba
if __name__ == "__main__":
    # Creamos la instancia con una lista de valores que representa el árbol

    entrada = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
    p = 2
    q = 8

    arbol = ArbolBusqueda(entrada)

    acbm_dict_memo = ACMB_dict_memoizacion()
    acbm_construc = ACMB_Constructivo()
    acbm_fb = ACMB_FuerzaBruta()

    print("Memoizacion:", acbm_dict_memo.encontrar_amcb(arbol.raiz, p, q).valor)

    print("Constructivo:", acbm_construc.encontrar_amcb(arbol.raiz, p, q).valor)

    print("Fuerza Bruta:", acbm_fb.encontrar_amcb(arbol.raiz, p, q).valor)
