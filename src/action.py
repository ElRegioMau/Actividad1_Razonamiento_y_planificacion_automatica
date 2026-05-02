from enum import Enum


class Action(Enum):
    """Acciones que puede realizar el robot."""
    INITIAL = "inicialR"
    FINAL = "finalR"
    PICKUP = "cargarR"
    DROP = "descargarR"
    MOVE = "moverR"
