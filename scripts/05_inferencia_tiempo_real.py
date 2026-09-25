import argparse
import threading
import time
from collections import deque
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
import torch
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision

from msl150_datos import (
    CARPETA_MODELOS,
    MODELO_HOLISTIC_RUTA,
    NUM_FRAMES,
    URL_MODELO_HOLISTIC,
    extraer_fila_holistic,
)
from msl150_modelo import cargar_modelo, predecir_probs

COLOR_VERDE = (60, 200, 120)
COLOR_ROJO = (0, 0, 255)
COLOR_BLANCO = (255, 255, 255)


def asegurar_modelo_holistic() -> Path:
    if MODELO_HOLISTIC_RUTA.exists():
        return MODELO_HOLISTIC_RUTA

    import urllib.request

    MODELO_HOLISTIC_RUTA.parent.mkdir(parents=True, exist_ok=True)
    print(f"Descargando modelo holistic: {URL_MODELO_HOLISTIC}")
    urllib.request.urlretrieve(URL_MODELO_HOLISTIC, MODELO_HOLISTIC_RUTA)
    return MODELO_HOLISTIC_RUTA


def crear_holistic_landmarker() -> vision.HolisticLandmarker:
    opciones = vision.HolisticLandmarkerOptions(
        base_options=mp_tasks.BaseOptions(
            model_asset_path=str(asegurar_modelo_holistic())
        ),
        running_mode=vision.RunningMode.VIDEO,
        min_pose_detection_confidence=0.5,
        min_pose_landmarks_confidence=0.5,
        min_hand_landmarks_confidence=0.5,
    )
    return vision.HolisticLandmarker.create_from_options(opciones)


def dibujar_manos(frame, resultado):
    altura, ancho = frame.shape[:2]
    for manos in (resultado.left_hand_landmarks, resultado.right_hand_landmarks):
        if not manos:
            continue
        for p in manos:
            x = int(p.x * ancho)
            y = int(p.y * altura)
            cv2.circle(frame, (x, y), 3, COLOR_VERDE, -1)


def procesar_video(modelo, clases, cap, detener, confianza_umbral, espejo, dispositivo):
    landmarker = crear_holistic_landmarker()
    buffer = deque(maxlen=NUM_FRAMES)
    inicio = time.monotonic()
    palabra = "..."

    try:
        while cap.isOpened() and not detener.is_set():
            ok, frame = cap.read()
            if not ok:
                break

            if espejo:
                frame = cv2.flip(frame, 1)

            frame_ms = int((time.monotonic() - inicio) * 1000)
            imagen = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            )
            resultado = landmarker.detect_for_video(imagen, frame_ms)

            fila = extraer_fila_holistic(resultado)
            hay_senal = bool(fila[:100].any()) or bool(fila[100:226].any())
            buffer.append(fila)

            dibujar_manos(frame, resultado)

            confianza = 0.0
            if len(buffer) == NUM_FRAMES:
                probs = predecir_probs(modelo, np.stack(list(buffer)), dispositivo)
                mejor = int(np.argmax(probs))
                confianza = float(probs[mejor])
                if confianza >= confianza_umbral:
                    palabra = clases[mejor]
                else:
                    palabra = "..."
                top = list(np.argsort(probs)[::-1][:3])
                top_texto = " | ".join(f"{clases[i]}({probs[i]:.2f})" for i in top)
            else:
                top_texto = "llenando buffer..."

            estado = "SEAL DETECTADA" if hay_senal else "SIN SEAL"
            color = COLOR_VERDE if hay_senal else COLOR_ROJO
            cv2.putText(frame, f"{estado} [{len(buffer)}/{NUM_FRAMES}]", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, f"Palabra: {palabra} ({confianza:.2f})", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, COLOR_VERDE, 2)
            cv2.putText(frame, f"Top3: {top_texto}", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_BLANCO, 1)

            cv2.imshow("MSL-150 LSTM en tiempo real", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cv2.destroyAllWindows()
        landmarker.close()


def main():
    parser = argparse.ArgumentParser(
        description="Inferencia en tiempo real del LSTM de MSL-150 con MediaPipe Holistic."
    )
    parser.add_argument("--modelo", default=str(CARPETA_MODELOS / "lstm_msl150.pt"))
    parser.add_argument("--camara", type=int, default=0)
    parser.add_argument("--archivo", default=None, help="Video .mp4 en lugar de camara.")
    parser.add_argument("--confianza", type=float, default=0.7)
    parser.add_argument("--sin-espejo", action="store_true",
                        help="No aplicar espejo horizontal a la captura.")
    args = parser.parse_args()

    if not Path(args.modelo).exists():
        raise FileNotFoundError(
            f"No hay modelo entrenado en {args.modelo}. "
            "Entrena primero con scripts/03_entrenar_lstm.py"
        )

    dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
    modelo, clases = cargar_modelo(args.modelo, dispositivo)
    print(f"Modelo cargado ({len(clases)} clases) en {dispositivo}")

    if args.archivo:
        cap = cv2.VideoCapture(args.archivo)
    else:
        cap = cv2.VideoCapture(args.camara)
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir la fuente de video: {args.camara or args.archivo}")

    detener = threading.Event()
    hilo = threading.Thread(
        target=procesar_video,
        args=(modelo, clases, cap, detener, args.confianza, not args.sin_espejo, dispositivo),
        daemon=True,
    )
    hilo.start()

    print("Mostrando video. Presiona Ctrl+C en la terminal o 'q' en la ventana para detener.")
    try:
        while hilo.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        detener.set()
        print("\nDetenido por el usuario.")

    hilo.join(timeout=5)
    cap.release()


if __name__ == "__main__":
    main()