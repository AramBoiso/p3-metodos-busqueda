import heapq
import matplotlib.pyplot as plt
import networkx as nx

cont = 0

class Nodo:
    def __init__(self, clave):
        global cont
        cont += 1
        self.clave = clave
        self.vecinos = {}
        self.h = cont

    def agregar_vecino(self, clave, peso=0):
        self.vecinos[clave] = peso

    def get_conexiones(self):
        return self.vecinos.keys()

    def get_peso(self, vecino):
        return self.vecinos[vecino]

    def __str__(self):
        return str(self.clave) + ' unido a ' + str([x for x in self.vecinos])

    def get_clave(self):
        return self.clave

    def set_clave(self, clave):
        self.clave = clave


class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_nodo(self, clave):
        newNodo = Nodo(clave)
        self.nodos[clave] = newNodo
        return newNodo

    def get_nodo(self, clave):
        if clave in self.nodos:
            return self.nodos[clave]
        else:
            return None

    def agregar_conexion(self, inicio, destino, peso=0):
        self.nodos[inicio].agregar_vecino(destino, peso)

    def get_nodos(self):
        return self.nodos.keys()

    def __iter__(self):
        return iter(self.nodos.values())

    def __contains__(self, n):
        return n in self.nodos

    def modificar_info(self, clave, nuevaClave):
        if clave in self.nodos:
            self.nodos[nuevaClave] = self.nodos.pop(clave)
            self.nodos[nuevaClave].set_clave(nuevaClave)
        else:
            return "No existe la clave"

    def visualizar(self):
        g = nx.Graph()
        lista_conexion = []
        for v in self:
            for w in v.get_conexiones():
                lista_conexion.append((v.get_clave(), w, v.get_peso(w)))
        g.add_weighted_edges_from(lista_conexion)
        pos = nx.spring_layout(g)
        pesos = nx.get_edge_attributes(g, "weight")
        nx.draw(g, pos)
        nx.draw_networkx_labels(g, pos)
        nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=pesos, with_labels=True)
        plt.show()

    def busqueda_anchura(self, nodoini, nodobuscar):
        visitados = {}
        for nodo in self.nodos.keys():
            visitados[nodo] = False
        cola = [nodoini]
        visitados[nodoini] = True
        while cola:
            nodoini = cola.pop(0)
            print(nodoini, end=" ")
            if nodoini == nodobuscar:
                break
            else:
                for i in self.nodos[nodoini].get_conexiones():
                    if not visitados[i]:
                        cola.append(i)
                        visitados[i] = True

    def busqueda_profundidad(self, nodoini, nodobuscar):
        visitados = []
        pila = [nodoini]
        if nodoini == nodobuscar:
            print(nodoini)
        else:
            while pila:
                actual = pila.pop()
                if actual == nodobuscar:
                    print(actual)
                    break
                elif actual not in visitados:
                    print(actual, end=" ")
                    visitados.append(actual)
                    for i in self.nodos[actual].get_conexiones():
                        if i not in visitados:
                            pila.append(i)

    def busqueda_general(self, inicio, destino):
        estados_abiertos = [inicio]
        estados_cerrados = []
        actual = estados_abiertos.pop(0)
        while estados_abiertos and (actual is not destino):
            estados_cerrados.append(actual)
            hijos = self._generar_sucesores(actual)
            hijos = self._tratar_repetidos(hijos, estados_abiertos, estados_cerrados)
            for i in range(len(hijos)):
                estados_abiertos.append(hijos[i][0].get_clave())
            actual = estados_abiertos.pop(0)
        if actual != destino:
            estados_cerrados.append(actual)
            for i in estados_cerrados:
                print(i, end=" ")
        else:
            print("No hay solucion")

    def _generar_sucesores(self, actual):
        if len(self.nodos[actual].get_conexiones()) == 0:
            return None
        else:
            hijos = []
            for sucesores in self.nodos[actual].get_conexiones():
                hijos.append((sucesores, actual))
            return hijos

    def _tratar_repetidos(self, hijos, estados_abiertos, estados_cerrados):
        if len(hijos) != 0:
            for i in range(len(hijos)):
                if hijos[i][0] in estados_abiertos or hijos[i][0] in estados_cerrados:
                    del hijos[i][0]
            return hijos
        else:
            return None

    def busqueda_informada(self, inicio, destino):
        # Basado en dijkstra
        ruta = {}
        inf = float("inf")
        distancias = {i: inf for i in self.nodos}
        visitados = {i: None for i in self.nodos}
        distancias[inicio] = 0
        nodos = visitados.copy()

        while nodos:
            nodo_actual = min(nodos, key=lambda nodo: distancias[nodo])

            if distancias[nodo_actual] == inf:
                break
            for nodo_vecino in self.nodos[nodo_actual].get_conexiones():
                ruta_alterna = distancias[nodo_actual] + self.nodos[nodo_actual].get_peso(nodo_vecino)

                if ruta_alterna < distancias[nodo_vecino]:
                    distancias[nodo_vecino] = ruta_alterna

                    visitados[nodo_vecino] = nodo_actual
            del nodos[nodo_actual]

        camino, nodo_actual = [], destino
        while visitados[nodo_actual] is not None:
            camino.insert(0, nodo_actual)
            nodo_actual = visitados[nodo_actual]
            if camino:
                camino.insert(0, nodo_actual)
        return [ruta.setdefault(x, x) for x in camino if x not in ruta]

    def busqueda_heuristica(self, inicio, destino):
        # basado en A*
        mejor = []
        heapq.heappush(mejor, (0, inicio))
        # mejor.put(inicio, 0)
        ruta = [inicio]
        camino = {}
        distancia = {inicio: 0}
        while mejor:
            nodo_actual = heapq.heappop(mejor)[1]

            if nodo_actual == destino:
                ruta.append(nodo_actual)
                break
            for hijo in self.nodos[nodo_actual].get_conexiones():
                costo = distancia[nodo_actual] + self.nodos[nodo_actual].get_peso(hijo)
                if hijo not in distancia or costo < distancia[hijo]:
                    distancia[hijo] = costo
                    prioridad = costo + self._heuristica(hijo, destino)
                    heapq.heappush(mejor, (prioridad, hijo))
                    ruta.append(nodo_actual)
        return [camino.setdefault(x, x) for x in ruta if x not in camino]

    def _heuristica(self, hijo, destino):
        return abs(self.nodos[destino].h - self.nodos[hijo].h)
