import argparse
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

import numpy as np

from msl150_datos import CARPETA_MODELOS, CARPETA_PREPARADOS, cargar_preparados
from msl150_modelo import ModeloLSTM, guardar_modelo


def evaluar(modelo, cargador, dispositivo):
    modelo.eval()
    totales, correctos = 0, 0
    perdida = 0.0
    criterio = nn.CrossEntropyLoss()
    with torch.inference_mode():
        for x, y in cargador:
            x, y = x.to(dispositivo), y.to(dispositivo)
            logits = modelo(x)
            perdida += criterio(logits, y).item() * len(x)
            correctos += (logits.argmax(dim=1) == y).sum().item()
            totales += len(x)
    modelo.train()
    return perdida / totales, correctos / totales


def main():
    parser = argparse.ArgumentParser(
        description="Entrena el LSTM de MSL-150 y guarda el mejor checkpoint."
    )
    parser.add_argument("--datos", default=str(CARPETA_PREPARADOS))
    parser.add_argument("--unidades", type=int, nargs="+", default=[64],
                        help="Unidades ocultas por capa LSTM, p.ej. --unidades 64 128")
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--epocas", type=int, default=25)
    parser.add_argument("--lote", type=int, default=32)
    parser.add_argument("--lr", type=float, default=0.002)
    parser.add_argument("--paciencia", type=int, default=5)
    parser.add_argument("--salida", default=str(CARPETA_MODELOS / "lstm_msl150.pt"))
    args = parser.parse_args()

    datos, clases = cargar_preparados(args.datos)
    num_clases = len(clases)

    dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Dispositivo: {dispositivo}")

    train_ds = TensorDataset(
        torch.from_numpy(datos["x_train"]),
        torch.from_numpy(datos["y_train"]),
    )
    valid_ds = TensorDataset(
        torch.from_numpy(datos["x_valid"]),
        torch.from_numpy(datos["y_valid"]),
    )
    train_dl = DataLoader(train_ds, batch_size=args.lote, shuffle=True)
    valid_dl = DataLoader(valid_ds, batch_size=args.lote, shuffle=False)

    modelo = ModeloLSTM(
        dim_entrada=226,
        unidades=args.unidades,
        num_clases=num_clases,
        dropout=args.dropout,
    ).to(dispositivo)

    criterio = nn.CrossEntropyLoss()
    optimizador = torch.optim.Adam(modelo.parameters(), lr=args.lr)

    mejor_precision = 0.0
    mejor_epoch = 0
    epocas_sin_mejora = 0
    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)

    print(f"Parametros: {sum(p.numel() for p in modelo.parameters()):,}")

    for epoca in range(1, args.epocas + 1):
        modelo.train()
        perdida_total = 0.0
        correctos, totales = 0, 0
        for x, y in train_dl:
            x, y = x.to(dispositivo), y.to(dispositivo)
            optimizador.zero_grad()
            logits = modelo(x)
            perdida = criterio(logits, y)
            perdida.backward()
            optimizador.step()
            perdida_total += perdida.item() * len(x)
            correctos += (logits.argmax(dim=1) == y).sum().item()
            totales += len(x)

        va_perdida, va_precision = evaluar(modelo, valid_dl, dispositivo)
        acc_train = correctos / totales
        print(
            f"Epoca {epoca:02d} | "
            f"loss {perdida_total / totales:.4f} | "
            f"acc {acc_train:.4f} | "
            f"val_loss {va_perdida:.4f} | "
            f"val_acc {va_precision:.4f}"
        )

        if va_precision > mejor_precision:
            mejor_precision = va_precision
            mejor_epoch = epoca
            epocas_sin_mejora = 0
            guardar_modelo(salida, modelo, clases)
            print(f"  * checkpoint guardado (val_acc {va_precision:.4f})")
        else:
            epocas_sin_mejora += 1
            if epocas_sin_mejora >= args.paciencia:
                print(f"Early stopping en epoca {epoca}. Mejor: epoca {mejor_epoch} ({mejor_precision:.4f})")
                break

    print(f"Mejor val_acc: {mejor_precision:.4f} -> {salida}")


if __name__ == "__main__":
    main()