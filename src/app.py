"""
app.py — Lógica principal del robot con algoritmo A* completo.

Implementa la búsqueda heurística A* para mover los tres inventarios
(M1, M2, M3) a sus posiciones objetivo en un almacén 4x4.
"""

import heapq
import logging
from typing import Dict, List, Optional, Set, Tuple

from action import Action
from activity import Activity
from direction import Direction
from exceptions import NotAbleToMoveException, OutOfLimitException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

Point = Tuple[int, int]   # (fila, columna)

UNIFORM_COST = 1

INITIAL_STATE: List[List[str]] = [
    ["M1", "#",  "",   "M3"],
    ["M2", "#",  "",   ""  ],
    ["",   "",   "R",  ""  ],
    ["",   "",   "",   ""  ],
]

FINAL_STATE: List[List[str]] = [
    ["",  "",   "",   "" ],
    ["",  "",   "",   "" ],
    ["",  "",   "",   "" ],
    ["",  "M3", "M2", "M1"],
]


class App:
    """
    Robot que resuelve el problema de inventario de Amazon usando A*.

    Atributos
    ---------
    open_list : List[Point]
        Nodos en la frontera de exploración (lista abierta).
    closed_list : List[Point]
        Nodos ya expandidos (lista cerrada).
    package_positions : Dict[str, Point]
        Posición actual de cada inventario en el estado inicial.
    package_destinations : Dict[str, Point]
        Posición objetivo de cada inventario.
    robot_position : Point
        Posición actual del robot (fila, columna).
    obstacles : List[Point]
        Celdas bloqueadas por paredes ('#').
    plan : List[Activity]
        Secuencia completa de actividades del plan generado.
    """

    def __init__(self) -> None:
        self.open_list: List[Point] = []
        self.closed_list: List[Point] = []
        self.package_positions: Dict[str, Point] = {}
        self.package_destinations: Dict[str, Point] = {}
        self.robot_position: Optional[Point] = None
        self.obstacles: List[Point] = []
        self.plan: List[Activity] = []

    # ── Inicialización ──────────────────────────────────────────────────────

    def initialize(self) -> None:
        """
        Parsea INITIAL_STATE y FINAL_STATE para extraer:
        - Posición inicial del robot (R).
        - Posiciones iniciales de los inventarios (M1, M2, M3).
        - Posiciones objetivo de los inventarios.
        - Obstáculos (#).
        Registra el estado inicial en el plan y en la lista cerrada.
        """
        for r, row in enumerate(INITIAL_STATE):
            for c, cell in enumerate(row):
                if cell.startswith("M"):
                    self.package_positions[cell] = (r, c)
                elif cell == "R":
                    self.robot_position = (r, c)
                elif cell == "#":
                    self.obstacles.append((r, c))

        for r, row in enumerate(FINAL_STATE):
            for c, cell in enumerate(row):
                if cell.startswith("M"):
                    self.package_destinations[cell] = (r, c)

        self.closed_list.append(self.robot_position)
        self.plan.append(Activity(self.robot_position, Action.INITIAL))

    def finalize(self) -> None:
        """Agrega la actividad FINAL al plan."""
        self.plan.append(Activity(self.robot_position, Action.FINAL))

    # ── Algoritmo A* ────────────────────────────────────────────────────────

    def move_robot(self, package_name: str, target: Point, action: Action) -> None:
        """
        Mueve el robot desde su posición actual hasta `target` usando A*.

        Utiliza una cola de prioridad (min-heap) donde la prioridad es
        f(n) = g(n) + h(n), siendo:
          - g(n): coste acumulado real (1 por cada movimiento).
          - h(n): heurística — distancia Manhattan hasta `target`.

        Una vez encontrado el camino óptimo, reconstruye la ruta y la
        agrega al plan de actividades. Actualiza open_list y closed_list
        para que queden disponibles para depuración o visualización.

        Parámetros
        ----------
        package_name : str   Nombre del inventario (p.ej. "M1").
        target : Point       Posición destino (fila, columna).
        action : Action      Acción al llegar: PICKUP o DROP.
        """
        start = self.robot_position

        # Si ya está en el destino, solo ejecutar la acción
        if start == target:
            self.plan.append(Activity(self.robot_position, action, package_name))
            return

        # Heap: (f, g, tie-breaker, posición, camino)
        counter = 0  # desempate FIFO para misma f
        heap: List = []
        heapq.heappush(heap, (0, 0, counter, start, [start]))

        visited: Set[Point] = set()

        while heap:
            f, g, _, current, path = heapq.heappop(heap)

            if current in visited:
                continue
            visited.add(current)

            # Actualizar listas para registro / visualización
            self.closed_list = list(visited)
            self.open_list = [item[3] for item in heap if item[3] not in visited]

            logger.debug(
                "Expandiendo %s  f=%d  g=%d  h=%d", current, f, g, f - g
            )
            logger.debug("  Lista abierta:  %s", self.open_list)
            logger.debug("  Lista cerrada:  %s", self.closed_list)

            # ¿Llegamos?
            if current == target:
                for pos in path[1:]:
                    self.plan.append(Activity(pos, Action.MOVE))
                self.plan.append(Activity(current, action, package_name))
                self.robot_position = current
                logger.debug(
                    "Objetivo %s alcanzado. Camino: %s", package_name, path
                )
                self.closed_list.clear()
                return

            # Expandir vecinos
            for neighbor in self._get_neighbors_for(current, visited):
                new_g = g + UNIFORM_COST
                h = self._manhattan_distance(neighbor, target)
                new_f = new_g + h
                counter += 1
                heapq.heappush(
                    heap, (new_f, new_g, counter, neighbor, path + [neighbor])
                )
                logger.debug(
                    "  Vecino %s  g=%d  h=%d  f=%d", neighbor, new_g, h, new_f
                )

        logger.error("No se encontró camino desde %s hasta %s.", start, target)

    # ── Métodos auxiliares ───────────────────────────────────────────────────

    def _get_neighbors_for(self, pos: Point, visited: Set[Point]) -> List[Point]:
        """
        Devuelve vecinos válidos de `pos` en orden UP, DOWN, LEFT, RIGHT,
        excluyendo límites del grid, obstáculos y nodos ya visitados.
        """
        rows = len(INITIAL_STATE)
        cols = len(INITIAL_STATE[0])
        r, c = pos

        delta = {
            Direction.UP:    (-1,  0),
            Direction.DOWN:  ( 1,  0),
            Direction.LEFT:  ( 0, -1),
            Direction.RIGHT: ( 0,  1),
        }

        neighbors: List[Point] = []
        for direction in Direction:
            dr, dc = delta[direction]
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            next_pos: Point = (nr, nc)
            if next_pos in self.obstacles or next_pos in visited:
                continue
            neighbors.append(next_pos)

        return neighbors

    @staticmethod
    def _manhattan_distance(origin: Point, destination: Point) -> int:
        """
        h(n) = |fila_origen − fila_destino| + |col_origen − col_destino|

        Admisible y consistente en grids con movimiento horizontal/vertical.
        """
        return abs(origin[0] - destination[0]) + abs(origin[1] - destination[1])
