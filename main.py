from tkinter import *
from tkinter import filedialog, messagebox
from clases import *
import traceback

texto_lfp = ""
codigo = ""
palabras_reservadas = ["Claves", "Registros", "imprimir", "imprimirln", "conteo", "promedio", "contarsi", "datos", "sumar", "max", "min", "exportarReporte"]
index = 0
tokens_leidos = []
errores_encontrados = []
encabezados = []
registros = []
registro_aux = []
errores_registros = 0
errores_claves = 0
flag_final = False

class Interfaz:
    def __init__(self, window):
        self.window = window
        self.window.title('Little Code - Proyecto 2')        
        self.window.state('zoomed')

        self.frame = Frame(self.window, bg="#05323D")
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)

        imagen = PhotoImage(file = "images/logo.png")
        logo = Label(self.frame, image = imagen, bg="#05323D")
        logo.photo = imagen
        logo.place(x=480, y=15, width=200, height=100)

        title = Label(self.frame, text="Little Code", font=("Consolas", 40, "bold"), bg="#05323D", fg="white")
        title.place(x=680, y=15)

        self.txtbox_code = Text(self.frame, font=("Consolas", 13))
        self.txtbox_code.tag_configure("izquierda", justify='left')
        self.txtbox_code.insert("1.0", "")
        self.txtbox_code.tag_add("izquierda", "1.0")
        self.txtbox_code.config(width=57, height=25)
        self.txtbox_code.place(x=300, y=120, width=1150, height=280)

        lb_txt2 = Label(self.frame, text="==================================================== CONSOLA ====================================================", font=("Consolas", 14), bg="#05323D", fg="AntiqueWhite")
        lb_txt2.place(x=300, y=405)

        self.txtbox_console = Text(self.frame, font=("Consolas", 13), bg="black", fg="white", wrap="none")
        self.txtbox_console.tag_configure("izquierda", justify='left')
        self.txtbox_console.insert("1.0", "")
        self.txtbox_console.tag_add("izquierda", "1.0")
        self.txtbox_console.config(width=57, height=25, state='disabled')
        self.txtbox_console.place(x=300, y=430, width=1150, height=300) 

        scroll_x = Scrollbar(self.txtbox_console, orient='horizontal')
        scroll_x.pack(side=BOTTOM, fill=X)

        self.txtbox_console.config(xscrollcommand=scroll_x.set)
        scroll_x.config(command=self.txtbox_console.xview)


        self.txtbox_console.tag_config('Negrita', font=("Consolas", 13, "bold"))
        self.txtbox_console.tag_config('Fin', font=("Consolas", 13, "bold"), foreground="#41AA0E")
        self.txtbox_console.tag_config('Fin_Warning', font=("Consolas", 13, "bold"), foreground="#CD870F")
        self.txtbox_console.tag_config('Error', font=("Consolas", 13, "bold"), foreground="#C81010")
        self.txtbox_console.tag_config('Exito', font=("Consolas", 13, 'bold'), foreground='#99DCF2')

        btn_clear = Button(self.frame, text="Limpiar Consola", font=("Ebrima", 15), bg="light blue", command = lambda:[self.txtbox_console.config(state='normal'), self.txtbox_console.delete(1.0, END), self.txtbox_console.config(state='disabled')])
        btn_clear.place(x=800, y=735)

        frame_btn = Frame(self.frame, bg="#05323D")
        frame_btn.place(x=25, y=200)

        img1 = PhotoImage(file = "images/upload.png")
        play = Label(frame_btn, image = img1, bg="#05323D")
        play.photo = img1
        play.grid(row=0, column=0, padx=10)

        abrir_btn = Button(frame_btn, text="Abrir Archivo", font=("Ebrima", 15), bg="steel blue", command = lambda:[self.abrirArchivo()])
        abrir_btn.grid(row=0, column=1)

        sep1 = Label(frame_btn, text="", bg="#05323D")
        sep1.grid(row=1, column=0, pady=20)

        img2 = PhotoImage(file = "images/play.png")
        play = Label(frame_btn, image = img2, bg="#05323D")
        play.photo = img2
        play.grid(row=2, column=0, padx=5)

        analizar_btn = Button(frame_btn, text="Analizar Código", font=("Ebrima", 15), bg="steel blue", command = lambda:[self.obtener_codigo()])
        analizar_btn.grid(row=2, column=1)

        sep2 = Label(frame_btn, text="", bg="#05323D")
        sep2.grid(row=3, column=0, pady=20)

        lb_txt3 = Label(frame_btn, text="Sección de reportes", font=("Ebrima bold", 16), bg="#05323D", fg="white")
        lb_txt3.grid(row=4, column=1, pady=15)

        list_reportes = [("Reporte de Tokens", 1), ("Reporte de Errores", 2), ("Árbol de derivación", 3)]
        reporte = StringVar()
        reporte.set("1")

        row_num = 5
        for (tipo_reporte, valor) in list_reportes:
            Radiobutton(frame_btn, text=tipo_reporte, variable=reporte, value=valor, font=("Ebrima bold", 12), bg="#05323D").grid(row=row_num, column=1, padx=10)
            row_num += 1
            Label(frame_btn, text="", bg="#05323D").grid(row=row_num, column=0, pady=2)
            row_num += 1

        img3 = PhotoImage(file = "images/html.png")
        play = Label(frame_btn, image = img3, bg="#05323D")
        play.photo = img3
        play.grid(row=row_num, column=0, padx=10)

        reportes_btn = Button(frame_btn, text="Generar Reporte", font=("Ebrima", 15), bg="steel blue", command = lambda:[self.reporte(reporte.get())])
        reportes_btn.grid(row=row_num, column=1)

    def abrirArchivo(self):
        global texto_lfp
        name_file = filedialog.askopenfilename(
            title = "Seleccionar archivo LFP",
            initialdir = "./",
            filetypes = {
                ("Archivos LFP", "*.lfp"),
                ("Todos los archivos", "*.*")
            }
        )
        try:
            archivo = open(name_file)
            texto = ""
            texto = archivo.read()
            texto_lfp = ""
            texto_lfp = texto
            print("->Archivo leído con éxito")            
            self.txtbox_code.insert(END, texto_lfp)
            archivo.close()            
        except Exception:
            traceback.print_exc()
            print("->No se seleccionó un archivo")
    
    def obtener_codigo(self):
        global codigo
        global tokens_leidos
        global errores_encontrados
        code = ""
        code = self.txtbox_code.get(1.0, END)
        if code != "\n":
            code += "$"
            codigo = ""
            codigo = code
            tokens_leidos = []
            errores_encontrados = []
            self.analizador_lexico()
            self.analizador_sintactico()
            print(f"ERRORES: {len(errores_encontrados)}")
            for error in errores_encontrados:
                print(error.caracter, error.tipo, error.descripcion, str(error.fila), str(error.columna), error.lexema, error.recuperado)
        else:
            self.txtbox_console.config(state='normal')
            self.txtbox_console.insert(END, ">> Fin de análisis de código. No se encontraron errores léxicos ni sintácticos.\n", 'Fin')
            self.txtbox_console.config(state='disabled')

    def is_number(self, caracter):
        if ord(caracter) >= 48 and ord(caracter) <= 57:
            return True
        return False
    
    def is_letter(self, caracter):
        if (ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122):
            return True
        return False
    
    def is_symbol(self, caracter):
        if caracter == "=" or caracter == "[" or caracter == "]" or caracter == "," or caracter == ";" or caracter == "{" or caracter == "}" or caracter == '(' or caracter == ')':
            return True
        return False
    
    def is_ascii(self, caracter):
        if ord(caracter) == 9 or ord(caracter) == 10 or ord(caracter) == 32 or ord(caracter) == 33 or (ord(caracter) >= 35 and ord(caracter) <= 154) or (ord(caracter) >= 160 and ord(caracter) <= 253):
            return True
        return False

    def analizador_lexico(self):
        global codigo
        global palabras_reservadas
        global tokens_leidos
        global errores_encontrados
        fila = 1
        columna = 0
        estado = "q0"
        lexema_actual = ""
        for caracter in codigo:
            if estado == "q0":
                if caracter == '"':
                    estado = "q1"
                elif caracter == "-":
                    lexema_actual += caracter
                    estado = "q2"
                elif self.is_number(caracter):
                    lexema_actual += caracter
                    estado = "q3"
                elif self.is_letter(caracter):
                    lexema_actual += caracter
                    estado = "q4"
                elif caracter == "_":
                    lexema_actual += caracter
                    estado = "q4"
                elif caracter == "#":
                    estado = "q5"
                elif caracter == "'":
                    estado = "q6"
                elif self.is_symbol(caracter):
                    lexema_actual += caracter
                    t_simbolo = Token("Simbolo", lexema_actual, fila, columna-(len(lexema_actual) - 2))
                    tokens_leidos.append(t_simbolo)
                    lexema_actual = ""
                    estado = "q7"
                elif ord(caracter) == 9 or ord(caracter) == 10 or ord(caracter) == 32:
                    pass
                elif caracter == "$":
                    print("->Fin de análisis de archivo")
                else:
                    error = Error(caracter, "Léxico", "El caracter no figura como parte del lenguaje del programa.", fila, columna+1)
                    errores_encontrados.append(error)
            elif estado == "q1":
                if self.is_ascii(caracter):
                    lexema_actual += caracter
                elif caracter == '"':
                    t_cadena = Token("Cadena", lexema_actual, fila, columna-(len(lexema_actual)))
                    tokens_leidos.append(t_cadena)
                    lexema_actual = ""
                    estado = "q7"
                else:
                    lexema_actual += caracter
                    error = Error(caracter, "Léxico", f"El caracter no figura como caracter ASCII imprimible ({ord(caracter)}).", fila, columna+1)
                    errores_encontrados.append(error)
            elif estado == "q2":
                if self.is_number(caracter):
                    lexema_actual += caracter
                    estado = "q3"
                else:
                    error = Error(caracter, "Léxico", "Se esperaba un número.", fila, columna+1)
                    errores_encontrados.append(error)
                    lexema_actual = ""
                    estado = "pre_validacion"
            elif estado == "q3":
                if self.is_number(caracter):
                    lexema_actual += caracter
                elif caracter == ".":
                    lexema_actual += caracter
                    estado = "q8"
                else:
                    entero = 0
                    entero = int(lexema_actual)
                    t_entero = Token("Entero", entero, fila, columna-(len(lexema_actual) - 1))
                    tokens_leidos.append(t_entero)
                    lexema_actual = ""
                    estado = "pre_validacion"
            elif estado == "q4":
                if self.is_letter(caracter):
                    lexema_actual += caracter
                elif caracter == "_":
                    lexema_actual += caracter
                elif self.is_number(caracter):
                    lexema_actual += caracter
                else:
                    is_id = True
                    for reservada in palabras_reservadas:
                        if lexema_actual == reservada:
                            is_id = False
                            t_reservada = Token("Palabra reservada", lexema_actual, fila, columna-(len(lexema_actual) - 1))
                            tokens_leidos.append(t_reservada)
                            lexema_actual = ""
                            break
                    if is_id:
                        t_id = Token("ID", lexema_actual, fila, columna-(len(lexema_actual) - 1))
                        tokens_leidos.append(t_id)
                        lexema_actual = ""
                    lexema_actual = ""
                    estado = "pre_validacion"
            elif estado == "q5":
                if ord(caracter) == 10: # Salto de línea
                    estado = "q7"
                else:
                    pass
            elif estado == "q6":
                if caracter == "'":
                    estado = "q9"
                else:
                    error = Error(caracter, "Sintáctico", "Se esperaba la segunda comilla simple de comentario multilínea.", fila, columna+1)
                    errores_encontrados.append(error)
                    lexema_actual = ""
                    estado = "pre_validacion"
            elif estado == "q8":
                if self.is_number(caracter):
                    lexema_actual += caracter
                    estado = "q10"
                else:
                    error = Error(caracter, "Léxico", "Se esperaba un número en la parte decimal.", fila, columna+1)
                    errores_encontrados.append(error)
                    lexema_actual = ""
                    estado = "pre_validacion"
            elif estado == "q9":
                if caracter == "'":
                    estado = "q11"
                else:
                    error = Error(caracter, "Sintáctico", "Se esperaba la tercera comilla simple de comentario multilínea.", fila, columna+1)
                    errores_encontrados.append(error)
                    lexema_actual = ""
                    estado = "pre_validacion"
            elif estado == "q10":
                if self.is_number(caracter):
                    lexema_actual += caracter
                else:
                    decimal = 0
                    decimal = float(lexema_actual)
                    t_decimal = Token("Decimal", decimal, fila, columna-(len(lexema_actual) - 1))
                    tokens_leidos.append(t_decimal)
                    lexema_actual = ""
                    estado = "pre_validacion"
            elif estado == "q11":
                if caracter == "'":
                    estado = "q12"
                else:
                    pass
            elif estado == "q12":
                if caracter == "'":
                    estado = "q13"
                else:
                    error = Error(caracter, "Sintáctico", "Se esperaba la segunda comilla simple que finaliza el comentario multilínea.", fila, columna+1)
                    errores_encontrados.append(error)
                    lexema_actual = ""
                    estado = "pre_validacion"
            elif estado == "q13":
                if caracter == "'":
                    estado = "q7"
                else:
                    error = Error(caracter, "Sintáctico", "Se esperaba la tercera comilla simple que finaliza el comentario multilínea.", fila, columna+1)
                    errores_encontrados.append(error)
                    lexema_actual = ""
                    estado = "pre_validacion"
            #Prevalidación de tokens en caso de un error
            if estado == "pre_validacion":
                if caracter == '"':
                    estado = "q1"
                elif caracter == "-":
                    lexema_actual += caracter
                    estado = "q2"
                elif self.is_number(caracter):
                    lexema_actual += caracter
                    estado = "q3"
                elif self.is_letter(caracter):
                    lexema_actual += caracter
                    estado = "q4"
                elif caracter == "_":
                    lexema_actual += caracter
                    estado = "q4"
                elif caracter == "#":
                    estado = "q5"
                elif caracter == "'":
                    estado = "q6"
                elif self.is_symbol(caracter):
                    lexema_actual += caracter
                    t_simbolo = Token("Simbolo", lexema_actual, fila, columna-(len(lexema_actual) - 2))
                    tokens_leidos.append(t_simbolo)
                    lexema_actual = ""
                    estado = "q7"
                elif ord(caracter) == 9 or ord(caracter) == 10 or ord(caracter) == 32:
                    pass
                elif caracter == "$":
                    print("->Fin de análisis de archivo")
                else:
                    error = Error(caracter, "Léxico", "El caracter no figura como parte del lenguaje del programa.", fila, columna+1)
                    errores_encontrados.append(error)
                    estado = "q0"
            #Estado de aceptación, redirección al estado inicial
            if estado == "q7":                
                estado = "q0"
            # Control Filas - columnas
            if ord(caracter) == 9: # tab
                columna += 4
            elif ord(caracter) == 10: # salto de linea
                columna = 0
                fila += 1
            elif ord(caracter) == 32: # espacio
                columna += 1
            else: # otro caracter
                columna +=1
        if lexema_actual != "":
            error = Error("N/A", "Sintáctico", "No vino la comilla doble que finaliza una cadena.", fila - 1, columna)
            errores_encontrados.append(error)
    
    def analizador_sintactico(self):
        global tokens_leidos
        global errores_encontrados
        global index
        global encabezados
        global registros
        global flag_final
        global errores_claves
        global errores_registros
        tokens_leidos.append("#")
        index = 0
        errores_claves = 0
        errores_registros = 0
        encabezados = []
        registros = []
        flag_final = False
        self.inicio()
        tokens_leidos.pop()
        self.txtbox_console.config(state='normal')
        if len(errores_encontrados) > 0:
            self.txtbox_console.insert(END, f"\n>> Fin de análisis de código. Se encontraron {len(errores_encontrados)} errores léxicos/sintácticos, se recomienda generar 'Reporte de Errores'.\n", 'Fin_Warning')
        else:
            self.txtbox_console.insert(END, "\n>> Fin de análisis de código. No se encontraron errores léxicos ni sintácticos.\n", 'Fin')
        self.txtbox_console.config(state='disabled')
    
    def inicio(self):
        global tokens_leidos
        global errores_encontrados
        global index
        global encabezados
        global registros
        global registro_aux
        global errores_registros
        global errores_claves

        if index < (len(tokens_leidos) - 1):
            id_token = tokens_leidos[index].id_token
            if id_token == 4: # Claves
                encabezados = []
                errores_claves = 0
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 17: # Igual
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 18: # Abre Corchete
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 1: # Cadena
                                        encabezados.append(tokens_leidos[index].lexema)
                                        sintax_error = self.cadenas()
                                        if not sintax_error:
                                            if not flag_final:
                                                id_token = tokens_leidos[index].id_token
                                                if id_token == 19: # Cierra Corchete
                                                    # Se leyeron las claves correctamente
                                                    for clave in encabezados:
                                                        if clave == "":
                                                            errores_claves += 1
                                                    if errores_claves > 0:
                                                        self.txtbox_console.config(state='normal')
                                                        self.txtbox_console.insert(END, f">> Error en el ingreso de Claves. No pueden venir cadenas vacías. Cadenas vacías ingresadas: {errores_claves}.  \n", 'Error')
                                                        self.txtbox_console.config(state='disabled')
                                                        encabezados = []
                                                    self.otra_ins()
                                                else:
                                                    self.panic_mode("Claves", ingreso_datos=True)
                                    else:
                                        self.panic_mode("Claves", ingreso_datos=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada Claves, la asignación de valores es inconclusa.")
                                    errores_encontrados.append(error)
                            else:
                                self.panic_mode("Claves", ingreso_datos=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada Claves, la asignación de valores es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("Claves", ingreso_datos=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada Claves, sin asignación de valores.")
                    errores_encontrados.append(error)
            elif id_token == 5: # Registros
                registros = []
                errores_registros = 0
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 17: # Igual
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 18: # Abre Corchete
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 22: # Abre llave
                                        registro_aux = []
                                        sintax_error = self.valor()
                                        if not sintax_error:
                                            if not flag_final:
                                                id_token = tokens_leidos[index].id_token
                                                if id_token == 23: # Cierra Llave
                                                    # Registro leído correctamente
                                                    if len(registro_aux) == len(encabezados):
                                                        registros.append(registro_aux)
                                                    elif len(registro_aux) < len(encabezados):
                                                        for i in range(len(encabezados)-len(registro_aux)):
                                                            registro_aux.append(None)
                                                        registros.append(registro_aux)
                                                    else:
                                                        errores_registros += 1
                                                    registro_aux = []
                                                    sintax_error = self.mult_registros()
                                                    if not sintax_error:
                                                        if not flag_final:
                                                            registro_aux = []
                                                            id_token = tokens_leidos[index].id_token
                                                            if id_token == 19: # Cierra Corchete
                                                                # Se leyeron todos los registros correctamente
                                                                if len(encabezados) == 0:
                                                                    self.txtbox_console.config(state='normal')
                                                                    self.txtbox_console.insert(END, ">> Error en el ingreso de Registros. No se han ingresado claves al sistema.\n", 'Error')
                                                                    self.txtbox_console.config(state='disabled')
                                                                    registros = []
                                                                elif errores_registros > 0:
                                                                    self.txtbox_console.config(state='normal')
                                                                    self.txtbox_console.insert(END, f">> Error en el ingreso de Registros. {errores_registros} registros poseen más valores que claves cargadas al sistema, por lo que no se ingresaron. Claves cargadas: {len(encabezados)}.  \n", 'Error')
                                                                    self.txtbox_console.config(state='disabled')
                                                                self.otra_ins()
                                                            else:
                                                                self.panic_mode("Registros", ingreso_datos=True)
                                                        else:
                                                            #FIN DE LECTURA DE TOKENS
                                                            if len(registro_aux) > 0:
                                                                error = Error("N/A", "Sintáctico", "En la asignación de Registros, no vinieron los tokens que finalizan la asignación.", recuperado = True)
                                                                registros.append(registro_aux)
                                                            else:
                                                                error = Error("N/A", "Sintáctico", "En la asignación de Registros, no vinieron los tokens que finalizan la asignación.")
                                                            errores_encontrados.append(error)
                                                else:
                                                    self.panic_mode("Registros", ingreso_datos=True)
                                            else:
                                                #FIN DE LECTURA DE TOKENS
                                                if len(registro_aux) > 0:
                                                    error = Error("N/A", "Sintáctico", "En la asignación de Registros, no vinieron los tokens '} ]' que finalizan la asignación.", recuperado = True)
                                                    registros.append(registro_aux)
                                                else:
                                                    error = Error("N/A", "Sintáctico", "En la asignación de Registros, no vinieron los tokens '} ]' que finalizan la asignación.")
                                                errores_encontrados.append(error)
                                    else:
                                        self.panic_mode("Registros", ingreso_datos=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada Claves, la asignación de valores es inconclusa.")
                                    errores_encontrados.append(error)
                            else:
                                self.panic_mode("Registros", ingreso_datos=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada Registros, con asignación de valores inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("Registros", ingreso_datos=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada Registros, sin asignación de valores.")
                    errores_encontrados.append(error)
            elif id_token == 6: # imprimir
                cadena_aux = ""
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 1: # Cadena
                                cadena_aux = tokens_leidos[index].lexema
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 25: # Cierra paréntesis
                                        index += 1
                                        if index < (len(tokens_leidos) - 1):
                                            id_token = tokens_leidos[index].id_token
                                            if id_token == 21: # Punto y coma
                                                # Función imprimir correcta
                                                self.txtbox_console.config(state='normal')
                                                self.txtbox_console.insert(END, cadena_aux)
                                                self.txtbox_console.config(state='disabled')
                                                self.otra_ins()
                                            else:
                                                self.panic_mode("imprimir", funcion=True)
                                        else:
                                            #FIN DE LECTURA DE TOKENS
                                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada imprimir, no vino el token ';' que finaliza la función.", recuperado=True)
                                            errores_encontrados.append(error)
                                            self.txtbox_console.config(state='normal')
                                            self.txtbox_console.insert(END, cadena_aux)
                                            self.txtbox_console.config(state='disabled')
                                    else:
                                        self.panic_mode("imprimir", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada imprimir, no vinieron los tokens ');' que finaliza la función.", recuperado=True)
                                    errores_encontrados.append(error)
                                    self.txtbox_console.config(state='normal')
                                    self.txtbox_console.insert(END, cadena_aux)
                                    self.txtbox_console.config(state='disabled')
                            else:
                                self.panic_mode("imprimir", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada imprimir, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("imprimir", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada imprimir, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            elif id_token == 7: # imprimirln
                cadena_aux = ""
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 1: # Cadena
                                cadena_aux = tokens_leidos[index].lexema
                                cadena_aux += "\n"
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 25: # Cierra paréntesis
                                        index += 1
                                        if index < (len(tokens_leidos) - 1):
                                            id_token = tokens_leidos[index].id_token
                                            if id_token == 21: # Punto y coma
                                                # Función imprimir correcta
                                                self.txtbox_console.config(state='normal')
                                                self.txtbox_console.insert(END, cadena_aux)
                                                self.txtbox_console.config(state='disabled')
                                                self.otra_ins()
                                            else:
                                                self.panic_mode("imprimirln", funcion=True)
                                        else:
                                            #FIN DE LECTURA DE TOKENS
                                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada imprimirln, no vino el token ';' que finaliza la función.", recuperado=True)
                                            errores_encontrados.append(error)
                                            self.txtbox_console.config(state='normal')
                                            self.txtbox_console.insert(END, cadena_aux)
                                            self.txtbox_console.config(state='disabled')
                                    else:
                                        self.panic_mode("imprimirln", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada imprimirln, no vinieron los tokens ');' que finaliza la función.", recuperado=True)
                                    errores_encontrados.append(error)
                                    self.txtbox_console.config(state='normal')
                                    self.txtbox_console.insert(END, cadena_aux)
                                    self.txtbox_console.config(state='disabled')
                            else:
                                self.panic_mode("imprimirln", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada imprimirln, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("imprimirln", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada imprimirln, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            elif id_token == 8: # conteo
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 25: # Cierra paréntesis
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 21: # Punto y coma
                                        # Función conteo correcta
                                        cantidad_registros = len(encabezados)*len(registros)
                                        elementos_nulos = 0
                                        for registro in registros:
                                            for elemento in registro:
                                                if elemento is None:
                                                    elementos_nulos += 1
                                        total_registros = cantidad_registros - elementos_nulos
                                        cantidad_registros = str(cantidad_registros)
                                        self.txtbox_console.config(state='normal')
                                        self.txtbox_console.insert(END, total_registros)
                                        self.txtbox_console.insert(END, "\n")
                                        self.txtbox_console.config(state='disabled')
                                        self.otra_ins()
                                    else:
                                        self.panic_mode("conteo", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada conteo, no vino el token ';' que finaliza la función.", recuperado = True)
                                    errores_encontrados.append(error)
                                    cantidad_registros = len(encabezados)*len(registros)
                                    cantidad_registros = str(cantidad_registros)
                                    self.txtbox_console.config(state='normal')
                                    self.txtbox_console.insert(END, cantidad_registros)
                                    self.txtbox_console.insert(END, "\n")
                                    self.txtbox_console.config(state='disabled')
                            else:
                                self.panic_mode("conteo", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada conteo, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("conteo", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada conteo, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            elif id_token == 9: # promedio
                campo = ""
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 1: # Cadena
                                campo = tokens_leidos[index].lexema
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 25: # Cierra paréntesis
                                        index += 1
                                        if index < (len(tokens_leidos) - 1):
                                            id_token = tokens_leidos[index].id_token
                                            if id_token == 21: # Punto y coma
                                                # Función promedio correcta
                                                self.txtbox_console.config(state='normal')
                                                pos = 0
                                                se_encontro = False
                                                for titulo in encabezados:
                                                    if titulo == campo:
                                                        se_encontro = True
                                                        suma = 0
                                                        filas = 0
                                                        hay_cadenas = False
                                                        if len(registros) > 0:
                                                            for fila in registros:
                                                                if type(fila[pos]) is int or type(fila[pos]) is float:
                                                                    suma += fila[pos]
                                                                    filas += 1
                                                                else:
                                                                    hay_cadenas = True
                                                                    break
                                                            if not hay_cadenas:
                                                                promedio = suma/filas
                                                                self.txtbox_console.insert(END, str(promedio))
                                                            else:
                                                                self.txtbox_console.insert(END, f">> Error en la función promedio. Todos los valores deben ser de tipo entero o decimal. Campo: {campo}", 'Error')
                                                            self.txtbox_console.insert(END, "\n")
                                                        else:
                                                            self.txtbox_console.insert(END, ">> Error en la función promedio. No se han ingresado registros al programa.\n", 'Error')
                                                        break
                                                    pos += 1
                                                if not se_encontro:
                                                    self.txtbox_console.insert(END, ">> Error en la función promedio. No se encontró el campo: " + campo + ".\n", 'Error')
                                                self.txtbox_console.config(state='disabled')
                                                self.otra_ins()
                                            else:
                                                self.panic_mode("promedio", funcion=True)
                                        else:
                                            #FIN DE LECTURA DE TOKENS
                                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada promedio, no vino el token ';' que finaliza la función.", recuperado=True)
                                            errores_encontrados.append(error)
                                            self.txtbox_console.config(state='normal')
                                            pos = 0
                                            se_encontro = False
                                            for titulo in encabezados:
                                                if titulo == campo:
                                                    se_encontro = True
                                                    suma = 0
                                                    filas = 0
                                                    hay_cadenas = False
                                                    if len(registros) > 0:
                                                        for fila in registros:
                                                            if type(fila[pos]) is int or type(fila[pos]) is float:
                                                                suma += fila[pos]
                                                                filas += 1
                                                            else:
                                                                hay_cadenas = True
                                                                break
                                                        if not hay_cadenas:
                                                            promedio = suma/filas
                                                            self.txtbox_console.insert(END, str(promedio))
                                                        else:
                                                            self.txtbox_console.insert(END, f">> Error en la función promedio. Todos los valores deben ser de tipo entero o decimal. Campo: {campo}", 'Error')
                                                        self.txtbox_console.insert(END, "\n")
                                                    else:
                                                        self.txtbox_console.insert(END, ">> Error en la función promedio. No se han ingresado registros al programa.\n", 'Error')
                                                    break
                                                pos += 1
                                            if not se_encontro:
                                                self.txtbox_console.insert(END, ">> Error en la función promedio. No se encontró el campo: " + campo + ".\n", 'Error')
                                            self.txtbox_console.config(state='disabled')
                                    else:
                                        self.panic_mode("promedio", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada promedio, no vinieron los tokens ');' que finalizan la función.")
                                    errores_encontrados.append(error)
                            else:
                                self.panic_mode("promedio", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada promedio, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("promedio", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada promedio, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            elif id_token == 10: # contarsi
                campo = ""
                valor = None
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 1: # Cadena
                                campo = tokens_leidos[index].lexema
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 20: # Coma
                                        index += 1
                                        if index < (len(tokens_leidos) - 1):
                                            id_token = tokens_leidos[index].id_token
                                            if id_token == 1 or id_token == 2 or id_token == 3: # Cadena | Entero | Decimal
                                                valor = tokens_leidos[index].lexema
                                                index += 1
                                                if index < (len(tokens_leidos) - 1):
                                                    id_token = tokens_leidos[index].id_token
                                                    if id_token == 25: # Cierra paréntesis
                                                        index += 1
                                                        if index < (len(tokens_leidos) - 1):
                                                            id_token = tokens_leidos[index].id_token
                                                            if id_token == 21: # Punto y coma
                                                                # Función contarsi correcta
                                                                self.txtbox_console.config(state='normal')
                                                                pos = 0
                                                                se_encontro = False
                                                                for titulo in encabezados:
                                                                    if titulo == campo:
                                                                        se_encontro = True
                                                                        contador = 0
                                                                        for fila in registros:
                                                                            if fila[pos] == valor:
                                                                                contador += 1
                                                                        self.txtbox_console.insert(END, str(contador))
                                                                        self.txtbox_console.insert(END, "\n")
                                                                        break
                                                                    pos += 1
                                                                if not se_encontro:
                                                                    self.txtbox_console.insert(END, ">> Error en la función contarsi. No se encontró el campo: " + campo + ".\n", 'Error')
                                                                self.txtbox_console.config(state='disabled')
                                                                self.otra_ins()
                                                            else:
                                                                self.panic_mode("contarsi", funcion=True)
                                                        else:
                                                            #FIN DE LECTURA DE TOKENS
                                                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada contarsi, no vino el token ';' que finaliza la función.", recuperado=True)
                                                            errores_encontrados.append(error)
                                                            self.txtbox_console.config(state='normal')
                                                            pos = 0
                                                            se_encontro = False
                                                            for titulo in encabezados:
                                                                if titulo == campo:
                                                                    se_encontro = True
                                                                    contador = 0
                                                                    for fila in registros:
                                                                        if fila[pos] == valor:
                                                                            contador += 1
                                                                    self.txtbox_console.insert(END, str(contador))
                                                                    self.txtbox_console.insert(END, "\n")
                                                                    break
                                                                pos += 1
                                                            if not se_encontro:
                                                                self.txtbox_console.insert(END, ">> Error en la función contarsi. No se encontró el campo: " + campo + ".\n", 'Error')
                                                            self.txtbox_console.config(state='disabled')
                                                    else:
                                                        self.panic_mode("contarsi", funcion=True)
                                                else:
                                                    #FIN DE LECTURA DE TOKENS
                                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada contarsi, la sintaxis de la función es inconclusa.")
                                                    errores_encontrados.append(error)
                                            else:
                                                self.panic_mode("contarsi", funcion=True)
                                        else:
                                            #FIN DE LECTURA DE TOKENS
                                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada contarsi, la sintaxis de la función es inconclusa.")
                                            errores_encontrados.append(error)
                                    else:
                                        self.panic_mode("contarsi", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada contarsi, la sintaxis de la función es inconclusa.")
                                    errores_encontrados.append(error)
                            else:
                                self.panic_mode("contarsi", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada contarsi, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("contarsi", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada contarsi, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            elif id_token == 11: # datos
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 25: # Cierra paréntesis
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 21: # Punto y coma
                                        # Función datos correcta
                                        self.txtbox_console.config(state='normal', )
                                        if len(encabezados)>0:
                                            self.txtbox_console.insert(END, " ")
                                            for titulo in encabezados:
                                                salida = "[ " + titulo + " ]"
                                                self.txtbox_console.insert(END, salida, "Negrita")
                                                self.txtbox_console.insert(END, "\t")
                                            self.txtbox_console.insert(END, "\n")
                                            for registro in registros:
                                                self.txtbox_console.insert(END, " ")
                                                pos = 0
                                                for element in registro:
                                                    len_titulo = len(encabezados[pos])
                                                    if element is not None:
                                                        if (len_titulo - len(str(element))) > 1:
                                                            espacios = round((len_titulo-len(str(element)))/2)
                                                            spc = ""
                                                            for i in range(espacios):
                                                                spc += " " 
                                                            salida = "[ " + spc + str(element) + spc + " ]"
                                                        else:
                                                            salida = "[ " + str(element) + " ]"
                                                    else:
                                                        if (len_titulo - len("-")) > 1:
                                                            espacios = round((len_titulo-len("---"))/2)
                                                            spc = ""
                                                            for i in range(espacios):
                                                                spc += " " 
                                                            salida = "[ " + spc + "---" + spc + " ]"
                                                        else:
                                                            salida = "[ --- ]"
                                                    self.txtbox_console.insert(END, salida)
                                                    self.txtbox_console.insert(END, "\t")
                                                    pos += 1
                                                self.txtbox_console.insert(END, "\n")
                                        else:
                                            self.txtbox_console.insert(END, ">> Error en la función datos. No se han ingresado Claves ni Registros al programa.  \n", 'Error')
                                        self.txtbox_console.config(state='disabled')
                                        self.otra_ins()
                                    else:
                                        self.panic_mode("datos", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada datos, no vino el token ';' que finaliza la función.", recuperado=True)
                                    errores_encontrados.append(error)
                                    self.txtbox_console.config(state='normal', )
                                    if len(encabezados)>0:
                                        self.txtbox_console.insert(END, " ")
                                        for titulo in encabezados:
                                            salida = "[ " + titulo + " ]"
                                            self.txtbox_console.insert(END, salida, "Negrita")
                                            self.txtbox_console.insert(END, "\t")
                                        self.txtbox_console.insert(END, "\n")
                                        for registro in registros:
                                            self.txtbox_console.insert(END, " ")
                                            pos = 0
                                            for element in registro:
                                                len_titulo = len(encabezados[pos])
                                                if (len_titulo - len(str(element))) > 1:
                                                    espacios = round((len_titulo-len(str(element)))/2)
                                                    spc = ""
                                                    for i in range(espacios):
                                                        spc += " " 
                                                    salida = "[ " + spc + str(element) + spc + " ]"
                                                else:
                                                    salida = "[ " + str(element) + " ]"
                                                self.txtbox_console.insert(END, salida)
                                                self.txtbox_console.insert(END, "\t")
                                                pos += 1
                                            self.txtbox_console.insert(END, "\n")
                                    else:
                                        self.txtbox_console.insert(END, ">> Error en la función datos. No se han ingresado Claves ni Registros al programa.  \n", 'Error')
                                    self.txtbox_console.config(state='disabled')
                            else:
                                self.panic_mode("datos", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada datos, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("datos", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada datos, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            elif id_token == 12: # sumar
                campo = ""
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 1: # Cadena
                                campo = tokens_leidos[index].lexema
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 25: # Cierra paréntesis
                                        index += 1
                                        if index < (len(tokens_leidos) - 1):
                                            id_token = tokens_leidos[index].id_token
                                            if id_token == 21: # Punto y coma
                                                # Función sumar correcta
                                                self.txtbox_console.config(state='normal')
                                                pos = 0
                                                se_encontro = False
                                                for titulo in encabezados:
                                                    if titulo == campo:
                                                        se_encontro = True
                                                        suma = 0
                                                        hay_cadenas = False
                                                        if len(registros) > 0:
                                                            for fila in registros:
                                                                if type(fila[pos]) is int or type(fila[pos]) is float:
                                                                    suma += fila[pos]
                                                                else:
                                                                    hay_cadenas = True
                                                                    break
                                                            if not hay_cadenas:
                                                                self.txtbox_console.insert(END, str(suma))
                                                            else:
                                                                self.txtbox_console.insert(END, f">> Error en la función sumar. Todos los valores deben ser de tipo entero o decimal. Campo: {campo}", 'Error')
                                                        else:
                                                            self.txtbox_console.insert(END, ">> Error en la función sumar. No se han ingresado registros al programa.", 'Error')
                                                        self.txtbox_console.insert(END, "\n")
                                                        break
                                                    pos += 1
                                                if not se_encontro:
                                                    self.txtbox_console.insert(END, ">> Error en la función sumar. No se encontró el campo: " + campo + ".\n", 'Error')
                                                self.txtbox_console.config(state='disabled')
                                                self.otra_ins()
                                            else:
                                                self.panic_mode("sumar", funcion=True)
                                        else:
                                            #FIN DE LECTURA DE TOKENS
                                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada sumar, no vino el token ';' que finaliza la función.", recuperado = True)
                                            errores_encontrados.append(error)
                                            self.txtbox_console.config(state='normal')
                                            pos = 0
                                            se_encontro = False
                                            for titulo in encabezados:
                                                if titulo == campo:
                                                    se_encontro = True
                                                    suma = 0
                                                    hay_cadenas = False
                                                    if len(registros) > 0:
                                                        for fila in registros:
                                                            if type(fila[pos]) is int or type(fila[pos]) is float:
                                                                suma += fila[pos]
                                                            else:
                                                                hay_cadenas = True
                                                                break
                                                        if not hay_cadenas:
                                                            self.txtbox_console.insert(END, str(suma))
                                                        else:
                                                            self.txtbox_console.insert(END, f">> Error en la función sumar. Todos los valores deben ser de tipo entero o decimal. Campo: {campo}", 'Error')
                                                    else:
                                                        self.txtbox_console.insert(END, ">> Error en la función sumar. No se han ingresado registros al programa.", 'Error')
                                                    self.txtbox_console.insert(END, "\n")
                                                    break
                                                pos += 1
                                            if not se_encontro:
                                                self.txtbox_console.insert(END, ">> Error en la función sumar. No se encontró el campo: " + campo + ".\n", 'Error')
                                            self.txtbox_console.config(state='disabled')
                                    else:
                                        self.panic_mode("sumar", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada sumar, la sintaxis de la función es inconclusa.")
                                    errores_encontrados.append(error)
                            else:
                                self.panic_mode("sumar", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada sumar, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("sumar", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada sumar, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            elif id_token == 13: # max
                campo = ""
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 1: # Cadena
                                campo = tokens_leidos[index].lexema
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 25: # Cierra paréntesis
                                        index += 1
                                        if index < (len(tokens_leidos) - 1):
                                            id_token = tokens_leidos[index].id_token
                                            if id_token == 21: # Punto y coma
                                                # Función max correcta
                                                self.txtbox_console.config(state='normal')
                                                pos = 0
                                                se_encontro = False
                                                for titulo in encabezados:
                                                    if titulo == campo:
                                                        se_encontro = True
                                                        max_campo = None
                                                        if len(registros)>0:
                                                            max_campo = registros[0][pos]
                                                            hay_cadenas = False
                                                            for fila in registros:
                                                                if type(fila[pos]) is int or type(fila[pos]) is float:
                                                                    if max_campo is not None:
                                                                        if fila[pos] > max_campo:
                                                                            max_campo = fila[pos]
                                                                    else:
                                                                        max_campo = fila[pos]
                                                                else:
                                                                    hay_cadenas = True
                                                                    break
                                                            if not hay_cadenas:
                                                                self.txtbox_console.insert(END, str(max_campo))
                                                            else:
                                                                self.txtbox_console.insert(END, f">> Error en la función max. Todos los valores deben ser de tipo entero o decimal. Campo: {campo}", 'Error')
                                                        else:
                                                            self.txtbox_console.insert(END, ">> Error en la función max. No se han ingresado registros al programa.", 'Error')
                                                        self.txtbox_console.insert(END, "\n")
                                                        break
                                                    pos += 1
                                                if not se_encontro:
                                                    self.txtbox_console.insert(END, ">> Error en la función max. No se encontró el campo: " + campo + ".\n", 'Error')
                                                self.txtbox_console.config(state='disabled')
                                                self.otra_ins()
                                            else:
                                                self.panic_mode("max", funcion=True)
                                        else:
                                            #FIN DE LECTURA DE TOKENS
                                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada max, no vino el token ';' que finaliza la función.", recuperado = True)
                                            errores_encontrados.append(error)
                                            self.txtbox_console.config(state='normal')
                                            pos = 0
                                            se_encontro = False
                                            for titulo in encabezados:
                                                if titulo == campo:
                                                    se_encontro = True
                                                    max_campo = None
                                                    if len(registros)>0:
                                                        max_campo = registros[0][pos]
                                                        hay_cadenas = False
                                                        for fila in registros:
                                                            if type(fila[pos]) is int or type(fila[pos]) is float:
                                                                if max_campo is not None:
                                                                    if fila[pos] > max_campo:
                                                                        max_campo = fila[pos]
                                                                else:
                                                                    max_campo = fila[pos]
                                                            else:
                                                                hay_cadenas = True
                                                                break
                                                        if not hay_cadenas:
                                                           self.txtbox_console.insert(END, str(max_campo))
                                                        else:
                                                            self.txtbox_console.insert(END, f">> Error en la función max. Todos los valores deben ser de tipo entero o decimal. Campo: {campo}", 'Error')
                                                    else:
                                                        self.txtbox_console.insert(END, ">> Error en la función max. No se han ingresado registros al programa.", 'Error')
                                                    self.txtbox_console.insert(END, "\n")
                                                    break
                                                pos += 1
                                            if not se_encontro:
                                                self.txtbox_console.insert(END, ">> Error en la función max. No se encontró el campo: " + campo + ".\n", 'Error')
                                            self.txtbox_console.config(state='disabled')
                                    else:
                                        self.panic_mode("max", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada max, la sintaxis de la función es inconclusa.")
                                    errores_encontrados.append(error)
                            else:
                                self.panic_mode("max", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada max, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("max", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada max, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            elif id_token == 14: # min
                campo = ""
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 1: # Cadena
                                campo = tokens_leidos[index].lexema
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 25: # Cierra paréntesis
                                        index += 1
                                        if index < (len(tokens_leidos) - 1):
                                            id_token = tokens_leidos[index].id_token
                                            if id_token == 21: # Punto y coma
                                                # Función min correcta
                                                self.txtbox_console.config(state='normal')
                                                pos = 0
                                                se_encontro = False
                                                for titulo in encabezados:
                                                    if titulo == campo:
                                                        se_encontro = True
                                                        min_campo = None
                                                        if len(registros)>0:
                                                            min_campo = registros[0][pos]
                                                            hay_cadenas = False
                                                            for fila in registros:
                                                                if type(fila[pos]) is int or type(fila[pos]) is float:
                                                                    if min_campo is not None:
                                                                        if fila[pos] > min_campo:
                                                                            min_campo = fila[pos]
                                                                    else:
                                                                        min_campo = fila[pos]
                                                                else:
                                                                    hay_cadenas = True
                                                                    break
                                                            if not hay_cadenas:
                                                                self.txtbox_console.insert(END, str(min_campo))
                                                            else:
                                                                self.txtbox_console.insert(END, f">> Error en la función min. Todos los valores deben ser de tipo entero o decimal. Campo: {campo}", 'Error')
                                                        else:
                                                            self.txtbox_console.insert(END, ">> Error en la función min. No se han ingresado registros al programa.", 'Error')
                                                        self.txtbox_console.insert(END, "\n")
                                                        break
                                                    pos += 1
                                                if not se_encontro:
                                                    self.txtbox_console.insert(END, ">> Error en la función min. No se encontró el campo: " + campo + ".\n", 'Error')
                                                self.txtbox_console.config(state='disabled')
                                                self.otra_ins()
                                            else:
                                                self.panic_mode("min", funcion=True)
                                        else:
                                            #FIN DE LECTURA DE TOKENS
                                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada min, no vino el token ';' que finaliza la función.", recuperado = True)
                                            errores_encontrados.append(error)
                                            self.txtbox_console.config(state='normal')
                                            pos = 0
                                            se_encontro = False
                                            for titulo in encabezados:
                                                if titulo == campo:
                                                    se_encontro = True
                                                    min_campo = None
                                                    if len(registros)>0:
                                                        min_campo = registros[0][pos]
                                                        hay_cadenas = False
                                                        for fila in registros:
                                                            if type(fila[pos]) is int or type(fila[pos]) is float:
                                                                if min_campo is not None:
                                                                    if fila[pos] > min_campo:
                                                                        min_campo = fila[pos]
                                                                else:
                                                                    min_campo = fila[pos]
                                                            else:
                                                                hay_cadenas = True
                                                                break
                                                        if not hay_cadenas:
                                                                self.txtbox_console.insert(END, str(min_campo))
                                                        else:
                                                            self.txtbox_console.insert(END, f">> Error en la función min. Todos los valores deben ser de tipo entero o decimal. Campo: {campo}", 'Error')
                                                    else:
                                                        self.txtbox_console.insert(END, ">> Error en la función min. No se han ingresado registros al programa.", 'Error')
                                                    self.txtbox_console.insert(END, "\n")
                                                    break
                                                pos += 1
                                            if not se_encontro:
                                                self.txtbox_console.insert(END, ">> Error en la función min. No se encontró el campo: " + campo + ".\n", 'Error')
                                            self.txtbox_console.config(state='disabled')
                                    else:
                                        self.panic_mode("min", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada min, la sintaxis de la función es inconclusa.")
                                    errores_encontrados.append(error)
                            else:
                                self.panic_mode("min", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada min, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("min", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada min, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            elif id_token == 15: # exportarReporte
                campo = ""
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 24: # Abre paréntesis
                        index += 1
                        if index < (len(tokens_leidos) - 1):
                            id_token = tokens_leidos[index].id_token
                            if id_token == 1: # Cadena
                                campo = tokens_leidos[index].lexema
                                index += 1
                                if index < (len(tokens_leidos) - 1):
                                    id_token = tokens_leidos[index].id_token
                                    if id_token == 25: # Cierra paréntesis
                                        index += 1
                                        if index < (len(tokens_leidos) - 1):
                                            id_token = tokens_leidos[index].id_token
                                            if id_token == 21: # Punto y coma
                                                # Función exportarReporte correcta
                                                self.txtbox_console.config(state='normal')
                                                generado = self.reporte_ejecucion(campo)
                                                if generado:
                                                    self.txtbox_console.insert(END, ">> Reporte generado con éxito (Reportes HTML/reporte.html)\n", 'Exito')
                                                else:
                                                    self.txtbox_console.insert(END, ">> Ocurrió un error en la generación del reporte\n", 'Error')
                                                self.txtbox_console.config(state='disabled')
                                                self.otra_ins()
                                            else:
                                                self.panic_mode("exportarReporte", funcion=True)
                                        else:
                                            #FIN DE LECTURA DE TOKENS
                                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada exportarReporte, no vino el token ';' que finaliza la función.", recuperado = True)
                                            errores_encontrados.append(error)
                                            self.txtbox_console.config(state='normal')
                                            generado = self.reporte_ejecucion(campo)
                                            if generado:
                                                self.txtbox_console.insert(END, ">> Reporte generado con éxito (Reportes HTML/reporte.html)\n", 'Exito')
                                            else:
                                                self.txtbox_console.insert(END, ">> Ocurrió un error en la generación del reporte\n", 'Error')
                                            self.txtbox_console.config(state='disabled')
                                    else:
                                        self.panic_mode("exportarReporte", funcion=True)
                                else:
                                    #FIN DE LECTURA DE TOKENS
                                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada exportarReporte, la sintaxis de la función es inconclusa.")
                                    errores_encontrados.append(error)
                            else:
                                self.panic_mode("exportarReporte", funcion=True)
                        else:
                            #FIN DE LECTURA DE TOKENS
                            error = Error("N/A", "Sintáctico", "Se encontró palabra reservada exportarReporte, la sintaxis de la función es inconclusa.")
                            errores_encontrados.append(error)
                    else:
                        self.panic_mode("exportarReporte", funcion=True)
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "Se encontró palabra reservada exportarReporte, la sintaxis de la función es inconclusa.")
                    errores_encontrados.append(error)
            else:
                error = Error("N/A", "Sintáctico", f"Se esperaba una palabra reservada. Vino token {tokens_leidos[index].nombre}.", lexema=tokens_leidos[index].lexema, fila=tokens_leidos[index].fila, columna=tokens_leidos[index].columna)
                errores_encontrados.append(error)
                index += 1
                self.inicio()
        else:
            #FIN DE LECTURA DE TOKENS
            pass

    def cadenas(self):
        global tokens_leidos
        global index
        global encabezados
        global flag_final
        index += 1
        flag_final = False
        if index < (len(tokens_leidos) - 1):
            id_token = tokens_leidos[index].id_token
            if id_token == 20: # Coma
                index += 1
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 1: # Cadena
                        encabezados.append(tokens_leidos[index].lexema)
                        sintax_error = self.cadenas()
                        if sintax_error is True:
                            return sintax_error
                    else:
                        self.panic_mode("Claves", ingreso_datos=True)
                        sintax_error = True
                        return sintax_error
                else:
                    #FIN DE LECTURA DE TOKENS
                    error = Error("N/A", "Sintáctico", "En la asignación de Claves, la sintaxis es inconclusa.", recuperado=True)
                    errores_encontrados.append(error)
                    flag_final = True
        else:
            #FIN DE LECTURA DE TOKENS
            error = Error("N/A", "Sintáctico", "En la asignación de Claves, no vino el token ']' que finaliza la asignación.", recuperado=True)
            errores_encontrados.append(error)
            flag_final = True
    
    def valor(self):
        # { valor } = { 1 valores | 2 valores | 3 valores }
        global tokens_leidos
        global index
        global registro_aux
        global flag_final
        index += 1
        sintax_error = False
        if index < (len(tokens_leidos) - 1):
            id_token = tokens_leidos[index].id_token
            if id_token == 1: # Cadena
                registro_aux.append(tokens_leidos[index].lexema)
                sintax_error = self.valores()
                if sintax_error is True:
                    return sintax_error
            elif id_token == 2: # Entero
                registro_aux.append(tokens_leidos[index].lexema)
                sintax_error = self.valores()
                if sintax_error is True:
                    return sintax_error
            elif id_token == 3: # Decimal
                registro_aux.append(tokens_leidos[index].lexema)
                sintax_error = self.valores()
                if sintax_error is True:
                    return sintax_error
            else:
                self.panic_mode("Registros", ingreso_datos=True)
                sintax_error = True
                return sintax_error
        else:
            flag_final = True
    
    def valores(self,):
        global tokens_leidos
        global index
        global flag_final
        index += 1
        if index < (len(tokens_leidos) - 1):
            id_token = tokens_leidos[index].id_token
            if id_token == 20: # Coma
                sintax_error = self.valor()
                if sintax_error is True:
                    return sintax_error
        else:
            flag_final = True

    def mult_registros(self):
        global tokens_leidos
        global index
        global registros
        global registro_aux
        global flag_final
        global errores_registros
        global encabezados
        index += 1
        if index < (len(tokens_leidos) - 1):
            id_token = tokens_leidos[index].id_token
            if id_token == 22: # Abre llave
                sintax_error = self.valor()
                if not sintax_error:
                    id_token = tokens_leidos[index].id_token
                    if id_token == 23: # Cierra Llave
                        # Registro leído correctamente
                        if len(registro_aux) == len(encabezados):
                            registros.append(registro_aux)
                        elif len(registro_aux) < len(encabezados):
                            for i in range(len(encabezados)-len(registro_aux)):
                                registro_aux.append(None)
                            registros.append(registro_aux)
                        else:
                            errores_registros += 1
                        registro_aux = []
                        sintax_error = self.mult_registros()
                        if sintax_error is True:
                            return sintax_error
                    else:
                        self.panic_mode("Registros", ingreso_datos=True)
                        sintax_error = True
                        return sintax_error
                else:
                    return sintax_error
        else:
            flag_final = True

    def otra_ins(self):
        global index
        index += 1
        if index < (len(tokens_leidos) - 1):
            self.inicio()
    
    def panic_mode(self, lexema_inicial, ingreso_datos = False, funcion = False, recuperado = False):
        global tokens_leidos
        global errores_encontrados
        global index
        global encabezados
        global registros

        if ingreso_datos:

            if lexema_inicial == "Claves":
                error = Error("N/A", "Sintáctico", f"En Claves, se encontró un token {tokens_leidos[index].nombre}, que ocasionó una sintaxis incorrecta.",
                            lexema=tokens_leidos[index].lexema, recuperado = recuperado, fila=tokens_leidos[index].fila, columna=tokens_leidos[index].columna)
                if len(encabezados) != 0 and not recuperado:
                    encabezados = []
            else:
                error = Error("N/A", "Sintáctico", f"En Registros, se encontró un token {tokens_leidos[index].nombre}, que ocasionó una sintaxis incorrecta.",
                            lexema=tokens_leidos[index].lexema, recuperado = recuperado, fila=tokens_leidos[index].fila, columna=tokens_leidos[index].columna)
                if len(registros) != 0 and not recuperado:
                    registros = []
            errores_encontrados.append(error)
            
            while True:
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 19: # Cierra Corchete - Token Sincronización
                        index += 1
                        self.inicio()
                        break
                else:
                    # FIN LECTURA DE TOKENS EN -PANIC MODE-
                    break
                index += 1

        elif funcion:
            
            error = Error("N/A", "Sintáctico", f"En {lexema_inicial}, se encontró un token {tokens_leidos[index].nombre}, que ocasionó una sintaxis incorrecta.",
                        lexema=tokens_leidos[index].lexema, recuperado = recuperado, fila=tokens_leidos[index].fila, columna=tokens_leidos[index].columna)
            errores_encontrados.append(error)
            
            while True:
                if index < (len(tokens_leidos) - 1):
                    id_token = tokens_leidos[index].id_token
                    if id_token == 21: # Punto y coma - Token Sincronización
                        index += 1
                        self.inicio()
                        break
                else:
                    # FIN LECTURA DE TOKENS EN -PANIC MODE-
                    break
                index += 1
        else:
            print("> ERROR Panic mode: No se mandó si el error es en ingreso_datos, o en función.")

    def reporte_ejecucion(self, titulo):
        global tokens_leidos
        global index
        global encabezados
        global registros
        html = f'''<!DOCTYPE html>
        <html lang="es">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <link rel="stylesheet" href="reporte.css" type="text/css" />
        <title>Reporte Datos Guardados</title>
        </head>
        <body>
        <header>
            <li><span class="material-icons md-dark md-100">summarize</span></li>
            <h1>{titulo}</h1>
        </header>
        <div class="container">
            <div class="tabla-reporte">
                <table class="table table-striped table-hover">
                    <thead style="background-color: black; color: white;">
                        <tr>\n'''
        for title in encabezados:
            html += f'<th scope="col">{title}</th>\n'
        html += '''</tr>\n</thead>\n<tbody>\n'''
        id_fila = ""
        registro_agregado = 0
        try:
            for registro in registros:
                registro_agregado += 1
                id_fila = "uno" if registro_agregado % 2 == 1 else "dos"
                html += f'<tr id="{id_fila}">\n'
                for element in registro:
                    if element is not None:
                        html += f'<td>{element}</td>\n'
                    else:
                        html += '<td>---</td>\n'
                html += '</tr>\n'
        except:
            traceback.print_exc()
            return False
        html += '''                    </tbody>
                </table>
            </div>
        </div>
        <footer>
            <p>Elías Abraham Vasquez Soto - 201900131</p>
            <p>Proyecto 2 - Laboratorio Lenguajes Formales y de Programación B-</p>        
            <img src="images/logo_usac.png" width="220" height="60"/>
        </footer>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        </body>
        </html>'''
        css = '''* {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Lato', sans-serif;
        }

        html {
            min-height: 100%;
            position: relative;
        }

        body {
            background-color:rgb(236, 239, 243);
            padding-top: 20px;
            margin-bottom: 150px;
        }

        /* ===== Iconos de Google ===== */
        /* Rules for sizing the icon. */
        .material-icons.md-24 { font-size: 24px; }
        .material-icons.md-30 { font-size: 30px; }
        .material-icons.md-100 { font-size: 100px; }
        /* Rules for using icons as black on a light background. */
        .material-icons.md-dark { color: rgba(0, 0, 0, 0.54); }
        .material-icons.md-dark.md-inactive { color: rgba(0, 0, 0, 0.26); }
        /* Rules for using icons as white on a dark background. */
        .material-icons.md-light { color: rgba(255, 255, 255, 1); }
        .material-icons.md-light.md-inactive { color: rgba(255, 255, 255, 0.3); }

        header {
            display: flex;
            justify-content: center;
            position: relative;
        }
        header h1 {
            font-size: 75px;
        }

        .container {
            background-color: rgb(6, 80, 99);
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 50px;
            margin: 30px 100px 30px 100px;
        }

        .tabla-reporte {
            padding-top: 20px;
            padding-left: 20px;
            padding-right: 40px;
            text-align: center;
            font-size: 20px;
            letter-spacing: 1px;
            overflow-x: scroll;
        }

        table {
            width: 100%;
            table-layout: fixed;
        }

        table thead{    
            color: white;
        }

        table td, th {
            width: 220px;
            vertical-align: middle;
        }

        #uno {
            background-color: rgb(221, 202, 177);
        }

        #dos {
            background-color: rgb(238, 236, 231);
        }

        footer {
            color: white;
            line-height: 10px;
            text-align: center;
            padding-top: 20px;
            padding-bottom: 5px;
            font-size: 15px;
            position: absolute;
            bottom: 0;
            width: 100%;
            background-image: url("images/footer.png");
        }'''
        try:
            reporte = open("Reportes HTML/reporte.html", "w",encoding="utf8")
            reporte.write(html)
            reporte.close()
            print("->HTML Reporte generado")
            css_reporte = open("Reportes HTML/reporte.css", "w",encoding="utf8")
            css_reporte.write(css)
            css_reporte.close()
            print("->CSS Reporte generado")
            return True
        except:
            traceback.print_exc()
            return False

    def reporte(self, value):
        if value == "1":
            tokens_generados = self.reporte_tokens()
            if tokens_generados:
                messagebox.showinfo("Reporte de tokens", "Reporte de Tokens generado exitosamente.")
            else:
                messagebox.showerror("Reporte de tokens", "Ocurrió un error en la generación del reporte :(")
        elif value == "2":
            errores_generados = self.reporte_errores()
            if errores_generados:
                messagebox.showinfo("Reporte de errores", "Reporte de Errores generado exitosamente.")
            else:
                messagebox.showerror("Reporte de errores", "Ocurrió un error en la generación del reporte :(")
        elif value == "3":
            print("Reporte Arbol")
        else:
            print("Error: VALUE de reporte no reconocido.")
    
    def reporte_tokens(self):
        global tokens_leidos
        html = '''<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <link rel="stylesheet" href="tokens.css" type="text/css" />
            <title>Reporte Tokens</title>
        </head>
        <body>
            <li style="float: left; padding-left: 25%; padding-right: 20px;"><span class="material-icons md-light md-100">generating_tokens</span></li>
            <h1>Reporte de Tokens</h1>
            <div class="datos-reporte">
                <div class="tabla-tokens">
                    <table class="table table-striped table-hover">
                        <thead style="background-color: black; color: white;">
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">Id Token</th>
                            <th scope="col">Token</th>
                            <th scope="col">Lexema</th>
                            <th scope="col">Fila</th>
                            <th scope="col">Columna</th>
                            </tr>
                        </thead>
                        <tbody>'''
        token_agregado = 0
        id_fila = ""
        try:
            for token in tokens_leidos:
                token_agregado += 1
                id_fila = "uno" if token_agregado % 2 == 1 else "dos"
                html += f'''\n<tr id="{id_fila}">
                <th scope="row">{token_agregado}</th>
                <td>{token.id_token}</td>
                <td>{token.nombre}</td>
                <td>{token.lexema}</td>
                <td>{token.fila}</td>
                <td>{token.columna}</td>
                </tr>'''
        except:
            traceback.print_exc()
            return False
        html += '''\n</tbody>
                    </table>
                </div>
            </div>
            <footer>
                <p>Elías Abraham Vasquez Soto - 201900131</p>
                <p>Proyecto 2 - Laboratorio Lenguajes Formales y de Programación B-</p>        
                <img src="images/logo_usac.png" width="220" height="60"/>
            </footer>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        </body>
        </html>'''
        css = '''html {
            min-height: 100%;
            position: relative;
        }

        body {
            background-color:rgb(1, 11, 26);
            padding-top: 20px;
            margin-bottom: 150px;
        }

        /* ===== Iconos de Google ===== */
        /* Rules for sizing the icon. */
        .material-icons.md-24 { font-size: 24px; }
        .material-icons.md-30 { font-size: 30px; }
        .material-icons.md-100 { font-size: 100px; }
        /* Rules for using icons as black on a light background. */
        .material-icons.md-dark { color: rgba(0, 0, 0, 0.54); }
        .material-icons.md-dark.md-inactive { color: rgba(0, 0, 0, 0.26); }
        /* Rules for using icons as white on a dark background. */
        .material-icons.md-light { color: rgba(255, 255, 255, 1); }
        .material-icons.md-light.md-inactive { color: rgba(255, 255, 255, 0.3); }

        h1 {
            color: white;
            font-family: 'Lato', sans-serif;
            font-size: 75px;
        }

        .datos-reporte {
            background-color: rgb(255, 255, 255);
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 50px;
            margin: 30px 100px 30px 100px;
        }

        .tabla-tokens {
            padding-top: 20px;
            padding-left: 20px;
            padding-right: 40px;
            text-align: center;
            font-family: 'Lato', sans-serif;
            font-size: 20px;
            letter-spacing: 1px;
        }

        table td{    
            color: white;
        }

        table th{    
            color: white;
        }

        #uno {
            background-color: rgb(61, 57, 48);
        }

        #dos {
            background-color: rgb(54, 1, 1);
        }

        footer {
            color: white;
            line-height: 10px;
            text-align: center;
            padding-top: 20px;
            padding-bottom: 5px;
            font-size: 15px;
            font-family: 'Lato', sans-serif;
            position: absolute;
            bottom: 0;
            width: 100%;
            background-image: url("images/footer.png");
        }'''
        try:
            reporte_tokens = open("Reportes HTML/tokens.html", "w",encoding="utf8")
            reporte_tokens.write(html)
            reporte_tokens.close()
            print("->HTML Tokens generado")
            css_tokens = open("Reportes HTML/tokens.css", "w",encoding="utf8")
            css_tokens.write(css)
            css_tokens.close()
            print("->CSS Tokens generado")
            return True
        except:
            traceback.print_exc()
            return False

    def reporte_errores(self):
        global errores_encontrados
        html = '''<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <link rel="stylesheet" href="errores.css" type="text/css" />
            <title>Reporte Errores</title>
        </head>
        <body>
            <li style="float: left; padding-left: 25%; padding-right: 20px;"><span class="material-icons md-light md-100">error</span></li>
            <h1>Reporte de Errores</h1>
        <div class="datos-reporte">
            <h2 style="color: black;">Errores Léxicos</h2>
            <div class="tabla-errores">
                <table class="table table-striped table-hover">
                    <thead style="background-color: black; color: white;">
                        <tr>
                        <th scope="col">#</th>
                        <th scope="col">Caracter</th>
                        <th scope="col">Descripcion</th>
                        <th scope="col">Fila</th>
                        <th scope="col">Columna</th>
                        </tr>
                    </thead>
                    <tbody>'''
        error_agregado = 0
        id_fila = ""
        try:
            for error in errores_encontrados:
                if error.tipo == "Léxico":
                    error_agregado += 1
                    id_fila = "uno" if error_agregado % 2 == 1 else "dos"
                    html += f'''\n<tr id="{id_fila}">
                    <th scope="row">{error_agregado}</th>
                    <td>{error.caracter}</td>
                    <td>{error.descripcion}</td>
                    <td>{error.fila}</td>
                    <td>{error.columna}</td>
                    </tr>'''
        except:
            traceback.print_exc()
            return False
        html += '''\n</tbody>
                    </table>
                </div>
            </div>

        <div class="datos-reporte">
            <h2 style="color: black;">Errores Sintácticos</h2>
            <div class="tabla-errores">
                <table class="table table-striped table-hover">
                    <thead style="background-color: black; color: white;">
                        <tr>
                        <th scope="col">#</th>
                        <th scope="col">Caracter/Lexema</th>
                        <th scope="col">Descripcion</th>
                        <th scope="col">Recuperado</th>
                        <th scope="col">Fila</th>
                        <th scope="col">Columna</th>
                        </tr>
                    </thead>
                    <tbody>'''
        error_agregado = 0
        id_fila = ""
        try:
            for error in errores_encontrados:
                if error.tipo == "Sintáctico":
                    error_agregado += 1
                    id_fila = "uno" if error_agregado % 2 == 1 else "dos"
                    html += f'''\n<tr id="{id_fila}">
                    <th scope="row">{error_agregado}</th>\n'''
                    if error.lexema:
                        html += f'<td>{error.lexema}</td>\n'
                    else:
                        html += f'<td>{error.caracter}</td>\n'
                    html += f'<td>{error.descripcion}</td>\n'
                    if error.recuperado:
                        html += '<td>Recuperado</td>\n'
                    else:
                        html += '<td>No</td>\n'
                    html += f'''<td>{error.fila}</td>
                    <td>{error.columna}</td>
                    </tr>'''
        except:
            traceback.print_exc()
            return False
        html += '''\n</tbody>
                    </table>
                </div>
            </div>

            <footer>
                <p>Elías Abraham Vasquez Soto - 201900131</p>
                <p>Proyecto 2 - Laboratorio Lenguajes Formales y de Programación B-</p>        
                <img src="images/logo_usac.png" width="220" height="60"/>
            </footer>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        </body>
        </html>'''
        
        css = '''html {
            min-height: 100%;
            position: relative;
        }

        body {
            background-color:rgb(54, 1, 1);
            padding-top: 20px;
            margin-bottom: 150px;
        }

        /* ===== Iconos de Google ===== */
        /* Rules for sizing the icon. */
        .material-icons.md-24 { font-size: 24px; }
        .material-icons.md-30 { font-size: 30px; }
        .material-icons.md-100 { font-size: 100px; }
        /* Rules for using icons as black on a light background. */
        .material-icons.md-dark { color: rgba(0, 0, 0, 0.54); }
        .material-icons.md-dark.md-inactive { color: rgba(0, 0, 0, 0.26); }
        /* Rules for using icons as white on a dark background. */
        .material-icons.md-light { color: rgba(255, 255, 255, 1); }
        .material-icons.md-light.md-inactive { color: rgba(255, 255, 255, 0.3); }


        h1 {
            color: white;
            font-family: 'Lato', sans-serif;
            font-size: 75px;
        }

        .datos-reporte {
            background-color: rgb(255, 255, 255);
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 50px;
            margin: 30px 100px 30px 100px;
        }

        .tabla-errores {
            padding-top: 20px;
            padding-left: 20px;
            padding-right: 40px;
            text-align: center;
            font-family: 'Lato', sans-serif;
            font-size: 20px;
            letter-spacing: 1px;
        }

        table td{    
            color: white;
        }

        table th{    
            color: white;
        }

        #uno {
            background-color: rgb(61, 57, 48);
        }

        #dos {
            background-color: rgb(9, 2, 41);
        }

        footer {
            color: white;
            line-height: 10px;
            text-align: center;
            padding-top: 20px;
            padding-bottom: 5px;
            font-size: 15px;
            font-family: 'Lato', sans-serif;
            position: absolute;
            bottom: 0;
            width: 100%;
            background-image: url("images/footer.png");
        }'''
        try:
            reporte_errores = open("Reportes HTML/errores.html", "w",encoding="utf8")
            reporte_errores.write(html)
            reporte_errores.close()
            print("->HTML Errores generado")
            css_errores = open("Reportes HTML/errores.css", "w",encoding="utf8")
            css_errores.write(css)
            css_errores.close()
            print("->CSS Errores generado")
            return True
        except:
            traceback.print_exc()
            return False

if __name__ == "__main__":
    ventana = Tk()
    app = Interfaz(ventana)
    ventana.mainloop()
    