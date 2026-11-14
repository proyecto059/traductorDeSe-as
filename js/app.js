/* SeñasAI · interfaz. detectarSena() y mostrarResultado() son los puntos donde se conectará
   el modelo de IA; mientras tanto no se muestra ningún resultado. */
const $ = id => document.getElementById(id);

/* Pestañas: van primero para que ningún otro código pueda impedir su registro */
const tabs = [...document.querySelectorAll('[role="tab"]')];
const HASH = { "tab-senas": "senas-a-texto", "tab-texto": "texto-a-senas" };
function activarPestana(tab, enfocar) {
  tabs.forEach(t => {
    const activa = t === tab;
    t.setAttribute("aria-selected", activa);
    t.tabIndex = activa ? 0 : -1;
    $(t.getAttribute("aria-controls")).hidden = !activa;
  });
  history.replaceState(null, "", "#" + HASH[tab.id]);
  if (enfocar) tab.focus();
}
function pestanaDesdeHash() {
  const id = Object.keys(HASH).find(k => HASH[k] === location.hash.slice(1));
  if (id) activarPestana($(id));
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
window.addEventListener("hashchange", pestanaDesdeHash);
pestanaDesdeHash();

const video = $("video"), toggleCamera = $("toggleCamera"), toggleLabel = $("toggleLabel"), toggleIcon = $("toggleIcon"),
  cameraPlaceholder = $("cameraPlaceholder"),
  cameraMsg = $("cameraMsg"), detectedSign = $("detectedSign"), translationText = $("translationText");
let stream = null, detectionInterval = null, ultimaTraduccion = "";
const SIGN_EMPTY = '<svg class="ic"><use href="#i-hand"/></svg><span>Esperando una seña…</span>';
const TXT_EMPTY = '<span class="ph">Esperando una seña para traducir.</span>';

/* Cámara: un solo botón que alterna entre activar y detener */
function estadoCamara(activa) {
  video.style.display = activa ? "block" : "none";
  cameraPlaceholder.style.display = activa ? "none" : "flex";
  toggleCamera.classList.toggle("is-on", activa);
  toggleCamera.setAttribute("aria-pressed", activa);
  toggleLabel.textContent = activa ? "Detener cámara" : "Activar cámara";
  toggleIcon.setAttribute("href", activa ? "#i-stop" : "#i-play");
}

async function iniciarCamara() {
  cameraMsg.textContent = "";
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    cameraMsg.textContent = "Este navegador no permite usar la cámara. Abre la página desde http://localhost o con HTTPS.";
    return;
  }
  toggleCamera.disabled = true;
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" }, audio: false });
    video.srcObject = stream;
    estadoCamara(true);
    iniciarDeteccion();
  } catch (error) {
    console.error("Error al acceder a la cámara:", error);
    cameraMsg.textContent = "No se pudo acceder a la cámara. Permite el acceso en tu navegador y vuelve a intentarlo.";
  } finally {
    toggleCamera.disabled = false;
  }
}

function detenerCamara() {
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
  video.srcObject = null;
  estadoCamara(false);
  detenerDeteccion();
}

function iniciarDeteccion() { detectionInterval = setInterval(detectarSena, 500); }
function detenerDeteccion() { clearInterval(detectionInterval); detectionInterval = null; }

function detectarSena() {
  /* AQUÍ SE INTEGRARÁ EL MODELO:
     const r = await modelo.predict(video);
     mostrarResultado(r.sena, r.traduccion); */
}

function mostrarResultado(sena, traduccion) {
  ultimaTraduccion = traduccion;
  detectedSign.className = "sign hit";
  detectedSign.innerHTML = '<svg class="ic"><use href="#i-hand"/></svg><span></span>';
  detectedSign.lastChild.textContent = sena;
  translationText.textContent = traduccion;
}

function limpiarTraduccion() {
  ultimaTraduccion = "";
  detectedSign.className = "sign"; detectedSign.innerHTML = SIGN_EMPTY;
  translationText.innerHTML = TXT_EMPTY;
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

toggleCamera.addEventListener("click", () => (stream ? detenerCamara() : iniciarCamara()));
$("clearButton").addEventListener("click", limpiarTraduccion);
$("speakButton").addEventListener("click", escucharTraduccion);
window.addEventListener("beforeunload", detenerCamara);

/* Texto a señas */
const userText = $("userText"), characterCount = $("characterCount"), textInputMessage = $("textInputMessage"), signStage = $("signStage");
const STAGE_VACIO = '<svg class="ic ic-xl"><use href="#i-hand"/></svg><p>Las señas aparecerán aquí.</p>';

userText.addEventListener("input", () => {
  characterCount.textContent = userText.value.length + " / 1000 caracteres";
  textInputMessage.textContent = "";
});

$("showUserText").addEventListener("click", () => {
  const texto = userText.value.trim();
  if (!texto) { textInputMessage.textContent = "Escribe una palabra o una oración antes de continuar."; userText.focus(); return; }
  /* Muestra las palabras en orden; aquí se insertará la animación de cada seña cuando exista el banco de poses. */
  signStage.textContent = ""; signStage.classList.add("has");
  texto.split(/\s+/).forEach(p => {
    const ficha = document.createElement("span"); ficha.className = "tok";
    ficha.innerHTML = '<svg class="ic"><use href="#i-hand"/></svg>';
    ficha.append(p); signStage.appendChild(ficha);
  });
  const nota = document.createElement("p"); nota.className = "stage-note";
  nota.textContent = "Las animaciones de cada seña se mostrarán aquí cuando estén integradas.";
  signStage.appendChild(nota);
});

$("clearUserText").addEventListener("click", () => {
  userText.value = "";
  characterCount.textContent = "0 / 1000 caracteres"; textInputMessage.textContent = "";
  signStage.classList.remove("has"); signStage.innerHTML = STAGE_VACIO;
  userText.focus();
});
