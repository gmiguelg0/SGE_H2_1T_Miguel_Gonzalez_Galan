# Gestión de Encuestas

Esta aplicación permite gestionar encuestas relacionadas con el consumo de alcohol y su impacto en la salud. Incluye funcionalidades de operaciones CRUD, exportación a Excel, filtros, y visualización de datos mediante gráficos.

## Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación](#instalación)
3. [Configuración de la Base de Datos MySQL](#configuración-de-la-base-de-datos-mysql)
4. [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
5. [Uso](#uso)
   - Operaciones CRUD
   - Exportación a Excel
   - Visualización de Gráficos
6. [Archivos del Proyecto](#archivos-del-proyecto)

---

## Requisitos del Sistema

Asegúrate de contar con lo siguiente en tu entorno:

- **Python**: Versión 3.10 o superior.
- **MySQL Server**.
- Librerías de Python:
  - `pymysql`
  - `tkinter` (incluido en la mayoría de las distribuciones de Python)
  - `matplotlib`
  - `pandas`

## Instalación

1. **Clonar el proyecto o copiar los archivos**:
   Descarga los archivos `db_connection.py`, `gui.py` y `app.py` y colócalos en un mismo directorio.

2. **Instalar las dependencias**:
   Abre una terminal en el directorio del proyecto y ejecuta:

   ```bash
   pip install pymysql matplotlib pandas
   
3. **Configuración de la Base de Datos MySQL**:
Crear la base de datos y la tabla: Conéctate a tu servidor MySQL y ejecuta los siguientes comandos para crear la base de datos y la tabla necesaria:

CREATE DATABASE ENCUESTAS;

USE ENCUESTAS;

CREATE TABLE ENCUESTA (
    idEncuesta INT PRIMARY KEY,
    edad INT,
    Sexo VARCHAR(7),
    BebidasSemana INT,
    CervezasSemana INT,
    BebidasFinSemana INT,
    BebidasDestiladasSemana INT,
    VinosSemana INT,
    PerdidasControl INT,
    DiversionDependenciaAlcohol CHAR(2),
    ProblemasDigestivos CHAR(2),
    TensionAlta CHAR(12),
    DolorCabeza CHAR(12)
);
Configurar las credenciales en db_connection.py: Abre el archivo db_connection.py y actualiza las credenciales según tu configuración:

connection = pymysql.connect(
    host="localhost",
    user="tu_usuario",       # Cambia por tu usuario de MySQL
    password="tu_contraseña", # Cambia por tu contraseña de MySQL
    database="ENCUESTAS",
    cursorclass=pymysql.cursors.DictCursor
)
4. **Ejecución de la Aplicación**:
Abre una terminal en el directorio del proyecto.

Ejecuta el archivo app.py:


python app.py
La interfaz gráfica se abrirá automáticamente.

5. **Uso**:
1. Operaciones CRUD
Añadir Encuesta: Haz clic en "Añadir Encuesta", completa el formulario y guarda los datos.
Actualizar Encuesta: Selecciona una encuesta de la tabla, haz clic en "Actualizar Encuesta", edita los datos y guárdalos.
Eliminar Encuesta: Selecciona una encuesta de la tabla y haz clic en "Eliminar Encuesta".
Filtrar Encuestas: Haz clic en "Filtrar Encuestas", introduce el campo y valor del filtro y aplica.
2. Exportación a Excel
Haz clic en "Exportar a Excel".
Selecciona una ubicación y un nombre para el archivo.
Los datos se guardarán en un archivo .xlsx.
3. Visualización de Gráficos
Consumo por Grupo de Edad: Ve a "Visualizar Gráficos" > "Consumo por Grupo de Edad" para ver el consumo promedio por edad.
Correlación Alcohol y Salud: Ve a "Visualizar Gráficos" > "Correlación Alcohol y Salud" para ver los efectos de consumo alto de alcohol en la salud.
Archivos del Proyecto
db_connection.py: Configuración de la conexión MySQL y funciones CRUD.
gui.py: Interfaz gráfica con operaciones y gráficos.
app.py: Archivo principal que ejecuta la aplicación.
