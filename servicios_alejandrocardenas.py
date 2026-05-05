from main import Servicio

class AlquilerEquipo(Servicio):
    """Clase para el servicio de alquiler de hardware."""
    def __init__(self, id_entidad, nombre, costo_por_hora, tipo_equipo):
        super().__init__(id_entidad, nombre, costo_por_hora)
        self.__tipo_equipo = tipo_equipo  # Atributo privado (Encapsulamiento)

    def calcular_costo(self, horas):
        """Calcula el costo total aplicando IVA del 19%."""
        if horas <= 0:
            return 0
        total = (self.costo_base * horas) * 1.19
        return round(total, 2)

class AsesoriaEspecializada(Servicio):
    """Clase para el servicio de consultoría técnica."""
    def __init__(self, id_entidad, nombre, costo_sesion, experto):
        super().__init__(id_entidad, nombre, costo_sesion)
        self.__experto = experto # Atributo privado (Encapsulamiento)

    def calcular_costo(self, sesiones=1):
        """Calcula el costo multiplicando por el número de sesiones."""
        if sesiones < 1:
            return 0
        return round(self.costo_base * sesiones, 2)