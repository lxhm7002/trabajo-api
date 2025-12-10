class Usuario:
    def __init__(self, id, name, username, email, encrypted_password=None):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.encrypted_password = encrypted_password


class Tarea:
    def __init__(self, userId, id, title, completed):
        self.userId = userId
        self.id = id
        self.title = title
        self.completed = completed

    def __str__(self):
        estado = "✔" if self.completed else "✘"
        return f"[{estado}] {self.id} - {self.title} (User {self.userId})"
