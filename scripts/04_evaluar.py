import argparse
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score)
from sklearn.model_selection import train_test_split

from msl150_datos import CARPETA_MODELOS, CARPETA_PREPARADOS, cargar_preparados
from msl150_modelo import cargar_modelo


def main():
    parser = argparse.ArgumentParser(
        description="Evalua el modelo LSTM sobre el conjunto de prueba."
    )
    parser.add_argument("--datos", default=str(CARPETA_PREPARADOS))
    parser.add_argument("--modelo", default=str(CARPETA_MODELOS / "lstm_msl150.pt"))
    parser.add_argument("--grafica", default=str(CARPETA_MODELOS / "matriz_confusion.png"))
    args = parser.parse_args()

    dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
    modelo, clases = cargar_modelo(args.modelo, dispositivo)
    datos, _ = cargar_preparados(args.datos)

    X_te = torch.from_numpy(datos["x_test"])
    y_te = datos["y_test"]

    modelo.eval()
    predicciones = []
    with torch.inference_mode():
        for i in range(0, len(X_te), 256):
            lote = X_te[i:i + 256].to(dispositivo)
            predicciones.append(modelo(lote).argmax(dim=1).cpu().numpy())
    y_pred = np.concatenate(predicciones)

    print("Exactitud:", round(accuracy_score(y_te, y_pred), 4))
    print(
        "F1 macro:",
        round(f1_score(y_te, y_pred, average="macro", zero_division=0), 4),
    )
    print(
        "F1 micro:",
        round(f1_score(y_te, y_pred, average="micro", zero_division=0), 4),
    )
    print(classification_report(y_te, y_pred, target_names=clases, zero_division=0))

    matriz = confusion_matrix(y_te, y_pred)
    salida = Path(args.grafica)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(matriz, cmap="Blues")
        ax.set_xticks(range(len(clases)), clases, rotation=90)
        ax.set_yticks(range(len(clases)), clases)
        ax.set_xlabel("Prediccion")
        ax.set_ylabel("Real")
        fig.colorbar(im, ax=ax)
        fig.tight_layout()
        salida.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(salida, dpi=150)
        print(f"Matriz de confusion guardada en: {salida}")
    except ImportError:
        print("matplotlib no disponible; no se genero la grafica.")


if __name__ == "__main__":
    main()