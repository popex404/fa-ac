# Plan — Landing de venta de Termitas

**Estado:** esqueleto completo y construido, ajustado con lo que salió de la
llamada de revisión con Francisco (FA) — "Fase 1 Revisiones", transcrita en
`C:\Users\Popex404\Downloads\Fase 1 Revisiones.mp4-es-asr.vtt` (referenciada
acá para no releerla). Deadline seguía siendo viernes 2026-07-31 la última vez
que se habló de fecha. Todo pusheado a GitHub (commit `71424e2`, 2026-07-30,
con confirmación explícita de Javier) — incluye la auditoría SEO técnica y
todos los ajustes de esta sesión (ver "Hecho esta sesión").

**Dónde está todo:**
- Landing: `web/servicios/exterminio-y-fumigacion-de-plagas-de-termitas/index.html`
- Cotizador especializado: `web/js/cotizador-termitas.js` (separado del genérico
  `js/cotizador.js` a propósito, para que futuras plagas tengan el suyo sin pisarse)
- Partials de contenido: `generador/_partials/{trust-bar,clientes,mecanismo,
  proof-counters,para-quien,value-stack,garantia,cobertura,contacto-final,
  cotizador-embed}.html` — aplicados solo a páginas de `servicios/` vía
  `SERVICE_PARTIAL_NAMES` en `build.py` (no a home/blog)
- Video hero: `web/img/hero-video/termitas-hero.mp4` (400×718, 16s completos,
  las 3 escenas: termita asomándose en la madera, técnico aplicando el
  tratamiento, inyección terminando en la espuma) + poster — **video
  definitivo**, ya no es el placeholder de prueba. Fuente HD exportada por
  Javier desde CapCut, comprimida a ~1MB para carga rápida en mobile. Mismo
  filtro oscuro (video a 55% opacidad + overlay parejo `rgba(8,8,8,.45)`,
  estilo liniero.cl) en mobile y desktop — ver "Hecho esta sesión".

---

## Pendiente — orden de prioridad que Javier le dio a FA en la llamada
(textual: *"le voy a dar prioridad al formulario [cotizador], también a la
sección de las provincias [cobertura], y después al final ya el giro [video
del hero]"*)

### 1. Cotizador — HECHO, testeado end-to-end contra el Sheet (2026-07-31)
El flujo (Indicios → Inmueble → Tamaño → Urgencia → Contacto) coincide con lo
acordado con FA. El botón flotante de WhatsApp ya quedó resuelto (ver
"Hecho esta sesión" abajo).

**Testeo completo — 3 problemas encontrados y resueltos, ver "Hecho esta
sesión (2026-07-31)" para el detalle técnico:**
1. Tracking de origen ampliado: `source` = página (`landing-principal` /
   `landing-termitas`), `cta` = botón exacto (`Seccion-Cotizador` /
   `Boton-Hero` / `Boton-Menu`), `indicio` con default `N/A` en el
   cotizador genérico.
2. Bug propio (introducido y corregido en la misma sesión): IDs de campos
   del formulario de contacto quedaron referenciando una variable que ya
   no existía tras el refactor de arriba.
3. **Causa real de por qué el Sheet llegaba desfasado:** el Apps Script
   tenía 4 implementaciones distintas (cada una con su propia URL) y
   `WEBHOOK_URL` en el sitio apuntaba a una vieja — Javier actualizó el
   código del Apps Script pero seguía "implementando" en URLs nuevas en
   vez de editar la implementación existente. Se corrigió actualizando
   `WEBHOOK_URL` en `cotizador.js` y `cotizador-termitas.js` a la URL de
   la implementación viva. Confirmado por Javier: **funciona**.

Dato de FA para el copy (no es tarea, es conocimiento técnico útil si más
adelante se quiere un mensaje contextual por indicio): gránulos café →
termita de madera seca; túneles de barro → termita subterránea; alitas/vuelo
distingue especie según la época del año.

### 2. Cobertura — mapa interactivo terminado (provincia + comuna), falta expandir a otras páginas
**Mapa interactivo — HECHO, incluyendo selección por comuna.** Se construyó un
mapa SVG real de las 7 provincias (con sus comunas) de la Región de
Valparaíso, sincronizado en ambos sentidos con los botones (clic en botón
resalta en el mapa, clic en el mapa resalta el botón y actualiza el listado
de comunas) **y ahora también a nivel de comuna individual**: clic en una
comuna del listado o directo en su trazo del mapa la pinta de naranjo
(`var(--primary)`) mientras la provincia se queda en verde, en vez de solo
resaltar toda la provincia. Fuente de los límites geográficos: dataset
público `jlhonora/geo` en GitHub (basado en datos DPA de la Biblioteca del
Congreso Nacional), simplificado con `shapely` para uso decorativo. Layout
desktop: provincias + comunas a la izquierda, mapa a la derecha (según lo
acordado con FA); en mobile el mapa va primero (después del subtítulo de la
sección, antes del listado). Isla de Pascua y Juan Fernández quedan fuera del
mapa visual (son parte de la Región/provincia de Valparaíso
administrativamente, pero son islas muy alejadas del continente — incluirlas
rompería la escala del mapa; Juan Fernández se marca con ❌ en el listado, sin
check verde, y no es clickeable).

**Sigue pendiente:**
- **Agregarla también a la home** (`web/index.html`). FA fue explícito: *"la
  idea es que esté en los dos lados porque es una sección que nos faltó y que
  nos ayuda para el SEO."* Hoy `cobertura.html` solo se aplica en páginas de
  `servicios/` vía `SERVICE_PARTIAL_NAMES`, no en home.

### 3. Hero video — HECHO, video definitivo instalado
Ya no es el placeholder de prueba. Javier grabó/editó el video final (3
escenas: termita asomándose, técnico aplicando el tratamiento, inyección
terminando en la espuma — el punto que FA quería que se viera), lo exportó en
alta calidad desde CapCut y quedó comprimido a ~1MB para no afectar la carga
en mobile. El enfoque pantalla-completa + overlay que ya estaba montado se
mantuvo (confirmado con FA, no era una contradicción real). Se agregó además
un filtro oscuro parejo (video a 55% opacidad + overlay `rgba(8,8,8,.45)`,
inspirado en liniero.cl) en mobile y desktop, reemplazando el degradado de
color naranjo/verde saturado que había antes.

**Sigue pendiente: aprobación de FA.** Técnicamente listo, falta que Francisco
lo vea y confirme.

### 4. Sección "4 síntomas de termita" (`#pain-points`) — HECHO, formato final con fotos reales
Ya no es la prueba de 4 variantes. Javier decidió el formato ganador (botón
"Ver foto real" arriba a la derecha de cada tarjeta + popup modal blanco) y
consiguió las 4 fotos reales de AyC (gránulos, alitas, madera hueca, túneles
de barro) — sin pendientes de FA en esta sección. Detalle en "Hecho esta
sesión".

---

## Hecho esta sesión (2026-07-31)

- **Cotizador testeado y funcionando de punta a punta contra el Google
  Sheet** — ver detalle en "1. Cotizador" arriba. Cambios técnicos:
  - `cotizador.js` y `cotizador-termitas.js`: nuevo campo `source` (slug
    fijo de la página, ej. `landing-principal`/`landing-termitas`) y
    nuevo campo `cta` (dinámico, según qué botón abrió el cotizador:
    `Seccion-Cotizador`, `Boton-Hero`, `Boton-Menu`). El viejo campo
    `source` (que mezclaba página+instancia) se separó en estos dos.
  - `indicio` con default `'N/A'` en el cotizador genérico (home), ya que
    ese flujo no pregunta indicio (solo Termitas lo hace).
  - HTML: `data-cta="Boton-Menu"` en `generador/_partials/header.html`
    (botón del menú móvil, aplica a las 11 páginas), `data-cta="Boton-Hero"`
    en el botón del hero de home y de la landing de Termitas,
    `data-cta="Seccion-Cotizador"` en ambos widgets embebidos. Se sacaron
    los `data-source` viejos.
  - `WEBHOOK_URL` actualizado en ambos JS a la implementación de Apps
    Script realmente activa (Javier tenía 4 implementaciones distintas del
    mismo proyecto, cada una con su propia URL — el sitio apuntaba a una
    vieja, por eso los datos llegaban desfasados de columna).
  - Apps Script (fuera de este repo, lo mantiene Javier): `doPost` ahora
    inserta `indicio` entre `plaga`/`propiedad` y `cta` entre
    `source`/`telefono` en el Sheet.
- **Auditoría SEO de las 11 páginas (título/meta/og, alt, width/height,
  CTAs) + fixes aplicados:**
  - `width`/`height` agregado a las ~97 imágenes del sitio que no lo
    tenían (dimensiones reales leídas de cada archivo). De paso se
    corrigieron 2 casos con `width`/`height` ya presente pero equivocado:
    logo del header (decía 160×60, el archivo real es 1135×1135) y logo
    SEREMI del footer (no tenía). Ambos en los partials compartidos, se
    propagan solos vía `build.py`.
  - `alt` descriptivo en 10 imágenes que tenían texto genérico (8 íconos
    de la grilla de servicios en home + 2 fotos de especie en la landing
    de Termitas).
  - `og:title`/`og:description`/`og:type`/`og:url`/`og:image` agregado a
    los 9 blog (antes solo home y la landing de Termitas los tenían) —
    mismo texto que su `<title>`/meta description existente, sin
    redacción nueva.
  - 3 CTAs de la landing de Termitas (value-stack, contacto final,
    footer) que mandaban el mensaje genérico de plagas ahora mandan uno
    de termitas propio y distinguible (mismo patrón "(menú)" que ya usaba
    el botón del header) — token nuevo en `SERVICIOS` (`build.py`).
  - Todo el detalle, con antes/después de cada texto tocado (para revisar
    con Francisco), en `FA/fa-ac/referencia-ctas-y-previews.md` — nuevo
    archivo, listado de CTAs + mensajes de WhatsApp + preview de cada
    página, pensado para no tener que releer el HTML cada vez.

---

## Hecho esta sesión (2026-07-30)

- **Título/preview del sitio corregido.** `<title>` y `og:title` decían
  "Exterminio de Plagas de Termitas en Valparaíso | Certificado SEREMI — A&C
  Soluciones" — cambiado a "A&C: Exterminio, Fumigación y Control de Plagas
  de Termitas en Valparaíso, V Región". Revisar el mismo tipo de texto en el
  resto de páginas queda pendiente en `FA-roadmap.md` (no es solo un tema de
  esta landing).
- **Pain-points ("¿Reconoces alguna de estas señales de termitas?") con
  formato final y fotos reales.** Se probaron 4 variantes de botón+popup
  ("Ver foto real"); Javier decidió el formato ganador: botón chip arriba a
  la derecha de cada tarjeta + popup modal blanco clásico (antes variante
  1, misma posición que ya tenía esa variante). Las 4 tarjetas quedaron
  iguales entre sí (se sacó la A/B de formato),
  con fotos reales de AyC en vez del placeholder compartido
  (`control-de-termitas.jpeg`) — ahora cada una tiene la suya en
  `web/img/pain-points/`: `termitas-madera-hueca.avif`, `termitas-alitas.avif`,
  `termitas-granulos.avif`, `termitas-tuneles-barro.avif`. La tarjeta de
  "túneles de barro" quedó con el botón en verde/blanco (`--secondary`) a
  modo de comparación de color contra el default blanco/naranjo de las otras
  3. Se limpiaron el CSS y el JS de las 3 variantes descartadas (V2 lightbox
  oscuro, V3 `<dialog>` nativo, V4 modal con CTA WhatsApp) y se sacó la nota
  "PRUEBA para decidir formato con Francisco".
- **Reordenadas 2 secciones**, a pedido de Javier: "¿Cuánto cuesta solucionar
  tu problema de termitas?" (cotizador) y "Cobertura en la Región de
  Valparaíso" ahora van justo después de pain-points, antes de
  "Especialistas en las dos especies..." — quedaron más arriba en la página.
  Orden nuevo: hero → trust-bar → clientes → pain-points → **cotizador** →
  **cobertura** → especialistas → método de tratamiento → mecanismo → proof
  → para-quién → value-stack → urgencia → garantía → FAQ → contacto.
- **Colores del mapa de Cobertura invertidos.** La Región de Valparaíso (las
  7 provincias interactivas) ahora usa el gris que antes tenían la IV Región
  y la Región Metropolitana de contexto (`#d9d9d9`); esas 2 regiones de
  contexto pasan a usar el blanco/verde muy pálido que antes tenía
  Valparaíso (`var(--bg-light-green)`). Cambio en `web/css/styles.css`,
  aplica a cualquier página que use la sección Cobertura.
- **Cotizador de Termitas: sacada la opción "No sé / Otro"** del paso "¿Qué
  señal notaste?" — quedan solo las 4 señales concretas (madera hueca,
  alitas, gránulos, túneles de barro).
- **Texto sacado de "Todo lo que incluye nuestro servicio":** "Otras
  empresas te cobran 3 sesiones a $120.000 cada una. Nosotros resolvemos en
  una, con garantía." — en `generador/_partials/value-stack.html`, aplica a
  cualquier página de servicio (hoy solo Termitas).
- **Sacado "Erradicación térmica"** del Método de Tratamiento, en la landing
  de Termitas **y** en `web/blog/termitas/index.html` (FA: *"se tiene que
  eliminar de los dos lados"*).
- **Garantía de Termitas = 1 año** (no 14 días) — pero **solo en esta
  landing**, no tocamos el default del resto del sitio. Se resolvió con un
  patrón parametrizable pensado para escalar (ver abajo "Arquitectura para
  futuras páginas"): `GARANTIA_DIAS` / `GARANTIA_PERIODO` son tokens con
  default "14 días" en `SERVICIO_CTX`, y la landing de Termitas los
  sobreescribe vía un diccionario de overrides en `SERVICIOS` (`build.py`).
  Afecta value-stack, la sección Garantía, meta description, og:description,
  el FAQ y su JSON-LD — los 8 lugares donde aparecía "14 días" en esta página
  quedaron en "1 año"; el resto del sitio (home, blog, futuras plagas) sigue
  con 14 días por default.
- **Botón flotante de WhatsApp con mensaje propio.** FA pidió que el botón
  flotante (`#whatsapp-fab`) y el "Agenda gratis" del header dijeran algo de
  termitas en esta landing, distinto al del hero, para poder diferenciar por
  cuál botón entra cada lead. Nuevo token `{{WA_HEADER_TEXT}}` en
  `header.html`: default = mensaje genérico de siempre (home/blog sin
  cambios, verificado con `git diff` que quedaron byte-idénticos), y en
  `SERVICIO_CTX` un mensaje de termitas con "(menú)" agregado para
  diferenciarlo del mensaje del hero.
- **Investigué el reporte de que el header de la landing de Termitas navega
  a otra página en vez de scrollear** (FAQ, Garantía). Revisé el HTML
  generado y el JS (`main.js`, smooth-scroll): los links son anchors locales
  (`href="#faq"`, `href="#garantia"`, etc.), y un anchor local no puede
  navegar a otra página por diseño del navegador — estructuralmente no
  debería pasar. No pude reproducirlo. Posible explicación: si lo probaste
  en el link de GitHub Pages, ese es de un push anterior a varios cambios de
  esta sesión (aunque el fix de anchors locales ya estaba desde el primer
  build). Si lo ves de nuevo, dime en qué página exacta, qué link, y
  desktop o mobile, para poder reproducirlo.
- **Fix "Llaillay" → "Llay-Llay"** en el listado de comunas de San Felipe de
  Aconcagua (nombre oficial correcto), y **emoji de Juan Fernández** cambiado
  de una cruz gris/negra (`✗`) a ❌.
- **Mapa: clic en comuna, no solo en provincia.** Antes clic en el mapa solo
  resaltaba toda la provincia; ahora clic en el trazo de una comuna específica
  (o en su nombre en el listado) la selecciona igual en ambos lugares.
- **Layout del hero en mobile reordenado**, a pedido de Javier: "A&C Control
  de Plagas" pegado arriba (justo debajo del navbar), los 3 CTAs pegados
  abajo, y el título principal (h1) inmediatamente encima de los CTAs — antes
  los 3 elementos quedaban centrados como un solo bloque a media pantalla,
  tapando el video de fondo.
- **Filtro del hero (mobile y desktop) cambiado.** El degradado naranjo/verde
  saturado ("polarizado", palabras de Javier) se reemplazó por un
  oscurecido parejo sin tinte de color (video a 55% opacidad + overlay
  `rgba(8,8,8,.45)`), inspirado en cómo lo hace liniero.cl. Se aplicó primero
  solo en mobile y después, a pedido de Javier, también en desktop.
- **Bug de layout en el hero desktop, encontrado y corregido:** el `<video>`
  de escritorio estaba en flujo normal con `width/height:100%`, así que su
  propio aspect ratio (401×718, muy angosto y alto en la versión HD) se
  metía en el cálculo de alto de la fila del grid del hero y estiraba todo el
  bloque —video y columna de texto— a más de 1000px de alto. Se corrigió
  poniendo el video en `position:absolute` dentro de su contenedor (mismo
  patrón que ya se usaba en mobile), así el tamaño del contenedor ya no
  depende del aspect ratio del archivo de video que se use.
- **Video hero reemplazado dos veces**: primero por un recorte de 5s de un
  clip de prueba, después (a pedido de Javier, el video ya venía armado para
  mostrar 3 escenas completas) por el video completo de 16s, y finalmente por
  la versión HD exportada desde CapCut, comprimida a ~1MB. Ver sección "3.
  Hero video" arriba para el detalle.
- **Contenido recortado en 2 secciones**, a pedido de Javier: en
  "Especialistas en las dos especies..." se sacó el link "conoce el detalle
  técnico de cada especie" (apuntaba a `blog/termitas/`) y el párrafo ahora
  termina en "...antes de definir el tratamiento."; en "Método de
  Tratamiento" se sacó el subtítulo "Protocolos específicos según la especie
  y el nivel de infestación."

---

## Arquitectura para futuras páginas — propuesta, PENDIENTE DE DECISIÓN
(conversada el 2026-07-30, Javier todavía no decide, "necesito pensarlo")

**El problema que planteó Javier:** si a futuro se generan muchas páginas
(ej. 50 landings por comuna/provincia), hay que garantizar que (1) el
header/footer/CTAs de cada página copiada interactúen con esa misma página,
no con otra ni con el home; (2) los distintos CTAs de una página no "se
solapen" (mismo mensaje indistinguible entre sí); (3) el repo no se vuelva
ineficiente o caro de analizar a medida que crece.

**Separar 2 ejes, tienen soluciones distintas:**
- **Eje A — otras plagas** (landing de Ratones, Cucarachas, etc.): ya
  resuelto por el sistema actual. Cada plaga = carpeta nueva en `servicios/`
  + su propio cotizador JS + entrada en `SERVICIOS` con overrides (patrón
  usado en el fix de garantía de Termitas). No es un problema de escala,
  serían ~5-10 páginas en total.
- **Eje B — variantes geográficas de la misma plaga** (potencialmente 50+
  páginas: "Control de Termitas en Quillota", "...en Viña del Mar", etc.):
  este es el que preocupa a Javier, el sistema actual no está pensado para
  esta escala.

**Por qué el punto 1 (header/CTAs de cada copia apuntando a sí misma) ya
está resuelto de base:** el sistema `HOME_CTX` / `BLOG_CTX` / `SERVICIO_CTX`
+ tokens (`{{ROOT}}`, `{{HOME_ANCHOR}}`, `{{PLAGA_PREFIX}}`, etc.) existe
exactamente para esto — cada página se registra con su contexto y sus links
se generan apuntando a sí misma, no se rompe al copiar. El patrón de
`SERVICIOS` como lista de diccionarios con overrides por página (ver fix de
garantía) es el que resuelve el punto 2: cualquier valor que varíe por
página se agrega como token con default sensato, se sobreescribe por
página, sin tocar partials compartidos a mano.

**LA DECISIÓN ESTRATÉGICA QUE FALTA (bloquea el diseño técnico del eje B):**
¿las páginas por comuna van a ser **landings completas** (duplicar todo:
hero, pain-points, mecanismo, FAQ, etc., solo cambiando el nombre de la
comuna) o **páginas delgadas** (cortas, SEO local, embudan hacia el
cotizador y linkean de vuelta a esta landing completa para el detalle)?

Recomendación dada a Javier: páginas delgadas. Razón — no es solo técnica,
es de SEO real: 50 páginas casi idénticas de miles de palabras cada una,
donde solo cambia el nombre de la comuna, es el patrón que Google identifica
como contenido duplicado/delgado (puede penalizar en vez de ayudar). El
patrón que funciona: una página "ancla" (esta landing) que concentra toda la
autoridad/contenido largo + N páginas cortas y genuinamente distintas que
capturan la búsqueda local y embudan hacia el cotizador o hacia la landing
completa.

**Si se opta por páginas delgadas (plano técnico propuesto, sin construir
todavía):**
1. **Una plantilla, no N archivos.** `generador/templates/servicio-comuna.html`
   — un solo archivo mantenido a mano. Los outputs
   (`web/servicios/control-de-termitas-en-[comuna]/index.html`, etc.) se
   **generan completos** desde la plantilla, nunca se editan a mano — a
   diferencia del sistema de partials actual (que parchea archivos ya
   escritos), acá el archivo entero es desechable/regenerable.
2. **Un archivo de datos**, ej. `generador/data/comunas-termitas.json`: lista
   de `{comuna, provincia, slug, keywords locales, cualquier dato único}`.
   Un script recorre la lista y genera cada página reusando el mecanismo de
   tokens (`render()`) que ya existe.
3. **Contexto nuevo** (`COMUNA_CTX` o similar), misma profundidad que
   `SERVICIO_CTX`, pero con los anchors (`#faq`, `#garantia`, etc.)
   apuntando de vuelta a la landing completa de Termitas en vez de a
   secciones locales (estas páginas delgadas no tendrían esas secciones
   propias).
4. **Tracking por página vía `data-source`, no por mensaje distinto de
   WhatsApp.** Mismo mensaje que la landing principal, diferenciado por
   `data-source` (ej. `"comuna-quillota"`) que ya viaja al Sheet — sabes de
   qué comuna vino cada lead sin mantener N mensajes distintos a mano.
5. **Por qué esto mantiene el repo liviano de analizar:** cambios se hacen
   en la plantilla (un archivo) y se regeneran todas las páginas — se
   razona sobre plantilla + datos, no sobre N HTMLs casi iguales. El
   problema de "300 páginas estáticas" solo se materializa si cada una se
   mantiene a mano por separado; generadas, el costo no crece con la
   cantidad.

**Si se opta por landings completas:** el plano cambia — ahí sí conviene
reusar `SERVICIO_CTX` tal cual (páginas con sus propias secciones locales),
pero sigue siendo necesario el enfoque plantilla+datos para no mantener N
archivos a mano, y hay que aceptar el riesgo de SEO de contenido
duplicado/delgado (mitigable con contenido único real por comuna, que es
más trabajo de copy).

**No se ha construido nada de esto.** Es diseño para cuando Javier decida
el punto estratégico de arriba.

---

## Ya hecho y confirmado por FA en la llamada (no volver a tocar)

- Header: "Servicios"→"Plagas" + nuevo "Servicios"→landing de Termitas. FA lo
  revisó en vivo, no pidió cambios.
- FAQ "exterminio vs. control": FA confirmó que el concepto técnico correcto
  es "control"/"manejo" (MIP) — nunca "exterminio" (riesgo legal si se
  promete 100%, las colonias pueden volver). "Exterminio"/"fumigación" solo
  deben aparecer en el FAQ para SEO, nunca como promesa del resto de la
  página.
- Título "Especialistas en las dos especies... más destructivas" con rojo —
  FA confirmó que hay 5 especies de termita en la región y estas 2 son las
  más dañinas (de ahí el "más destructivas").
- Wording del sistema de cebado ("...para detección de termitas
  subterráneas") ya corregido en landing y blog.
- Pretitle del hero = "A&C Control de Plagas".
- Popup "Ver foto real" (4 variantes) — la idea nació en esta misma llamada
  (Javier proponiéndole a FA un botón interactivo en vez del emoji).
- Testimonios: FA está de acuerdo en dejar el único testimonio de termitas
  por ahora; reseñas reales vendrán después con incentivo (descuento por
  reseña) — no es urgente.
- Preocupación de Javier sobre "páginas estáticas" (números fijos en
  Credenciales, etc.): FA dijo explícitamente que no había que preocuparse,
  está bien así (distinto del tema de escalabilidad de arriba, que sí es una
  preocupación vigente de Javier).
- Video hero pantalla-completa + overlay en mobile: confirmado, no es una
  contradicción real.

---

## Ideas mencionadas, no urgentes (quedan anotadas para más adelante)

- Mensaje contextual/explicativo en el cotizador según el indicio elegido.
- Reseñas reales vía incentivo de descuento (más adelante, con campaña).

---

## Referencia técnica (vigente)

- `generador/build.py`: `SERVICIO_CTX`, `SERVICE_PARTIAL_NAMES`,
  `SERVICIOS = [{"slug": ..., overrides...}]` — patrón de overrides por
  página para valores que varían (garantía, mensajes de WhatsApp). También
  `sync_business_jsonld()` (tipo/dirección/areaServed del JSON-LD) y
  `write_seo_files()` (robots.txt/sitemap.xml) — detalle en
  `generador/README.md`.
- `generador/_partials/`: partials de contenido reusables (ver arriba)
- `web/js/cotizador-termitas.js`: cotizador especializado, separado del genérico
- Testing local: `python build.py` desde `generador/`, luego
  `python -m http.server` desde `web/`
- No pushear a GitHub sin confirmación explícita de Javier
