class Token:
    def __init__(self, nombre, lexema, fila, columna):
        self.nombre = nombre
        self.lexema = lexema
        self.fila = fila
        self.columna = columna

class Error:
    def __init__ (self, caracter, tipo, descripcion, fila = None, columna = None):
        self.caracter = caracter
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna