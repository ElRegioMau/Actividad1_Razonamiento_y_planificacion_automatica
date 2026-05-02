from dataclasses import dataclass, field
from typing import Optional, Tuple
from action import Action


@dataclass
class Activity:
    """Representa una actividad del robot en el plan de ejecución."""
    position: Tuple[int, int]   # (fila, columna)
    action: Action
    detail: Optional[str] = field(default=None)

    def __str__(self) -> str:
        row, col = self.position
        if self.detail:
            return f"{self.action.value} ({self.detail},{row},{col})"
        return f"{self.action.value} ({row},{col})"
