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
    
class Pila:
    def __init__(self):
        self.pila = []
    
    def guardar(self, valor = None, lista_valores = None):
        if valor:
            self.pila.append(valor)
        elif lista_valores:
            self.pila.extend(lista_valores)
    
    def sacar(self, valor):
        if self.pila:
            if self.pila[-1] == valor:
                self.pila.pop()
                return True
        return False
    
    def reemplazar(self, antiguo, nuevo = None, lista_nuevos = None):
        for index, valor in enumerate(self.pila):
            if valor == antiguo:
                if nuevo:
                    self.pila[index] = nuevo
                elif lista_nuevos:
                    self.pila.pop(index)
                    lista_nuevos.reverse()
                    i = index
                    for new in lista_nuevos:
                        self.pila.insert(i, new)
                        i += 1
    
    def recorrer(self):
        for element in self.pila:
            print(element)