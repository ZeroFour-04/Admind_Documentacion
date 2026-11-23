// Presentación final de la sustentación técnica de AdMind (lunes 23-nov-2026).
// Parte del borrador del 16-nov; datos verificados el 18-nov y actualizados el 22-nov
// (CORS y Swagger en main, CI endurecido, segundo escaneo de SonarCloud, pruebas del CI del 22-nov).
// Uso: NODE_PATH=<carpeta con pptxgenjs e image-size> node build_deck.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const sizeOf = (() => { const m = require("image-size"); return m.imageSize || m.default || m; })();

const RAIZ = "C:/Users/Alejandro/Documents/A D M I N D";
const ENT = RAIZ + "/Entregables_Sustentacion";
const OUT = ENT + "/AdMind_Sustentacion_Final.pptx";
const IMG = path.join(__dirname, "img");
const R = {
  logo: RAIZ + "/Frontend/Admind_Front-End/static/img/logo-marca.png",
  mer: RAIZ + "/MER_AdMind.png",
  qr: ENT + "/capturas/qr_admind.png",
  coberturaTop: IMG + "/cobertura_recorte.png", // parte superior de evidencias/cobertura_back.png
  actions: ENT + "/evidencias/ci_actions_back_2026-11-18.png",
  ingreso: IMG + "/nube_ingreso.png",
  e404: IMG + "/nube_404.png",
  panel: IMG + "/panel_admin.png",
  mAdmin: IMG + "/menu_admin.png",
  mVig: IMG + "/menu_vigilancia.png",
  mRes: IMG + "/menu_residente.png",
  swagger: IMG + "/swagger_nube.jpg", // /api/docs/ del VPS, por túnel SSH, 22-nov
};

// Paleta de AdMind (estilo_entregables.md)
const V600 = "0E6B5A", V700 = "0B5546", V900 = "06302A", V50 = "EEF5F2", V100 = "D7EAE3";
const TXT = "14201D", GRIS = "64706C", BORDE = "D6DCDA";
const AMB_BG = "FBF0DC", AMB_TX = "6B4A05";
const TERM_BG = "10221E", TERM_TX = "D9F2EA", TERM_OK = "7EE0B8";
const F = "Calibri", MONO = "Courier New";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "AdMind — Sustentación técnica final";
pres.author = "Manuel Alejandro Aldana Rincón y Anderson Camilo Remiso Niño";
pres.subject = "Ingeniería de Software II — Universidad de Cundinamarca";
pres.theme = { headFontFace: F, bodyFontFace: F };

pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: "FFFFFF" },
  objects: [
    { text: { text: "AdMind · Ingeniería de Software II · 2026",
        options: { x: 0.6, y: 7.05, w: 6, h: 0.3, fontSize: 10, color: GRIS, fontFace: F, margin: 0 } } },
  ],
  slideNumber: { x: 12.13, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: GRIS, fontFace: F, align: "right" },
});
pres.defineSlideMaster({ title: "OSCURO", background: { color: V900 } });

const X = 0.6, W = 12.13;

// ---------- ayudas ----------
function contenido(tag, titulo, notas) {
  const s = pres.addSlide({ masterName: "CONTENIDO" });
  s.addText(tag, { x: X, y: 0.38, w: W, h: 0.3, fontSize: 13, bold: true, color: V600, fontFace: F, margin: 0, charSpacing: 2, isTextBox: true });
  s.addText(titulo, { x: X, y: 0.68, w: W, h: 0.75, fontSize: 32, bold: true, color: V700, fontFace: F, margin: 0, valign: "top", isTextBox: true });
  s.addNotes(notas);
  return s;
}

function bullets(s, items, o) {
  const runs = [];
  items.forEach((it, i) => {
    const last = i === items.length - 1;
    if (Array.isArray(it)) {
      runs.push({ text: it[0] + " ", options: { bold: true, bullet: true, color: V700 } });
      runs.push({ text: it[1], options: { breakLine: !last } });
    } else {
      runs.push({ text: it, options: { bullet: true, breakLine: !last } });
    }
  });
  s.addText(runs, Object.assign({ fontSize: 17, color: TXT, fontFace: F, valign: "top", paraSpaceAfter: 9, margin: 0, isTextBox: true }, o));
}

// Imagen ajustada (contain) dentro de la caja, centrada, con marco suave.
function foto(s, ruta, x, y, w, h, alt, marco) {
  const d = sizeOf(ruta);
  const r = d.width / d.height;
  let iw = w, ih = w / r;
  if (ih > h) { ih = h; iw = h * r; }
  const ix = x + (w - iw) / 2, iy = y + (h - ih) / 2;
  if (marco !== false) {
    s.addShape(pres.ShapeType.rect, { x: ix - 0.04, y: iy - 0.04, w: iw + 0.08, h: ih + 0.08, fill: { color: "FFFFFF" },
      line: { color: BORDE, width: 0.75 }, shadow: { type: "outer", blur: 6, offset: 2, angle: 90, color: "000000", opacity: 0.15 } });
  }
  s.addImage({ path: ruta, x: ix, y: iy, w: iw, h: ih, altText: alt });
  return { x: ix, y: iy, w: iw, h: ih };
}

// Espacio para una captura que solo existe fuera de este equipo.
function imagen(s, x, y, w, h, etiqueta) {
  s.addText([
    { text: "CAPTURA PENDIENTE", options: { bold: true, fontSize: 12, color: V600, breakLine: true } },
    { text: etiqueta, options: { fontSize: 12, color: GRIS } },
  ], { x, y, w, h, shape: pres.ShapeType.roundRect, rectRadius: 0.08, fill: { color: V50 },
       line: { color: "9DB5AE", width: 1.25, dashType: "dash" }, align: "center", valign: "middle",
       fontFace: F, margin: 8, objectName: "captura_pendiente" });
}

function tarjeta(s, x, y, w, h, titulo, items, tam, chip) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: V50 }, line: { color: V50, width: 0 } });
  s.addText(titulo, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.4, fontSize: 17, bold: true, color: V700, fontFace: F, margin: 0, isTextBox: true });
  if (chip) etiqueta(s, x + w - 0.2 - chip.w, y + 0.17, chip.w, chip.t, chip.ok);
  bullets(s, items, { x: x + 0.2, y: y + 0.65, w: w - 0.4, h: h - 0.8, fontSize: tam || 14, paraSpaceAfter: 6 });
}

// Pastilla de estado: verde = hecho, ámbar = no implementado / pendiente.
function etiqueta(s, x, y, w, t, ok) {
  s.addText(t, { x, y, w, h: 0.34, shape: pres.ShapeType.roundRect, rectRadius: 0.17,
    fill: { color: ok ? V100 : AMB_BG }, color: ok ? V700 : AMB_TX, bold: true, fontSize: 11,
    fontFace: F, align: "center", valign: "middle", margin: 0 });
}

function caja(s, x, y, w, h, texto, oscura, tam) {
  s.addText(texto, { x, y, w, h, shape: pres.ShapeType.roundRect, rectRadius: 0.08,
    fill: { color: oscura ? V600 : V50 }, color: oscura ? "FFFFFF" : V700, bold: true, fontSize: tam || 14,
    fontFace: F, align: "center", valign: "middle", margin: 6 });
}

function flecha(s, x, y, w) {
  s.addText("→", { x, y, w, h: 0.4, fontSize: 22, color: V600, bold: true, align: "center", valign: "middle", fontFace: F, margin: 0, isTextBox: true });
}

// Recuadro tipo terminal con salida real.
function terminal(s, x, y, w, h, lineas, tam) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: TERM_BG }, line: { color: TERM_BG, width: 0 } });
  const runs = lineas.map((l, i) => {
    const t = Array.isArray(l) ? l[0] : l;
    const c = Array.isArray(l) ? l[1] : TERM_TX;
    return { text: t, options: { color: c, breakLine: i < lineas.length - 1 } };
  });
  s.addText(runs, { x: x + 0.25, y: y + 0.2, w: w - 0.5, h: h - 0.4, fontFace: MONO, fontSize: tam || 13, valign: "top", margin: 0, isTextBox: true, paraSpaceAfter: 3 });
}

// =====================================================================
// 1. Portada
// =====================================================================
{
  const s = pres.addSlide({ masterName: "OSCURO" });
  s.addShape(pres.ShapeType.roundRect, { x: 0.9, y: 1.0, w: 2.0, h: 2.0, rectRadius: 0.2, fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 } });
  s.addImage({ path: R.logo, x: 1.1, y: 1.2, w: 1.6, h: 1.6, altText: "Logo de AdMind" });
  s.addText("AdMind", { x: 3.4, y: 1.0, w: 9, h: 1.0, fontSize: 54, bold: true, color: "FFFFFF", fontFace: F, margin: 0, isTextBox: true });
  s.addText("Plataforma de administración de conjuntos residenciales", { x: 3.4, y: 2.0, w: 9, h: 0.6, fontSize: 22, color: "CFE5DD", fontFace: F, margin: 0, isTextBox: true });
  s.addText("Sustentación técnica final · 23 de noviembre de 2026", { x: 3.4, y: 2.65, w: 9, h: 0.4, fontSize: 16, color: "CFE5DD", fontFace: F, margin: 0, isTextBox: true });

  s.addText([
    { text: "Integrantes", options: { bold: true, color: "9ED3C3", fontSize: 14, breakLine: true } },
    { text: "MANUEL ALEJANDRO ALDANA RINCÓN", options: { color: "FFFFFF", fontSize: 18, breakLine: true } },
    { text: "ANDERSON CAMILO REMISO NIÑO", options: { color: "FFFFFF", fontSize: 18, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Asignatura", options: { bold: true, color: "9ED3C3", fontSize: 14, breakLine: true } },
    { text: "Ingeniería de Software II", options: { color: "FFFFFF", fontSize: 18, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Docente", options: { bold: true, color: "9ED3C3", fontSize: 14, breakLine: true } },
    { text: "Oscar Gómez", options: { color: "FFFFFF", fontSize: 18, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Universidad de Cundinamarca · sede Facatativá", options: { color: "FFFFFF", fontSize: 18 } },
  ], { x: 0.9, y: 3.55, w: 7.5, h: 3.4, fontFace: F, valign: "top", margin: 0, isTextBox: true });

  s.addShape(pres.ShapeType.roundRect, { x: 9.55, y: 3.65, w: 2.9, h: 3.2, rectRadius: 0.15, fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 } });
  s.addImage({ path: R.qr, x: 9.8, y: 3.8, w: 2.4, h: 2.45, altText: "Código QR a https://admind.detkor.com" });
  s.addText("admind.detkor.com", { x: 9.55, y: 6.3, w: 2.9, h: 0.4, fontSize: 14, bold: true, color: V700, fontFace: F, align: "center", margin: 0, isTextBox: true });
  s.addNotes("Portada. ~20 s. Presenta: Alejo.\nPresentarse, nombrar el proyecto y decir que la presentación sigue los criterios de evaluación en el mismo orden (A a K).\nEl QR ya está en la portada: el profe puede ir abriendo la app mientras hablamos.");
}

// =====================================================================
// 2. Recorrido
// =====================================================================
{
  const s = contenido("RECORRIDO", "Qué vamos a mostrar",
    "Recorrido. ~30 s. Presenta: Alejo.\nLos 11 criterios del profe, en su mismo orden, y al final la demostración en vivo con el QR.\nCada diapositiva trae su evidencia: captura, historial o la app en vivo.");
  const items = [
    ["A", "Diseño y experiencia de usuario"], ["B", "Manejo de roles"], ["C", "Seguridad"], ["D", "API, CORS y JWT"],
    ["E", "Estructura y documentación de la API"], ["F", "Correo y reportes"], ["G", "Pruebas unitarias"], ["H", "Base de datos"],
    ["I", "Integración continua"], ["J", "Calidad de código (SonarQube)"], ["K", "Despliegue en la nube"],
  ];
  const cw = (W - 3 * 0.25) / 4, ch = 1.35;
  items.concat([[null, "Demostración en vivo con el QR"]]).forEach((it, i) => {
    const x = X + (i % 4) * (cw + 0.25), y = 1.75 + Math.floor(i / 4) * (ch + 0.25);
    if (it[0]) {
      s.addShape(pres.ShapeType.roundRect, { x, y, w: cw, h: ch, rectRadius: 0.08, fill: { color: V50 }, line: { color: V50, width: 0 } });
      s.addText(it[0], { x: x + 0.2, y: y + 0.38, w: 0.6, h: 0.6, shape: pres.ShapeType.ellipse, fill: { color: V600 }, color: "FFFFFF", bold: true, fontSize: 20, align: "center", valign: "middle", fontFace: F, margin: 0 });
      s.addText(it[1], { x: x + 0.95, y: y + 0.15, w: cw - 1.1, h: ch - 0.3, fontSize: 15, bold: true, color: V700, fontFace: F, valign: "middle", margin: 0, isTextBox: true });
    } else {
      s.addText(it[1], { x, y, w: cw, h: ch, shape: pres.ShapeType.roundRect, rectRadius: 0.08, fill: { color: V600 }, color: "FFFFFF", bold: true, fontSize: 16, align: "center", valign: "middle", fontFace: F, margin: 12 });
    }
  });
}

// =====================================================================
// 3. Qué es AdMind
// =====================================================================
{
  const s = contenido("CONTEXTO", "Qué es AdMind",
    "Qué es AdMind. ~1 min. Presenta: Alejo.\nUna app web para administrar conjuntos residenciales en Colombia, pensada para la Ley 675 de 2001.\nUn solo sistema sirve a varios conjuntos y los datos de cada uno quedan separados.\nMódulos construidos: reservas de zonas comunes, casos, anuncios, pagos de administración, visitantes, ingresos a zonas, infracciones y parqueaderos.\nLa arquitectura son dos servidores Django (front y API) y una base PostgreSQL; el front nunca habla directo con la base, y el navegador nunca habla directo con la API.\nLa captura es la pantalla de pagos con el rol Administración.");
  bullets(s, [
    "Administra conjuntos residenciales en Colombia, bajo la Ley 675 de 2001",
    "Un solo sistema para varios conjuntos; los datos de cada uno quedan aislados",
    "Reservas de zonas, casos, anuncios, pagos, visitantes, ingresos a zonas, infracciones y parqueaderos",
    "Cuatro roles de conjunto y un Superusuario de plataforma",
  ], { x: X, y: 1.7, w: 6.6, h: 3.3 });
  foto(s, R.panel, 7.55, 1.7, 5.18, 3.2, "Pantalla de pagos de administración con el rol Administración");
  caja(s, X, 5.4, 2.6, 0.9, "Navegador", false);
  flecha(s, X + 2.6, 5.65, 0.55);
  caja(s, X + 3.15, 5.4, 2.9, 0.9, "Front-end · Django + Alpine.js", true);
  flecha(s, X + 6.05, 5.65, 0.55);
  caja(s, X + 6.6, 5.4, 2.9, 0.9, "API · Django REST Framework", true);
  flecha(s, X + 9.5, 5.65, 0.55);
  caja(s, X + 10.05, 5.4, 2.08, 0.9, "PostgreSQL", true);
}

// =====================================================================
// 4. A. UX / UI
// =====================================================================
{
  const s = contenido("CRITERIO A", "Diseño y experiencia de usuario",
    "Criterio A. ~1 min. Presenta: Alejo.\nUna sola línea gráfica: el verde de AdMind (#0E6B5A), con las tipografías Archivo e Inter, desde el ingreso hasta el último panel.\nEl sistema de diseño es propio (tokens y componentes am-*): sin Bootstrap ni Tailwind.\nNavegación: el menú lateral muestra solo lo que el rol puede usar (se ve en la siguiente diapositiva).\nLos errores también llevan la identidad y hablan en español: las páginas 403, 404 y 500 y los mensajes de la API ya traducidos.\nLas dos capturas son de la app en la nube, tomadas el 18-nov: el ingreso y la página 404.\nPREGUNTA PROBABLE: «¿el acento por conjunto no rompe la coherencia?». Respuesta: cada conjunto elige su color y su foto, pero la marca, la tipografía y los componentes son los mismos.");
  bullets(s, [
    ["Una sola línea gráfica:", "el verde de AdMind y las tipografías Archivo e Inter, del ingreso a todos los paneles"],
    ["Sistema de diseño propio:", "colores, tipografías y componentes reutilizables, sin Bootstrap ni Tailwind"],
    ["Navegación por rol:", "el menú lateral muestra solo lo que ese rol puede usar"],
    ["Cada conjunto", "elige su color de acento y su foto; la marca no cambia"],
    ["Errores legibles:", "páginas 403, 404 y 500 con el mismo diseño y mensajes en español"],
  ], { x: X, y: 1.7, w: 5.4, h: 4.6, fontSize: 16 });
  const a = foto(s, R.ingreso, 6.35, 1.75, 3.05, 4.3, "Pantalla de ingreso de AdMind en la nube");
  const b = foto(s, R.e404, 9.65, 1.75, 3.08, 4.3, "Página 404 propia de AdMind en la nube");
  s.addText("Ingreso, en la nube", { x: 6.35, y: a.y + a.h + 0.15, w: 3.05, h: 0.3, fontSize: 12, color: GRIS, align: "center", fontFace: F, margin: 0, isTextBox: true });
  s.addText("Página 404 propia, en la nube", { x: 9.65, y: b.y + b.h + 0.15, w: 3.08, h: 0.3, fontSize: 12, color: GRIS, align: "center", fontFace: F, margin: 0, isTextBox: true });
}

// =====================================================================
// 5. B. Roles (1)
// =====================================================================
{
  const s = contenido("CRITERIO B", "Manejo de roles: quién es quién",
    "Criterio B, primera parte. ~1 min. Presenta: Camilo.\nEl mínimo es 4 roles; AdMind tiene 5: Superusuario (plataforma), Administración, Secretaría, Vigilancia y Residente.\nLos roles y los permisos viven en código, no se editan desde la interfaz: el administrador solo asigna. Una persona tiene un solo rol vigente por conjunto.\nA la derecha, el menú lateral de tres roles en el mismo conjunto: Administración ve 17 opciones y Vigilancia solo 5. Las capturas son de las pruebas locales del Manual de Usuario.");
  const enc = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: V600 }, fontSize: 14 } });
  const c = (t, alt, b) => ({ text: t, options: { fontSize: 14, color: TXT, bold: !!b, fill: { color: alt ? V50 : "FFFFFF" } } });
  const filas = [
    ["Superusuario", "Plataforma", "Crea y da de baja conjuntos, ve la auditoría técnica y tiene todos los permisos"],
    ["Administración", "Conjunto", "Gestiona reglas, zonas, personas, reservas, pagos y reportes"],
    ["Secretaría", "Conjunto", "Clasifica solicitudes, gestiona casos y publica anuncios; no aprueba reservas"],
    ["Vigilancia", "Conjunto", "Registra visitantes y los ingresos a zonas con aforo"],
    ["Residente", "Conjunto", "Solicita y cancela sus reservas, abre casos y ve anuncios y documentos"],
  ];
  s.addTable([[enc("Rol"), enc("Alcance"), enc("Qué puede hacer")]].concat(
    filas.map((f, i) => [c(f[0], i % 2 === 1, true), c(f[1], i % 2 === 1), c(f[2], i % 2 === 1)])),
    { x: X, y: 1.7, w: 7.4, colW: [1.8, 1.2, 4.4], border: { type: "solid", pt: 0.75, color: BORDE }, fontFace: F, valign: "middle", margin: [4, 8, 4, 8] });
  s.addText("Mínimo exigido: 4 roles. AdMind tiene 5.", { x: X, y: 5.6, w: 7.4, h: 0.45, fontSize: 18, bold: true, color: V700, fontFace: F, margin: 0, isTextBox: true });

  const menus = [["Administración", R.mAdmin], ["Residente", R.mRes], ["Vigilancia", R.mVig]];
  const mw = 1.3, mg = 0.35, x0 = 8.35;
  menus.forEach((m, i) => {
    const x = x0 + i * (mw + mg);
    s.addText(m[0], { x, y: 1.6, w: mw, h: 0.3, fontSize: 12, bold: true, color: V700, align: "center", fontFace: F, margin: 0, isTextBox: true });
    const d = sizeOf(m[1]);
    const h = mw * d.height / d.width;
    s.addShape(pres.ShapeType.rect, { x: x - 0.03, y: 1.97, w: mw + 0.06, h: h + 0.06, fill: { color: "FFFFFF" }, line: { color: BORDE, width: 0.75 } });
    s.addImage({ path: m[1], x, y: 2.0, w: mw, h, altText: "Menú lateral del rol " + m[0] });
  });
}

// =====================================================================
// 6. B. Roles (2)
// =====================================================================
{
  const s = contenido("CRITERIO B", "Manejo de roles: cómo se restringe el acceso",
    "Criterio B, segunda parte. ~1 min. Presenta: Camilo.\nSe valida en tres sitios: la interfaz oculta lo que el rol no puede usar; cada endpoint de la API exige su permiso y responde 403 si no lo tiene; y los datos de cada conjunto están aislados.\nCrear, ver, editar y eliminar son permisos distintos del catálogo. Eliminar es baja lógica: no hay borrado físico (y la base lo impide con un trigger, criterio H).\nLos permisos sensibles piden además el segundo factor (código de 6 dígitos).\nEVIDENCIA: la carpeta tests/aislamiento tiene la prueba «del intruso», que recorre automáticamente todas las rutas de la API (101 al 22-nov; falla si aparece una ruta nueva sin registrar) con un usuario sin permiso y con uno de otro conjunto. La salida de la derecha es real: 104 pruebas, corridas el 18-nov.\nDEMO EN VIVO: con la sesión de un Residente, escribir en la barra la URL de una pantalla de Administración; sale la página 403.");
  bullets(s, [
    ["Front-end:", "el menú y los botones solo aparecen si el rol tiene el permiso; si escribe la URL, ve una página 403"],
    ["Back-end:", "cada endpoint exige su permiso y responde 403 sin él; el front no es la única barrera"],
    ["Datos:", "cada conjunto queda aislado; ningún endpoint acepta el conjunto desde afuera"],
    ["Permisos por acción:", "crear, ver, editar y eliminar son permisos distintos; eliminar es baja lógica"],
    ["Sensibles con 2FA:", "las acciones delicadas piden además el segundo factor"],
  ], { x: X, y: 1.7, w: 6.4, h: 4.6, fontSize: 16 });
  terminal(s, 7.3, 1.75, 5.43, 1.75, [
    "$ pytest tests/aislamiento -q",
    "",
    ["104 passed in 21.58s", TERM_OK],
  ], 15);
  s.addText("Salida real, 18-nov", { x: 7.3, y: 3.6, w: 5.43, h: 0.3, fontSize: 12, color: GRIS, fontFace: F, margin: 0, isTextBox: true });
  tarjeta(s, 7.3, 4.15, 5.43, 2.15, "Prueba del intruso", [
    "Recorre todas las rutas de la API con un usuario sin permiso",
    "Y con un usuario de otro conjunto",
  ], 15);
}

// =====================================================================
// 7. C. Seguridad
// =====================================================================
{
  const s = contenido("CRITERIO C", "Seguridad",
    "Criterio C. ~1 min. Presenta: Camilo.\nLas contraseñas no se guardan ni en texto plano ni con un hash simple: se guardan con PBKDF2-SHA256, con sal aleatoria y 1.000.000 de iteraciones, que es el hasher por defecto de Django 5.2. El proyecto no lo reemplaza en producción; solo la configuración de pruebas usa uno rápido, a propósito, para que las pruebas corran en segundos.\nLos secretos no están en el código: salen de variables de entorno (.env), que no se suben a GitHub. En producción DEBUG está apagado y ALLOWED_HOSTS solo acepta el dominio (C3, en main desde el 17-nov).\nSegundo factor TOTP. La sesión dura 1 hora contada desde el ingreso (no «una hora sin uso»). El token de sesión es opaco, vive en una tabla y en la base se guarda solo su huella SHA-256; en el navegador solo hay una cookie HttpOnly del front. Cerrar sesión lo invalida de verdad.\nAl dar Atrás después de cerrar sesión no se ve nada: las páginas llevan never_cache.\nEl recuadro oscuro muestra el formato con que Django guarda una contraseña; la sal y el hash van como marcadores. EN VIVO (opcional): SELECT password FROM la tabla de usuarios, en la base local, para que se vea el hash real.");
  bullets(s, [
    ["Contraseñas:", "PBKDF2-SHA256 con sal y 1.000.000 de iteraciones; nunca texto plano"],
    ["Secretos fuera del código:", "claves y conexión en variables de entorno, sin subirlos a GitHub"],
    ["Producción:", "DEBUG apagado, solo el dominio permitido y cookies seguras"],
    ["Segundo factor:", "código de 6 dígitos para las acciones sensibles"],
    ["Sesión:", "dura 1 hora; el token se guarda solo como huella SHA-256 y cerrar sesión lo invalida"],
    ["Botón Atrás:", "tras cerrar sesión no muestra páginas guardadas"],
  ], { x: X, y: 1.7, w: 6.6, h: 4.7, fontSize: 16 });
  s.addText("Así se guarda una contraseña", { x: 7.5, y: 1.7, w: 5.23, h: 0.4, fontSize: 16, bold: true, color: V700, fontFace: F, margin: 0, isTextBox: true });
  terminal(s, 7.5, 2.2, 5.23, 1.9, [
    ["algoritmo$iteraciones$sal$hash", "8FB3A8"],
    "",
    "pbkdf2_sha256$1000000$",
    "<sal>$<hash>",
  ], 14);
  tarjeta(s, 7.5, 4.3, 5.23, 2.0, "Token de sesión", [
    "Opaco, en una tabla: se puede revocar",
    "El navegador solo ve una cookie HttpOnly",
  ], 14);
}

// =====================================================================
// 8. D. API, CORS y JWT
// =====================================================================
{
  const s = contenido("CRITERIO D", "Consumo de la API, JWT y CORS",
    "Criterio D. ~1,5 min. Presenta: Camilo.\nCONSUMO (hecho): las pantallas las arma el servidor del front, que llama a la API con requests (carpeta cliente_api), de servidor a servidor. El navegador nunca habla directo con la API; solo tiene la cookie HttpOnly del front.\nCORS (hecho, PR #19 del back, en main y en la nube desde el 22-nov): django-cors-headers 4.9.0. CorsMiddleware va arriba en MIDDLEWARE. La lista blanca sale de la variable de entorno CORS_ALLOWED_ORIGINS: en la nube vale https://admind.detkor.com; en local, http://127.0.0.1:8001. Nunca el comodín * y CORS_ALLOW_CREDENTIALS = False. Pruebas: tests/test_cors.py (el preflight del front recibe permiso; el de un origen ajeno, no).\nPor qué casi no entra en juego: CORS es una política del navegador, y en AdMind el navegador nunca llama a la API. La lista blanca cierra la puerta de atrás si algún día la API se publica.\nEN VIVO (en el VPS): curl -X OPTIONS con Origin https://admind.detkor.com devuelve access-control-allow-origin; con Origin https://malo.com no devuelve nada.\nJWT (no implementado): hoy el token es opaco (32 bytes aleatorios), viaja en Authorization: Token y en la base solo se guarda su huella SHA-256. Se revoca al instante: cerrar sesión borra la fila y cambiar la contraseña cierra todas las sesiones. Un JWT puro no se puede revocar sin una lista negra, que es justo una tabla como la nuestra. La decisión del 14-nov fue un JWT híbrido (firmado HS256, con la tabla para revocar) y no alcanzó. Decirlo así, sin rodeos.");
  // Flujo
  caja(s, X, 1.75, 2.4, 0.95, "Navegador", false, 15);
  s.addText("cookie HttpOnly", { x: X + 2.4, y: 1.6, w: 1.9, h: 0.3, fontSize: 12, color: GRIS, align: "center", fontFace: F, margin: 0, isTextBox: true });
  flecha(s, X + 2.4, 2.02, 1.9);
  caja(s, X + 4.3, 1.75, 3.2, 0.95, "Servidor del front (Django)", true, 15);
  s.addText("token, servidor a servidor", { x: X + 7.5, y: 1.6, w: 2.2, h: 0.3, fontSize: 12, color: GRIS, align: "center", fontFace: F, margin: 0, isTextBox: true });
  flecha(s, X + 7.5, 2.02, 2.2);
  caja(s, X + 9.7, 1.75, 2.43, 0.95, "API (DRF)", true, 15);

  const cw = 3.9, gap = 0.215, y = 3.1, h = 2.7;
  tarjeta(s, X, y, cw, h, "Consumo de la API", [
    "El front llama a la API desde su servidor, con el token",
    "El navegador nunca llama a la API directo",
  ], 14, { w: 0.9, t: "Hecho", ok: true });
  tarjeta(s, X + cw + gap, y, cw, h, "JWT", [
    "Hoy: token opaco en una tabla de sesiones",
    "Se revoca al cerrar sesión o cambiar la contraseña",
    "El JWT híbrido decidido no se construyó",
  ], 14, { w: 1.6, t: "No implementado", ok: false });
  tarjeta(s, X + 2 * (cw + gap), y, cw, h, "CORS", [
    "django-cors-headers con lista blanca: solo https://admind.detkor.com",
    "Un origen ajeno no recibe permiso; sin comodín ni credenciales",
    "La lista sale del entorno, no del código",
  ], 14, { w: 0.9, t: "Hecho", ok: true });
}

// =====================================================================
// 9. E. Estructura y documentación de la API
// =====================================================================
{
  const s = contenido("CRITERIO E", "Estructura y documentación de la API",
    "Criterio E. ~1 min. Presenta: Camilo.\nArquitectura limpia: cada petición pasa por capas — vista (recibe y responde), servicio (reglas de negocio) y repositorio (acceso a datos). Es el flujo que pidió el profesor.\nSWAGGER (hecho, PR #20 del back, en main y en la nube desde el 22-nov): drf-spectacular 0.30.0 genera el esquema OpenAPI 3.0 leyendo las vistas, y Swagger UI lo muestra. Rutas: /api/schema/ (el esquema) y /api/docs/ (la interfaz). Las vistas llevan @extend_schema con su grupo y descripción.\nNúmeros, leídos del esquema de la nube el 22-nov: 101 rutas de negocio (más la del propio esquema), 123 operaciones, 18 grupos (Cuentas 19, Reservas 15, Casos 9…).\nSeguridad: la documentación es pública, pero cada operación de negocio sigue pidiendo el token (el candado del botón Authorize). La API no está publicada en internet: la captura se tomó en el servidor, por un túnel SSH. EN VIVO: si el profe la pide, abrir el túnel (ssh -L 18000:127.0.0.1:8000) y entrar a http://127.0.0.1:18000/api/docs/.\nAdemás está el anexo de rutas del Manual Técnico entregado el 14-nov.");
  caja(s, X, 1.7, 1.55, 0.8, "Vista", true);
  flecha(s, X + 1.55, 1.9, 0.5);
  caja(s, X + 2.05, 1.7, 1.55, 0.8, "Servicio", true);
  flecha(s, X + 3.6, 1.9, 0.5);
  caja(s, X + 4.1, 1.7, 1.6, 0.8, "Repositorio", true);
  flecha(s, X + 5.7, 1.9, 0.5);
  caja(s, X + 6.2, 1.7, 1.1, 0.8, "BD", true);
  bullets(s, [
    ["Capas claras:", "la vista recibe, el servicio aplica las reglas y el repositorio habla con la base"],
    ["101 rutas y 123 operaciones", "en 18 grupos; todas piden token salvo el ingreso y la recuperación de contraseña"],
    ["Swagger / OpenAPI 3.0:", "drf-spectacular genera el esquema desde el código, así no se desactualiza"],
  ], { x: X, y: 2.85, w: 6.7, h: 2.6, fontSize: 16 });
  s.addShape(pres.ShapeType.roundRect, { x: X, y: 5.55, w: 6.7, h: 0.75, rectRadius: 0.08, fill: { color: V50 }, line: { color: V50, width: 0 } });
  s.addText([
    { text: "Documentación en vivo: ", options: { bold: true } },
    { text: "/api/docs/ (Swagger UI) y /api/schema/ (OpenAPI)" },
  ], { x: X + 0.25, y: 5.55, w: 5.1, h: 0.75, fontSize: 15, color: V700, fontFace: F, margin: 0, valign: "middle", isTextBox: true });
  etiqueta(s, X + 6.7 - 1.15, 5.75, 0.9, "Hecho", true);

  const sw = foto(s, R.swagger, 8.2, 1.7, 4.53, 4.15, "Swagger UI de la API de AdMind, servido desde la nube");
  s.addText("Swagger UI de la API, en el servidor de la nube", { x: 8.2, y: sw.y + sw.h + 0.15, w: 4.53, h: 0.3, fontSize: 12, color: GRIS, align: "center", fontFace: F, margin: 0, isTextBox: true });
}

// =====================================================================
// 10. F. Correo y reportes
// =====================================================================
{
  const s = contenido("CRITERIO F", "Notificaciones por correo y reportes",
    "Criterio F. ~1,5 min. Presenta: correo Alejo, reportes Camilo.\nCORREO (hecho, PR #14): automático y en HTML, no en texto plano. Lleva el logo incrustado en el mensaje (CID), el verde de AdMind y el nombre del conjunto, con una alternativa en texto. Tres puntos de envío: los avisos (anuncios, casos, infracciones, ingresos y decisión de una reserva), la recuperación de contraseña y el restablecimiento del segundo factor.\nREPORTES (hechos, PR #17 y #10): PDF «Uso de zonas comunes» y Excel «Estado de pagos del mes», en la pantalla /reportes/. Solo Administración (y el Superusuario) los descarga. Los datos salen de funciones de la base (fn_ocupacion_areas y fn_estado_pagos, criterio H): ahí se ve la utilidad práctica de las funciones.\nEN VIVO: descargar los dos reportes desde la app en la nube.\nCAPTURA PENDIENTE: el correo abierto en Gmail, enviado desde la nube (por ejemplo, la recuperación de contraseña). Reemplazar el recuadro punteado.");
  const cw = 5.95;
  s.addText("Correo en HTML", { x: X, y: 1.65, w: cw, h: 0.4, fontSize: 20, bold: true, color: V700, fontFace: F, margin: 0, isTextBox: true });
  bullets(s, [
    "Maquetación HTML con el logo incrustado y el verde de AdMind",
    "Avisos, recuperación de contraseña y restablecer el segundo factor",
  ], { x: X, y: 2.1, w: cw, h: 1.3, fontSize: 15, paraSpaceAfter: 6 });
  imagen(s, X, 3.5, cw, 2.8, "El correo abierto en Gmail, enviado desde la nube, con el logo");

  const x2 = X + cw + 0.23;
  s.addText("Reportes PDF y Excel", { x: x2, y: 1.65, w: cw, h: 0.4, fontSize: 20, bold: true, color: V700, fontFace: F, margin: 0, isTextBox: true });
  bullets(s, [
    "PDF «Uso de zonas comunes» y Excel «Estado de pagos del mes»",
    "Logo, títulos y tabla en verde; solo Administración los descarga",
  ], { x: x2, y: 2.1, w: cw, h: 1.3, fontSize: 15, paraSpaceAfter: 6 });
  // Flujo del reporte
  const fw = 1.75, fg = 0.35;
  [["Pantalla /reportes/", false], ["API: permiso de reportes", true], ["Función de la base", true]].forEach((p, i) => {
    caja(s, x2 + i * (fw + fg), 3.55, fw, 1.0, p[0], p[1], 13);
    if (i < 2) flecha(s, x2 + i * (fw + fg) + fw, 3.85, fg);
  });
  tarjeta(s, x2, 4.8, cw, 1.5, "De dónde salen los datos", [
    "PDF: fn_ocupacion_areas · Excel: fn_estado_pagos",
  ], 14);
}

// =====================================================================
// 11. G. Pruebas unitarias
// =====================================================================
{
  const s = contenido("CRITERIO G", "Pruebas unitarias y cobertura",
    "Criterio G. ~1 min. Presenta: Alejo.\nBack-end: 854 pruebas con 94,2 % de cobertura; el mínimo exigido es 70 %. Es la salida real del CI de main del 22-nov (recuadro de la derecha), con CORS y Swagger ya dentro.\nEl front tiene 541 pruebas (mismo CI), que son extra: el criterio solo pide el back.\nHerramientas: pytest, pytest-django y pytest-cov (coverage.py). Las pruebas corren contra PostgreSQL real, no SQLite, para que los triggers, las funciones y las restricciones de la base también se prueben.\nHay camino feliz y casos de error: permisos denegados (403), recursos de otro conjunto (404), datos inválidos y concurrencia de reservas.\nLa cobertura se mide en cada ejecución del CI (--cov-fail-under=70): si baja, el CI falla y el PR no se funde. El reporte HTML queda como artefacto de cada ejecución.\nPREGUNTA PROBABLE: «¿por qué el hasher de pruebas es MD5?». Respuesta: solo en config/settings_pruebas.py, para que las 854 pruebas corran en segundos; producción usa PBKDF2.");
  const stats = [["854", "pruebas en el back-end"], ["94,2 %", "de cobertura (mínimo 70 %)"], ["541", "pruebas en el front (extra)"]];
  const sw = 3.9, sg = 0.215;
  stats.forEach((st, i) => {
    const x = X + i * (sw + sg);
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.65, w: sw, h: 1.55, rectRadius: 0.08, fill: { color: V50 }, line: { color: V50, width: 0 } });
    s.addText(st[0], { x, y: 1.7, w: sw, h: 0.95, fontSize: 52, bold: true, color: V600, align: "center", valign: "middle", fontFace: F, margin: 0, isTextBox: true });
    s.addText(st[1], { x, y: 2.6, w: sw, h: 0.45, fontSize: 15, color: V700, align: "center", valign: "middle", fontFace: F, margin: 0, isTextBox: true });
  });
  bullets(s, [
    ["Camino feliz y errores:", "permiso denegado, recurso de otro conjunto, datos inválidos y concurrencia"],
    ["Cobertura en el CI:", "cada ejecución la mide y falla si baja del 70 %"],
    ["Prueba del intruso:", "todas las rutas de la API contra un usuario sin permiso"],
  ], { x: X, y: 3.5, w: 5.5, h: 2.8, fontSize: 16 });
  terminal(s, 6.45, 3.5, 6.28, 2.45, [
    ["CI de main · back-end · 22-nov", "8FB3A8"],
    "$ pytest -q --cov --cov-fail-under=70",
    "",
    "TOTAL   6183   272   94.2%",
    ["Required test coverage of 70% reached.", TERM_OK],
    ["854 passed in 36.21s", TERM_OK],
  ], 14);
  s.addText("Salida real de GitHub Actions", { x: 6.45, y: 6.03, w: 6.28, h: 0.3, fontSize: 12, color: GRIS, fontFace: F, margin: 0, isTextBox: true });
}

// =====================================================================
// 12. H. Base de datos
// =====================================================================
{
  const s = contenido("CRITERIO H", "Base de datos",
    "Criterio H. ~1,5 min. Presenta: Camilo.\nDiseño: 42 tablas en PostgreSQL (el diccionario de datos está en la documentación entregada). A la izquierda, el diagrama entidad-relación.\nCOMPLETAR ANTES DEL LUNES: 3 o 4 diferencias concretas frente al MER inicial (tablas nuevas, relaciones que cambiaron, restricciones que ahora impone la base). Esto lo saben ustedes; no está escrito en la bóveda.\nLo que la base impone por sí misma: llaves foráneas compuestas para aislar conjuntos, índices únicos parciales, auditoría de solo inserción.\nObjetos (todos en migraciones con RunSQL, así viajan con el esquema; aplicados en el VPS el 17-nov):\n- 4 funciones: fn_ocupacion_areas (alimenta el PDF), fn_estado_pagos (alimenta el Excel), fn_resumen_casos, fn_aforo_actual.\n- 1 procedimiento: sp_expirar_bloqueos_vencidos (se llama con CALL; libera las franjas bloqueadas que vencieron).\n- 5 triggers: trg_sin_borrado_fisico en casos, infracciones, pagos y solicitudes de reserva (cuatro tablas, la misma regla), y trg_infraccion_anulada_inmutable.\nPREGUNTA PROBABLE: «¿por qué cuatro son funciones y una es procedimiento?». Respuesta: las cuatro devuelven datos para leer (SELECT); el procedimiento modifica datos y no devuelve nada, por eso es PROCEDURE y se invoca con CALL.\nPREGUNTA PROBABLE: «el criterio pide 5 triggers distintos». Respuesta honesta: son 5 triggers en la base, con dos reglas distintas; la del borrado físico protege cuatro tablas.\nEN VIVO (opcional): \\df y SELECT trigger_name, event_object_table FROM information_schema.triggers;");
  foto(s, R.mer, X, 1.65, 3.3, 2.75, "Diagrama entidad-relación de AdMind");
  bullets(s, [
    ["42 tablas", "en PostgreSQL"],
    ["La base también impone reglas:", "llaves foráneas por conjunto, índices únicos parciales y auditoría de solo inserción"],
    ["En migraciones:", "funciones y triggers viajan con el esquema"],
  ], { x: X + 3.6, y: 1.65, w: 4.6, h: 2.75, fontSize: 15, paraSpaceAfter: 6 });
  s.addText("Se usan en la app", { x: 8.95, y: 1.65, w: 3.78, h: 0.35, fontSize: 14, bold: true, color: V700, fontFace: F, margin: 0, isTextBox: true });
  terminal(s, 8.95, 2.05, 3.78, 2.35, [
    "SELECT * FROM",
    "  fn_ocupacion_areas(...)",
    "SELECT * FROM",
    "  fn_estado_pagos(...)",
    "CALL sp_expirar_bloqueos_",
    "     vencidos(...)",
  ], 12);
  tarjeta(s, X, 4.6, 5.95, 1.75, "5 rutinas: 4 funciones y 1 procedimiento", [
    "fn_ocupacion_areas · fn_estado_pagos · fn_resumen_casos · fn_aforo_actual",
    "sp_expirar_bloqueos_vencidos (PROCEDURE)",
  ], 13);
  tarjeta(s, X + 6.18, 4.6, 5.95, 1.75, "5 triggers", [
    "trg_sin_borrado_fisico en casos, infracciones, pagos y reservas",
    "trg_infraccion_anulada_inmutable",
  ], 13);
}

// =====================================================================
// 13. I. Integración continua
// =====================================================================
{
  const s = contenido("CRITERIO I", "Integración continua con GitHub Actions",
    "Criterio I. ~1 min. Presenta: Alejo.\nGitHub Actions en los dos repositorios (back y front). Corre en cada push y en cada pull request hacia main, desarrollo y pruebas.\nBack: levanta un PostgreSQL 18, comprueba que el lock coincida con requirements.txt, instala, comprueba que no falten migraciones (makemigrations --check) y corre pytest con cobertura mínima de 70 %. Front: lo mismo sin base de datos.\nEndurecido el 22-nov (PR #21 del back y #12 del front): instala solo wheels cuyo hash SHA-256 está en requirements.lock (--require-hashes --only-binary :all:), así ningún paquete cambiado en PyPI entra y ningún setup.py se ejecuta; el token de GitHub del flujo es de solo lectura; acciones en Node 24. Eso corrigió las dos vulnerabilidades MAJOR de Sonar en ci.yml (criterio J).\nHistorial al 22-nov: 30 ejecuciones en el back y 15 en el front; 21 PR en el back y 12 en el front. La captura es del 18-nov.\nPREGUNTA PROBABLE: «hay dos ejecuciones en rojo el 22-nov». Respuesta honesta: el ci.yml nuevo tenía un error de sintaxis YAML (los dos puntos de «:all:» seguidos de espacio); el CI lo detectó, se corrigió en minutos y la siguiente ejecución quedó en verde. Para eso está el CI.\nPREGUNTA PROBABLE: «los primeros dos meses no hay PR». Respuesta: es cierto; desde el 24-oct todo cambio entra por PR, y el CI existe desde el 16-nov.\nTener abierta: github.com/ZeroFour-04/Admind_Backend/actions y la del front.");
  const st = [["30 · 15", "ejecuciones del CI (back · front)"], ["21 · 12", "pull requests (back · front)"]];
  st.forEach((t, i) => {
    const y = 1.7 + i * 1.3;
    s.addShape(pres.ShapeType.roundRect, { x: X, y, w: 4.6, h: 1.1, rectRadius: 0.08, fill: { color: V50 }, line: { color: V50, width: 0 } });
    s.addText(t[0], { x: X + 0.2, y, w: 1.9, h: 1.1, fontSize: 30, bold: true, color: V600, valign: "middle", fontFace: F, margin: 0, isTextBox: true });
    s.addText(t[1], { x: X + 2.15, y, w: 2.3, h: 1.1, fontSize: 14, color: V700, valign: "middle", fontFace: F, margin: 0, isTextBox: true });
  });
  bullets(s, [
    ["Back:", "migraciones, pruebas y cobertura mínima de 70 %"],
    ["Solo paquetes", "verificados por hash"],
  ], { x: X, y: 4.35, w: 4.6, h: 0.9, fontSize: 15, paraSpaceAfter: 4 });
  foto(s, R.actions, 5.55, 1.7, 7.18, 3.5, "Pestaña Actions del backend con el historial de ejecuciones en verde");
  const bw = (W - 4 * 0.35) / 5;
  ["Rama corta por cambio", "Pull request a desarrollo", "CI: pruebas y cobertura", "Merge a desarrollo", "desarrollo → main"].forEach((t, i) => {
    caja(s, X + i * (bw + 0.35), 5.5, bw, 0.8, t, i === 2);
    if (i < 4) flecha(s, X + i * (bw + 0.35) + bw, 5.7, 0.35);
  });
}

// =====================================================================
// 14. J. SonarQube
// =====================================================================
{
  const s = contenido("CRITERIO J", "Calidad de código con SonarQube",
    "Criterio J. ~1,5 min. Presentan: Alejo los pasos y su corrección; Camilo la suya.\nTres pasos que pide el profe: (1) mostrar el reporte del primer escaneo; (2) cada integrante corrige al menos una vulnerabilidad alta o media, en su propio PR; (3) mostrar un segundo escaneo con menos incidencias. No se exige calificación A.\nHerramienta: SonarCloud, sobre los dos repos; analiza main en cada merge.\nPrimer escaneo (17-nov). Back: 3 vulnerabilidades MAJOR — dos en .github/workflows/ci.yml (githubactions S8541: pip podía ejecutar setup.py; S8544: dependencias sin verificar) y una contraseña de ejemplo en .env _ejemplo (secrets S2068). Front: 17 — las mismas dos del ci.yml, una MAJOR en cliente_api/http.py (pythonsecurity S7044) y 14 MINOR (python S3752, vistas que aceptan GET y POST a la vez).\nCORRECCIÓN DE ALEJO (PR #21 del back y #12 del front, 22-nov): las dos MAJOR del ci.yml, en los dos repos. El CI instala solo wheels con hash verificado desde requirements.lock.\nSegundo escaneo (22-nov, leído de la API pública de SonarCloud): back 3 → 1, front 17 → 15. Lo que queda abierto en el back es la contraseña de ejemplo de .env _ejemplo; en el front, la MAJOR de cliente_api/http.py y las 14 MINOR.\nCORRECCIÓN DE CAMILO: PENDIENTE al 22-nov. Si la hace antes de la sustentación (por ejemplo la de .env _ejemplo, que es quitar la contraseña de ejemplo), el back queda en 0: cambiar el paso 2 a «Hecho» y la tabla en build_deck.js. Si no alcanza, decirlo: la de Alejo está hecha y la de Camilo identificada.\nMostrar en vivo la pestaña Activity de SonarCloud.");
  const cw = 3.9, gap = 0.215;
  const pasos = [
    ["1", "Primer escaneo", "17-nov, los dos repos", true],
    ["2", "Corregir", "Alejo: las 2 del ci.yml · Camilo: pendiente", false],
    ["3", "Segundo escaneo", "22-nov: back 3 → 1 y front 17 → 15", true],
  ];
  pasos.forEach((p, i) => {
    const x = X + i * (cw + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.65, w: cw, h: 1.55, rectRadius: 0.08, fill: { color: V50 }, line: { color: V50, width: 0 } });
    s.addText(p[0], { x: x + 0.2, y: 1.85, w: 0.55, h: 0.55, shape: pres.ShapeType.ellipse, fill: { color: V600 }, color: "FFFFFF", bold: true, fontSize: 18, align: "center", valign: "middle", fontFace: F, margin: 0 });
    s.addText(p[1], { x: x + 0.9, y: 1.85, w: cw - 2.1, h: 0.55, fontSize: 17, bold: true, color: V700, fontFace: F, valign: "middle", margin: 0, isTextBox: true });
    etiqueta(s, x + cw - 1.15, 1.95, 0.95, p[3] ? "Hecho" : "En curso", p[3]);
    s.addText(p[2], { x: x + 0.2, y: 2.55, w: cw - 0.4, h: 0.55, fontSize: 14, color: TXT, fontFace: F, valign: "top", margin: 0, isTextBox: true });
  });

  const enc = (t, a) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: V600 }, fontSize: 14, align: a || "center" } });
  const c = (t, i, o) => ({ text: t, options: Object.assign({ fontSize: 14, color: TXT, fill: { color: i % 2 ? V50 : "FFFFFF" }, align: "center" }, o || {}) });
  const mejor = (t, i) => c(t, i, { color: V600, bold: true });
  const filas = [
    [enc("SonarCloud", "left"), enc("Back 17-nov"), enc("Back 22-nov"), enc("Front 17-nov"), enc("Front 22-nov")],
    [c("Vulnerabilidades", 0, { align: "left", bold: true }), c("3", 0), mejor("1", 0), c("17", 0), mejor("15", 0)],
    [c("Calificación de seguridad", 1, { align: "left", bold: true }), c("C", 1), c("C", 1), c("C", 1), c("C", 1)],
    [c("Bugs", 0, { align: "left", bold: true }), c("0", 0), c("0", 0), c("3", 0), c("3", 0)],
    [c("Duplicación", 1, { align: "left", bold: true }), c("0,9 %", 1), c("0,9 %", 1), c("0,2 %", 1), c("0,2 %", 1)],
    [c("Líneas de código", 0, { align: "left", bold: true }), c("19.815", 0), c("20.201", 0), c("16.464", 0), c("16.525", 0)],
  ];
  s.addTable(filas, { x: X, y: 3.45, w: W, colW: [3.73, 2.1, 2.1, 2.1, 2.1], rowH: 0.45, border: { type: "solid", pt: 0.75, color: BORDE }, fontFace: F, valign: "middle", margin: [2, 10, 2, 10] });
}

// =====================================================================
// 15. K. Despliegue
// =====================================================================
{
  const s = contenido("CRITERIO K", "Despliegue en la nube",
    "Criterio K. ~1 min. Presenta: Alejo.\nFront, API y base de datos desplegados en un servidor virtual (VPS) de Oracle Cloud con Ubuntu 24.04: PostgreSQL 16, gunicorn para los dos servidores Django, y Cloudflare Tunnel delante, que da el HTTPS. Dirección: https://admind.detkor.com (sin www).\nDespliegue continuo: un merge a main dispara un webhook de GitHub (firmado con HMAC); el servidor lo encola y corre el script de despliegue (pull, dependencias, migraciones, reinicio con systemd). El 22-nov quedó igual a main (back b4d5c7c, front a0feaf4), con CORS y Swagger.\nLos secretos y la configuración de producción no están en el repositorio: el .env del back (con CORS_ALLOWED_ORIGINS=https://admind.detkor.com) y los ajustes de producción en /etc/admind/ (DEBUG=False, ALLOWED_HOSTS).\nLa API no tiene dominio propio: escucha solo en 127.0.0.1:8000 y la usa el servidor del front, dentro del VPS.\nPara que el profe la pruebe: el QR en pantalla y el mismo enlace por Teams. Cuentas demo de Residente y Vigilancia, que no piden segundo factor; los otros roles los muestra el equipo.\nTener abiertos por si los pide: systemctl status de los servicios y la instancia en la consola de Oracle.");
  bullets(s, [
    ["Todo en la nube:", "front, API y base de datos, en un servidor de Oracle Cloud"],
    ["Dirección:", "https://admind.detkor.com, con HTTPS por Cloudflare"],
    ["Despliegue continuo:", "cada merge a main se despliega solo"],
    ["Para el docente:", "QR en pantalla, el enlace por Teams y cuentas demo de Residente y Vigilancia"],
  ], { x: X, y: 1.7, w: 7.3, h: 2.6, fontSize: 16 });
  const bg = 0.3, bw = (7.3 - 4 * bg) / 5, y = 4.55;
  [["Navegador", false], ["Cloudflare HTTPS", false], ["Front gunicorn", true], ["API gunicorn", true], ["PostgreSQL 16", true]].forEach((p, i) => {
    caja(s, X + i * (bw + bg), y, bw, 0.9, p[0], p[1], 13);
    if (i < 4) flecha(s, X + i * (bw + bg) + bw, y + 0.25, bg);
  });
  s.addText("VPS de Oracle Cloud · Ubuntu 24.04", { x: X + 2 * (bw + bg), y: 5.55, w: 7.3 - 2 * (bw + bg), h: 0.3, fontSize: 12, color: GRIS, align: "center", fontFace: F, margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.roundRect, { x: 8.55, y: 1.7, w: 4.18, h: 4.6, rectRadius: 0.1, fill: { color: V50 }, line: { color: V50, width: 0 } });
  s.addImage({ path: R.qr, x: 8.99, y: 1.95, w: 3.3, h: 3.37, altText: "Código QR a https://admind.detkor.com" });
  s.addText("admind.detkor.com", { x: 8.55, y: 5.55, w: 4.18, h: 0.5, fontSize: 22, bold: true, color: V700, align: "center", fontFace: F, margin: 0, isTextBox: true });
}

// =====================================================================
// 16. Cierre
// =====================================================================
{
  const s = pres.addSlide({ masterName: "OSCURO" });
  s.addText("Demostración en vivo", { x: 0.9, y: 0.8, w: 11.5, h: 0.9, fontSize: 38, bold: true, color: "FFFFFF", fontFace: F, margin: 0, isTextBox: true });
  const pasos = [
    "Escanear el QR: https://admind.detkor.com",
    "Entrar con Residente y con Vigilancia",
    "Intentar romperla: la URL, el botón Atrás, pantallas de otro rol",
    "Descargar los reportes y ver el correo",
    "Evidencias: Actions, SonarCloud y cobertura",
  ];
  pasos.forEach((p, i) => {
    const y = 2.0 + i * 0.85;
    s.addText(String(i + 1), { x: 0.9, y, w: 0.6, h: 0.6, shape: pres.ShapeType.ellipse, fill: { color: V600 }, color: "FFFFFF", bold: true, fontSize: 18, align: "center", valign: "middle", fontFace: F, margin: 0 });
    s.addText(p, { x: 1.75, y, w: 7.0, h: 0.6, fontSize: 18, color: "FFFFFF", fontFace: F, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addShape(pres.ShapeType.roundRect, { x: 9.3, y: 1.95, w: 3.1, h: 3.1, rectRadius: 0.15, fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 } });
  s.addImage({ path: R.qr, x: 9.5, y: 2.12, w: 2.7, h: 2.76, altText: "Código QR a https://admind.detkor.com" });
  s.addText("¿Preguntas?", { x: 8.9, y: 5.3, w: 3.9, h: 0.8, fontSize: 36, bold: true, color: "FFFFFF", fontFace: F, margin: 0, align: "center", isTextBox: true });
  s.addText("Gracias", { x: 8.9, y: 6.05, w: 3.9, h: 0.5, fontSize: 20, color: "CFE5DD", fontFace: F, margin: 0, align: "center", isTextBox: true });
  s.addNotes("Cierre y demostración. ~3 min más preguntas. Presentan los dos: Alejo maneja el QR, la nube y las evidencias (Actions, SonarCloud, VPS); Camilo hace el intento de romper la app y, si lo piden, muestra Swagger por el túnel.\nGuion de la demo en este orden: QR → entrar con Residente y Vigilancia → intentar romperla (URL de Administración con sesión de Residente: 403; Atrás después de Salir: vuelve al ingreso; URL inventada: 404 propio) → descargar los reportes con Administración desde el celular del equipo → abrir el correo en Gmail → evidencias.\nPlan B si falla la red o el servidor: las capturas de esta presentación y del Manual de Usuario.\nTener abiertas de antemano: Actions de los dos repos, SonarCloud (Activity) de los dos, el reporte de cobertura y el Manual Técnico (anexo de rutas).\nSi preguntan por lo que falta: JWT no se implementó (ver las notas de la diapositiva 8). CORS y Swagger sí, desde el 22-nov.");
}

pres.writeFile({ fileName: OUT }).then((f) => console.log("OK " + f));
