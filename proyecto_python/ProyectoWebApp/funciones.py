def convertir_prioridad(value):
    if value == 1:
        return 'Alta'
    if value == 2:
        return 'Media'
    if value == 3:
        return 'Baja'

def convertir_estado(value):
    if value == 1:
        return 'Pendiente'
    if value == 2:
        return 'En Proceso'
    if value == 3:
        return 'Finalizado'