# =================================================================
# PROYECTO FASE 4: SISTEMA SOFTWARE FJ
# Rol: Compilador y Entregas - Santiago Sierra
# Integración de Módulos: Santiago Sierra & Alejandro Cárdenas
# =================================================================

from abc import ABC, abstractmethod
import datetime
import re
import math
from excepcion import ErrorValidacionDatos, ErrorServicioNoDisponible

# --- 1. MANEJO DE LOGS ---
def registrar_log(error_mensaje):
    try:
        with open("log_errores.txt", "a") as archivo:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] ERROR/EVENTO: {error_mensaje}\n")
    except Exception as e:
        print(f"Error crítico de log: {e}")

# --- 2. CLASES ABSTRACTAS ---
class EntidadGeneral(ABC):
    @abstractmethod
    def obtener_detalles(self):
        pass

class Servicio(ABC):
    def __init__(self, id_servicio, nombre_servicio, costo_base):
        self.id_servicio = id_servicio
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
    
    @abstractmethod
    def calcular_costo(self):
        pass

# --- 3. CLASES DE SERVICIO (Aporte: Alejandro Cárdenas - Corregido) ---
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, tipo_equipo):
        super().__init__(id_servicio, nombre, costo_base)
        self.__tipo_equipo = tipo_equipo # Encapsulamiento

    def calcular_costo(self, horas):
        if horas <= 0:
            registrar_log(f"Horas inválidas en Alquiler: {horas}")
            raise ErrorValidacionDatos("Las horas de alquiler deben ser mayores a 0.")
        # Cálculo con IVA del 19% como propuso el compañero
        total = (self.costo_base * horas) * 1.19
        return round(total, 2)

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, experto):
        super().__init__(id_servicio, nombre, costo_base)
        self.__experto = experto

    def calcular_costo(self, sesiones=1):
        if sesiones < 1:
            raise ErrorValidacionDatos("Debe haber al menos 1 sesión de asesoría.")
        return round(self.costo_base * sesiones, 2)

# --- 4. CLASE CLIENTE (Aporte: Santiago Sierra) ---
class Cliente(EntidadGeneral):
    def __init__(self, id_cliente, nombre, correo):
        self.__id_cliente = self.__validar_id(id_cliente)
        self.__nombre = self.__validar_nombre(nombre)
        self.__correo = self.__validar_correo(correo)

    def __validar_id(self, id_cliente):
        if not isinstance(id_cliente, int) or id_cliente <= 0:
            registrar_log(f"ID inválido: {id_cliente}")
            raise ErrorValidacionDatos("El ID debe ser un entero positivo.")
        return id_cliente

    def __validar_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ErrorValidacionDatos("Nombre demasiado corto.")
        return nombre

    def __validar_correo(self, correo):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            raise ErrorValidacionDatos(f"Correo inválido: {correo}")
        return correo

    def obtener_detalles(self):
        return f"CLIENTE -> ID: {self.__id_cliente} | Nombre: {self.__nombre}"

# --- 5. SIMULACIÓN DE OPERACIONES (Requisito: 10 operaciones) ---
if __name__ == "__main__":
    print("=== Sistema Software FJ - Integración Progresiva ===")
    
    try:
        # Op 1: Registro Cliente
        c1 = Cliente(1, "Santiago Sierra", "santiago@unad.edu.co")
        print(f"[OK] {c1.obtener_detalles()}")

        # Op 2: Alquiler de Equipo (Éxito)
        laptop = AlquilerEquipo(501, "Laptop Gamer", 25000, "Hardware")
        costo_laptop = laptop.calcular_costo(4)
        print(f"[OK] Servicio: {laptop.nombre_servicio} | Costo (4h + IVA): ${costo_laptop}")

        # Op 3: Asesoría (Éxito)
        asesoria = AsesoriaEspecializada(601, "Consultoría Java", 50000, "Ing. Alejandro")
        print(f"[OK] Servicio: {asesoria.nombre_servicio} | Costo: ${asesoria.calcular_costo(2)}")

        # Op 4: Intento de Alquiler con horas negativas (Error controlado)
        print("[PRUEBA ERROR] Intentando alquiler con -2 horas...")
        laptop.calcular_costo(-2)

    except ErrorValidacionDatos as e:
        print(f"Control de Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
