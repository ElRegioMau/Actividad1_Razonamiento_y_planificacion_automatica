class OutOfLimitException(Exception):
    """Se lanza cuando el robot intenta salir de los límites del grid."""
    pass


class NotAbleToMoveException(Exception):
    """Se lanza cuando el robot no puede moverse (obstáculo u otro impedimento)."""
    pass
