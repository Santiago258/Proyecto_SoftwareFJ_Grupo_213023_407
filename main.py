# --- PROYECTO FASE 4: SOFTWARE FJ ---
# Rol: Compilador y Entregas - Santiago Sierra

from abc import ABC, abstractmethod
import datetime
import re

# 1. CLASE ABSTRACTA GENERAL
class EntidadGeneral(ABC):
    @abstractmethod
    def obtener_detalles(self):
        pass

# 2. CLASE CLIENTE (Aporte inicial - Santiago Sierra)
class Cliente(EntidadGeneral):
    def __init__(self, id_cliente, nombre, correo):
        # Encapsulación: Atributos privados
        self.__id_cliente = self.__validar_id(id_cliente)
        self.__nombre = self.__validar_nombre(nombre)
        self.__correo = self.__validar_correo(correo)

    # Validaciones robustas (Requisito Anexo 3)
    def __validar_id(self, id_cliente):
        if not isinstance(id_cliente, int) or id_cliente <= 0:
            registrar_log(f"ID de cliente inválido: {id_cliente}")
            raise ValueError("El ID debe ser un número entero positivo.")
        return id_cliente

    def __validar_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            registrar_log("Intento de registro con nombre vacío o muy corto.")
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def __validar_correo(self, correo):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            registrar_log(f"Formato de correo inválido: {correo}")
            raise ValueError("El formato del correo electrónico no es válido.")
        return correo

    def obtener_detalles(self):
        return f"CLIENTE -> ID: {self.__id_cliente} | Nombre: {self.__nombre} | Correo: {self.__correo}"

# 3. CLASE ABSTRACTA SERVICIO
class Servicio(ABC):
    def __init__(self, id_servicio, nombre_servicio):
        self.id_servicio = id_servicio
        self.nombre_servicio = nombre_servicio
    
    @abstractmethod
    def calcular_costo(self):
        pass

# 4. MANEJO DE LOGS (Archivo .txt)
def registrar_log(error_mensaje):
    try:
        with open("log_errores.txt", "a") as archivo:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] ERROR: {error_mensaje}\n")
    except Exception as e:
        print(f"No se pudo escribir en el log: {e}")

# 5. SIMULACIÓN
if __name__ == "__main__":
    print("--- Sistema de Gestión Software FJ ---")
    try:
        # Ejemplo de creación exitosa
        c1 = Cliente(101, "Santiago Sierra", "santiago@unad.edu.co")
        print(c1.obtener_detalles())
    except Exception as e:
        print(f"Error detectado: {e}")
