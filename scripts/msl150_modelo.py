import torch
from torch import nn


class ModeloLSTM(nn.Module):
    def __init__(
        self,
        dim_entrada=226,
        unidades=(64,),
        num_clases=150,
        dropout=0.3,
        semilla=42,
    ):
        super().__init__()
        self.unidades = list(unidades)
        self.num_clases = num_clases
        torch.manual_seed(semilla)

        capas = []
        entrada = dim_entrada
        for i, h in enumerate(unidades):
            capas.append((entrada, h))
            entrada = h
        self.lstms = nn.ModuleList([nn.LSTM(inp, out, batch_first=True) for inp, out in capas])

        self.dropout = nn.Dropout(dropout)
        self.cabeza = nn.Sequential(
            nn.Linear(entrada, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, num_clases),
        )

    def forward(self, x):
        for i, capa in enumerate(self.lstms):
            x, _ = capa(x)
            if i < len(self.lstms) - 1:
                x = self.dropout(x)
        return self.cabeza(self.dropout(x[:, -1, :]))


def guardar_modelo(ruta, modelo, clases):
    ruta = str(ruta)
    torch.save(
        {
            "state_dict": modelo.state_dict(),
            "unidades": modelo.unidades,
            "num_clases": modelo.num_clases,
            "clases": list(clases),
        },
        ruta,
    )


def cargar_modelo(ruta, dispositivo="cpu"):
    datos = torch.load(ruta, map_location=dispositivo, weights_only=False)
    modelo = ModeloLSTM(
        dim_entrada=226,
        unidades=datos["unidades"],
        num_clases=datos["num_clases"],
        dropout=0.3,
        semilla=42,
    )
    modelo.load_state_dict(datos["state_dict"])
    modelo.to(dispositivo)
    modelo.eval()
    return modelo, datos["clases"]


@torch.inference_mode()
def predecir_probs(modelo, secuencia, dispositivo="cpu"):
    secuencia = torch.as_tensor(
        secuencia, dtype=torch.float32, device=dispositivo
    ).unsqueeze(0)
    logits = modelo(secuencia)
    probs = torch.softmax(logits, dim=1)[0]
    return probs.cpu().numpy()