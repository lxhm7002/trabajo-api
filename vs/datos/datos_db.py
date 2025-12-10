import sqlite3
from datos.conexion import ConexionDB
from modelos.modelo import Tarea, Usuario

class DatosDB:

    def __init__(self):
        self.db = ConexionDB()

    # ===========================================
    #                USUARIOS
    # ===========================================
    def insertar_usuario_local(self, usuario: Usuario):
        conn = self.db.get_conn()
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (id, name, username, email, encrypted_password)
                VALUES (?, ?, ?, ?, ?)
            """, (usuario.id, usuario.name, usuario.username, usuario.email, usuario.encrypted_password))
            conn.commit()
            return True
        except Exception as e:
            print("Error usuario:", e)
            return False

    def obtener_usuario_por_email(self, email):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT id, name, username, email, encrypted_password FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row:
            return Usuario(*row)
        return None

    # ===========================================
    #             GET API → INSERTAR
    # ===========================================
    def insertar_tareas_api(self, tareas: list[dict]):
        conn = self.db.get_conn()
        cursor = self.db.get_cursor()

        try:
            for tarea_dict in tareas:

                # Si el usuario eliminó esta tarea API, NO reinsertarla
                cursor.execute("SELECT id FROM eliminadas WHERE id = ?", (tarea_dict["id"],))
                if cursor.fetchone():
                    continue

                # Buscar si existe
                cursor.execute("SELECT id FROM todos WHERE id = ?", (tarea_dict["id"],))
                existe = cursor.fetchone()

                if existe:
                    cursor.execute("""
                        UPDATE todos
                        SET userId=?, title=?, completed=?
                        WHERE id=?
                    """, (
                        tarea_dict["userId"],
                        tarea_dict["title"],
                        tarea_dict["completed"],
                        tarea_dict["id"]
                    ))
                else:
                    cursor.execute("""
                        INSERT INTO todos (userId, id, title, completed)
                        VALUES (?, ?, ?, ?)
                    """, (
                        tarea_dict["userId"],
                        tarea_dict["id"],
                        tarea_dict["title"],
                        tarea_dict["completed"]
                    ))

            conn.commit()
            return "Tareas API sincronizadas."

        except Exception as e:
            print("Error API DB:", e)
            return "Error insertando API."

    # ===========================================
    #                   CRUD LOCAL
    # ===========================================
    def crear_tarea_local(self, tarea_dict):
        conn = self.db.get_conn()
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO todos (userId, id, title, completed)
                VALUES (?, ?, ?, ?)
            """, (
                tarea_dict["userId"],
                tarea_dict["id"],
                tarea_dict["title"],
                tarea_dict["completed"]
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error crear local:", e)
            return False

    def actualizar_tarea_local(self, tarea_dict):
        conn = self.db.get_conn()
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                UPDATE todos
                SET title=?, completed=?
                WHERE id=?
            """, (
                tarea_dict["title"],
                tarea_dict["completed"],
                tarea_dict["id"]
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error actualizar local:", e)
            return False

    def eliminar_tarea_local(self, tarea_id):
        conn = self.db.get_conn()
        cursor = self.db.get_cursor()
        try:
            cursor.execute("INSERT OR IGNORE INTO eliminadas (id) VALUES (?)", (tarea_id,))
            cursor.execute("DELETE FROM todos WHERE id = ?", (tarea_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error eliminar:", e)
            return False

    # Mostrar primeras tareas
    def consultar_tareas_db(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT userId, id, title, completed FROM todos ORDER BY id LIMIT 10")
        rows = cursor.fetchall()

        print("\n--- TAREAS EN BD ---")
        for r in rows:
            print(Tarea(*r))
        print("----------------------")