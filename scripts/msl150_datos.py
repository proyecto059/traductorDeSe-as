import csv
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

NUM_FRAMES = 30
DIMENSION = 226

RUTAS_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS = RUTAS_PROYECTO / "data" / "msl150"
CARPETA_SAMPLE_NPY = CARPETA_DATOS / "sample_npy"
CARPETA_PREPARADOS = CARPETA_DATOS / "procesado"
CARPETA_MODELOS = RUTAS_PROYECTO / "models" / "msl150"

URL_ZENODO = "https://zenodo.org/api/records/17783312"
URL_REPO_ZIP = (
    "https://codeload.github.com/armandobecerril/MSL-150-Dataset/zip/refs/heads/main"
)
URL_MODELO_HOLISTIC = (
    "https://storage.googleapis.com/mediapipe-models/holistic_landmarker/"
    "holistic_landmarker/float16/1/holistic_landmarker.task"
)
MODELO_HOLISTIC_RUTA = RUTAS_PROYECTO / "models" / "holistic_landmarker.task"

INDICES_POSE = [i for i in range(33) if i < 25 or i > 32]


def _clave_directorio(p):
    return int(p.name)


def _clave_archivo(p):
    return int(p.stem)


def _aplanar_landmarks(landmarks):
    if not landmarks:
        return []
    primeros = landmarks[0]
    if hasattr(primeros, "x"):
        return landmarks
    return [lm for sub in landmarks for lm in sub]


def extraer_fila_holistic(resultado):
    pose = _aplanar_landmarks(getattr(resultado, "pose_landmarks", None))
    if pose:
        pose = [pose[i] for i in INDICES_POSE if i < len(pose)]
        pose = np.array(
            [[p.x, p.y, p.z, p.visibility] for p in pose], dtype=np.float32
        ).flatten()
    else:
        pose = np.zeros(25 * 4, dtype=np.float32)

    lh = _aplanar_landmarks(getattr(resultado, "left_hand_landmarks", None))
    if lh:
        lh = np.array([[p.x, p.y, p.z] for p in lh], dtype=np.float32).flatten()
    else:
        lh = np.zeros(21 * 3, dtype=np.float32)

    rh = _aplanar_landmarks(getattr(resultado, "right_hand_landmarks", None))
    if rh:
        rh = np.array([[p.x, p.y, p.z] for p in rh], dtype=np.float32).flatten()
    else:
        rh = np.zeros(21 * 3, dtype=np.float32)

    return np.concatenate([pose, lh, rh])


def centrar_secuencia(secuencia, n_frames=NUM_FRAMES):
    arr = np.asarray(secuencia, dtype=np.float32)
    if arr.ndim == 1:
        arr = arr.reshape(-1, DIMENSION)

    con_informacion = (arr != 0).sum(axis=1) > arr.shape[1] * 0.5
    arr = arr[con_informacion]
    total = len(arr)

    if total >= n_frames:
        inicio = (total - n_frames) // 2
        return arr[inicio:inicio + n_frames]

    relleno = np.zeros((n_frames - total, arr.shape[1]), dtype=arr.dtype)
    antes = (n_frames - total) // 2
    return np.concatenate([relleno[:antes], arr, relleno[antes:]])


def cargar_sample_npy(origen=None):
    raiz = Path(origen) if origen else CARPETA_SAMPLE_NPY
    if not raiz.exists():
        raise FileNotFoundError(f"No existe la carpeta: {raiz}")

    clases = sorted(d.name for d in raiz.iterdir() if d.is_dir())
    X, y = [], []
    for indice, clase in enumerate(clases):
        carpeta_clase = raiz / clase
        for ejemplar in sorted(carpeta_clase.iterdir(), key=_clave_directorio):
            frames = sorted((carpeta_clase / ejemplar.name).glob("*.npy"), key=_clave_archivo)
            if not frames:
                continue
            secuencia = np.stack([np.load(f).astype(np.float32) for f in frames])
            X.append(centrar_secuencia(secuencia))
            y.append(indice)

    if not X:
        raise ValueError(f"No se encontraron muestras en: {raiz}")
    return np.stack(X), np.array(y, dtype=np.int64), clases


def cargar_npz(origen=None):
    raiz = Path(origen) if origen else CARPETA_DATOS / "npz_samples"
    archivos = sorted(raiz.glob("*.npz"))
    if not archivos:
        raise FileNotFoundError(f"No se encontraron .npz en: {raiz}")

    X, y, clases = [], [], []
    for indice, archivo in enumerate(archivos):
        datos = np.load(archivo, allow_pickle=True)
        candidatos = [datos[n] for n in datos.files]
        secuencias = None
        for cand in candidatos:
            if cand.ndim == 3:
                secuencias = cand
                break
        if secuencias is None and candidatos:
            secuencias = candidatos[0]
        if secuencias is None:
            continue
        if secuencias.ndim == 2:
            secuencias = secuencias[None]
        X.extend(secuencias.astype(np.float32))
        y.extend([indice] * len(secuencias))
        clases.append(archivo.stem)

    return np.stack(X), np.array(y, dtype=np.int64), clases


def cargar_csv(origen):
    ruta = Path(origen)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    grupos = {}
    clases_orden = []
    with ruta.open("r", encoding="utf-8", errors="replace") as f:
        lector = csv.reader(f)
        next(lector, None)
        for fila in lector:
            if len(fila) < 230:
                continue
            clase = fila[1].strip()
            muestra = fila[0].strip()
            try:
                frame = int(fila[2])
            except ValueError:
                continue
            if clase not in grupos:
                grupos[clase] = {}
                clases_orden.append(clase)
            grupos[clase].setdefault(muestra, []).append((frame, fila))

    X, y = [], []
    for indice, clase in enumerate(clases_orden):
        for muestra, filas in grupos[clase].items():
            filas.sort(key=lambda t: t[0])
            matriz = np.array([fila[4:230] for _, fila in filas], dtype=np.float32)
            rh = matriz[:, 0:63]
            lh = matriz[:, 63:126]
            pose = matriz[:, 126:226]
            secuencia = np.concatenate([pose, lh, rh], axis=1)
            X.append(centrar_secuencia(secuencia))
            y.append(indice)

    return np.stack(X), np.array(y, dtype=np.int64), clases_orden


def dividir_datos(X, y, valido=0.15, test=0.15, semilla=42):
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=test, stratify=y, random_state=semilla
    )
    valido_rel = valido / (1 - test)
    X_tr, X_va, y_tr, y_va = train_test_split(
        X_tr, y_tr, test_size=valido_rel, stratify=y_tr, random_state=semilla
    )
    return X_tr, y_tr, X_va, y_va, X_te, y_te


def guardar_preparados(destino, X_tr, y_tr, X_va, y_va, X_te, y_te, clases):
    carpeta = Path(destino)
    carpeta.mkdir(parents=True, exist_ok=True)
    np.save(carpeta / "x_train.npy", X_tr)
    np.save(carpeta / "y_train.npy", y_tr)
    np.save(carpeta / "x_valid.npy", X_va)
    np.save(carpeta / "y_valid.npy", y_va)
    np.save(carpeta / "x_test.npy", X_te)
    np.save(carpeta / "y_test.npy", y_te)
    (carpeta / "clases.txt").write_text("\n".join(clases), encoding="utf-8")


def cargar_preparados(origen):
    carpeta = Path(origen)
    datos = {
        "x_train": np.load(carpeta / "x_train.npy"),
        "y_train": np.load(carpeta / "y_train.npy"),
        "x_valid": np.load(carpeta / "x_valid.npy"),
        "y_valid": np.load(carpeta / "y_valid.npy"),
        "x_test": np.load(carpeta / "x_test.npy"),
        "y_test": np.load(carpeta / "y_test.npy"),
    }
    clases = (carpeta / "clases.txt").read_text(encoding="utf-8").splitlines()
    return datos, clases


def asegurar_paquetes_requeridos():
    requeridos = {
        "numpy": np,
        "requests": None,
        "scipy": None,
        "sklearn": None,
        "torch": None,
    }
    faltantes = []
    for nombre in requeridos:
        try:
            __import__(nombre)
        except ImportError:
            faltantes.append(nombre)
    if faltantes:
        print("Instala los paquetes faltantes:")
        print("pip install " + " ".join(faltantes))
        return False
    return True