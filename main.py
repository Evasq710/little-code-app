from tkinter import *
from tkinter import filedialog
import traceback

texto_cargado = False
texto_lfp = ""

class Interfaz:
    def __init__(self, window):
        self.window = window
        self.window.title('Bitxelart')        
        self.window.state('zoomed')

        self.frame = Frame(self.window, bg="black")
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)

        imagen = PhotoImage(file = "images/logo.png")
        logo = Label(self.frame, image = imagen, bg="black")
        logo.photo = imagen
        logo.place(x=100, y=50, width=200, height=100)

        title = Label(self.frame, text="Proyecto 2", font=("Ebrima", 60, "bold"), bg="black", fg="white")
        title.place(x=575, y=50)

        frame_btn = Frame(self.frame, bg="black")
        frame_btn.place(x=410, y=175)

        img1 = PhotoImage(file = "images/upload.png")
        play = Label(frame_btn, image = img1, bg="black")
        play.photo = img1
        play.grid(row=0, column=0, padx=10)

        abrir_btn = Button(frame_btn, text="Abrir Archivo", font=("Ebrima", 15), bg="steel blue", command = lambda:[self.abrirArchivo()])
        abrir_btn.grid(row=0, column=1)

        sep1 = Label(frame_btn, text="", bg="black")
        sep1.grid(row=0, column=2, padx=30)

        img2 = PhotoImage(file = "images/play.png")
        play = Label(frame_btn, image = img2, bg="black")
        play.photo = img2
        play.grid(row=0, column=3, padx=5)

        analizar_btn = Button(frame_btn, text="Analizar Código", font=("Ebrima", 15), bg="steel blue", command = lambda:[])
        analizar_btn.grid(row=0, column=4)

        sep2 = Label(frame_btn, text="", bg="black")
        sep2.grid(row=0, column=5, padx=30)

        img3 = PhotoImage(file = "images/html.png")
        play = Label(frame_btn, image = img3, bg="black")
        play.photo = img3
        play.grid(row=0, column=6, padx=10)

        reportes_btn = Button(frame_btn, text="Reportes", font=("Ebrima", 15), bg="steel blue", command = lambda:[])
        reportes_btn.grid(row=0, column=7)

    def abrirArchivo(self):
        global texto_lfp
        global texto_cargado
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
            texto += "$"
            texto_lfp = ""
            texto_lfp = texto
            texto_cargado = True
            print("->Archivo leído con éxito")
            print(texto_lfp)
            
            #TODO Archivo en Textbox

            archivo.close()
            
        except Exception:
            traceback.print_exc()
            print("->No se seleccionó un archivo")

if __name__ == "__main__":
    ventana = Tk()
    app = Interfaz(ventana)
    ventana.mainloop()
    