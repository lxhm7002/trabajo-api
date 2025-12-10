from negocio.encriptacion import Encriptador
from datos import DatosDB
from modelos.modelo import Usuario

class NegocioUsuarios:

    def __init__(self):
        self.encriptador = Encriptador()
        self.datos_db = DatosDB()

    def registrar_usuario(self, name, username, email, password):
        encrypted = self.encriptador.encriptar_contrasena(password)
        usuario = Usuario(id=999, name=name, username=username, email=email, encrypted_password=encrypted)
        if self.datos_db.insertar_usuario_local(usuario):
            return "Registro exitoso."
        return "Error registrando usuario."

    def login_usuario(self, email, password):
        user = self.datos_db.obtener_usuario_por_email(email)
        if not user:
            return "Usuario no encontrado."

        if self.encriptador.verificar_contrasena(user.encrypted_password, password):
            return f"Login exitoso, {user.username}."
        return "Contraseña incorrecta."
