import argparse
from pathlib import Path

from msl150_datos import (
    CARPETA_PREPARADOS,
    cargar_csv,
    cargar_npz,
    cargar_sample_npy,
    dividir_datos,
    guardar_preparados,
    NUM_FRAMES,
)


def main():
    parser = argparse.ArgumentParser(
        description="Convierte datos MSL-150 al tensor (N, 30, 226) y hace el split."
    )
    parser.add_argument(
        "--origen",
        choices=["sample_npy", "npz", "csv"],
        default="sample_npy",
        help="Formato de entrada de los datos MSL-150.",
    )
    parser.add_argument("--ruta", default=None, help="Ruta de datos de entrada.")
    parser.add_argument("--salida", default=str(CARPETA_PREPARADOS))
    parser.add_argument("--valid", type=float, default=0.15)
    parser.add_argument("--test", type=float, default=0.15)
    args = parser.parse_args()

    if args.origen == "sample_npy":
        X, y, clases = cargar_sample_npy(args.ruta)
    elif args.origen == "npz":
        X, y, clases = cargar_npz(args.ruta)
    else:
        X, y, clases = cargar_csv(args.ruta)

    X_tr, y_tr, X_va, y_va, X_te, y_te = dividir_datos(
        X, y, valido=args.valid, test=args.test
    )

    guardar_preparados(args.salida, X_tr, y_tr, X_va, y_va, X_te, y_te, clases)

    print(f"Clases: {len(clases)}")
    print(f"Forma X: {X.shape}  (N, {NUM_FRAMES}, 226)")
    print(f"Train: {len(X_tr)} | Valid: {len(X_va)} | Test: {len(X_te)}")
    print(f"Salida: {args.salida}")


if __name__ == "__main__":
    main()