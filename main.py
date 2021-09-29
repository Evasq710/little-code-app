from tkinter import *

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

if __name__ == "__main__":
    ventana = Tk()
    app = Interfaz(ventana)
    ventana.mainloop()
    