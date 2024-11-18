import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import create_connection, create_encuesta, read_encuestas, update_encuesta, delete_encuesta, close_connection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import create_connection, create_encuesta, read_encuestas, update_encuesta, delete_encuesta, close_connection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd  # Importar pandas para la exportación a Excel

class EncuestasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Encuestas")
        self.root.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        # Menú
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Botones principales
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=10)
        
        button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 12), "width": 15, "height": 2}
        
        tk.Button(frame, text="Añadir Encuesta", command=self.add_encuesta, **button_style).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Actualizar Encuesta", command=self.update_encuesta, **button_style).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Eliminar Encuesta", command=self.delete_encuesta, **button_style).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Filtrar Encuestas", command=self.filter_encuestas, **button_style).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Exportar a Excel", command=self.export_to_excel, **button_style).grid(row=0, column=4, padx=5)  # Nuevo botón
        tk.Button(frame, text="Visualizar Gráficos", command=self.show_visualization_menu, **button_style).grid(row=0, column=5, padx=5)
        tk.Button(frame, text="Volver", command=self.load_data, **button_style).grid(row=0, column=6, padx=5)
        
        # Tabla para mostrar encuestas
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4CAF50", foreground="black")
        style.configure("Treeview", font=("Arial", 10), rowheight=20)
        
        self.tree = ttk.Treeview(self.root, columns=("idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", 
                                                     "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", 
                                                     "PerdidasControl", "DiversionDependenciaAlcohol", 
                                                     "ProblemasDigestivos", "TensionAlta", "DolorCabeza"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_by(_col))
            self.tree.column(col, width=100, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 50))
        
        self.load_data()

    def load_data(self, order_by=None, filter_by=None):
        connection = create_connection()
        if connection:
            encuestas = read_encuestas(connection, order_by, filter_by)
            for row in self.tree.get_children():
                self.tree.delete(row)
            for encuesta in encuestas:
                self.tree.insert("", "end", values=(encuesta["idEncuesta"], encuesta["edad"], encuesta["Sexo"], 
                                                    encuesta["BebidasSemana"], encuesta["CervezasSemana"], 
                                                    encuesta["BebidasFinSemana"], encuesta["BebidasDestiladasSemana"], 
                                                    encuesta["VinosSemana"], encuesta["PerdidasControl"], 
                                                    encuesta["DiversionDependenciaAlcohol"], encuesta["ProblemasDigestivos"], 
                                                    encuesta["TensionAlta"], encuesta["DolorCabeza"]))
            close_connection(connection)

    def export_to_excel(self):
        """Exporta los datos actuales de la tabla a un archivo Excel."""
        # Obtener los datos de la tabla
        data = []
        for item in self.tree.get_children():
            data.append(self.tree.item(item)["values"])

        # Crear un DataFrame de pandas
        df = pd.DataFrame(data, columns=["idEncuesta", "edad", "Sexo", "BebidasSemana", "CervezasSemana", 
                                         "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", 
                                         "PerdidasControl", "DiversionDependenciaAlcohol", 
                                         "ProblemasDigestivos", "TensionAlta", "DolorCabeza"])

        # Guardar el DataFrame en un archivo Excel
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {file_path}")

    def load_data(self, order_by=None, filter_by=None):
        connection = create_connection()
        if connection:
            encuestas = read_encuestas(connection, order_by, filter_by)
            for row in self.tree.get_children():
                self.tree.delete(row)
            for encuesta in encuestas:
                self.tree.insert("", "end", values=(encuesta["idEncuesta"], encuesta["edad"], encuesta["Sexo"], 
                                                    encuesta["BebidasSemana"], encuesta["CervezasSemana"], 
                                                    encuesta["BebidasFinSemana"], encuesta["BebidasDestiladasSemana"], 
                                                    encuesta["VinosSemana"], encuesta["PerdidasControl"], 
                                                    encuesta["DiversionDependenciaAlcohol"], encuesta["ProblemasDigestivos"], 
                                                    encuesta["TensionAlta"], encuesta["DolorCabeza"]))
            close_connection(connection)

    def add_encuesta(self):
        self.edit_encuesta()

    def update_encuesta(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una encuesta para actualizar.")
            return
        item = self.tree.item(selected_item)
        self.edit_encuesta(item["values"])

    def delete_encuesta(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una encuesta para eliminar.")
            return
        item = self.tree.item(selected_item)
        idEncuesta = item["values"][0]
        if messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar esta encuesta?"):
            connection = create_connection()
            if connection:
                delete_encuesta(connection, idEncuesta)
                close_connection(connection)
                self.load_data()

    def filter_encuestas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Filtrar Encuestas")
        ventana.configure(bg="#f0f0f0")
        
        tk.Label(ventana, text="Campo:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        campo_entry = tk.Entry(ventana, font=("Arial", 12))
        campo_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(ventana, text="Valor:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        valor_entry = tk.Entry(ventana, font=("Arial", 12))
        valor_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def aplicar_filtro():
            campo = campo_entry.get()
            valor = valor_entry.get()
            filtro = f"{campo}='{valor}'"
            self.load_data(filter_by=filtro)
            ventana.destroy()
        
        tk.Button(ventana, text="Aplicar Filtro", command=aplicar_filtro, bg="#4CAF50", fg="white", 
                 font=("Arial", 12), width=15, height=2).grid(row=2, column=0, columnspan=2, pady=10)

    def sort_by(self, col):
        self.load_data(order_by=col)

    def edit_encuesta(self, values=None):
        ventana = tk.Toplevel(self.root)
        ventana.title("Añadir/Editar Encuesta")
        ventana.configure(bg="#f0f0f0")
        
        labels = ["ID Encuesta", "Edad", "Sexo", "Bebidas Semana", "Cervezas Semana", "Bebidas Fin de Semana", 
                  "Bebidas Destiladas Semana", "Vinos Semana", "Pérdidas de Control", "Diversión Dependencia Alcohol", 
                  "Problemas Digestivos", "Tensión Alta", "Dolor de Cabeza"]
        entries = []
        
        for i, label in enumerate(labels):
            tk.Label(ventana, text=label, bg="#f0f0f0", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            if label in ["Sexo", "Dolor de Cabeza", "Tensión Alta", "Problemas Digestivos", "Diversión Dependencia Alcohol"]:
                options = {
                    "Sexo": ["Masculino", "Femenino", "Otro"],
                    "Dolor de Cabeza": ["Muy a menudo", "Alguna vez", "Nunca"],
                    "Tensión Alta": ["Sí", "No", "No lo sé"],
                    "Problemas Digestivos": ["Sí", "No"],
                    "Diversión Dependencia Alcohol": ["Sí", "No"]
                }
                var = tk.StringVar(ventana)
                combobox = ttk.Combobox(ventana, textvariable=var, values=options[label], font=("Arial", 12), state="readonly")
                combobox.grid(row=i, column=1, padx=10, pady=5)
                if values:
                    combobox.set(values[i])
                entries.append(var)
            else:
                entry = tk.Entry(ventana, font=("Arial", 12))
                entry.grid(row=i, column=1, padx=10, pady=5)
                if values:
                    entry.insert(0, values[i])
                entries.append(entry)

        def save_encuesta():
            datos = tuple(entry.get() if isinstance(entry, tk.Entry) else entry.get() for entry in entries)
            connection = create_connection()
            if connection:
                if values:
                    update_encuesta(connection, datos[1:] + (datos[0],))
                else:
                    create_encuesta(connection, datos)
                close_connection(connection)
                ventana.destroy()
                self.load_data()
                messagebox.showinfo("Éxito", "Encuesta guardada correctamente")

        tk.Button(ventana, text="Guardar", command=save_encuesta, bg="#4CAF50", fg="white", 
                 font=("Arial", 12), width=15, height=2).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def show_visualization_menu(self):
        """Muestra el menú de visualización de gráficos"""
        vis_window = tk.Toplevel(self.root)
        vis_window.title("Visualización de Datos")
        vis_window.geometry("300x200")
        vis_window.configure(bg="#f0f0f0")

        button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 12), "width": 25, "height": 2}

        tk.Button(
            vis_window, 
            text="Consumo por Grupo de Edad", 
            command=lambda: self.show_age_consumption_graph(vis_window),
            **button_style
        ).pack(pady=20)

        tk.Button(
            vis_window, 
            text="Correlación Alcohol y Salud", 
            command=lambda: self.show_health_correlation_graph(vis_window),
            **button_style
        ).pack(pady=20)

    def show_age_consumption_graph(self, parent_window):
        """Muestra gráfico de consumo por grupo de edad"""
        graph_window = tk.Toplevel(parent_window)
        graph_window.title("Consumo por Grupo de Edad")
        graph_window.geometry("800x600")

        connection = create_connection()
        if connection:
            encuestas = read_encuestas(connection)
            close_connection(connection)

            # Procesar datos
            ages = []
            consumption = []
            for encuesta in encuestas:
                ages.append(int(encuesta['edad']))
                total_consumption = (
                    float(encuesta['BebidasSemana']) +
                    float(encuesta['CervezasSemana']) +
                    float(encuesta['BebidasFinSemana']) +
                    float(encuesta['BebidasDestiladasSemana']) +
                    float(encuesta['VinosSemana'])
                )
                consumption.append(total_consumption)

            # Crear grupos de edad
            age_groups = ['18-25', '26-35', '36-45', '46+']
            group_consumption = {group: [] for group in age_groups}

            for age, cons in zip(ages, consumption):
                if 18 <= age <= 25:
                    group_consumption['18-25'].append(cons)
                elif 26 <= age <= 35:
                    group_consumption['26-35'].append(cons)
                elif 36 <= age <= 45:
                    group_consumption['36-45'].append(cons)
                else:
                    group_consumption['46+'].append(cons)

            # Calcular promedios
            averages = [np.mean(group_consumption[group]) if group_consumption[group] else 0 
                       for group in age_groups]

            # Crear gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(age_groups, averages)
            ax.set_title('Consumo Promedio de Alcohol por Grupo de Edad')
            ax.set_xlabel('Grupo de Edad')
            ax.set_ylabel('Consumo Promedio (Bebidas/Semana)')

            # Añadir valores sobre las barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}',
                       ha='center', va='bottom')

            # Mostrar gráfico en Tkinter
            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_health_correlation_graph(self, parent_window):
        """Muestra gráfico de correlación entre consumo de alcohol y problemas de salud"""
        graph_window = tk.Toplevel(parent_window)
        graph_window.title("Correlación Alcohol y Salud")
        graph_window.geometry("800x600")

        connection = create_connection()
        if connection:
            encuestas = read_encuestas(connection)
            close_connection(connection)

            # Procesar datos para el gráfico circular
            health_issues = {
                'Problemas Digestivos': 0,
                'Tensión Alta': 0,
                'Dolor de Cabeza': 0
            }
            
            total_high_consumption = 0
            
            for encuesta in encuestas:
                total_consumption = (
                    float(encuesta['BebidasSemana']) +
                    float(encuesta['CervezasSemana']) +
                    float(encuesta['BebidasFinSemana']) +
                    float(encuesta['BebidasDestiladasSemana']) +
                    float(encuesta['VinosSemana'])
                )
                
                if total_consumption > 10:  # Consideramos consumo alto
                    total_high_consumption += 1
                    if encuesta['ProblemasDigestivos'] == 'Sí':
                        health_issues['Problemas Digestivos'] += 1
                    if encuesta['TensionAlta'] == 'Sí':
                        health_issues['Tensión Alta'] += 1
                    if encuesta['DolorCabeza'] == 'Muy a menudo':
                        health_issues['Dolor de Cabeza'] += 1

            # Calcular porcentajes
            if total_high_consumption > 0:
                sizes = [
                    (health_issues[issue] / total_high_consumption) * 100 
                    for issue in health_issues
                ]
            else:
                sizes = [0, 0, 0]

            # Crear gráfico circular
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(sizes, labels=list(health_issues.keys()), autopct='%1.1f%%')
            ax.set_title('Problemas de Salud en Consumidores de Alto Nivel')

            # Mostrar gráfico en Tkinter
            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)