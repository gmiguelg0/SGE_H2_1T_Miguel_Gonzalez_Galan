import pymysql
from pymysql.err import OperationalError

def create_connection():
    """Establece la conexión con la base de datos ENCUESTAS."""
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",          # Cambia por tu usuario
            password="curso",   # Cambia por tu contraseña
            database="ENCUESTAS",       # Base de datos ENCUESTAS
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Conexión exitosa a la base de datos ENCUESTAS")
        return connection
    except OperationalError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_connection(connection):
    """Cierra la conexión a la base de datos."""
    if connection and connection.open:
        connection.close()
        print("Conexión cerrada")

# Funciones CRUD básicas
def create_encuesta(connection, datos):
    """
    Inserta una nueva encuesta en la base de datos.
    :param connection: Conexión activa
    :param datos: Lista o tupla con los datos de la encuesta
    """
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO ENCUESTA (idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, 
                                  BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, 
                                  ProblemasDigestivos, TensionAlta, DolorCabeza) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, datos)
        connection.commit()
        print("Encuesta creada exitosamente")
    except Exception as e:
        print(f"Error al crear la encuesta: {e}")

def read_encuestas(connection, order_by=None, filter_by=None):
    """Lee todas las encuestas de la base de datos con opciones de ordenación y filtrado."""
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM ENCUESTA"
            if filter_by:
                query += f" WHERE {filter_by}"
            if order_by:
                query += f" ORDER BY {order_by}"
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error al leer las encuestas: {e}")
        return []

def update_encuesta(connection, datos):
    """
    Actualiza una encuesta en la base de datos.
    :param connection: Conexión activa
    :param datos: Lista o tupla con los datos de la encuesta
    """
    try:
        with connection.cursor() as cursor:
            query = """
            UPDATE ENCUESTA SET edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s, 
                                BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, 
                                DiversionDependenciaAlcohol=%s, ProblemasDigestivos=%s, TensionAlta=%s, 
                                DolorCabeza=%s WHERE idEncuesta=%s
            """
            cursor.execute(query, datos)
        connection.commit()
        print("Encuesta actualizada exitosamente")
    except Exception as e:
        print(f"Error al actualizar la encuesta: {e}")

def delete_encuesta(connection, idEncuesta):
    """Elimina una encuesta de la base de datos."""
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM ENCUESTA WHERE idEncuesta=%s"
            cursor.execute(query, (idEncuesta,))
        connection.commit()
        print("Encuesta eliminada exitosamente")
    except Exception as e:
        print(f"Error al eliminar la encuesta: {e}")