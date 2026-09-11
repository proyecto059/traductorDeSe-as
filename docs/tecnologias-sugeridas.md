# Tecnologías sugeridas

## Lenguaje de programación

- **Python**: ecosistema maduro para visión artificial y aprendizaje automático, amplia comunidad y gran cantidad de librerías especializadas.

## Visión artificial y procesamiento de imágenes

- **OpenCV**: captura y procesamiento de video en tiempo real, operaciones geométricas y preprocesamiento de imágenes.
- **MediaPipe (Google)**: detección y seguimiento de manos y cuerpo mediante puntos de referencia (landmarks), ideal para extraer características de las señas realizadas frente a la cámara sin necesidad de grandes recursos de cómputo.

## Aprendizaje automático

- **TensorFlow** o **PyTorch**: entrenamiento e inferencia de redes neuronales para el reconocimiento de señas.
- **Modelos secuenciales (LSTM/GRU)** o **redes neuronales convolucionales (CNN/3D-CNN)**: clasificación de secuencias de puntos de referencia de manos para identificar la seña ejecutada. MediaPipe permite reducir el problema a una tarea de clasificación de secuencias de landmarks, lo que simplifica el entrenamiento y mejora la velocidad de inferencia.

## Despliegue y aplicación

- **Flask** o **FastAPI**: API web que expone los módulos de traducción, reconocimiento y aprendizaje.
- **Interfaz web (HTML/CSS/JavaScript)** con consumo de video desde la cámara mediante WebRTC o la API de MediaDevices, enviando los frames al backend para su procesamiento.

## Módulo texto a señas

- **Representación por avatar o animación (JSON + reproductor de animaciones)**: cada seña puede modelarse como una secuencia de poses de manos y cuerpo reproducibles en una interfaz, permitiendo la construcción de frases a partir de un banco de señas.

## Gestión de datos y entrenamiento

- **Conjunto de datos propio**: grabación de ejemplos de señas por parte del equipo; estructura de carpetas por palabra y metadata en JSON.
- **Pandas / NumPy**: organización, limpieza y manipulación de los datos para el entrenamiento.