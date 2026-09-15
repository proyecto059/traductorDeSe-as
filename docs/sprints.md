# Plan de 10 sprints — Enfoque con modelos preentrenados

Cada sprint se compone de: **Meta**, **Acciones** y **MVP** (producto mínimo viable entregable al cierre del sprint).

**Enfoque:** en lugar de construir y entrenar un modelo desde cero, el proyecto se basa en modelos y datos preentrenados existentes. El Sprint 1 define qué tecnologías se usarán, para qué, y qué modelos/corpora preentrenados se aprovecharán.

## Sprint 1 — Selección de tecnologías y evaluación de modelos preentrenados

- **Meta:** Definir la pila tecnológica del proyecto y seleccionar los modelos preentrenados y corpora de lengua de señas en español (LSE/LSM) que se usarán.
- **Acciones:**
  - Listar necesidades por módulo: reconocimiento de señas, texto a señas, educativo, API e interfaz web.
  - Seleccionar tecnologías con su justificación:
    - **Python**: lenguaje base de todo el backend.
    - **MediaPipe (HandLandmarker)**: detección preentrenada de manos y 21 landmarks.
    - **OpenCV**: captura y procesamiento de video en tiempo real.
    - **TensorFlow/PyTorch**: cargar el clasificador preentrenado y hacer ajuste fino.
    - **FastAPI/Flask**: API que expone los módulos.
    - **HTML/CSS/JS + MediaDevices**: interfaz web con la cámara del navegador.
    - **Docker**: empaquetado y despliegue.
  - Investigar modelos preentrenados disponibles (MediaPipe, Hugging Face, GitHub, Kaggle).
  - Evaluar corpora públicos en español: Sign4all (LSE), LSE_UVIGO y variantes para LSM; verificar licencias y formatos.
- **MVP:** Documento de selección con la tabla tecnología → para qué se usa, y los modelos/corpora elegidos con su licencia.

## Sprint 2 — Preparación del entorno, detección y corpus

- **Meta:** Tener el entorno configurado, el detector preentrenado funcionando y el corpus en español descargado.
- **Acciones:**
  - Crear entorno virtual e instalar las tecnologías seleccionadas en el Sprint 1.
  - Probar MediaPipe HandLandmarker con la cámara y validar los landmarks contra el formato de los corpora.
  - Descargar el corpus en español (Sign4all / LSE_UVIGO) y dejar los keypoints listos para el clasificador.
  - Seleccionar el subconjunto de señas del vocabulario inicial.
- **MVP:** Entorno listo, detección de landmarks validada en tiempo real y corpus en español preparado.

## Sprint 3 — Adecuación del clasificador preentrenado

- **Meta:** Obtener un clasificador de señas funcional sin entrenar desde cero.
- **Acciones:**
  - Buscar clasificadores preentrenados sobre landmarks (ASL como base, en su defecto).
  - Adaptar el modelo existente al vocabulario del corpus español mediante ajuste fino (transfer learning) o cambio de capa de salida.
  - Entrenar solo la última capa (o un clasificador ligero) sobre los landmarks del corpus.
- **MVP:** Clasificador funcional que reconoce las señas del vocabulario inicial con precisión evaluada.

## Sprint 4 — Reconocimiento de señas en tiempo real

- **Meta:** Integrar el detector y el clasificador para traducir señas a texto en vivo.
- **Acciones:**
  - Conectar MediaPipe HandLandmarker con el clasificador.
  - Implementar búfer de secuencia y predicción con umbral de confianza.
  - Mostrar la palabra reconocida sobre el video.
- **MVP:** Traducción de señas → texto en tiempo real con la cámara.

## Sprint 5 — API backend e interfaz web

- **Meta:** Exponer los módulos mediante una API y construir la interfaz web que muestra la traducción en vivo.
- **Acciones:**
  - Levantar FastAPI o Flask con endpoints: `/reconocer`, `/texto-a-senas`, `/registrar-se-na`.
  - Manejar subida de frames y devolución de resultados en JSON.
  - Frontend (HTML/CSS/JS) con captura de video mediante MediaDevices y envío de frames al backend.
  - Vista de estado (mano detectada / no detectada).
- **MVP:** Página web que consume la API y muestra la traducción de señas a texto en vivo; API probada con Swagger o curl.

## Sprint 6 — Módulo texto a señas

- **Meta:** Convertir texto en una representación visual de señas reproducibles.
- **Acciones:**
  - Usar reproductores/avatares existentes y bancos de señas (JSON de poses) disponibles.
  - Definir banco de señas del vocabulario con los landmarks del corpus.
  - Construir frases a partir del banco.
- **MVP:** El usuario escribe una palabra y la aplicación la representa en señas.

## Sprint 7 — Registro de nuevas señas en la app

- **Meta:** Ampliar el vocabulario grabando señas nuevas sin rediseñar el sistema.
- **Acciones:**
  - Endpoint y UI para grabar una seña nueva desde la cámara.
  - Añadir la seña al banco y actualizar el clasificador con ajuste fino.
- **MVP:** Una seña nueva grabada desde la web que pasa a formar parte del reconocimiento.

## Sprint 8 — Módulo educativo

- **Meta:** Brindar aprendizaje de señas con consulta, práctica y retroalimentación.
- **Acciones:**
  - Sección de consulta de señas (ver ejemplo de cómo se realiza).
  - Modo práctica con cámara que evalúa la ejecución con el clasificador.
  - Retroalimentación básica (correcto/incorrecto, consejos).
- **MVP:** El usuario practica una seña y recibe evaluación sobre su ejecución.

## Sprint 9 — Pruebas y pulido

- **Meta:** Garantizar la estabilidad, el rendimiento y la usabilidad del sistema completo.
- **Acciones:**
  - Pruebas de los módulos (unitarias e integración).
  - Corrección de fallos, rendimiento y manejo de errores.
  - Ajustes de usabilidad en la interfaz.
- **MVP:** Aplicación completa y estable con los 3 módulos funcionando.

## Sprint 10 — Despliegue y documentación

- **Meta:** Publicar la aplicación y documentar su instalación y uso.
- **Acciones:**
  - Empaquetar la aplicación (Docker, requisitos, guía de ejecución).
  - Redactar documentación técnica y de uso.
  - Desplegar en servidor o dirección compartible.
- **MVP:** Aplicación publicada con documentación de instalación y uso.