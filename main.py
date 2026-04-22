# --- PROYECTO FASE 4: SOFTWARE FJ ---
# Rol: Compilador y Entregas - Santiago Sierra

from abc import ABC, abstractmethod
import datetime

# 1. CLASE ABSTRACTA GENERAL (Requisito Anexo 3)
class EntidadGeneral(ABC):
    @abstractmethod
    def obtener_detalles(self):
        pass

# 2. CLASE ABSTRACTA SERVICIO (Requisito Anexo 3)
class Servicio(ABC):
    def __init__(self, id_servicio, nombre_servicio):
        self.id_servicio = id_servicio
        self.nombre_servicio = nombre_servicio
    
    @abstractmethod
    def calcular_costo(self):
        pass

# 3. MANEJO DE LOGS (Archivo .txt para errores)
def registrar_log(error_mensaje):
    try:
        with open("log_errores.txt", "a") as archivo:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] ERROR: {error_mensaje}\n")
    except Exception as e:
        print(f"No se pudo escribir en el log: {e}")

# 4. SIMULACIÓN DE OPERACIONES
if __name__ == "__main__":
    print("--- Sistema de Gestión Software FJ ---")
    # Aquí integraremos los aportes de los compañeros
