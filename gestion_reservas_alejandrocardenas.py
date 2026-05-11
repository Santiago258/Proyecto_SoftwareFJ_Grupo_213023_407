from main import EntidadBase
from excepcion import ReservaInvalidaError  # Importa la excepción que creó Santiago

class Reserva(EntidadBase):
    """
    Clase que gestiona la unión de un Cliente y un Servicio.
    Cumple con el requerimiento del Compañero 4.
    """
    def __init__(self, id_reserva, cliente, servicio, cantidad_tiempo):
        super().__init__(id_reserva)
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad_tiempo = cantidad_tiempo

    def confirmar_reserva(self):
        """
        Método con manejo avanzado de excepciones.
        """
        try:
            print(f"--- Procesando Reserva ID: {self._id_entidad} ---")
            
            # Validación: Si el tiempo es cero o negativo, lanza error personalizado
            if self.cantidad_tiempo <= 0:
                raise ReservaInvalidaError("La duración del servicio debe ser mayor a cero.")
            
            # Calculamos el costo usando el polimorfismo de los servicios
            total = self.servicio.calcular_costo(self.cantidad_tiempo)
            
        except ReservaInvalidaError as e:
            print(f"ERROR EN RESERVA: {e}")
            # Aquí es donde Santiago capturará esto en el log
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
        else:
            # Se ejecuta solo si NO hubo errores
            print(f"Reserva exitosa para el cliente: {self.cliente}")
            print(f"Servicio: {self.servicio.nombre}")
            print(f"Total a pagar: ${total}")
        finally:
            # Se ejecuta siempre al final
            print("Finalizando validación de la operación.")