# traductorDeSe-as

Traductor de Lengua de Señas Mexicana (LSM) basado en inteligencia artificial y visión artificial. El proyecto convierte señas **a texto** (reconocimiento en tiempo real con la cámara) y **texto a señas** (representación visual de la seña correspondiente), e incorpora un módulo educativo para consultar, practicar y recibir retroalimentación al aprender la lengua de señas.

## Objetivo

Reducir las barreras de comunicación entre personas sordas, con discapacidad auditiva y personas oyentes, ofreciendo una herramienta de traducción bidireccional y educativa en un solo lugar, desarrollada inicialmente con un conjunto limitado de señas y ampliable de forma progresiva.

## Módulos

- **Reconocimiento de señas (señas → texto):** detección de manos con MediaPipe y clasificación de landmarks para traducir en vivo lo que la persona señala frente a la cámara.
- **Texto a señas:** el usuario escribe texto y la aplicación muestra la representación visual de las señas correspondientes (banco de señas + reproductor).
- **Módulo educativo:** consulta de señas, modo de práctica con cámara y retroalimentación automática sobre la ejecución.
- **Registro de nuevas señas:** grabación de señas nuevas desde la web para ampliar el vocabulario sin rediseñar el sistema.

## Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python |
| Visión artificial | OpenCV, MediaPipe (HandLandmarker) |
| Aprendizaje automático | TensorFlow / PyTorch (clasificador sobre landmarks) |
| API | FastAPI / Flask |
| Interfaz web | HTML, CSS, JavaScript (MediaDevices) |
| Despliegue | Docker |

**Enfoque:** se usan modelos y corpora preentrenados (evitando entrenar desde cero) y se aplica ajuste fino (transfer learning) sobre el corpus de lengua de señas en español (p. ej. Sign4all / LSE_UVIGO).

## Estructura del proyecto

```
traductorDeSe-as/
├── docs/                      # Documentación del proyecto
│   ├── planteamiento-del-problema.md
│   ├── justificacion.md
│   ├── tecnologias-sugeridas.md
│   └── sprints.md             # Plan de 12 sprints (Scrum)
├── models/                    # Modelos preentrenados (.task) — descargados automáticamente
├── src/                       # Código fuente
│   └── deteccion_manos.py     # Detección de manos en tiempo real
└── README.md
```

## Instalación

Se requiere Python 3.10+.

```bash
git clone https://github.com/proyecto059/traductorDeSe-as.git
cd traductorDeSe-as

# (opcional) crear y activar un entorno virtual
python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

> **Nota:** el modelo de detección de manos (`hand_landmarker.task`) se descarga automáticamente a `models/` la primera vez que se ejecuta el script.

## Uso

**Detección de manos en tiempo real (módulo base de reconocimiento):**

```bash
python src/deteccion_manos.py
```

Se abre la ventana de la cámara con los landmarks de las manos dibujados y el estado de detección en pantalla. Para detenerla, presiona `Ctrl+C` en la terminal.

## Plan de desarrollo

El proyecto se desarrolla en **12 sprints** bajo metodología **Scrum**. Detalle completo en [docs/sprints.md](docs/sprints.md).

## Documentación

- [Planteamiento del problema](docs/planteamiento-del-problema.md)
- [Justificación](docs/justificacion.md)
- [Tecnologías sugeridas](docs/tecnologias-sugeridas.md)
- [Plan de sprints](docs/sprints.md)