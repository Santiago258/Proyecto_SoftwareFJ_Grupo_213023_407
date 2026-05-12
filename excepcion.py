# --- REQUERIMIENTO: EXCEPCIONES PERSONALIZADAS ---
# Definición de errores específicos para Software FJ

class ErrorSoftwareFJ(Exception):
    """Clase base para excepciones del sistema."""
    pass

class ErrorReservaInvalida(ErrorSoftwareFJ):
    """Se lanza cuando una reserva no cumple los requisitos."""
    pass

class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros de tiempo de una reserva son inválidos."""
    pass

class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    """Se lanza cuando el servicio solicitado ya está ocupado."""
    pass

class ErrorValidacionDatos(ErrorSoftwareFJ):
    """Se lanza cuando los datos de entrada no cumplen el formato."""
    pass
