from main import Servicio

class ReservaSala(Servicio):
    """
    Clase para el servicio de alquiler de salas de juntas o eventos.
    Aporta la lógica de polimorfismo para el Compañero 3.
    """
    def __init__(self, id_entidad, nombre, costo_base, capacidad):
        super().__init__(id_entidad, nombre, costo_base)
        self.__capacidad = capacidad # Atributo privado (Encapsulamiento)
        self.__tasa_limpieza = 50000 # Costo fijo adicional

    def calcular_costo(self, horas):
        """
        Polimorfismo: Calcula el costo total sumando una tasa fija de limpieza.
        """
        if horas <= 0:
            return 0
        
        # El costo base se multiplica por las horas y se suma la limpieza
        total = (self.costo_base * horas) + self.__tasa_limpieza
        return round(total, 2)

    def obtener_detalles(self):
        return f"Sala: {self.nombre} (Capacidad: {self.__capacidad} personas)"
