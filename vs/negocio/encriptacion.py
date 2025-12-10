import hashlib
import os

class Encriptador:

    def encriptar_contrasena(self, password: str) -> bytes:
        password_bytes = password.encode('utf-8')
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 200000)
        return salt + key

    def verificar_contrasena(self, stored_password: bytes, provided_password: str) -> bool:
        provided_bytes = provided_password.encode('utf-8')
        salt = stored_password[:16]
        original_key = stored_password[16:]
        new_key = hashlib.pbkdf2_hmac('sha256', provided_bytes, salt, 200000)
        return new_key == original_key
