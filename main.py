# =================================================================
# PROYECTO FASE 4: SISTEMA SOFTWARE FJ
# Rol: Compilador y Entregas - Santiago Sierra
# Integración Final: Santiago, Alejandro y Deiby
# =================================================================

from abc import ABC, abstractmethod
import datetime
import re
# Importamos todas las excepciones necesarias
from excepcion import (
    ErrorValidacionDatos, 
    ErrorReservaInvalida, 
    ErrorServicioNoDisponible, 
    ReservaInvalidaError
)

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
    def calcular_costo(self, cantidad):
        pass

# --- 3. CLASES DE SERVICIO (Aporte: Alejandro Cárdenas) ---
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, tipo_equipo):
        super().__init__(id_servicio, nombre, costo_base)
        self.__tipo_equipo = tipo_equipo

    def calcular_costo(self, horas):
        if horas <= 0:
            registrar_log(f"Intento de alquiler con horas inválidas: {horas}")
            raise ErrorValidacionDatos("Las horas de alquiler deben ser mayores a cero.")
        total = (self.costo_base * horas) * 1.19
        return round(total, 2)

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, experto):
        super().__init__(id_servicio, nombre, costo_base)
        self.__experto = experto

    def calcular_costo(self, sesiones=1):
        if sesiones < 1:
            registrar_log(f"Sesiones inválidas: {sesiones}")
            raise ErrorValidacionDatos("Debe programar al menos una sesión.")
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
            raise ErrorValidacionDatos("Nombre inválido o muy corto.")
        return nombre

    def __validar_correo(self, correo):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            raise ErrorValidacionDatos(f"Correo inválido: {correo}")
        return correo

    def obtener_detalles(self):
        return f"ID: {self.__id_cliente} | Nombre: {self.__nombre}"

# --- 5. SIMULACIÓN DE LAS 10 OPERACIONES ---
if __name__ == "__main__":
    print("=== SIMULACIÓN SISTEMA SOFTWARE FJ - 10 OPERACIONES ===")
    operaciones_exitosas = 0
    
    try:
        # Ops 1-2: Clientes
        c1 = Cliente(101, "Santiago Sierra", "santiago@unad.edu.co")
        c2 = Cliente(102, "Alejandro Cardenas", "alejandro@unad.edu.co")
        print(f"Op 1 & 2: Registro de clientes exitoso [OK]")
        operaciones_exitosas += 2

        # Ops 3-4: Servicios exitosos
        pc = AlquilerEquipo(501, "PC Escritorio", 15000, "Hardware")
        java = AsesoriaEspecializada(601, "Curso Java", 40000, "Ing. Alejandro")
        print(f"Op 3: Alquiler PC: ${pc.calcular_costo(5)} [OK]")
        print(f"Op 4: Asesoría Java: ${java.calcular_costo(3)} [OK]")
        operaciones_exitosas += 2

        # Ops 5-7: Pruebas de error (Manejo de excepciones)
        print("\n--- Validando Excepciones y Logs ---")
        try: Cliente(-1, "Error", "e@e.com")
        except: print("Op 5: ID Negativo capturado [OK]"); operaciones_exitosas += 1
        
        try: pc.calcular_costo(0)
        except: print("Op 6: Horas cero capturadas [OK]"); operaciones_exitosas += 1
        
        try: Cliente(104, "Juan", "correo_mal")
        except: print("Op 7: Email inválido capturado [OK]"); operaciones_exitosas += 1

        # Ops 8-10: Integración de Reserva (Aporte Deiby)
        # Importación dinámica para asegurar que los archivos existan
        from reserva_completa import Reserva
        from Servicio_salas_alejandrocardenas import ReservaSala

        print("\n--- Integración Clase Reserva (Aporte Deiby) ---")
        # Op 8: Reserva Exitosa
        sala = ReservaSala(701, "Sala A", 30000, 20)
        res_ok = Reserva(801, c1, sala, 3)
        if res_ok.confirmar_reserva():
            print("Op 8: Reserva de sala exitosa [OK]")
            operaciones_exitosas += 1

        # Op 9: Reserva Error (Tiempo 0)
        res_err = Reserva(802, c2, pc, 0)
        if not res_err.confirmar_reserva():
            print("Op 9: Error de tiempo en reserva capturado [OK]")
            operaciones_exitosas += 1

        # Op 10: Cancelación
        res_ok.cancelar_reserva("Cambio de planes")
        print("Op 10: Cancelación de reserva funcional [OK]")
        operaciones_exitosas += 1

    except Exception as e:
        print(f"Error en la simulación: {e}")

    print(f"\nResumen final: {operaciones_exitosas}/10 operaciones completadas.")
    print("======================================================")
