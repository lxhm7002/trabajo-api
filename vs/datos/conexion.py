import sqlite3
from auxiliares.constantes import DB_NAME

class ConexionDB:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self._conectar()
        self._inicializar_tablas()

    def _conectar(self):
        try:
            self.conn = sqlite3.connect(DB_NAME)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error al conectar:", e)

    def _inicializar_tablas(self):
        try:
            with open("base_datos/ddl_usuarios.sql", "r") as f:
                self.cursor.executescript(f.read())
            self.conn.commit()
        except Exception as e:
            print("Error creando tablas:", e)

    def get_conn(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()