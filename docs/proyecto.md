# Proyecto: traductorDeSe-as

## ¿Qué es el proyecto?

Un **traductor de Lengua de Señas Mexicana (LSM)** basado en inteligencia artificial y visión artificial, accesible desde el navegador, que ofrece traducción bidireccional:

1. **Señas → texto:** reconoce en tiempo real las señas realizadas frente a la cámara y las convierte en texto.
2. **Texto → señas:** el usuario escribe una palabra o frase y la aplicación la muestra como representación visual de señas.

Además incorpora un **módulo educativo** para consultar, practicar y recibir retroalimentación al aprender la lengua de señas, y un **módulo de registro** que permite ampliar el vocabulario grabando señas nuevas sin rediseñar el sistema.

## ¿Qué problema resuelve?

Reduce las barreras de comunicación entre personas sordas, con discapacidad auditiva y personas oyentes, ofreciendo una herramienta accesible, gratuita y en tiempo real que combina traducción y aprendizaje en un solo lugar.

## Alcance

- Vocabulario inicial limitado de señas de LSM, ampliable de forma progresiva mediante el registro de nuevas señas.
- Funciona con una cámara web estándar, sin hardware especializado.
- Desarrollado con un enfoque de **modelos preentrenados** (sin entrenar desde cero), aplicando ajuste fino (transfer learning) sobre corpora de lengua de señas en español (p. ej. Sign4all / LSE_UVIGO, con variantes para LSM).

## Módulos

| Módulo | Descripción |
|---|---|
| Reconocimiento de señas | Detección de manos con MediaPipe (HandLandmarker) y clasificación de landmarks para traducir en vivo lo que la persona señala. |
| Texto a señas | El usuario escribe texto y la app reproduce la secuencia de señas correspondiente desde un banco de poses. |
| Educativo | Consulta de señas, modo práctica con cámara y retroalimentación automática sobre la ejecución. |
| Registro de señas | Grabación de señas nuevas desde la web para ampliar el vocabulario del sistema. |

## Arquitectura propuesta

- **Backend (Python):** captura y procesamiento de video (OpenCV), detección de manos (MediaPipe), clasificación de landmarks (TensorFlow/PyTorch) y API (FastAPI/Flask).
- **Frontend (HTML/CSS/JS):** interfaz web que accede a la cámara mediante la API MediaDevices, envía los frames al backend y muestra los resultados.

## Enfoque de desarrollo

- **Scrum** con plan de 12 sprints (ver [sprints.md](sprints.md)).
- Uso de modelos y corpora preentrenados + ajuste fino, priorizando velocidad de desarrollo y bajo costo de cómputo.
- Detalles técnicos en [tecnologias-sugeridas.md](tecnologias-sugeridas.md).

## Estado actual

En fase de definición y arranque: tecnologías seleccionadas, plan de sprints establecido y módulo base de detección de manos en desarrollo.