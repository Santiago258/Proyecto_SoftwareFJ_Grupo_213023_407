# =================================================================
# PROYECTO FASE 4: SISTEMA SOFTWARE FJ
# Rol: Compilador y Entregas - Santiago Sierra
# Integración de Módulos y Pruebas de Estabilidad
# =================================================================

from abc import ABC, abstractmethod
import datetime
import re
# Importamos las excepciones del archivo independiente
from excepcion import ErrorValidacionDatos, ErrorReservaInvalida, ErrorServicioNoDisponible

# --- 1. MANEJO DE LOGS (Requisito: Registro en .txt) ---
def registrar_log(error_mensaje):
    """Registra errores y eventos en un archivo externo sin detener el programa."""
    try:
        with open("log_errores.txt", "a") as archivo:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] ERROR/EVENTO: {error_mensaje}\n")
    except Exception as e:
        print(f"Error crítico de log: {e}")

# --- 2. CLASES ABSTRACTAS (Requisito: Abstracción) ---
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

# --- 3. CLASES DE SERVICIO (Integración: Alejandro Cárdenas & Santiago Sierra) ---
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, tipo_equipo):
        super().__init__(id_servicio, nombre, costo_base)
        self.__tipo_equipo = tipo_equipo

    def calcular_costo(self, horas):
        if horas <= 0:
            registrar_log(f"Intento de alquiler con horas inválidas: {horas}")
            raise ErrorValidacionDatos("Las horas de alquiler deben ser mayores a cero.")
        total = (self.costo_base * horas) * 1.19  # Aplicando IVA del 19%
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

# --- 4. CLASE CLIENTE (Requisito: Encapsulación y Validaciones) ---
class Cliente(EntidadGeneral):
    def __init__(self, id_cliente, nombre, correo):
        self.__id_cliente = self.__validar_id(id_cliente)
        self.__nombre = self.__validar_nombre(nombre)
        self.__correo = self.__validar_correo(correo)

    def __validar_id(self, id_cliente):
        if not isinstance(id_cliente, int) or id_cliente <= 0:
            registrar_log(f"ID inválido detectado: {id_cliente}")
            raise ErrorValidacionDatos("El ID debe ser un número entero positivo.")
        return id_cliente

    def __validar_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ErrorValidacionDatos("Nombre inválido o muy corto.")
        return nombre

    def __validar_correo(self, correo):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            raise ErrorValidacionDatos(f"Formato de correo inválido: {correo}")
        return correo

    def obtener_detalles(self):
        return f"CLIENTE -> ID: {self.__id_cliente} | Nombre: {self.__nombre}"

# --- 5. SIMULACIÓN DE LAS 10 OPERACIONES (Requisito de Guía) ---
if __name__ == "__main__":
    print("=== SIMULACIÓN SISTEMA SOFTWARE FJ - 10 OPERACIONES ===")
    
    operaciones_exitosas = 0
    
    # OP 1: Creación de Cliente 1 (Éxito)
    try:
        c1 = Cliente(101, "Santiago Sierra", "santiago@unad.edu.co")
        print(f"Op 1: {c1.obtener_detalles()} [OK]")
        operaciones_exitosas += 1
    except Exception as e: print(f"Op 1 Error: {e}")

    # OP 2: Creación de Cliente 2 (Éxito)
    try:
        c2 = Cliente(102, "Alejandro Cardenas", "alejandro@unad.edu.co")
        print(f"Op 2: {c2.obtener_detalles()} [OK]")
        operaciones_exitosas += 1
    except Exception as e: print(f"Op 2 Error: {e}")

    # OP 3: Alquiler de Equipo (Éxito)
    try:
        pc = AlquilerEquipo(501, "PC Escritorio", 15000, "Hardware")
        costo = pc.calcular_costo(5)
        print(f"Op 3: Alquiler {pc.nombre_servicio} por 5h: ${costo} [OK]")
        operaciones_exitosas += 1
    except Exception as e: print(f"Op 3 Error: {e}")

    # OP 4: Asesoría Especializada (Éxito)
    try:
        java = AsesoriaEspecializada(601, "Curso Java", 40000, "Ing. Alejandro")
        costo_a = java.calcular_costo(3)
        print(f"Op 4: {java.nombre_servicio} (3 sesiones): ${costo_a} [OK]")
        operaciones_exitosas += 1
    except Exception as e: print(f"Op 4 Error: {e}")

    # OP 5: PRUEBA DE ERROR - ID de Cliente Negativo
    print("\n--- Pruebas de Estabilidad (Manejo de Excepciones) ---")
    try:
        c3 = Cliente(-20, "Error", "test@mail.com")
    except ErrorValidacionDatos as e:
        print(f"Op 5: Captura de error esperada en Cliente: {e} [OK - Log Registrado]")
        operaciones_exitosas += 1

    # OP 6: PRUEBA DE ERROR - Alquiler con 0 horas
    try:
        pc.calcular_costo(0)
    except ErrorValidacionDatos as e:
        print(f"Op 6: Captura de error esperada en Alquiler: {e} [OK - Log Registrado]")
        operaciones_exitosas += 1

    # OP 7: PRUEBA DE ERROR - Correo electrónico mal formado
    try:
        c4 = Cliente(104, "Juan Perez", "correo_sin_arroba.com")
    except ErrorValidacionDatos as e:
        print(f"Op 7: Captura de error esperada en Email: {e} [OK - Log Registrado]")
        operaciones_exitosas += 1

    # =================================================================
    # APORTE: [Tu nombre]
    # Integración de la clase Reserva y operaciones 8, 9 y 10.
    # Archivo requerido en el mismo directorio: reserva_completa.py
    # Los imports van aquí (locales al bloque main) para no interferir
    # con las importaciones globales del compañero Santiago Sierra.
    # =================================================================
    from reserva_completa import Reserva, ReservaInvalidaError
    from Servicio_salas_alejandrocardenas import ReservaSala

    print("\n=================================================================")
    print("APORTE [Tu nombre]: Operaciones 8, 9 y 10 — Clase Reserva")
    print("=================================================================")

    # OP 8: Reserva de sala EXITOSA (demuestra try/except/else/finally)
    try:
        cliente_8 = Cliente(201, "Maria Lopez", "maria@unad.edu.co")
        sala_8    = ReservaSala(701, "Sala Conferencias A", 30000, 20)
        reserva_8 = Reserva(801, cliente_8, sala_8, 3)
        reserva_8.confirmar_reserva()
        operaciones_exitosas += 1
    except Exception as e:
        registrar_log(f"Op 8 - Error no capturado: {e}")
        print(f"Op 8 Error crítico: {e}")

    # OP 9: Reserva con tiempo CERO
    # Demuestra encadenamiento de excepciones:
    # raise ReservaInvalidaError(...) from ValueError(...)
    # implementado dentro de reserva_completa.py
    try:
        cliente_9 = Cliente(202, "Carlos Ruiz", "carlos@unad.edu.co")
        equipo_9  = AlquilerEquipo(502, "Laptop Dell", 20000, "Hardware")
        reserva_9 = Reserva(802, cliente_9, equipo_9, 0)  # tiempo=0 → debe fallar
        reserva_9.confirmar_reserva()
        operaciones_exitosas += 1
    except Exception as e:
        registrar_log(f"Op 9 - Error no capturado: {e}")
        print(f"Op 9 Error crítico: {e}")

    # OP 10: Reserva CONFIRMADA y luego CANCELADA
    try:
        cliente_10  = Cliente(203, "Ana Torres", "ana@unad.edu.co")
        asesoria_10 = AsesoriaEspecializada(602, "Python Avanzado", 50000, "Ing. Torres")
        reserva_10  = Reserva(803, cliente_10, asesoria_10, 2)
        exito = reserva_10.confirmar_reserva()
        if exito:
            reserva_10.cancelar_reserva("Cliente solicitó reprogramación")
        operaciones_exitosas += 1
    except Exception as e:
        registrar_log(f"Op 10 - Error no capturado: {e}")
        print(f"Op 10 Error crítico: {e}")

    print(f"\nResumen final: {operaciones_exitosas}/10 operaciones completadas.")
    print("======================================================")
