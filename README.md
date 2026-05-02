#  Robot de Inventario Amazon — Búsqueda Heurística A*

Actividad grupal de la asignatura **Razonamiento y Planificación Automática** (UNIR).

Implementación del algoritmo A* en Python para resolver el problema de ordenamiento
de inventarios en un almacén 4×4, usando la distancia Manhattan como heurística.

## Problema

Un robot debe mover tres inventarios (M1, M2, M3) desde sus posiciones iniciales
hasta sus destinos objetivo, evitando paredes y usando el menor número de pasos posible.

```
Estado inicial        Estado objetivo
┌────┬────┬────┬────┐  ┌────┬────┬────┬────┐
│ M1 │ #  │    │ M3 │  │    │    │    │    │
│ M2 │ #  │    │    │  │    │    │    │    │
│    │    │ R  │    │  │    │    │    │    │
│    │    │    │    │  │    │ M3 │ M2 │ M1 │
└────┴────┴────┴────┘  └────┴────┴────┴────┘
```

## Estructura del proyecto

```
robot-amazon-astar/
├── src/
│   ├── action.py       # Enum de acciones del robot
│   ├── activity.py     # Dataclass de un paso del plan
│   ├── app.py          # Clase App con el algoritmo A*
│   ├── direction.py    # Enum de direcciones
│   ├── exceptions.py   # Excepciones personalizadas
│   └── main.py         # Punto de entrada
├── memoria_actividad_astar.ipynb   # Memoria completa en Jupyter
├── requirements.txt
└── README.md
```

## Cómo ejecutar

### Requisitos
- Python 3.8 o superior

### Instalar dependencias opcionales (solo para visualización gráfica)
```bash
pip install -r requirements.txt
```

### Ejecutar el robot
```bash
cd src
python main.py
```

### Abrir la memoria (Jupyter Notebook)
```bash
jupyter notebook memoria_actividad_astar.ipynb
```
O abrirla directamente en VSCode con la extensión **Jupyter**.

## Algoritmo

Se implementa **A\*** con:
- **Heurística h(n):** distancia Manhattan — admisible y consistente.
- **Coste g(n):** uniforme (1 por movimiento).
- **Estructura:** min-heap (`heapq`) para la lista abierta y `set` para la lista cerrada.

La función de evaluación es: `f(n) = g(n) + h(n)`

## Resultado

El plan generado cubre **36 pasos** en total:

| Sub-tarea | Pasos |
|-----------|-------|
| Robot → M1 (PICKUP) | 5 |
| M1 → destino [3,3] (DROP) | 7 |
| Robot → M2 (PICKUP) | 6 |
| M2 → destino [3,2] (DROP) | 5 |
| Robot → M3 (PICKUP) | 5 |
| M3 → destino [3,1] (DROP) | 6 |

---

Universidad Internacional de La Rioja (UNIR) · Razonamiento y Planificación Automática
