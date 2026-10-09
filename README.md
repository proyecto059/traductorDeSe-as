# traductorDeSe-as

Traductor de **Lengua de Señas Mexicana (LSM)** basado en inteligencia artificial y visión
artificial. El proyecto convierte señas **a texto** (reconocimiento en tiempo real con la
cámara) y **texto a señas** (representación visual), e incorpora un módulo educativo para
consultar, practicar y recibir retroalimentación al aprender la lengua de señas.

## Módulos

| Módulo | Descripción |
|---|---|
| Reconocimiento de señas (señas → texto) | Detección de manos con MediaPipe y clasificación de landmarks (LSTM) para traducir en vivo. |
| Texto a señas | El usuario escribe texto y la app reproduce la secuencia de señas correspondiente. |
| Educativo | Consulta de señas, modo práctica con cámara y retroalimentación. |
| Registro de señas | Grabación de señas nuevas para ampliar el vocabulario. |

## Estructura del proyecto

```
traductorDeSe-as/
├── web/                        # Interfaz web (frontend)
│   ├── index.html              # Página principal
│   ├── css/estilos.css         # Estilos
│   ├── js/app.js               # Lógica de cámara y traducción
│   ├── assets/                 # Recursos estáticos (imágenes)
│   └── modelo/                 # Modelo web (JSON) para el frontend
├── src/                        # Código Python reutilizable
│   ├── deteccion_manos.py      # Detección de manos en tiempo real (MediaPipe)
│   ├── msl150_datos.py         # Carga, preprocesado y split del dataset MSL-150
│   └── msl150_modelo.py        # Arquitectura LSTM + carga/guardado de pesos
├── scripts/                    # Pipeline de ML ejecutable (numerado)
│   ├── 01_descargar_datos.py   # Descarga del dataset MSL-150
│   ├── 02_preparar_datos.py    # Convierte a tensores (N, 30, 226) y hace split
│   ├── 03_entrenar_lstm.py     # Entrena el LSTM y guarda checkpoint
│   ├── 04_evaluar.py           # Reporte de métricas y matriz de confusión
│   └── 05_inferencia_tiempo_real.py  # Traducción en tiempo real con la cámara
├── tests/                      # Pruebas unitarias (pytest)
├── docs/                       # Documentación del proyecto
├── models/                     # Modelos .task/.pt (descargados automáticamente, no versionados)
├── data/                       # Datasets (no versionados)
├── requirements.txt            # Dependencias Python
└── README.md
```

## Instalación

Requiere Python 3.10+.

```bash
git clone https://github.com/proyecto059/traductorDeSe-as.git
cd traductorDeSe-as

# (opcional) entorno virtual
python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

> Los modelos (`hand_landmarker.task`, `holistic_landmarker.task`) se descargan
> automáticamente a `models/` la primera vez que se ejecutan los scripts.

## Uso

**Interfaz web:**

```bash
cd web
python -m http.server 8000
# abre http://localhost:8000
```

**Pipeline de ML:**

```bash
# 1) Descargar el subset demo del dataset MSL-150
python scripts/01_descargar_datos.py --fuente github

# 2) Preparar datos de entrada (N, 30, 226)
python scripts/02_preparar_datos.py

# 3) Entrenar el LSTM
python scripts/03_entrenar_lstm.py

# 4) Evaluar el modelo
python scripts/04_evaluar.py

# 5) Pruebas unitarias
pytest
```

**Detección de manos en tiempo real (módulo base):**

```bash
python src/deteccion_manos.py
```

## Documentación

- [Planteamiento del problema](docs/planteamiento-del-problema.md)
- [Justificación](docs/justificacion.md)
- [Tecnologías sugeridas](docs/tecnologias-sugeridas.md)
- [Plan de sprints](docs/sprints.md)
- [Estructura y convenciones](docs/estructura.md)