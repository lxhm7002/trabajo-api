import json
from servicios.api_servicio import APIServicio
from negocio.negocio_users import NegocioUsuarios
from datos import DatosDB

api_service = APIServicio()
negocio_users = NegocioUsuarios()
datos_db = DatosDB()

usuario_logueado = None


# ===========================================
#            REGISTRO
# ===========================================
def registrar_usuario():
    print("\n--- REGISTRO ---")
    name = input("Nombre: ")
    username = input("Usuario: ")
    email = input("Email: ")
    password = input("Contraseña: ")
    print(negocio_users.registrar_usuario(name, username, email, password))


# ===========================================
#              LOGIN
# ===========================================
def login_usuario():
    global usuario_logueado
    print("\n--- LOGIN ---")
    email = input("Email: ")
    password = input("Contraseña: ")

    r = negocio_users.login_usuario(email, password)
    print(r)

    if "Login exitoso" in r:
        usuario_logueado = r.split(", ")[1]
        return True
    return False


def logout_usuario():
    global usuario_logueado
    print(f"Sesión cerrada para {usuario_logueado}")
    usuario_logueado = None


# ===========================================
#               GET API
# ===========================================
def obtener_y_guardar_datos_api():
    print("\nObteniendo datos...")
    datos = api_service.obtener_datos_todos()
    if datos:
        print(datos_db.insertar_tareas_api(datos))
        datos_db.consultar_tareas_db()


# ===========================================
#               POST LOCAL
# ===========================================
def enviar_datos_post():
    print("\n--- NUEVA TAREA ---")
    user = int(input("userId: "))
    tid = int(input("ID nuevo (ej 3000): "))
    title = input("Título: ")

    tarea = {
        "userId": user,
        "id": tid,
        "title": title,
        "completed": False
    }

    api_service.crear_tarea(tarea)
    datos_db.crear_tarea_local(tarea)

    print("\nTarea creada:")
    print(json.dumps(tarea, indent=2))


# ===========================================
#               PUT LOCAL
# ===========================================
def enviar_datos_put():
    print("\n--- ACTUALIZAR TAREA ---")
    tid = int(input("ID tarea: "))
    new_title = input("Nuevo título: ")

    tarea = {
        "id": tid,
        "title": new_title,
        "completed": True
    }

    api_service.actualizar_tarea(tid, tarea)
    ok = datos_db.actualizar_tarea_local(tarea)

    print("Actualizada" if ok else "No existe ese ID.")


# ===========================================
#               DELETE LOCAL
# ===========================================
def eliminar_datos_delete():
    print("\n--- ELIMINAR TAREA ---")
    tid = int(input("ID tarea: "))

    api_service.eliminar_tarea(tid)
    ok = datos_db.eliminar_tarea_local(tid)

    print("Eliminada" if ok else "No existe ese ID.")


# ===========================================
#               MENÚ
# ===========================================
def menu_principal():
    while True:
        print("\n==============================")
        print(" API MANAGE - EVALUACIÓN 3")
        print("==============================")

        if usuario_logueado:
            print(f"Sesión: {usuario_logueado}")

        print("1. Registrar usuario")
        if not usuario_logueado:
            print("2. Iniciar sesión")
        if usuario_logueado:
            print("3. Obtener tareas API")
            print("4. Crear tarea (POST)")
            print("5. Actualizar tarea (PUT)")
            print("6. Eliminar tarea (DELETE)")
            print("7. Cerrar sesión")
        print("0. Salir")

        op = input("Opción: ")

        if op == "1":
            registrar_usuario()
        elif op == "2" and not usuario_logueado:
            login_usuario()
        elif op == "3" and usuario_logueado:
            obtener_y_guardar_datos_api()
        elif op == "4" and usuario_logueado:
            enviar_datos_post()
        elif op == "5" and usuario_logueado:
            enviar_datos_put()
        elif op == "6" and usuario_logueado:
            eliminar_datos_delete()
        elif op == "7" and usuario_logueado:
            logout_usuario()
        elif op == "0":
            print("Adiós!")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_principal()