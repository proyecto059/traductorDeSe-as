import types
from pathlib import Path

import numpy as np

import msl150_datos as mod


class TestFormatoTamano:
    def test_bytes(self):
        assert mod.formato_tamano(512) == "512 B"

    def test_megabytes(self):
        assert mod.formato_tamano(5 * 1024 * 1024) == "5.0 MB"


class TestCentrarSecuencia:
    def test_rellena_secuencias_cortas(self):
        secuencia = np.ones((10, 226), dtype=np.float32)
        resultado = mod.centrar_secuencia(secuencia)
        assert resultado.shape == (mod.NUM_FRAMES, mod.DIMENSION)
        assert resultado.sum() == 10 * 226

    def test_recorta_secuencias_largas(self):
        secuencia = np.ones((60, 226), dtype=np.float32)
        resultado = mod.centrar_secuencia(secuencia)
        assert resultado.shape == (mod.NUM_FRAMES, mod.DIMENSION)
        assert resultado.sum() == mod.NUM_FRAMES * 226

    def test_deshecha_frames_vacios(self):
        secuencia = np.concatenate(
            [np.ones((10, 226)), np.zeros((20, 226)), np.ones((10, 226))]
        )
        resultado = mod.centrar_secuencia(secuencia)
        assert resultado.shape == (mod.NUM_FRAMES, mod.DIMENSION)
        assert resultado.sum() == 20 * 226


class TestExtraerFilaHolistic:
    def test_devuelve_ceros_sin_deteccion(self):
        resultado = types.SimpleNamespace(
            pose_landmarks=None,
            left_hand_landmarks=None,
            right_hand_landmarks=None,
        )
        fila = mod.extraer_fila_holistic(resultado)
        assert fila.shape == (mod.DIMENSION,)
        assert not fila.any()

    def test_combina_pose_y_ambas_manos(self):
        class Punto:
            def __init__(self, x, y, z, visibility=1.0):
                self.x = x
                self.y = y
                self.z = z
                self.visibility = visibility

        pose = [Punto(i + 1, i, i) for i in range(33)]
        mano = [Punto(i, i, i) for i in range(21)]
        resultado = types.SimpleNamespace(
            pose_landmarks=pose,
            left_hand_landmarks=mano,
            right_hand_landmarks=mano,
        )
        fila = mod.extraer_fila_holistic(resultado)
        assert fila.shape == (mod.DIMENSION,)
        assert fila[0] > 0
        assert fila[100:226].any()


class TestDividirDatos:
    def test_split_balanceado_con_todas_las_clases(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(120, mod.NUM_FRAMES, mod.DIMENSION)).astype(np.float32)
        y = np.repeat(np.arange(3), 40)

        X_tr, y_tr, X_va, y_va, X_te, y_te = mod.dividir_datos(X, y)

        assert len(X_tr) + len(X_va) + len(X_te) == 120
        assert set(np.unique(y_tr)) == {0, 1, 2}
        assert set(np.unique(y_va)) == {0, 1, 2}
        assert set(np.unique(y_te)) == {0, 1, 2}


class TestCargarSampleNpy:
    def test_carga_estructura_de_carpetas(self, tmp_path):
        rng = np.random.default_rng(1)
        for clase in ("hola", "gracias"):
            for ejemplar in ("1", "2"):
                carpeta = Path(tmp_path) / clase / ejemplar
                carpeta.mkdir(parents=True, exist_ok=True)
                for frame in range(5):
                    np.save(carpeta / f"{frame}.npy", rng.normal(size=mod.DIMENSION))

        X, y, clases = mod.cargar_sample_npy(tmp_path)

        assert clases == ["gracias", "hola"]
        assert X.shape == (4, mod.NUM_FRAMES, mod.DIMENSION)
        assert set(np.unique(y)) == {0, 1}


class TestGuardarCargarPreparados:
    def test_roundtrip(self, tmp_path):
        X = np.zeros((10, mod.NUM_FRAMES, mod.DIMENSION), dtype=np.float32)
        y = np.zeros(10, dtype=np.int64)
        clases = ["hola", "mundo"]

        mod.guardar_preparados(tmp_path, X, y, X, y, X, y, clases)
        datos, clases_leidas = mod.cargar_preparados(tmp_path)

        assert datos["x_train"].shape == (10, mod.NUM_FRAMES, mod.DIMENSION)
        assert datos["y_test"].shape == (10,)
        assert clases_leidas == clases