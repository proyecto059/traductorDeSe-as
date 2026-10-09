
/* =========================================================
   SEÑAS AI
   JAVASCRIPT
========================================================= */


/* =========================================================
   ELEMENTOS
========================================================= */

const video =
    document.getElementById("video");

const canvas =
    document.getElementById("canvas");

const startCamera =
    document.getElementById("startCamera");

const stopCamera =
    document.getElementById("stopCamera");

const cameraPlaceholder =
    document.getElementById("cameraPlaceholder");

const cameraStatus =
    document.getElementById("cameraStatus");

const detectingIndicator =
    document.getElementById("detectingIndicator");

const detectedSign =
    document.getElementById("detectedSign");

const translationText =
    document.getElementById("translationText");

const confidence =
    document.getElementById("confidence");

const speakButton =
    document.getElementById("speakButton");

const clearButton =
    document.getElementById("clearButton");

const clearHistoryButton =
    document.getElementById("clearHistory");

const historyContainer =
    document.getElementById("historyContainer");

const emptyHistory =
    document.getElementById("emptyHistory");

const modelStatus =
    document.getElementById("modelStatus");

const aiStatusTitle =
    document.getElementById("aiStatusTitle");

const aiStatusText =
    document.getElementById("aiStatusText");


/* =========================================================
   VARIABLES
========================================================= */

let stream = null;

let detectionInterval = null;

let ultimaSena = "";

let ultimaTraduccion = "";

let historial = [];


/* =========================================================
   INICIAR CÁMARA
========================================================= */

async function iniciarCamara() {

    try {

        stream =
            await navigator.mediaDevices.getUserMedia({

                video: {

                    width: {
                        ideal: 1280
                    },

                    height: {
                        ideal: 720
                    },

                    facingMode: "user"

                },

                audio: false

            });


        video.srcObject = stream;

        video.style.display = "block";

        cameraPlaceholder.style.display = "none";


        startCamera.disabled = true;

        stopCamera.disabled = false;


        cameraStatus.classList.add("active");

        cameraStatus.innerHTML =
            "<span></span>Cámara activa";


        detectingIndicator.style.display =
            "flex";


        modelStatus.textContent =
            "Detectando";


        aiStatusTitle.textContent =
            "Detectando señas";


        aiStatusText.textContent =
            "Realiza una seña frente a la cámara.";


        iniciarDeteccion();


    }

    catch (error) {

        console.error(
            "Error al acceder a la cámara:",
            error
        );


        alert(
            "No se pudo acceder a la cámara.\n\n" +
            "Verifica que hayas permitido el acceso " +
            "a la cámara en tu navegador."
        );

    }

}


/* =========================================================
   DETENER CÁMARA
========================================================= */

function detenerCamara() {

    if (stream) {

        stream
            .getTracks()
            .forEach(track => track.stop());

        stream = null;

    }


    video.srcObject = null;

    video.style.display = "none";

    cameraPlaceholder.style.display =
        "flex";


    startCamera.disabled = false;

    stopCamera.disabled = true;


    cameraStatus.classList.remove(
        "active"
    );


    cameraStatus.innerHTML =
        "<span></span>Cámara apagada";


    detectingIndicator.style.display =
        "none";


    modelStatus.textContent =
        "Preparado";


    aiStatusTitle.textContent =
        "Listo para detectar";


    aiStatusText.textContent =
        "Activa la cámara y realiza una seña frente a ella.";


    detenerDeteccion();

}


/* =========================================================
   INICIAR DETECCIÓN
========================================================= */

function iniciarDeteccion() {

    /*
     * ESTA PARTE SE UTILIZARÁ DESPUÉS
     * PARA CONECTAR EL MODELO DE IA.
     */

    detectionInterval =
        setInterval(() => {

            detectarSena();

        }, 500);

}


/* =========================================================
   DETENER DETECCIÓN
========================================================= */

function detenerDeteccion() {

    if (detectionInterval) {

        clearInterval(
            detectionInterval
        );

        detectionInterval = null;

    }

}


/* =========================================================
   DETECTAR SEÑA
========================================================= */

function detectarSena() {

    /*
     * =====================================================
     * AQUÍ SE INTEGRARÁ EL MODELO
     * =====================================================
     *
     * Ejemplo:
     *
     * const resultado =
     *      await modelo.predict(video);
     *
     *
     * mostrarResultado(
     *      resultado.sena,
     *      resultado.traduccion,
     *      resultado.confianza
     * );
     *
     * =====================================================
     */


    // Actualmente no hacemos predicciones.


}


/* =========================================================
   MOSTRAR RESULTADO
========================================================= */

function mostrarResultado(
    sena,
    traduccion,
    porcentaje
) {

    ultimaSena = sena;

    ultimaTraduccion = traduccion;


    /* SEÑA DETECTADA */

    detectedSign.innerHTML = `

        <span class="empty-icon">
            ✋
        </span>

        <p>
            ${sena}
        </p>

    `;


    /* TRADUCCIÓN */

    translationText.innerHTML = `
        ${traduccion}
    `;


    /* CONFIANZA */

    confidence.textContent =
        Math.round(porcentaje) + "%";


    /* ESTADO */

    aiStatusTitle.textContent =
        "Seña detectada";


    aiStatusText.textContent =
        "El modelo ha reconocido una seña.";


    /* HISTORIAL */

    agregarHistorial(
        traduccion,
        porcentaje
    );

}


/* =========================================================
   AGREGAR HISTORIAL
========================================================= */

function agregarHistorial(
    traduccion,
    porcentaje
) {

    const ultimo =
        historial.length > 0
            ? historial[0]
            : null;


    /*
     * Evitar repetir la misma palabra
     */

    if (
        ultimo &&
        ultimo.texto === traduccion
    ) {

        return;

    }


    const ahora =
        new Date();


    const hora =
        ahora.toLocaleTimeString(
            "es-MX",
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        );


    const nuevoElemento = {

        texto: traduccion,

        confianza:
            Math.round(porcentaje),

        hora: hora

    };


    historial.unshift(
        nuevoElemento
    );


    /*
     * Máximo 20 elementos
     */

    if (historial.length > 20) {

        historial.pop();

    }


    mostrarHistorial();

}


/* =========================================================
   MOSTRAR HISTORIAL
========================================================= */

function mostrarHistorial() {

    historyContainer.innerHTML = "";


    if (historial.length === 0) {

        historyContainer.appendChild(
            emptyHistory
        );

        return;

    }


    historial.forEach(item => {


        const elemento =
            document.createElement("div");


        elemento.className =
            "history-item";


        elemento.innerHTML = `

            <div class="history-left">

                <div class="history-icon">
                    ✋
                </div>

                <div>

                    <div class="history-word">
                        ${item.texto}
                    </div>

                    <div class="history-time">
                        ${item.hora}
                    </div>

                </div>

            </div>


            <div class="history-confidence">

                ${item.confianza}%

            </div>

        `;


        historyContainer.appendChild(
            elemento
        );

    });

}


/* =========================================================
   LIMPIAR TRADUCCIÓN
========================================================= */

function limpiarTraduccion() {

    ultimaSena = "";

    ultimaTraduccion = "";


    detectedSign.innerHTML = `

        <span class="empty-icon">
            ✋
        </span>

        <p>
            Esperando una seña...
        </p>

    `;


    translationText.innerHTML = `

        <span>
            La traducción aparecerá aquí
        </span>

    `;


    confidence.textContent =
        "--%";


    aiStatusTitle.textContent =
        "Listo para detectar";


    aiStatusText.textContent =
        "Activa la cámara y realiza una seña frente a ella.";

}


/* =========================================================
   ESCUCHAR TRADUCCIÓN
========================================================= */

function escucharTraduccion() {

    if (!ultimaTraduccion) {

        alert(
            "Todavía no hay una traducción."
        );

        return;

    }


    if (!("speechSynthesis" in window)) {

        alert(
            "Tu navegador no soporta la función de voz."
        );

        return;

    }


    window.speechSynthesis.cancel();


    const mensaje =
        new SpeechSynthesisUtterance(
            ultimaTraduccion
        );


    mensaje.lang =
        "es-MX";


    mensaje.rate =
        0.9;


    mensaje.pitch =
        1;


    window.speechSynthesis.speak(
        mensaje
    );

}


/* =========================================================
   LIMPIAR HISTORIAL
========================================================= */

function limpiarHistorial() {

    historial = [];

    mostrarHistorial();

}


/* =========================================================
   EVENTOS
========================================================= */

startCamera.addEventListener(
    "click",
    iniciarCamara
);


stopCamera.addEventListener(
    "click",
    detenerCamara
);


clearButton.addEventListener(
    "click",
    limpiarTraduccion
);


speakButton.addEventListener(
    "click",
    escucharTraduccion
);


clearHistoryButton.addEventListener(
    "click",
    limpiarHistorial
);


/* =========================================================
   CERRAR PÁGINA
========================================================= */

window.addEventListener(
    "beforeunload",
    () => {

        detenerCamara();

    }
);


/* =========================================================
   PRUEBA DEL SISTEMA
=========================================================

   Para comprobar que la interfaz funciona antes
   de integrar la IA, abre la consola del navegador
   (F12) y escribe:

       mostrarResultado("Hola", "Hola", 96);

   También puedes probar:

       mostrarResultado("Gracias", "Gracias", 92);

   Cuando integremos el modelo, estas llamadas
   vendrán automáticamente de la predicción.
========================================================= */

