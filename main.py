from grafo import Grafo


if __name__ == '__main__':
    opcion = 0
    while opcion != 11:
        print("---------------Menu:----------------")
        print("------------------------------------")
        print("Crear un nuevo grafo             [1]")
        print("Mostrar estructura del grafo     [2]")
        print("Modificar informacion del grafo  [3]")
        print("Busqueda en anchura              [4]")
        print("Busqueda en profundidad          [5]")
        print("Borrar grafo                     [6]")
        print("Recorrido por todo el grafo      [7]")
        print("Busqueda informada               [8]")
        print("Busqueda general                 [9]")
        print("Busqueda heuristica              [10]")
        print("Salir                            [11]")
        opcion = int(input("Ingrese una opción: "))
        if opcion == 1:
            grafo = Grafo()
            opc = '0'
            while opc != '1':
                nodo = input("Ingrese un nodo: ")
                grafo.agregar_nodo(nodo)
                opc = input("Ya termino? Si[1], No[2]: ")
                while opc != '1' and opc != '2':
                    print("Opcion incorrecta")
                    opc = input("Ya termino? Si[1], No[2]: ")
            print("Añadir enlaces")
            opc = "2"
            peso = input("Desea agregar peso al enlace? Si[1] No[2]: ")
            while opc != "1":
                n1 = input("nodo inicio: ")
                n2 = input("nodo destino: ")
                if peso == "1":
                    pes = int(input("ingrese el peso: "))
                    grafo.agregar_conexion(n1, n2, peso=pes)
                else:
                    grafo.agregar_conexion(n1, n2)
                opc = input("Ya termino? Si[1], No[2]: ")
                while opc != '1' and opc != '2':
                    print("Opcion incorrecta")
                    opc = input("Ya termino? Si[1], No[2]: ")
        elif opcion == 2:
            grafo.visualizar()
        elif opcion == 3:
            clave = input("Ingrese clave antigua: ")
            nuevaClave = input("Ingrese nueva clave: ")
            grafo.modificar_info(clave, nuevaClave)
        elif opcion == 4:
            nodoini = input("Ingrese nodo inicial: ")
            nodob = input("Ingrese nodo a buscar: ")
            grafo.busqueda_anchura(nodoini, nodob)
            print()
        elif opcion == 5:
            nodoini = input("Ingrese nodo inicial: ")
            nodob = input("Ingrese nodo a buscar: ")
            grafo.busqueda_profundidad(nodoini, nodob)
            print()
        elif opcion == 6:
            del grafo
            print("Grafo eliminado")
        elif opcion == 7:
            for n in grafo.get_nodos():
                print(grafo.get_nodo(n))
        elif opcion == 8:
            nodoini = input("Ingrese nodo inicial: ")
            nodob = input("Ingrese nodo a buscar: ")
            print(grafo.busqueda_informada(nodoini, nodob))
        elif opcion == 9:
            nodoini = input("Ingrese nodo inicial: ")
            nodob = input("Ingrese nodo a buscar: ")
            grafo.busqueda_general(nodoini, nodob)
            print()
        elif opcion == 10:
            nodoini = input("Ingrese nodo inicial: ")
            nodob = input("Ingrese nodo a buscar: ")
            print(grafo.busqueda_heuristica(nodoini, nodob))
            print()
