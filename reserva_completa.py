# =================================================================
# PROYECTO FASE 4: SISTEMA SOFTWARE FJ
# Archivo: reserva_completa.py
# Aporte: Deiby Nicolás Carrillo Sánchez Clase Reserva corregida + 3 operaciones faltantes
#         para completar las 10 requeridas por la guía.
#
# CORRECCIONES APLICADAS:
#   1. Se unifica el nombre de la clase base (EntidadGeneral).
#   2. Se corrige el nombre del atributo: nombre_servicio.
#   3. Se agrega ReservaInvalidaError al archivo de excepciones.
#   4. Se implementa encadenamiento de excepciones (raise X from Y).
#   5. Se agrega método cancelar_reserva().
#   6. Se simulan las operaciones 8, 9 y 10 que faltaban.
# =================================================================

import datetime
from abc import ABC, abstractmethod
import re

# ------------------------------------------------------------------
# NOTA PARA EL EQUIPO:
# Este archivo asume que excepcion.py ya tiene estas clases.
# Si no, agregar ReservaInvalidaError a excepcion.py así:
#
#   class ReservaInvalidaError(ErrorSoftwareFJ):
#       """Se lanza cuando los parámetros de una reserva son inválidos."""
#       pass
# ------------------------------------------------------------------

# Importamos desde los archivos del equipo
from excepcion import (
    ErrorSoftwareFJ,
    ErrorValidacionDatos,
    ErrorReservaInvalida,
    ErrorServicioNoDisponible
)
from main import EntidadGeneral, Servicio, Cliente, registrar_log
from Servicio_salas_alejandrocardenas import ReservaSala


# ------------------------------------------------------------------
# EXCEPCIÓN FALTANTE (se agrega aquí para no romper excepcion.py)
# ------------------------------------------------------------------
class ReservaInvalidaError(ErrorSoftwareFJ):
    """
    Se lanza cuando los parámetros de tiempo de una reserva son inválidos.
    Hereda de ErrorSoftwareFJ para mantener la jerarquía del sistema.
    """
    pass


# ------------------------------------------------------------------
# CLASE RESERVA - CORREGIDA Y COMPLETA
# Requisitos cumplidos:
#   - Integra cliente, servicio, duración y estado
#   - Confirmación con try/except/else/finally
#   - Cancelación
#   - Encadenamiento de excepciones (raise X from Y)
# ------------------------------------------------------------------
class Reserva(EntidadGeneral):
    """
    Gestiona la unión de un Cliente y un Servicio.
    Implementa confirmación, cancelación y manejo avanzado de excepciones.
    """

    # Estados posibles de una reserva
    ESTADO_PENDIENTE   = "PENDIENTE"
    ESTADO_CONFIRMADA  = "CONFIRMADA"
    ESTADO_CANCELADA   = "CANCELADA"

    def __init__(self, id_reserva: int, cliente: Cliente,
                 servicio: Servicio, cantidad_tiempo: float):
        """
        Parámetros:
            id_reserva     : identificador único de la reserva (int positivo)
            cliente        : instancia de Cliente
            servicio       : instancia de alguna subclase de Servicio
            cantidad_tiempo: horas o sesiones a reservar (debe ser > 0)
        """
        self.__id_reserva     = id_reserva
        self.__cliente        = cliente
        self.__servicio       = servicio
        self.__cantidad_tiempo = cantidad_tiempo
        self.__estado         = Reserva.ESTADO_PENDIENTE
        self.__costo_total    = 0.0

    # ---- Propiedades de solo lectura (encapsulación) --------------
    @property
    def id_reserva(self):
        return self.__id_reserva

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    # ---- Método abstracto heredado --------------------------------
    def obtener_detalles(self) -> str:
        """Retorna un resumen legible de la reserva."""
        return (
            f"Reserva #{self.__id_reserva} | "
            f"Cliente: {self.__cliente.obtener_detalles()} | "
            f"Servicio: {self.__servicio.nombre_servicio} | "
            f"Tiempo: {self.__cantidad_tiempo} | "
            f"Estado: {self.__estado} | "
            f"Costo: ${self.__costo_total}"
        )

    # ---- Confirmación con manejo completo de excepciones ----------
    def confirmar_reserva(self) -> bool:
        """
        Intenta confirmar la reserva.
        Usa try/except/else/finally y encadenamiento de excepciones.

        Retorna True si fue exitosa, False si hubo error.
        """
        print(f"\n  [Reserva #{self.__id_reserva}] Iniciando confirmación...")

        try:
            # Validación 1: tiempo debe ser positivo
            if self.__cantidad_tiempo <= 0:
                # ENCADENAMIENTO DE EXCEPCIONES (raise X from Y):
                # Primero creamos el error de validación base...
                error_base = ValueError(
                    f"Tiempo inválido recibido: {self.__cantidad_tiempo}"
                )
                # ...luego lo encadenamos con nuestro error personalizado.
                # Esto preserva el traceback original para depuración.
                raise ReservaInvalidaError(
                    "La duración debe ser mayor a cero."
                ) from error_base

            # Validación 2: el servicio no debe estar cancelado
            if self.__estado == Reserva.ESTADO_CANCELADA:
                raise ErrorReservaInvalida(
                    "No se puede confirmar una reserva ya cancelada."
                )

            # Cálculo de costo usando polimorfismo
            self.__costo_total = self.__servicio.calcular_costo(
                self.__cantidad_tiempo
            )

        except ReservaInvalidaError as e:
            # Error de tiempo inválido — registramos y reportamos
            mensaje = f"Reserva #{self.__id_reserva} - ReservaInvalidaError: {e}"
            registrar_log(mensaje)
            print(f"  ✗ ERROR: {e}")
            return False

        except ErrorReservaInvalida as e:
            # Error de estado inválido
            mensaje = f"Reserva #{self.__id_reserva} - ErrorReservaInvalida: {e}"
            registrar_log(mensaje)
            print(f"  ✗ ERROR: {e}")
            return False

        except ErrorValidacionDatos as e:
            # Error que puede venir del calcular_costo() del servicio
            mensaje = f"Reserva #{self.__id_reserva} - ErrorValidacionDatos: {e}"
            registrar_log(mensaje)
            print(f"  ✗ ERROR en datos del servicio: {e}")
            return False

        except Exception as e:
            # Captura genérica para errores inesperados
            mensaje = f"Reserva #{self.__id_reserva} - Error inesperado: {e}"
            registrar_log(mensaje)
            print(f"  ✗ ERROR inesperado: {e}")
            return False

        else:
            # Se ejecuta SOLO si no hubo ninguna excepción
            self.__estado = Reserva.ESTADO_CONFIRMADA
            evento = (
                f"Reserva #{self.__id_reserva} CONFIRMADA | "
                f"Cliente: {self.__cliente.obtener_detalles()} | "
                f"Costo: ${self.__costo_total}"
            )
            registrar_log(evento)
            print(f"  ✓ Reserva confirmada. Costo total: ${self.__costo_total}")
            return True

        finally:
            # Se ejecuta SIEMPRE, haya o no excepción
            print(f"  → Estado final de la reserva: {self.__estado}")

    # ---- Cancelación ----------------------------------------------
    def cancelar_reserva(self, motivo: str = "Sin motivo especificado") -> bool:
        """
        Cancela la reserva si está en estado PENDIENTE o CONFIRMADA.
        Registra el motivo en el log.

        Retorna True si se canceló, False si ya estaba cancelada.
        """
        try:
            if self.__estado == Reserva.ESTADO_CANCELADA:
                raise ErrorReservaInvalida(
                    f"La reserva #{self.__id_reserva} ya fue cancelada."
                )
            self.__estado = Reserva.ESTADO_CANCELADA

        except ErrorReservaInvalida as e:
            registrar_log(str(e))
            print(f"  ✗ No se pudo cancelar: {e}")
            return False

        else:
            evento = (
                f"Reserva #{self.__id_reserva} CANCELADA | Motivo: {motivo}"
            )
            registrar_log(evento)
            print(f"  ✓ Reserva #{self.__id_reserva} cancelada. Motivo: {motivo}")
            return True

        finally:
            print(f"  → Estado tras cancelación: {self.__estado}")


# ------------------------------------------------------------------
# OPERACIONES 8, 9 Y 10 — completan las 10 requeridas por la guía
# ------------------------------------------------------------------
if __name__ == "__main__":
    from main import AlquilerEquipo, AsesoriaEspecializada

    print("\n=== OPERACIONES 8, 9 Y 10 — Aporte reserva_completa.py ===\n")

    # ---- OP 8: Reserva de sala EXITOSA ----------------------------
    print("-- Op 8: Reserva de sala exitosa --")
    try:
        cliente_sala = Cliente(201, "Maria Lopez", "maria@unad.edu.co")
        sala_conf    = ReservaSala(701, "Sala Conferencias A", 30000, 20)
        reserva_8    = Reserva(801, cliente_sala, sala_conf, 3)
        reserva_8.confirmar_reserva()
    except Exception as e:
        registrar_log(f"Op 8 - Error no capturado: {e}")
        print(f"  Error crítico Op 8: {e}")

    # ---- OP 9: Reserva con tiempo CERO (error esperado) -----------
    print("\n-- Op 9: Reserva con duración 0 (debe fallar) --")
    try:
        cliente_err = Cliente(202, "Carlos Ruiz", "carlos@unad.edu.co")
        equipo_err  = AlquilerEquipo(502, "Laptop Dell", 20000, "Hardware")
        reserva_9   = Reserva(802, cliente_err, equipo_err, 0)  # tiempo=0
        reserva_9.confirmar_reserva()
    except Exception as e:
        registrar_log(f"Op 9 - Error no capturado: {e}")
        print(f"  Error crítico Op 9: {e}")

    # ---- OP 10: Reserva confirmada y luego CANCELADA --------------
    print("\n-- Op 10: Reserva confirmada y después cancelada --")
    try:
        cliente_can  = Cliente(203, "Ana Torres", "ana@unad.edu.co")
        asesoria_can = AsesoriaEspecializada(602, "Python Avanzado", 50000, "Ing. Torres")
        reserva_10   = Reserva(803, cliente_can, asesoria_can, 2)

        exito = reserva_10.confirmar_reserva()
        if exito:
            reserva_10.cancelar_reserva("Cliente solicitó reprogramación")

        # Intento de cancelar una reserva ya cancelada (error encadenado esperado)
        print("\n  Intentando cancelar la misma reserva nuevamente...")
        reserva_10.cancelar_reserva("Segundo intento de cancelación")

    except Exception as e:
        registrar_log(f"Op 10 - Error no capturado: {e}")
        print(f"  Error crítico Op 10: {e}")

    print("\n=== Fin de las operaciones 8-10. Revisa log_errores.txt ===")
