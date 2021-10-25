class Token:
    def __init__(self, nombre, lexema, fila, columna):
        self.nombre = nombre
        self.lexema = lexema
        self.fila = fila
        self.columna = columna

        if nombre == "Cadena":
            self.id_token = 1
        elif nombre == "Entero":
            self.id_token = 2
        elif nombre == "Decimal":
            self.id_token = 3
        elif nombre == "Palabra reservada":
            if lexema == "Claves":
                self.id_token = 4
            elif lexema == "Registros":
                self.id_token = 5
            elif lexema == "imprimir":
                self.id_token = 6
            elif lexema == "imprimirln":
                self.id_token = 7
            elif lexema == "conteo":
                self.id_token = 8
            elif lexema == "promedio":
                self.id_token = 9
            elif lexema == "contarsi":
                self.id_token = 10
            elif lexema == "datos":
                self.id_token = 11
            elif lexema == "sumar":
                self.id_token = 12
            elif lexema == "max":
                self.id_token = 13
            elif lexema == "min":
                self.id_token = 14
            elif lexema == "exportarReporte":
                self.id_token = 15
            else:
                print(f"->ERROR: {lexema} no es palabra reservada")
        elif nombre == "ID":
            self.id_token = 16
        elif nombre == "Simbolo":
            if lexema == "=":
                self.id_token = 17
            elif lexema == "[":
                self.id_token = 18
            elif lexema == "]":
                self.id_token = 19
            elif lexema == ",":
                self.id_token = 20
            elif lexema == ";":
                self.id_token = 21
            elif lexema == "{":
                self.id_token = 22
            elif lexema == "}":
                self.id_token = 23
            elif lexema == "(":
                self.id_token = 24
            elif lexema == ")":
                self.id_token = 25
            else:
                print(f"->ERROR: {lexema} no es un símbolo.")
        else:
            print(f"->ERROR: {nombre} no es un nombre de token válido")

class Error:
    def __init__ (self, caracter, tipo, descripcion, fila = None, columna = None, lexema = None, recuperado = False):
        self.caracter = caracter
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        self.lexema = lexema
        self.recuperado = recuperado

        if self.fila is None:
            self.fila = "-"
        if self.columna is None:
            self.columna = "-"

class Arbol_Graphviz:
    def __init__(self, str_nodos):
        self.str_graphviz = '''digraph G {
        graph[label="Arbol de derivacion"]
        node[style="filled", fillcolor="palegreen"]\n'''
        self.str_graphviz += str_nodos
        self.str_graphviz += '}'

class Dato:
    def __init__(self, id_node, label, inicio = False, no_terminal = False, id_nodo_padre = None):
        self.id_node = id_node
        self.label = label
        self.inicio = inicio
        self.no_terminal = no_terminal
        self.id_nodo_padre = id_nodo_padre

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.nodos_hijo = []
        self.str_nodos_graphviz = ''
    
    def insertar_hijo(self, dato):
        nodo_hijo = Nodo(dato)
        self.nodos_hijo.append(nodo_hijo)

    def obtener_nodo(self, id_node):
        if self.dato.id_node == id_node:
            return self
        for nodo_hijo in self.nodos_hijo:
            nodo = nodo_hijo.obtener_nodo(id_node)
            if nodo is not None:
                return nodo
        return None
    
    def insertar_hijo_en(self, dato, id_node_padre):
        nodo_padre = self.obtener_nodo(id_node_padre)
        if nodo_padre is not None:
            nodo_padre.insertar_hijo(dato)
            return True
        print(f"No se encontró al nodo interior con id {id_node_padre}")
        return False
    
    def imprimir_arbol(self):
        print(f"Mi id: {self.dato.id_node}, mi label: {self.dato.label}, mi padre: {self.dato.id_nodo_padre}")
        if self.nodos_hijo:
            print(">> Soy No Terminal, y mis hijos son:")
            for nodo_hijo in self.nodos_hijo:
                nodo_hijo.imprimir_arbol()
        else:
            print(">> Soy Terminal, por lo que no tengo hijos")
    
    def crear_nodos_graphviz(self):
        if self.dato.inicio:
            self.str_nodos_graphviz += f'node{self.dato.id_node}[label="{self.dato.label}", fillcolor="cyan3"];\n'
        elif self.dato.no_terminal:
            self.str_nodos_graphviz += f'node{self.dato.id_node}[label="{self.dato.label}", fillcolor="coral2"];\n'
            self.str_nodos_graphviz += f'node{self.dato.id_nodo_padre} -> node{self.dato.id_node};\n'
        else:
            self.str_nodos_graphviz += f'node{self.dato.id_node}[label="{self.dato.label}"];\n'
            self.str_nodos_graphviz += f'node{self.dato.id_nodo_padre} -> node{self.dato.id_node};\n'
        if self.nodos_hijo:
            for nodo_hijo in self.nodos_hijo:
                self.str_nodos_graphviz += nodo_hijo.crear_nodos_graphviz()
        return self.str_nodos_graphviz