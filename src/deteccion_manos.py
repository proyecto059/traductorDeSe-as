import threading
import time
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision

MODELO_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)
MODELO_RUTA = Path(__file__).resolve().parent.parent / "models" / "hand_landmarker.task"
LANDMARK_COLOR = (50, 200, 120)
CONEXION_COLOR = (255, 255, 255)


def asegurar_modelo() -> Path:
    if MODELO_RUTA.exists():
        return MODELO_RUTA

    import urllib.request

    MODELO_RUTA.parent.mkdir(parents=True, exist_ok=True)
    print(f"Descargando modelo: {MODELO_URL}")
    urllib.request.urlretrieve(MODELO_URL, MODELO_RUTA)
    return MODELO_RUTA


def crear_landmarker() -> vision.HandLandmarker:
    opciones = vision.HandLandmarkerOptions(
        base_options=mp_tasks.BaseOptions(model_asset_path=str(asegurar_modelo())),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    return vision.HandLandmarker.create_from_options(opciones)


def procesar_video(
    landmarker: vision.HandLandmarker,
    cap: cv2.VideoCapture,
    detener: threading.Event,
) -> None:
    conexiones = vision.HandLandmarksConnections.HAND_CONNECTIONS
    inicio = time.monotonic()

    try:
        while cap.isOpened() and not detener.is_set():
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            frame_ms = int((time.monotonic() - inicio) * 1000)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            )
            resultado = landmarker.detect_for_video(mp_image, frame_ms)

            num_manos = 0
            if resultado.hand_landmarks:
                num_manos = len(resultado.hand_landmarks)
                for landmarks, clasificaciones in zip(
                    resultado.hand_landmarks, resultado.handedness
                ):
                    for punto in landmarks:
                        x = int(punto.x * frame.shape[1])
                        y = int(punto.y * frame.shape[0])
                        cv2.circle(frame, (x, y), 3, LANDMARK_COLOR, -1)

                    for conexion in conexiones:
                        x1 = int(landmarks[conexion.start].x * frame.shape[1])
                        y1 = int(landmarks[conexion.start].y * frame.shape[0])
                        x2 = int(landmarks[conexion.end].x * frame.shape[1])
                        y2 = int(landmarks[conexion.end].y * frame.shape[0])
                        cv2.line(frame, (x1, y1), (x2, y2), CONEXION_COLOR, 2)

                    etiqueta = clasificaciones[0].category_name
                    confianza = clasificaciones[0].score
                    cx = int(landmarks[0].x * frame.shape[1])
                    cy = int(landmarks[0].y * frame.shape[0])
                    cv2.putText(
                        frame,
                        f"{etiqueta} ({confianza:.2f})",
                        (cx, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        LANDMARK_COLOR,
                        2,
                    )

            estado = "MANO(S) DETECTADA(S)" if num_manos > 0 else "SIN MANO"
            color = (0, 255, 0) if num_manos > 0 else (0, 0, 255)
            cv2.putText(
                frame,
                f"{estado} - {num_manos} mano(s)",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )

            cv2.imshow("Deteccion de manos - MediaPipe", frame)
            cv2.waitKey(1)
    finally:
        cv2.destroyAllWindows()


def main() -> None:
    landmarker = crear_landmarker()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        landmarker.close()
        raise RuntimeError("No se pudo abrir la cámara (índice 0).")

    detener = threading.Event()
    hilo = threading.Thread(
        target=procesar_video,
        args=(landmarker, cap, detener),
        daemon=True,
    )
    hilo.start()

    print("Mostrando video en pantalla. Presiona Ctrl+C para detener.")
    try:
        while hilo.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        detener.set()
        print("\nDeteccion detenida por el usuario (Ctrl+C).")

    hilo.join(timeout=5)
    cap.release()
    landmarker.close()


if __name__ == "__main__":
    main()