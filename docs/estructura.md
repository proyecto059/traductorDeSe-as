# Estructura y convenciones del proyecto

Este documento describe la organización del repositorio y las convenciones para agregar
nuevo trabajo de forma consistente.

## Organización por capas

| Carpeta | Contenido | Ejemplo |
|---|---|---|
| `web/` | Interfaz web (frontend) | `web/index.html`, `web/js/app.js` |
| `src/` | Código Python reutilizable (libertas y módulos) | `src/msl150_datos.py` |
| `scripts/` | Puntos de entrada ejecutables del pipeline | `scripts/03_entrenar_lstm.py` |
| `tests/` | Pruebas unitarias (pytest) | `tests/test_msl150_datos.py` |
| `docs/` | Documentación | `docs/sprints.md` |
| `models/` | Modelos descargados/entrenados (no versionados) | `models/hand_landmarker.task` |
| `data/` | Datasets (no versionados) | `data/msl150/` |

## Convenciones

### Python

- Los scripts de `scripts/` son **entrypoints**: solo contendrán lógica de CLI/orquestación
  y delegarán el trabajo a módulos de `src/`.
- La lógica reutilizable vive en `src/` (p. ej. `msl150_datos.py`, `msl150_modelo.py`).
- Los scripts cargan los módulos de `src/` agregando la ruta al inicio:

  ```python
  import sys
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
  ```

- Nombrar los scripts del pipeline con prefijo numérico (`01_`, `02_`, ...) para indicar
  el orden de ejecución.
- Constantes compartidas (rutas, URL, hiperparámetros) en `src/msl150_datos.py`.
- Las funciones de datos que no dependen de red ni de disco directo deben probarse en
  `tests/`.

### Web

- Todo el frontend vive dentro de `web/`. Las referencias relativas (`css/`, `js/`,
  `assets/`, `modelo/`) se resuelven dentro de esa carpeta.
- El modelo para el navegador (`modelo.json`, etiquetas) vive en `web/modelo/`.

### Git / CI

- `models/` y `data/` no se versionan (ver `.gitignore`); se generan mediante scripts.
- No commitear `__pycache__/`, `.pytest_cache/`, ni entornos virtuales.
- Cada commit debe ser temático (fix, feature, refactor, docs, test) e idealmente
  corresponder a un ítem de trabajo del plan de sprints.

## Cómo agregar nuevo trabajo

1. Identificar el sprint relacionado en `docs/sprints.md`.
2. Si es lógica reutilizable → crear/editar módulo en `src/`.
3. Si es un paso del pipeline → agregar script en `scripts/` con prefijo numérico.
4. Si es regla de negocio o procesamiento → agregar pruebas en `tests/`.
5. Documentar el cambio en `README.md` y/o `docs/` si afecta el uso.

### Checklist antes de commitear

- [ ] Se ejecutó `pytest` y pasan las pruebas.
- [ ] Se ejecutó el script con `--help` (si aplica).
- [ ] No se incluyen `data/`, `models/`, `__pycache__/`.
- [ ] El mensaje de commit describe el cambio y su alcance.