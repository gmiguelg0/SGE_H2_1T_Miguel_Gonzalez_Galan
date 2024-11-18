import tkinter as tk
from gui import EncuestasApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1400x900")  # Ajusta la ventana para aprovechar más espacio
    app = EncuestasApp(root)
    root.mainloop()
