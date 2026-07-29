# FA/fa-ac — Sitio A&C Soluciones (aycmip.cl)

CLAUDE.md del proyecto. Los hechos del cliente viven en el vault (ver punteros).

## Quién + qué
Sitio de Francisco Aracena ("Pancho"), A&C Soluciones (control de plagas, Quinta Región). Live en https://www.aycmip.cl/ (v2.3).

## Scope
Activo (2026-07-29 en adelante) — landing de venta de Termitas en construcción, deadline viernes 2026-07-31, y proyecto de SEO local por comuna detrás de esa. `fa-ac` = única fuente de verdad; `popex404/fa-ac-demos` = archivo de mockups (no tocar para producción). CRM IA sigue pausado aparte, sin relación con esto.

## Datos operativos que el código toca (`web/`)
- **Estructura (actualizada 2026-07-29):** `index.html` (home/landing, usa `css/styles.css` + `css/cotizador.css`) + `js/main.js` (dos IntersectionObserver: `.reveal`, `.fade-in`) + `js/cotizador.js` (solo se carga en home, no en `blog/`) + `blog/[plaga]/index.html` (×9, informativas tipo blog: arañas, avispas, chinche, cucarachas, hormigas, mosquito, palomas, ratones, termitas — usan `css/subpages.css` + `css/styles.css`). Antes del 2026-07-29 estas 9 vivían en la raíz de `web/` como `[plaga]/index.html`; se movieron a `web/blog/` porque su contenido es informativo (especies, tratamiento), no una landing de venta. Enlaces entre ellas son relativos de un nivel (`../[plaga]/index.html`); hacia `css/js/img/index.html` son de dos niveles (`../../`).
- **Landing de venta de Termitas (en construcción, deadline 2026-07-31):** página nueva, separada de `blog/termitas/`, enfocada 100% en vender el servicio. Ver `zk-vault/clientes/FA/FA-roadmap.md` → "En curso ahora" para el detalle de contenido y objetivo.
- **Regla CSS (resuelta 2026-07-29):** `styles.css` es la fuente de verdad de `.btn-primary` / `.btn-secondary` / `.btn-sistema`. Antes decía que había que duplicarlas también en `subpages.css` porque "no se heredan" — eso era código muerto: `subpages.css` carga antes que `styles.css` en las páginas de `blog/`, así que `styles.css` ya gana en la cascada. Se borró la copia duplicada de `subpages.css` (era idéntica o subconjunto exacto, cero cambio visual). No hay que volver a duplicar nada ahí.
- **Header/footer/analytics ya NO se editan a mano por archivo (desde 2026-07-29).** Viven una sola vez en `web/_partials/*.html` (header, footer, analytics, main-js, year-script) con tokens de contexto (`{{ROOT}}`, `{{HOME_LINK}}`, `{{HOME_ANCHOR}}`, `{{PLAGA_PREFIX}}`, `{{WA_DIGITS}}`, `{{WA_DISPLAY}}`, `{{EMAIL}}`, `{{GA4_ID}}`, `{{CLARITY_ID}}`) resueltos desde `web/_data.json`. Para cambiar cualquiera de esos bloques o el número de WhatsApp/email/IDs de analítica: editar el partial o `_data.json`, correr `python web/build.py`, listo, se regeneran los 10 HTML (home + `blog/*`). **Nunca editar a mano** el contenido entre `<!-- PARTIAL:x:start -->` y `<!-- PARTIAL:x:end -->` en `index.html` o `blog/*/index.html`, se pierde en el próximo build. El resto de cada página (meta tags, contenido de especies/tratamiento, JSON-LD) sigue siendo HTML normal, fuera de esos marcadores.
- **Blast radius — al cambiar identidad:**

  | Dato | Dónde se cambia ahora |
  |---|---|
  | Teléfono / WhatsApp | `web/_data.json` (`wa_number`) → `python web/build.py` |
  | Email | `web/_data.json` (`email`) → `python web/build.py` |
  | GA4 / Clarity IDs | `web/_data.json` (`ga4_id`, `clarity_id`) → `python web/build.py` |
  | Color `#E8731A` / `#3A6B28` | `css/styles.css` y `subpages.css` (sin cambios, sigue duplicado ahí) |
  | Garantía "14 días" | `web/index.html` (6+ ocurrencias, contenido único de la home, no es partial) |
  | SEREMI | `web/index.html` (8+) + subpáginas (contenido único, no es partial) |

## Reglas críticas / no-tocar
- Sello de calidad = imagen (`Calidad-AyC.png`), NO crear CSS alternativo.
- No pushear sin OK de Javier.

## Punteros al vault
- Hechos del cliente → `../../zk-vault/clientes/FA/FA.md`
- Estado vivo / tareas → `../../zk-vault/clientes/FA/FA-roadmap.md`
- protocolo de actualización → zk-vault/clientes/FA/FA.md
