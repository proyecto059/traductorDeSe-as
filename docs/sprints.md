# Plan de 12 sprints — Metodología Scrum

Cada sprint se compone de: **Meta**, **Acciones** y **MVP** (mínimo producto viable entregable al cierre del sprint).

**Enfoque:** en lugar de construir y entrenar un modelo desde cero, el proyecto se basa en modelos y datos preentrenados existentes. El Sprint 1 define qué tecnologías se usarán, para qué, y qué modelos/corpora preentrenados se aprovecharán.

## Sprint 1 — Selección de tecnologías y evaluación de modelos preentrenados

- **Meta:** Definir la pila tecnológica del proyecto, seleccionar los modelos preentrenados y corpora de lengua de señas en español (LSE/LSM) que se usarán y elaborar el Product Backlog inicial.
- **Acciones:**
  - Listar necesidades por módulo: reconocimiento de señas, texto a señas, educativo, API e interfaz web.
  - Seleccionar tecnologías con su justificación:
    - **Python**: lenguaje base de todo el backend.
    - **MediaPipe (HandLandmarker)**: detección preentrenada de manos y 21 landmarks.
    - **OpenCV**: captura y procesamiento de video en tiempo real.
    - **TensorFlow/PyTorch**: cargar el clasificador preentrenado y hacer ajuste fino.
    - **FastAPI/Flask**: API que expone los módulos.
    - **HTML/CSS/JS + MediaDevices**: interfaz web con la cámara del navegador.
  - Investigar modelos preentrenados disponibles (MediaPipe, Hugging Face, GitHub, Kaggle).
  - Evaluar corpora públicos en español: Sign4all (LSE), LSE_UVIGO y variantes para LSM; verificar licencias y formatos.
  - Priorizar el Product Backlog para planificar los siguientes sprints.
- **MVP:** Documento de selección con la tabla tecnología → para qué se usa, los modelos/corpora elegidos con su licencia y el Product Backlog inicial priorizado.

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
  - Evaluar la precisión del clasificador por seña del vocabulario inicial.
- **MVP:** Clasificador funcional que reconoce las señas del vocabulario inicial con precisión evaluada.

## Sprint 4 — Reconocimiento de señas en tiempo real

- **Meta:** Integrar el detector y el clasificador para traducir señas a texto en vivo.
- **Acciones:**
  - Conectar MediaPipe HandLandmarker con el clasificador.
  - Implementar búfer de secuencia y predicción con umbral de confianza.
  - Mostrar la palabra reconocida sobre el video.
  - Manejar estados de mano ausente y errores sin interrumpir la captura.
- **MVP:** Traducción de señas → texto en tiempo real con la cámara.

## Sprint 5 — API backend

- **Meta:** Exponer los módulos del sistema mediante una API documentada.
- **Acciones:**
  - Levantar FastAPI o Flask con los endpoints: `/reconocer`, `/texto-a-senas`, `/registrar-se-na`.
  - Manejar subida de frames y devolución de resultados en JSON.
  - Validar entradas y devolver mensajes de error consistentes.
  - Documentar la API (Swagger u OpenAPI).
- **MVP:** API funcional probada con Swagger o curl y lista para ser consumida por la interfaz web.

## Sprint 6 — Interfaz web de traducción en vivo

- **Meta:** Construir la interfaz web que consume la API y muestra la traducción de señas a texto en vivo.
- **Acciones:**
  - Frontend (HTML/CSS/JS) con captura de video mediante MediaDevices y envío de frames al backend.
  - Integrar la visualización del resultado del endpoint `/reconocer`.
  - Vista de estado (mano detectada / no detectada) y de la palabra reconocida.
  - Ajustes básicos de usabilidad y accesibilidad.
- **MVP:** Página web que consume la API y muestra la traducción de señas a texto en vivo.

## Sprint 7 — Módulo texto a señas

- **Meta:** Convertir texto en una representación visual de señas reproducibles.
- **Acciones:**
  - Usar reproductores/avatares existentes y bancos de señas (JSON de poses) disponibles.
  - Definir banco de señas del vocabulario con los landmarks del corpus.
  - Construir frases a partir del banco.
  - Conectar el endpoint `/texto-a-senas` con la interfaz web.
- **MVP:** El usuario escribe una palabra y la aplicación la representa en señas.

## Sprint 8 — Registro de nuevas señas en la app

- **Meta:** Ampliar el vocabulario grabando señas nuevas desde la web sin rediseñar el sistema.
- **Acciones:**
  - Endpoint y UI para grabar una seña nueva desde la cámara.
  - Añadir la seña al banco y actualizar el clasificador con ajuste fino.
  - Definir un flujo de validación de las señas registradas.
- **MVP:** Una seña nueva grabada desde la web que pasa a formar parte del reconocimiento.

## Sprint 9 — Módulo educativo

- **Meta:** Brindar aprendizaje de señas con consulta, práctica y retroalimentación.
- **Acciones:**
  - Sección de consulta de señas (ver ejemplo de cómo se realiza).
  - Modo práctica con cámara que evalúa la ejecución con el clasificador.
  - Retroalimentación básica (correcto/incorrecto, consejos).
  - Registro del progreso del usuario.
- **MVP:** El usuario practica una seña y recibe evaluación sobre su ejecución.

## Sprint 10 — Pruebas y aseguramiento de calidad

- **Meta:** Garantizar la estabilidad, el rendimiento y la usabilidad del sistema completo.
- **Acciones:**
  - Pruebas unitarias e integración de los módulos (API, clasificador, frontend).
  - Corrección de fallos, rendimiento y manejo de errores.
  - Pruebas con usuarios y registro de retroalimentación.
  - Ajustes de usabilidad en la interfaz.
- **MVP:** Aplicación completa y estable con los 3 módulos funcionando y pruebas aplicadas.

## Sprint 11 — Despliegue

- **Meta:** Publicar la aplicación en un entorno accesible para los usuarios finales.
- **Acciones:**
  - Preparar la aplicación para su despliegue (requisitos, guía de ejecución).
  - Configurar el despliegue (servidor o servicio en la nube) con variables de entorno seguras.
  - Verificar el funcionamiento de la cámara y de las rutas HTTPS en producción.
- **MVP:** Aplicación publicada y accesible desde cualquier navegador mediante una URL.

## Sprint 12 — Documentación y cierre del proyecto

- **Meta:** Documentar la instalación, el uso y el mantenimiento del sistema, y cerrar formalmente el proyecto.
- **Acciones:**
  - Redactar documentación técnica y de uso.
  - Documentar los procesos de reentrenamiento y ampliación de vocabulario.
  - Organizar el repositorio y preparar los materiales de entrega.
  - Realizar la revisión final y la retrospectiva del proyecto.
- **MVP:** Documentación completa de instalación y uso con el repositorio organizado y listo para entrega.