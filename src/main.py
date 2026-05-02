"""
main.py — Punto de entrada del programa.

Ejecuta el robot de Amazon para mover los tres inventarios (M1, M2, M3)
a sus posiciones objetivo usando búsqueda heurística A*.
"""

import logging
from action import Action
from app import App

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Inicializa el robot, ejecuta el plan A* e imprime el resultado."""
    robot = App()
    robot.initialize()

    # Procesar cada inventario: ir a buscarlo y llevarlo a su destino
    for package_name in sorted(robot.package_positions.keys()):
        # 1) Ir hasta el inventario y cargarlo
        robot.move_robot(
            package_name,
            robot.package_positions[package_name],
            Action.PICKUP,
        )
        # 2) Llevar el inventario a su destino y descargarlo
        robot.move_robot(
            package_name,
            robot.package_destinations[package_name],
            Action.DROP,
        )

    robot.finalize()

    logger.info("=" * 50)
    logger.info("PLAN DE EJECUCIÓN GENERADO POR A*:")
    logger.info("=" * 50)
    for step, activity in enumerate(robot.plan, start=1):
        logger.info("Paso %02d: %s", step, activity)


if __name__ == "__main__":
    main()
