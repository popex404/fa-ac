# Referencia — CTAs, mensajes de WhatsApp y preview de cada página

Generado a partir de una auditoría de las 11 páginas del sitio (2026-07-31). Sirve para
tener en un solo lugar: (1) cómo se ve cada página en la pestaña del navegador y al
compartir el link (buscadores, WhatsApp, redes), y (2) qué botones de contacto tiene
cada página y qué mensaje de WhatsApp manda cada uno por defecto.

No es contenido fuente — el contenido real vive en cada `.html` (y en `generador/_partials/`
para lo compartido). Si cambia algo ahí, esta tabla queda desactualizada hasta la próxima
auditoría manual.

---

## Dónde está todo / referencia técnica

Movido acá desde `plan-landing-termitas.md` (eliminado 2026-08-04) — vigente para
Termitas y como plantilla para los servicios de `plan-fase-2.md`.

- Landing: `web/servicios/exterminio-y-fumigacion-de-plagas-de-termitas/index.html`
- Cotizador especializado: `web/js/cotizador-termitas.js` (separado del
  genérico `js/cotizador.js` a propósito, para que futuras plagas tengan el
  suyo sin pisarse)
- Partials de contenido reusables para futuras páginas de servicio:
  `generador/_partials/{trust-bar,clientes,mecanismo,proof-counters,
  para-quien,value-stack,garantia,cobertura,contacto-final,
  cotizador-embed}.html`, aplicados vía `SERVICE_PARTIAL_NAMES` en `build.py`
- `generador/build.py`: `SERVICIO_CTX`, `SERVICE_PARTIAL_NAMES`,
  `SERVICIOS = [{"slug": ..., overrides...}]` — patrón de overrides por
  página para valores que varían (garantía, mensajes de WhatsApp por cada
  CTA). También `sync_business_jsonld()` (tipo/dirección/areaServed/name del
  JSON-LD) y `write_seo_files()` (robots.txt/sitemap.xml) — detalle en
  `generador/README.md`.
- `web/js/cotizador-termitas.js` / `web/js/cotizador.js`: cotizadores
  separados por plaga; tracking de `source` (página) + `cta` (botón exacto:
  sección, hero o menú) + `indicio`, mandan a un Apps Script vía
  `WEBHOOK_URL`.
- Testing local: `python build.py` desde `generador/`, luego
  `python -m http.server` desde `web/`.
- No pushear a GitHub sin confirmación explícita de Javier.

---

## Fase 2 — 5 landings nuevas (2026-08-04)

Mismo patrón que Termitas: partial + override propio en `SERVICIOS` de
`generador/build.py`. Detalle de negocio/roadmap → `plan-fase-2.md`. Acá
solo lo técnico.

| Servicio | Slug (`web/servicios/`) | Cotizador | Fuente de contenido |
|---|---|---|---|
| Desratización | `exterminio-y-fumigacion-de-plagas-de-ratones` | `js/cotizador-ratones.js` | `blog/ratones` (guarén, rata negra, laucha) |
| Predemolición | `exterminio-y-fumigacion-de-plagas-de-predemolicion` | `js/cotizador-predemolicion.js` | Sin blog fuente — redactado con criterio general |
| Desinsectación | `exterminio-y-fumigacion-de-plagas-de-desinsectacion` | `js/cotizador-desinsectacion.js` | `blog/aranas` + `blog/avispas` + `blog/hormigas` (chinches no entra) |
| Sanitización | `exterminio-y-fumigacion-de-plagas-de-sanitizacion` | `js/cotizador-sanitizacion.js` | Sin blog fuente — redactado con criterio general |
| Control de Palomas | `exterminio-y-fumigacion-de-plagas-de-palomas` | `js/cotizador-palomas.js` | `blog/palomas` (paloma doméstica, única especie) |

### Cotizadores nuevos

5 archivos nuevos en `web/js/`, cada uno clon de `cotizador-termitas.js`
(mismo patrón: salta la pregunta "qué plaga tienes" porque la página ya es
de esa plaga/servicio, pregunta directo la señal/necesidad detectada). Cada
uno tiene su propio `PAGE_SLUG` (`landing-ratones`, `landing-predemolicion`,
`landing-desinsectacion`, `landing-sanitizacion`, `landing-palomas`) para
que el Sheet distinga el origen del lead. Los 5 resultan siempre en la rama
"visita técnica" (sin cálculo de precio online), igual que Termitas — no
como el `cotizador.js` genérico del home, que sí calcula precio para
algunas plagas. Si más adelante Francisco quiere precio fijo para
Sanitización (el genérico ya tiene `PRECIOS_BASE.sanitizacion = 100000`),
es un cambio acotado a `cotizador-sanitizacion.js`.

### `SERVICIOS` en `build.py` — bug corregido de paso

`WA_HEADER_TEXT` no estaba en el diccionario de Termitas — dependía del
default de `SERVICIO_CTX`, que está hardcodeado a "...plaga de termitas".
Antes de esta fase eso no se notaba porque Termitas era el único servicio.
Con 6 servicios ya habría sido un bug visible (el botón del header de
Ratones diciendo "termitas"). Se corrigió agregando `WA_HEADER_TEXT`
explícito a las 6 entradas de `SERVICIOS` (incluida Termitas).

### `header.html` — dropdown "Servicios"

Antes apuntaba directo a la landing de Termitas (único servicio que
existía). Ahora lista los 6 en el orden que pidió Javier (Termitas,
Desratización, Predemolición, Desinsectación, Sanitización, Palomas) y el
trigger del dropdown apunta a `{{SERVICIOS_GRID_ANCHOR}}` (la grilla de
"Nuestros Servicios" del home), mismo patrón que ya usaba el dropdown
"Plagas".

### Decisiones de contenido (para que Javier las revise/ajuste)

- **Hero con video**: las 5 páginas nuevas reusan el video de Termitas
  (`img/hero-video/termitas-hero.mp4` + poster) a pedido de Javier, solo
  para probar dimensiones/layout del hero. Cada `<video>` tiene un
  comentario `<!-- TODO: video placeholder de Termitas -->` — reemplazar el
  `src` cuando exista contenido propio por servicio.
- **Sección "especies"**: se adaptó el layout según cuántas especies tiene
  cada servicio — 3 para Ratones (grilla), 3 "plagas" para Desinsectación
  (no 7 especies individuales — se agrupó por plaga: arañas/avispas/hormigas,
  cada una linkeando a su blog), 1 para Palomas (foto+texto simple).
  Predemolición y Sanitización no tienen especies — esa sección se
  reemplazó por una lista de "qué incluye el servicio".
- **"Ver foto real" en pain-points**: no se replicó en ninguna de las 5
  páginas nuevas. Termitas tiene fotos reales de evidencia
  (`img/pain-points/termitas-*.avif`) que no existen para el resto de las
  plagas — en vez de inventar o reusar fotos que no calzan con el texto,
  se dejaron las tarjetas de pain-points sin el botón/popup. El mecanismo
  (CSS/JS) sigue disponible tal cual si Francisco consigue fotos reales.
- **Testimonios**: cada página nueva tiene un testimonio genérico de
  ejemplo (mismo formato que el de Termitas: "Agrícola Los Naranjos"),
  marcado con `<!-- TODO: reemplazar por un testimonio real, revisar con
  Francisco -->`. No son reseñas reales de clientes.
- **Predemolición y Sanitización — sin blog fuente**: todo el copy (pain
  points, protocolo, FAQ) se redactó con criterio general de la industria,
  no viene de contenido ya validado por Francisco. Quedaron 2 FAQ con
  comentario `<!-- TODO -->` pidiendo específicamente confirmar el marco
  legal/normativo (si la inspección de predemolición es obligatoria, y en
  qué rubros aplica la sanitización DS 157/05) — son las dos afirmaciones
  más sensibles a estar mal si no se revisan.
- **`especialistas-crosslink`**: cada landing nueva linkea de vuelta a su
  blog fuente en la sección de especies (mismo lugar que Termitas). Blogs →
  landing: banner naranja agregado en `blog/ratones`, `blog/palomas`,
  `blog/aranas`, `blog/avispas`, `blog/hormigas` (estos 3 últimos apuntan
  todos a la landing de Desinsectación).

---

## Palabras clave SEO en consideración (de `meta name="keywords"` de cada página)

Esto es lo que ya está escrito en el `<meta name="keywords">` de cada página — no son
keywords nuevas que yo esté "decidiendo", son las que ya persigue el sitio hoy. Las uso
como referencia para que el `alt` de las imágenes hable el mismo idioma que el resto de la
página (mismo criterio que usaste para pedir "control de plagas de cucarachas" en vez de
"control de cucarachas"). Si cambias las keywords de una página, esta lista queda
desactualizada — no se regenera sola.

| Página | Keywords actuales |
|---|---|
| Home | control de plagas Valparaíso/Viña del Mar/Quilpué, fumigación, desinsectación, desratización, sanitización, manejo integrado de plagas (MIP), SEREMI DS 157/05, control plagas Quinta Región |
| Arañas | control arañas Valparaíso, araña de rincón, *Loxosceles laeta*, fumigación/desinsectación arañas, control plagas arañas SEREMI |
| Avispas | control avispas Valparaíso, eliminar nido avispas, chaqueta amarilla, *Vespula germanica*, avispa papelera, emergencia avispas 24 horas |
| Chinches | chinches de cama Valparaíso, *Cimex lectularius*, tratamiento térmico chinches, chinches cama hotel |
| Cucarachas | eliminar/fumigación cucarachas Valparaíso, cucaracha alemana/oriental, gel insecticida cucarachas, cucarachas restaurante SEREMI |
| Hormigas | control hormigas Valparaíso, hormiga argentina/negra, cebo hormigas, hormigas en casa/cocina |
| Mosquitos | control mosquitos Valparaíso, *Culex*, *Aedes aegypti*, nebulización/larvicida mosquitos, mosquito tigre |
| Palomas | control palomas Valparaíso, antiposada, mallas antipalomas, guano, *Columba livia*, histoplasmosis |
| Ratones | control roedores Valparaíso, desratización, guarén, laucha, rata negra, hantavirus/leptospirosis, estaciones de cebado |
| Termitas (blog) | control termitas Chile, termita madera seca/subterránea, *Cryptotermes brevis*, *Reticulitermes flavipes*, informe técnico termitas |
| Landing Termitas | control de termitas, plaga/problema de termitas, tratamiento/fumigación/exterminio de termitas, diagnóstico gratuito termitas, certificado SEREMI |

---

## 0. Cambios de `alt` aplicados (2026-07-31) — para revisar con FA

Parte de la limpieza SEO pendiente (`alt` descriptivo en imágenes). Estos 10 ya están
aplicados en el HTML — se documentan acá porque son texto que no se ve en la página (solo
en el código/lectores de pantalla/buscadores), así que es fácil que a Javier se le olvide
qué decía antes. **Si Francisco pide otra redacción, se edita esta tabla y se le pide a
Claude que la lleve a la página correspondiente** (no hace falta que Javier edite el HTML
a mano).

| Página | Imagen | Alt original | Alt actual |
|---|---|---|---|
| Home | `img/arana.png` (ícono grilla servicios) | "Araña" | "Icono de control de plagas de arañas" |
| Home | `img/avispa.png` | "Avispa" | "Icono de control de plagas de avispas" |
| Home | `img/cucaracha.png` | "Cucaracha" | "Icono de control de plagas de cucarachas" |
| Home | `img/rata.png` | "Roedor" | "Icono de control de plagas de roedores (ratones y ratas)" |
| Home | `img/hormiga.png` | "Hormiga" | "Icono de control de plagas de hormigas" |
| Home | `img/mosquito.png` | "Mosquito" | "Icono de control de plagas de mosquitos" |
| Home | `img/paloma.png` | "Paloma" | "Icono de control de plagas de palomas" |
| Home | `img/termitas-soldado.png` | "Termita" | "Icono de control de plagas de termitas" |
| Landing Termitas | `img/maderaseca-scaled.png` | "Termita de Madera Seca" | "Termita de madera seca (Cryptotermes brevis)" |
| Landing Termitas | `img/Termita-subterranea-03.jpg` | "Termita Subterránea" | "Termita subterránea (Reticulitermes flavipes)" |

**2026-07-31, 2do ajuste:** los 8 íconos de home pasaron de "Icono de control de X" a
"Icono de control de plagas de X" — pediste ese patrón exacto para que calce con las
keywords reales del sitio (ver sección de arriba). Aplica el mismo criterio a futuro si
agregas íconos nuevos (ej. una plaga nueva).

Las 9 páginas de blog ya tenían alt descriptivo bueno en sus fotos de especie (con nombre
científico) — no se tocaron.

## 0.1 `width`/`height` — hecho (2026-07-31), sin decisiones de contenido

Se agregó `width`/`height` a las ~97 imágenes del sitio que no lo tenían (dimensiones
reales del archivo, leídas directo del PNG/JPG/WebP/AVIF/SVG — esto es puramente técnico,
no cambia nada visible, previene que la página "salte" mientras cargan las imágenes).

De paso se encontraron y corrigieron 2 casos donde el `width`/`height` **ya existía pero no
coincidía con el archivo real** (bug preexistente, no relacionado con este pendiente):
- Logo del header (`img/LOGO-01.jpg`): decía 160×60, el archivo real es 1135×1135 (cuadrado).
  Corregido en `generador/_partials/header.html` (un solo lugar, se propaga a las 11 páginas).
- Logo SEREMI del footer (`img/seremi-salud.png`): no tenía `width`/`height`. Agregado
  (300×300), en `generador/_partials/footer.html`.

En ambos casos el tamaño visible en pantalla lo sigue controlando el CSS (`max-height`,
`object-fit`), este cambio solo corrige el "aviso" que el navegador usa antes de que la
imagen cargue.

---

## 1. Título de pestaña + preview al compartir

| Página | Título de pestaña (`<title>`) | Preview al compartir (`og:title` / `og:description`) |
|---|---|---|
| **Home** | A&C Soluciones Agricolas y Urbanas \| Control de Plagas Profesional Chile | **Control de Plagas Profesional en Valparaíso \| A&C Soluciones — SEREMI** — Empresa certificada SEREMI DS 157/05. Cucarachas, roedores, termitas, chinches, avispas, mosquitos, hormigas, palomas. Atendemos Valparaíso, Viña del Mar, Quilpué y Quinta Región. Diagnóstico gratuito. |
| Blog/Arañas | Control de Arañas en Valparaíso \| Araña de Rincón — AYC MiP | Control de Arañas en Valparaíso \| Araña de Rincón — AYC MiP — Eliminamos arañas de rincón (Loxosceles laeta) con insecticida residual profesional en Valparaíso, Viña del Mar y Quilpué. Empresa certificada SEREMI. Una sola sesión, garantía 14 días. |
| Blog/Avispas | Control de Avispas y Abejas en Valparaíso \| AYC MiP — SEREMI | Control de Avispas y Abejas en Valparaíso \| AYC MiP — SEREMI — Extracción y eliminación profesional de nidos de avispas en Valparaíso, Viña del Mar y Quilpué. Chaqueta amarilla, avispa papelera. Técnicos certificados SEREMI. Atención de emergencia 24/7. |
| Blog/Chinche | Control de Chinches de Cama en Valparaíso \| Tratamiento Térmico — AYC MiP | Control de Chinches de Cama en Valparaíso \| Tratamiento Térmico — AYC MiP — Eliminamos chinches de cama con tratamiento térmico y químico residual en Valparaíso, Viña del Mar y Quilpué. Certificado SEREMI. Garantía de erradicación total en la Quinta Región. |
| Blog/Cucarachas | Control de Cucarachas en Valparaíso \| Gel No Repelente — AYC MiP | Control de Cucarachas en Valparaíso \| Gel No Repelente — AYC MiP — Eliminamos cucarachas en una sola sesión con gel no repelente de última generación en Valparaíso, Viña del Mar y Quilpué. Certificado SEREMI. Garantía 14 días. |
| Blog/Hormigas | Control de Hormigas en Valparaíso \| Efecto Dominó — AYC MiP | Control de Hormigas en Valparaíso \| Efecto Dominó — AYC MiP — Eliminamos colonias de hormigas negras y argentinas en Valparaíso, Viña del Mar y Quilpué con cebos de efecto dominó que destruyen el nido completo. Empresa certificada SEREMI. Tratamiento no repelente. |
| Blog/Mosquitos | Control de Mosquitos en Valparaíso \| AYC MiP | Control de Mosquitos en Valparaíso \| AYC MiP — Control profesional de mosquitos en Valparaíso, Viña del Mar y Quilpué. Fumigación, nebulización y larvicidas. Empresa certificada SEREMI DS 157/05. Garantía 14 días. |
| Blog/Palomas | Control de Palomas en Valparaíso \| Antiposada y Mallas — AYC MiP | Control de Palomas en Valparaíso \| Antiposada y Mallas — AYC MiP — Instalamos sistemas antiposada, mallas y repelentes para el control de palomas en edificios y viviendas de Valparaíso, Viña del Mar y Quilpué. Limpieza y desinfección incluida. Empresa certificada SEREMI. |
| Blog/Ratones | Control de Ratones y Roedores en Valparaíso \| Estaciones de Cebado — AYC MiP | Control de Ratones y Roedores en Valparaíso \| Estaciones de Cebado — AYC MiP — Programa integral de control de roedores con estaciones de cebado profesionales en Valparaíso, Viña del Mar y Quilpué. Certificado SEREMI DS 157/05. Desratización y sellado de accesos. |
| Blog/Termitas | Control de Termitas en Valparaíso \| Madera Seca y Subterránea — AYC MiP | Control de Termitas en Valparaíso \| Madera Seca y Subterránea — AYC MiP — Especialistas en termita de madera seca (Cryptotermes) y subterránea (Reticulitermes) en Valparaíso, Viña del Mar y Quilpué. Diagnóstico gratuito, informe técnico y certificado SEREMI. |
| **Landing Termitas** | A&C: Exterminio, Fumigación y Control de Plagas de Termitas en Valparaíso, V Región | **A&C: Exterminio, Fumigación y Control de Plagas de Termitas en Valparaíso, V Región** — Tratamiento especializado de termita de madera seca y subterránea. Diagnóstico gratuito, certificado SEREMI y garantía de 1 año. |

**Hecho (2026-07-31):** se agregaron `og:title`/`og:description`/`og:type`/`og:url`/`og:image`
a los 9 blog, copiando exactamente el `<title>` y `meta description` que ya tenía cada uno
(mismo texto, ninguna redacción nueva — si Francisco quiere otra redacción para el preview,
se cambia acá y se pide que se lleve al HTML). `og:image` de los 9 apunta al logo
(`img/LOGO-01.jpg`), igual que home y la landing de Termitas.

**Pendiente de decisión con Francisco:** las 11 páginas usan el logo como `og:image` — no
hay ninguna con foto representativa propia en el preview. Vale la pena decidir si quieren
una imagen más "vendedora" para home y/o la landing de Termitas (las de mayor tráfico).

---

## 2. CTAs y mensajes de WhatsApp por defecto

### Compartido en todo el sitio (header/footer — igual en home y en los 9 blog)

| Botón | Ubicación | Mensaje de WhatsApp |
|---|---|---|
| Botón flotante (WhatsApp) | Todas las páginas | "Hola, vi su página y necesito asesoria tecnica de control de plagas." |
| "Agenda gratis" (header + menú móvil) | Todas las páginas | mismo mensaje genérico de arriba |
| "Agenda visita gratis" | Footer, todas las páginas | mismo mensaje genérico |
| "Cotizar" | Header + menú móvil | Abre el modal del cotizador (no es link directo) |
| "Sistema para clientes" | Header | Link a `sistema.centralmip.com/login`, no es contacto |
| Teléfono / email / Instagram | Footer | `tel:+56 9 3667 8897`, `ventas@aycmip.cl`, `instagram.com/ayc.mip` |

### Home — CTAs propios del cuerpo

| Ubicación | Botón | Mensaje |
|---|---|---|
| Hero | "Habla con un especialista técnico ahora" | mensaje genérico (igual al del fab) |
| Hero | "Emergencia 24/7 · Llama ahora" | `tel:` directo |
| Hero | "Cotiza en 30 segundos" | abre cotizador (sección/modal genérico) |
| Sección "Todo lo que incluye" | "Agenda tu visita técnica gratuita" | mensaje genérico |
| Sección "Urgencia" | "Agenda ahora por WhatsApp" | mensaje genérico |
| Sección "Garantía" | "Agenda tu visita gratuita" | "Hola, quiero consultar sobre la garantía del servicio." |
| Contacto final | "WhatsApp ahora" | mensaje genérico |

### Blog — CTA propio del cuerpo (uno por página, mismo texto de botón, mensaje distinto)

Botón: **"Hablemos por WhatsApp"** en todas. Mensaje según plaga:

| Página | Mensaje |
|---|---|
| Arañas | "Hola, necesito ayuda con aranas en mi hogar" |
| Avispas | "Hola, necesito ayuda con avispas en mi hogar" |
| Chinche | "Hola, necesito ayuda con chinches en mi hogar" |
| Cucarachas | "Hola, necesito ayuda con cucarachas en mi hogar" |
| Hormigas | "Hola, necesito ayuda con hormigas en mi hogar" |
| Mosquitos | "Hola, necesito ayuda con mosquitos e insectos" |
| Palomas | "Hola, necesito ayuda con palomas en mi edificio" |
| Ratones | "Hola, necesito ayuda con roedores en mi hogar" |
| Termitas (blog) | "Hola, necesito ayuda con termitas en mi hogar" |

### Landing Termitas — header/footer y cuerpo propios (no comparte los del resto del sitio)

| Ubicación | Botón | Mensaje |
|---|---|---|
| Botón flotante + "Agenda gratis" (header/menú) | — | "Hola, vi su página (menú) y necesito ayuda con una plaga de termitas." |
| Hero | "Habla con un especialista en termitas ahora" | "Hola, vi su página y necesito ayuda con una plaga de termitas." |
| Hero | "Emergencia 24/7 · Llama ahora" | `tel:` directo |
| Hero | "Cotiza en 30 segundos" | abre `cotizador-termitas.js` (especializado) |
| Pain points (×4) | "Ver foto real" | no es de contacto — abre popup con foto |
| Sección "Todo lo que incluye" | "Agenda tu visita técnica gratuita" | "Hola, vi su página (detalle del servicio) y necesito ayuda con una plaga de termitas." |
| Sección "Urgencia" | "Agenda ahora por WhatsApp" | "Hola, vi su página y necesito ayuda con una plaga de termitas." |
| Sección "Garantía" | "Agenda tu visita gratuita" | "Hola, quiero consultar sobre la garantía del servicio." |
| Contacto final | "WhatsApp ahora" | "Hola, vi su página (contacto) y necesito ayuda con una plaga de termitas." |
| Footer | "Agenda visita gratis" | "Hola, vi su página (pie de página) y necesito ayuda con una plaga de termitas." |

**Hecho (2026-07-31):** los 3 botones que antes mandaban el mensaje genérico de plagas
("value-stack", contacto final, footer) ahora mandan un mensaje de termitas propio, cada
uno con una etiqueta distinta entre paréntesis — mismo patrón que ya usaba el botón del
header (que dice "(menú)") — para poder distinguir por el texto que llega a WhatsApp de
cuál botón exacto vino cada lead, no solo que vino de la landing de Termitas en general.
Técnicamente: se agregaron tokens `WA_VALUESTACK_TEXT` / `WA_CONTACTOFINAL_TEXT` /
`WA_FOOTER_TEXT` en `generador/build.py`, con default genérico (home/blog siguen igual,
sin cambios) y override de termitas en la lista `SERVICIOS` — mismo patrón que
`GARANTIA_DIAS`/`WA_HEADER_TEXT`, listo para que la próxima landing de servicio (ej.
Ratones) tenga los suyos sin heredar los de Termitas por accidente.

**Si Francisco quiere otra redacción para alguno de estos 4 mensajes** (header/menú,
detalle del servicio, contacto, pie de página), se edita esta tabla y se pide que se lleve
al `build.py` (son 4 líneas, no hay que tocar el HTML a mano).

También encontrado: comentario `<!-- TODO: revisar testimonios de termitas con Francisco -->`
todavía en el HTML de la landing (línea ~1256) — recordatorio viejo, sigue sin resolver
(a pedido tuyo, se deja en pausa por ahora).

---

## 3. Fondo verde de las 9 páginas de blog — corrección y rediseño (2026-07-31)

**Corrección a algo que dije mal antes:** había afirmado que `tarb.png` (2.3 MB) era el
fondo verde que se ve en las 9 páginas de blog. Es falso — revisé de nuevo y `tarb.png`
no lo carga ninguna página (la clase CSS que lo usa, `.hero__bg`, no está aplicada en
ningún HTML del sitio, es CSS muerto). El fondo verde real es otra clase,
`.breadcrumb-hero__bg`, que hasta hoy sí cargaba una foto real por página (distinta para
6 plagas, y un placeholder genérico compartido para las otras 4) detrás de un tinte verde
al 79% de opacidad — la foto apenas se distinguía.

**Cambio aplicado:** ese fondo ahora usa el logo blanco de A&C
(`img/logo_ayc_blanco@4x.png`, 28.6 KB — existía en el repo pero no se usaba en ningún
lado) como marca de agua, igual en las 9 páginas. Se sacó la foto de cada página
(`style="background-image: url(...)"` inline) y se centralizó en `css/subpages.css`
(`.breadcrumb-hero__bg`). Antes eran 6 fotos distintas + 1 repetida 4 veces; ahora es 1
solo archivo, que el navegador cachea una vez para las 9 páginas — igual de estándar que
pediste, y bastante más liviano.

Las fotos que antes se usaban ahí siguen en el repo — la mayoría se siguen usando como
foto real dentro del cuerpo de su artículo (ej. `chinche-cama.jpg` sigue apareciendo en
el blog de Chinches), así que no se borraron. La única que quedó sin ningún uso después
de este cambio es `hotniga.webp` (ver tabla de limpieza abajo).

---

## 4. Housekeeping — imágenes sin uso encontradas en el repo (pendiente tu OK para borrar)

Escaneé todo `web/img/` contra todo el sitio (HTML, CSS, JS, `build.py`, partials). Estas
no las carga ninguna página hoy:

| Archivo | Peso | Qué es / por qué no se usa |
|---|---|---|
| `hero_tecnico_frente.png` | 3.6 MB | No referenciado en ningún lado. |
| `hero_tecnico_accion.png` | 2.3 MB | No referenciado en ningún lado. |
| `tarb.png` | 2.3 MB | CSS muerto (`.hero__bg`, ver sección 3 arriba). |
| `hotniga.webp` | ~60 KB | Quedó huérfana tras el cambio del fondo de blog (sección 3). |
| `page-title.webp` | 326.9 KB | Foto de un campo/viñedo — no parece ni de plagas ni de A&C, posible descarga de stock sin usar. |
| `aranas.png` | 261.1 KB | Del lote `ayc__000X_*` — algunas de este lote sí se usan (ver inventario abajo), esta no. |
| `ayc__0005_termmit.png` | 234.6 KB | Ídem — no se usó, se usó `control-de-termitas.jpeg` en su lugar. |
| `ayc__0002_Avispas.png` | 219.2 KB | Ídem — se usó `panal-avispas.webp` en su lugar. |
| `ayc__0008_ratones.png` | 210.5 KB | Ídem — se usó `breadcrumb_controlplagas.jpg` en su lugar. |
| `ayc__0004_aranas.png` | 137.1 KB | Ídem — se usó `arana.jpg` en su lugar. |
| `logo_vina_montes.svg` | 73.4 KB | Existe también `logo_vina_montes.png`, que es el que sí se usa. |
| `ratones.webp` | 61.8 KB | No referenciado. |
| `image-57.webp` | 9.7 KB | No referenciado (nombre genérico, probable export sin terminar de integrar). |

**Ojo, no recomiendo borrar `heroe-fa.png`** (664 KB) aunque tampoco se usa hoy — es una
foto real de Francisco con gorro/polera de A&C, se ve como un asset preparado a propósito
para algo (¿bio, sección "conoce al equipo"?), no basura de prueba. Lo dejo fuera de la
lista de borrado salvo que confirmes que no se va a usar.

Todo lo de arriba está en git, así que borrar es recuperable si hace falta. Dime si borro
esta lista tal cual (13 archivos, ~10.3 MB) o si sacas alguno.

---

## 5. Inventario de imágenes por página (para revisar `alt` — 2026-07-31)

Todas las imágenes reales (`<img>`) de las 11 páginas, con su `alt` actual. Los logos de
clientes (Starken, Copec, Integra, Viña Montes, BanAmor) y el sello SEREMI se repiten
varias veces en la misma página (carrusel + trust-bar) — se muestran una sola vez acá,
no fila por repetición.

### Home
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/hero_main_ayc.png` (×2, mobile/desktop) | Técnico certificado A&C / Técnico certificado A&C de frente con brazos cruzados frente a cartel AyC MiP |
| `img/clientes/logo_starken.png` | Logo Starken *(y 3 repeticiones decorativas con `alt=""`)* |
| `img/clientes/logo_copec.png` | Logo Copec *(+3 repeticiones `alt=""`)* |
| `img/clientes/logo_integra.jpg` | Logo Fundación Integra *(+3 repeticiones `alt=""`)* |
| `img/clientes/logo_vina_montes.png` | Logo Viña Montes *(+3 repeticiones `alt=""`)* |
| `img/clientes/logo_banamor.svg` | Logo Fundación BanAmor *(+3 repeticiones `alt=""`)* |
| `img/seremi-salud.png` | Empresa Certificada SEREMI / Empresa Certificada SEREMI Ministerio de Salud *(2 apariciones, texto levemente distinto)* |
| `img/Calidad-AyC.png` | Garantía de Calidad A&C / Sello Garantía de Calidad A&C *(2 apariciones)* |
| `img/transbank_medios_pago.png` | Medios de pago Transbank Webpay |
| `img/arana.png` | Icono de control de plagas de arañas |
| `img/avispa.png` | Icono de control de plagas de avispas |
| `img/cucaracha.png` | Icono de control de plagas de cucarachas |
| `img/rata.png` | Icono de control de plagas de roedores (ratones y ratas) |
| `img/hormiga.png` | Icono de control de plagas de hormigas |
| `img/mosquito.png` | Icono de control de plagas de mosquitos |
| `img/paloma.png` | Icono de control de plagas de palomas |
| `img/termitas-soldado.png` | Icono de control de plagas de termitas |

### Blog/Arañas
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/leaf.webp`, `img/leaf-2.webp` | *(decorativas, `alt=""`)* |
| `img/ARANA-DE-RINCON-1.jpg` | Araña de Rincón — Loxosceles laeta |
| `img/aranas-patas-largas.png` | Araña Tigre — Scytodes globula |
| `img/arana-pollito.jpg` | Araña Pollito — Grammostola sp. |
| `img/arana.jpg` | Tratamiento profesional contra arañas — AYC MiP |
| `img/seremi-salud.png` | Empresa Certificada SEREMI Ministerio de Salud |

### Blog/Avispas
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/leaf.webp`, `img/leaf-2.webp` | *(decorativas, `alt=""`)* |
| `img/wasp-538470_1280.jpg` | Vespula germanica — Chaqueta Amarilla |
| `img/avispa-papelera.jpg.webp` | Polistes sp. — Avispa Papelera |
| `img/panal-avispas.webp` | Nido de avispas — control profesional |
| `img/seremi-salud.png` | Empresa Certificada SEREMI Ministerio de Salud |

### Blog/Chinche
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/leaf.webp`, `img/leaf-2.webp` | *(decorativas, `alt=""`)* |
| `img/chinche.jpg` | Chinche de Cama — Cimex lectularius |
| `img/chinche-cama.jpg` | Control profesional de chinches — AYC MiP |
| `img/seremi-salud.png` | Empresa Certificada SEREMI Ministerio de Salud |

### Blog/Cucarachas
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/leaf.webp`, `img/leaf-2.webp` | *(decorativas, `alt=""`)* |
| `img/blattlla-germanica.webp` | Cucaracha Alemana — Blattella germanica |
| `img/cucaracha-orienta.webp` | Cucaracha Oriental — Blatta orientalis |
| `img/cucaracha_americana_480x480.png` | Cucaracha Americana — Periplaneta americana |
| `img/ayc__0007_cucarachas1.png` | Control profesional de cucarachas — AYC MiP |
| `img/seremi-salud.png` | Empresa Certificada SEREMI Ministerio de Salud |

### Blog/Hormigas
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/leaf.webp`, `img/leaf-2.webp` | *(decorativas, `alt=""`)* |
| `img/03formiche.jpg` | Hormiga Negra Común — Lasius niger |
| `img/hor_ar.jpg` | Hormiga Argentina — Linepithema humile |
| `img/ayc__0003_Hormigas.png` | Control profesional de hormigas — AYC MiP |
| `img/seremi-salud.png` | Empresa Certificada SEREMI Ministerio de Salud |

### Blog/Mosquito
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/leaf.webp`, `img/leaf-2.webp` | *(decorativas, `alt=""`)* |
| `img/Culex-Mosquito.jpg` | Mosquito Común — Culex sp. |
| `img/mosquito-tigre.jpg` | Mosquito Tigre — Aedes aegypti |
| `img/ayc__0000_Desinsectao.png` | Desinsectado profesional — AYC MiP |
| `img/seremi-salud.png` | Empresa Certificada SEREMI Ministerio de Salud |

### Blog/Palomas
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/leaf.webp`, `img/leaf-2.webp` | *(decorativas, `alt=""`)* |
| `img/ayc__0001_palomas.png` (×2) | Paloma Doméstica — Columba livia / Control de palomas — AYC MiP |
| `img/seremi-salud.png` | Empresa Certificada SEREMI Ministerio de Salud |

### Blog/Ratones
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/leaf.webp`, `img/leaf-2.webp` | *(decorativas, `alt=""`)* |
| `img/raton-guaren.jpg` | Guarén (Rattus norvegicus) |
| `img/rata-negra.png` | Rata Negra (Rattus rattus) |
| `img/laucha.jpg` | Laucha (Mus musculus) |
| `img/breadcrumb_controlplagas.jpg` | Control profesional de roedores |
| `img/seremi-salud.png` | Empresa Certificada SEREMI Ministerio de Salud |

### Blog/Termitas
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/leaf.webp`, `img/leaf-2.webp` | *(decorativas, `alt=""`)* |
| `img/maderaseca-scaled.png` | Termita de Madera Seca — Cryptotermes brevis |
| `img/Termita-subterranea-03.jpg` | Termita Subterránea — Reticulitermes flavipes |
| `img/control-de-termitas.jpeg` | Tratamiento profesional de termitas |
| `img/seremi-salud.png` | Empresa Certificada SEREMI Ministerio de Salud |

### Landing Termitas
| Imagen | Alt actual |
|---|---|
| `img/LOGO-01.jpg` | Logo A&C Soluciones Agrícolas y Urbanas |
| `img/clientes/logo_starken.png` | Logo Starken *(+2 repeticiones `alt=""`)* |
| `img/clientes/logo_copec.png` | Logo Copec *(+2 repeticiones `alt=""`)* |
| `img/clientes/logo_integra.jpg` | Logo Fundación Integra *(+2 repeticiones `alt=""`)* |
| `img/clientes/logo_vina_montes.png` | Logo Viña Montes *(+2 repeticiones `alt=""`)* |
| `img/clientes/logo_banamor.svg` | Logo Fundación BanAmor *(+2 repeticiones `alt=""`)* |
| `img/pain-points/termitas-madera-hueca.avif` | Viga de madera abierta mostrando el daño interno de una infestación de termita de madera seca |
| `img/pain-points/termitas-alitas.avif` | Alitas de termita acumuladas en el marco de una ventana, señal de enjambre |
| `img/pain-points/termitas-granulos.avif` | Gránulos color café de termita de madera seca sobre una superficie de madera |
| `img/pain-points/termitas-tuneles-barro.avif` | Túnel de barro de termita subterránea subiendo por una muralla |
| `img/maderaseca-scaled.png` | Termita de madera seca (Cryptotermes brevis) |
| `img/Termita-subterranea-03.jpg` | Termita subterránea (Reticulitermes flavipes) |
| `img/control-de-termitas.jpeg` | Tratamiento profesional de termitas |
| `img/seremi-salud.png` | Empresa Certificada SEREMI / Empresa Certificada SEREMI Ministerio de Salud *(2 apariciones)* |
| `img/Calidad-AyC.png` | Garantía de Calidad A&C / Sello Garantía de Calidad A&C *(2 apariciones)* |
| `img/transbank_medios_pago.png` | Medios de pago Transbank Webpay |

**Candidatos a mejorar con keywords** (buenos hoy, pero se podrían acercar más a las
keywords de la sección de arriba): los alt de `hero_main_ayc.png` (home) y las fotos de
"Control profesional de X — AYC MiP" del lote `ayc__000X` (cucarachas, hormigas, mosquito,
palomas) ya son descriptivos pero genéricos — podrían sumar la ciudad (Valparaíso/Viña del
Mar) igual que ya lo hacen los `<title>`/meta description. No los cambié todavía porque son
~6 imágenes de contenido único por página, no un patrón repetido como los íconos — dime si
quieres que los ajuste uno por uno.
