import requests
from auxiliares.constantes import BASE_API_URL

class APIServicio:

    def __init__(self):
        self.base_url = BASE_API_URL

    def obtener_datos_todos(self):
        try:
            r = requests.get(f"{self.base_url}/todos", timeout=10)
            r.raise_for_status()
            return r.json()
        except:
            return None

    def crear_tarea(self, data):
        try:
            r = requests.post(f"{self.base_url}/todos", json=data)
            return r.json()
        except:
            return None

    def actualizar_tarea(self, id, data):
        try:
            r = requests.put(f"{self.base_url}/todos/{id}", json=data)
            return r.json()
        except:
            return None

    def eliminar_tarea(self, id):
        try:
            requests.delete(f"{self.base_url}/todos/{id}")
            return True
        except:
            return False
