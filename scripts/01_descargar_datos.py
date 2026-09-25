import argparse
import io
import zipfile
from pathlib import Path

import requests

from msl150_datos import (
    CARPETA_DATOS,
    CARPETA_SAMPLE_NPY,
    URL_REPO_ZIP,
    URL_ZENODO,
    NUM_FRAMES,
)

TAMANO_CHUNK = 1024 * 1024


def descargar_github(destino):
    if destino.exists() and any(destino.iterdir()):
        print(f"[SKIP] Ya existe contenido en: {destino}")
        return

    print("Descargando ZIP del repositorio MSL-150-Dataset (subset demo)...")
    respuesta = requests.get(URL_REPO_ZIP, stream=True, timeout=120)
    respuesta.raise_for_status()

    marcador = "/data/sample_npy/"
    clases = set()
    with zipfile.ZipFile(io.BytesIO(respuesta.content)) as zipf:
        for nombre in zipf.namelist():
            pos = nombre.find(marcador)
            if pos == -1 or nombre.endswith("/"):
                continue
            relativo = nombre[pos + len(marcador):]
            with zipf.open(nombre) as fuente:
                datos = fuente.read()
            if not datos:
                continue
            salida = destino / relativo
            salida.parent.mkdir(parents=True, exist_ok=True)
            salida.write_bytes(datos)
            partes = Path(relativo).parts
            if len(partes) >= 3:
                clases.add(partes[0])

    print(f"[OK] {len(clases)} clases demo descargadas en: {destino}")


def descargar_zenodo(salida):
    salida.mkdir(parents=True, exist_ok=True)
    print("Consultando archivos del registro Zenodo...")
    respuesta = requests.get(URL_ZENODO, timeout=120)
    respuesta.raise_for_status()
    archivos = respuesta.json().get("files", [])

    if not archivos:
        raise RuntimeError("El registro Zenodo no expone archivos descargables.")

    for archivo in archivos:
        nombre = archivo["key"]
        enlace = archivo["links"]["download"]
        destino = salida / nombre
        if destino.exists():
            print(f"[SKIP] {nombre} ya existe")
            continue
        total = archivo.get("size", 0)
        print(f"Descargando {nombre} ({total / 1e9:.2f} GB)...")
        with requests.get(enlace, stream=True, timeout=120) as r:
            r.raise_for_status()
            with destino.open("wb") as f:
                for chunk in r.iter_content(chunk_size=TAMANO_CHUNK):
                    f.write(chunk)
        print(f"[OK] {nombre} -> {destino}")

    print(
        "El dataset completo requiere organizar los .npz/CSV antes de usar "
        "02_preparar_datos.py --origen npz|csv"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Descarga el dataset MSL-150 (subset demo de GitHub o completo de Zenodo)."
    )
    parser.add_argument(
        "--fuente",
        choices=["github", "zenodo"],
        default="github",
        help="github: subset demo (pequeno, por defecto). zenodo: dataset completo 17.8 GB.",
    )
    parser.add_argument(
        "--destino",
        default=str(CARPETA_SAMPLE_NPY),
        help="Carpeta raiz de salida de los datos.",
    )
    args = parser.parse_args()

    if args.fuente == "github":
        descargar_github(Path(args.destino))
    else:
        descargar_zenodo(CARPETA_DATOS / "zenodo")

    print(f"Formato por clase: {NUM_FRAMES} frames de {226} keypoints.")


if __name__ == "__main__":
    main()