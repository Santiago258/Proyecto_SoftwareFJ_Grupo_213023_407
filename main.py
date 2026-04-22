# =================================================================
# PROYECTO FASE 4: SISTEMA SOFTWARE FJ
# Rol: Compilador y Entregas - Santiago Sierra
# Estructura: POO, Abstracción, Encapsulación y Manejo de Errores
# =================================================================

from abc import ABC, abstractmethod
import datetime
import re

# --- 1. MANEJO DE LOGS (Requisito: Registro de eventos en .txt) ---
def registrar_log(error_mensaje):
    """Registra errores y eventos en un archivo externo sin detener el programa."""
    try:
        with open("log_errores.txt", "a") as archivo:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] ERROR/EVENTO: {error_mensaje}\n")
    except Exception as e:
        print(f"Error crítico: No se pudo escribir en el log. {e}")

# --- 2. CLASES ABSTRACTAS (Requisito: Abstracción) ---
class EntidadGeneral(ABC):
    @abstractmethod
    def obtener_detalles(self):
        pass

class Servicio(ABC):
    def __init__(self, id_servicio, nombre_servicio):
        self.id_servicio = id_servicio
        self.nombre_servicio = nombre_servicio
    
    @abstractmethod
    def calcular_costo(self):
        pass

# --- 3. CLASE CLIENTE (Requisito: Encapsulación y Validaciones) ---
class Cliente(EntidadGeneral):
    def __init__(self, id_cliente, nombre, correo):
        # Atributos privados (Encapsulación)
        self.__id_cliente = self.__validar_id(id_cliente)
        self.__nombre = self.__validar_nombre(nombre)
        self.__correo = self.__validar_correo(correo)

    # Validaciones robustas
    def __validar_id(self, id_cliente):
        if not isinstance(id_cliente, int) or id_cliente <= 0:
            registrar_log(f"ID inválido detectado: {id_cliente}")
            raise ValueError("El ID del cliente debe ser un número entero positivo.")
        return id_cliente

    def __validar_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            registrar_log("Intento de registro con nombre vacío o inválido.")
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def __validar_correo(self, correo):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            registrar_log(f"Formato de correo incorrecto: {correo}")
            raise ValueError("El correo electrónico no tiene un formato válido.")
        return correo

    # Implementación de método abstracto
    def obtener_detalles(self):
        return f"CLIENTE -> ID: {self.__id_cliente} | Nombre: {self.__nombre} | Email: {self.__correo}"

# --- 4. SIMULACIÓN DE OPERACIONES (Prueba de estabilidad) ---
if __name__ == "__main__":
    print("=== Sistema de Gestión Software FJ - Fase 4 ===")
    
    try:
        # Operación 1: Registro exitoso
        print("\n[Simulación 1: Registro válido]")
        usuario1 = Cliente(101, "Santiago Sierra", "santiago@unad.edu.co")
        print(usuario1.obtener_detalles())
        registrar_log("Usuario registrado exitosamente.")

        # Operación 2: Intento de registro inválido (activará el log y la excepción)
        print("\n[Simulación 2: Registro inválido - ID Negativo]")
        usuario2 = Cliente(-5, "Prueba Error", "error@correo.com")
        
    except ValueError as ve:
        print(f"Control de error: {ve}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        print("\n=== Fin de la simulación de arranque ===")
