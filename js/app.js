/* SeñasAI · interfaz. Las funciones detectarSena() y mostrarResultado() son los puntos
   donde se conectará el modelo de IA; mientras tanto no se muestra ningún resultado. */
const $ = id => document.getElementById(id);
const video = $("video"), startCamera = $("startCamera"), stopCamera = $("stopCamera"),
  cameraPlaceholder = $("cameraPlaceholder"), cameraStatus = $("cameraStatus"), cameraStatusText = $("cameraStatusText"),
  cameraMsg = $("cameraMsg"), detectingIndicator = $("detectingIndicator"), detectedSign = $("detectedSign"),
  translationText = $("translationText"), confidence = $("confidence"), aiStatusTitle = $("aiStatusTitle"),
  aiStatusText = $("aiStatusText"), historyContainer = $("historyContainer"), emptyHistory = $("emptyHistory");
let stream = null, detectionInterval = null, ultimaTraduccion = "", historial = [];
const SIGN_EMPTY = '<svg class="ic"><use href="#i-hand"/></svg><span>Esperando una seña…</span>';
const MSG_LISTO = "Listo para conectar el modelo.", TXT_LISTO = " Cuando exista, aquí verás cada seña con su traducción.";

/* Navegación móvil */
const navToggle = $("navToggle"), navMenu = $("navMenu");
navToggle.addEventListener("click", () => {
  const abierto = navMenu.classList.toggle("open");
  navToggle.setAttribute("aria-expanded", abierto);
});
navMenu.addEventListener("click", e => { if (e.target.tagName === "A") { navMenu.classList.remove("open"); navToggle.setAttribute("aria-expanded", "false"); } });

/* Cámara */
function estadoCamara(activa) {
  cameraStatus.classList.toggle("on", activa);
  cameraStatusText.textContent = activa ? "Cámara activa" : "Cámara apagada";
  video.style.display = activa ? "block" : "none";
  cameraPlaceholder.style.display = activa ? "none" : "flex";
  detectingIndicator.hidden = !activa;
  startCamera.disabled = activa; stopCamera.disabled = !activa;
}

async function iniciarCamara() {
  cameraMsg.textContent = "";
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    cameraMsg.textContent = "Este navegador no permite usar la cámara. Abre la página desde http://localhost o con HTTPS.";
    return;
  }
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" }, audio: false });
    video.srcObject = stream;
    estadoCamara(true);
    aiStatusTitle.textContent = "Cámara activa, modelo sin conectar.";
    aiStatusText.lastChild.textContent = " Por ahora no se reconocen señas.";
    iniciarDeteccion();
  } catch (error) {
    console.error("Error al acceder a la cámara:", error);
    cameraMsg.textContent = "No se pudo acceder a la cámara. Permite el acceso en tu navegador y vuelve a intentarlo.";
  }
}

function detenerCamara() {
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
  video.srcObject = null;
  estadoCamara(false);
  aiStatusTitle.textContent = MSG_LISTO;
  aiStatusText.lastChild.textContent = TXT_LISTO;
  detenerDeteccion();
}

function iniciarDeteccion() { detectionInterval = setInterval(detectarSena, 500); }
function detenerDeteccion() { clearInterval(detectionInterval); detectionInterval = null; }

function detectarSena() {
  /* AQUÍ SE INTEGRARÁ EL MODELO:
     const r = await modelo.predict(video);
     mostrarResultado(r.sena, r.traduccion, r.confianza); */
}

function mostrarResultado(sena, traduccion, porcentaje) {
  ultimaTraduccion = traduccion;
  detectedSign.className = "sign hit";
  detectedSign.innerHTML = '<svg class="ic"><use href="#i-hand"/></svg><span></span>';
  detectedSign.lastChild.textContent = sena;
  translationText.textContent = traduccion;
  confidence.textContent = Math.round(porcentaje) + "%";
  aiStatusTitle.textContent = "Seña reconocida.";
  agregarHistorial(traduccion, porcentaje);
}

/* Historial */
function agregarHistorial(texto, porcentaje) {
  if (historial[0] && historial[0].texto === texto) return;
  const hora = new Date().toLocaleTimeString("es-MX", { hour: "2-digit", minute: "2-digit" });
  historial.unshift({ texto, confianza: Math.round(porcentaje), hora });
  if (historial.length > 20) historial.pop();
  mostrarHistorial();
}

function mostrarHistorial() {
  historyContainer.textContent = "";
  if (!historial.length) { historyContainer.appendChild(emptyHistory); return; }
  historial.forEach(item => {
    const fila = document.createElement("div");
    fila.className = "history-item";
    const izq = document.createElement("div");
    const palabra = document.createElement("div"); palabra.className = "history-word"; palabra.textContent = item.texto;
    const hora = document.createElement("div"); hora.className = "history-time"; hora.textContent = item.hora;
    izq.append(palabra, hora);
    const conf = document.createElement("div"); conf.className = "history-confidence"; conf.textContent = item.confianza + "%";
    fila.append(izq, conf);
    historyContainer.appendChild(fila);
  });
}

function limpiarTraduccion() {
  ultimaTraduccion = "";
  detectedSign.className = "sign"; detectedSign.innerHTML = SIGN_EMPTY;
  translationText.innerHTML = '<span class="ph">Esperando una seña para traducir.</span>';
  confidence.textContent = "--%";
  aiStatusTitle.textContent = MSG_LISTO; aiStatusText.lastChild.textContent = TXT_LISTO;
}

function escucharTraduccion() {
  if (!ultimaTraduccion) { cameraMsg.textContent = "Todavía no hay una traducción para escuchar."; return; }
  if (!("speechSynthesis" in window)) { cameraMsg.textContent = "Tu navegador no soporta la función de voz."; return; }
  cameraMsg.textContent = "";
  speechSynthesis.cancel();
  const voz = new SpeechSynthesisUtterance(ultimaTraduccion);
  voz.lang = "es-MX"; voz.rate = 0.9;
  speechSynthesis.speak(voz);
}

function limpiarHistorial() { historial = []; mostrarHistorial(); }

startCamera.addEventListener("click", iniciarCamara);
stopCamera.addEventListener("click", detenerCamara);
$("clearButton").addEventListener("click", limpiarTraduccion);
$("speakButton").addEventListener("click", escucharTraduccion);
$("clearHistory").addEventListener("click", limpiarHistorial);
window.addEventListener("beforeunload", detenerCamara);

/* Texto a señas */
const userText = $("userText"), characterCount = $("characterCount"), textInputMessage = $("textInputMessage"),
  userTextResult = $("userTextResult"), userTextPreview = $("userTextPreview"), signStage = $("signStage");
const STAGE_VACIO = '<svg class="ic ic-xl"><use href="#i-hand"/></svg><p>Las señas aparecerán aquí cuando agregues un texto.</p>';

userText.addEventListener("input", () => {
  characterCount.textContent = userText.value.length + " / 1000 caracteres";
  textInputMessage.textContent = "";
});

$("showUserText").addEventListener("click", () => {
  const texto = userText.value.trim();
  if (!texto) { textInputMessage.textContent = "Escribe una palabra o una oración antes de continuar."; userText.focus(); return; }
  userTextPreview.textContent = texto;
  userTextResult.hidden = false;
  /* Muestra las palabras en orden; aquí se insertará la animación de cada seña cuando exista el banco de poses. */
  signStage.textContent = ""; signStage.classList.add("has");
  texto.split(/\s+/).forEach(p => {
    const ficha = document.createElement("span"); ficha.className = "tok";
    ficha.innerHTML = '<svg class="ic"><use href="#i-hand"/></svg>';
    ficha.append(p); signStage.appendChild(ficha);
  });
  const nota = document.createElement("p"); nota.className = "stage-note";
  nota.textContent = "Las animaciones de las señas se mostrarán aquí cuando el banco de señas esté integrado.";
  signStage.appendChild(nota);
});

$("clearUserText").addEventListener("click", () => {
  userText.value = ""; userTextPreview.textContent = ""; userTextResult.hidden = true;
  characterCount.textContent = "0 / 1000 caracteres"; textInputMessage.textContent = "";
  signStage.classList.remove("has"); signStage.innerHTML = STAGE_VACIO;
  userText.focus();
});

/* Pestañas del traductor */
const tabs = [...document.querySelectorAll('[role="tab"]')];
function activarPestana(tab, enfocar) {
  tabs.forEach(t => {
    const activa = t === tab;
    t.setAttribute("aria-selected", activa);
    t.tabIndex = activa ? 0 : -1;
    $(t.getAttribute("aria-controls")).hidden = !activa;
  });
  if (enfocar) tab.focus();
}
tabs.forEach((tab, i) => {
  tab.addEventListener("click", () => activarPestana(tab));
  tab.addEventListener("keydown", e => {
    const d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
    if (d) { e.preventDefault(); activarPestana(tabs[(i + d + tabs.length) % tabs.length], true); }
    else if (e.key === "Home") { e.preventDefault(); activarPestana(tabs[0], true); }
    else if (e.key === "End") { e.preventDefault(); activarPestana(tabs[tabs.length - 1], true); }
  });
});
