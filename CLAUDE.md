# FA/fa-ac — Sitio A&C Soluciones (aycmip.cl)

CLAUDE.md del proyecto. Los hechos del cliente viven en el vault (ver punteros).

## Quién + qué
Sitio de Francisco Aracena ("Pancho"), A&C Soluciones (control de plagas, Quinta Región) — marca visible en el sitio: "A&C Control de Plagas" (rebranding v3.0, 2026-07-31; nombre legal/de Google Business sin cambio, ver `FA.md`). Live en https://www.aycmip.cl/, próxima subida por Miguel: **v3.0**.

## Scope
Activo — v3.0 (landing de venta de Termitas + auditoría SEO técnica + rebranding) completa y pusheada (2026-07-31), pendiente que Javier suba el `.zip` de `web/` al hosting de Miguel. Pendientes sin urgencia: revisar textos/mensajes con Francisco, seguir mejorando SEO/alt, limpiar links internos (muestran `index.html` en la URL). Detalle → `zk-vault/clientes/FA/FA-roadmap.md` → "En curso ahora". `fa-ac` = única fuente de verdad; `popex404/fa-ac-demos` = archivo de mockups (no tocar para producción). CRM IA sigue pausado aparte, sin relación con esto.

## Datos operativos que el código toca (`web/`)
- **Estructura:** `index.html` (home) + `js/main.js` (`.reveal`/`.fade-in`) + `js/cotizador.js` (home) + `js/cotizador-termitas.js` (landing de Termitas, especializado y separado a propósito) + `blog/[plaga]/index.html` (×9, informativas: arañas, avispas, chinche, cucarachas, hormigas, mosquito, palomas, ratones, termitas — `css/subpages.css` + `css/styles.css`) + `servicios/exterminio-y-fumigacion-de-plagas-de-termitas/index.html` (landing de venta, 100% enfocada en vender, separada de `blog/termitas/`).
- **Herramienta de build vive en `generador/` (hermana de `web/`, NUNCA se le pasa a Miguel):** `generador/build.py` lee `generador/_partials/*.html` + `generador/_data.json` y regenera header/footer/analytics/main-js/year-script en las 11 páginas (home + 9 blog + la landing de Termitas). Para páginas de `servicios/` además aplica un segundo set de partials de contenido (`SERVICE_PARTIAL_NAMES`: trust-bar, clientes, mecanismo, proof-counters, para-quien, value-stack, garantia, cobertura, contacto-final, cotizador-embed) vía overrides por página en la lista `SERVICIOS`. Correr `python build.py` desde `generador/` regenera todo, sincroniza teléfono/email/JSON-LD (tipo de negocio, areaServed, `name`), y regenera `robots.txt`/`sitemap.xml`. **Nunca editar a mano** el contenido entre `<!-- PARTIAL:x:start -->` y `<!-- PARTIAL:x:end -->` en `web/*.html`, se pierde en el próximo build. Detalle completo → `generador/README.md`.
- **Regla CSS:** `styles.css` es la fuente de verdad de `.btn-primary` / `.btn-secondary` / `.btn-sistema` / colores/fondos de sección (`--bg-light-blue` = naranjo cálido pese al nombre, `--bg-light-green` = verde) — no duplicar en `subpages.css`.
- **Blast radius — al cambiar identidad:**

  | Dato | Dónde se cambia ahora |
  |---|---|
  | Teléfono / WhatsApp | `generador/_data.json` (`wa_number`) → `python build.py` (sincroniza HTML + `cotizador*.js` + `main.js`) |
  | Email | `generador/_data.json` (`email`) → `python build.py` |
  | GA4 / Clarity IDs | `generador/_data.json` (`ga4_id`, `clarity_id`) → `python build.py` |
  | Nombre de marca visible ("A&C Control de Plagas") | Contenido único por página (title/meta/og/hero/navbar) — no es un token, se cambió a mano en las 11 páginas 2026-07-31 |
  | Nombre legal / Google Business (JSON-LD `name`) | `generador/build.py` → `BUSINESS_NAME_PATTERN` / `sync_business_jsonld()` |
  | Garantía (default "14 días", Termitas la sobreescribe a "1 año") | `generador/build.py` → `SERVICIO_CTX` (`GARANTIA_DIAS`) + overrides en `SERVICIOS` |
  | Color `#E8731A` / `#3A6B28` | `css/styles.css` y `subpages.css` (sigue duplicado ahí) |
  | SEREMI | Contenido único por página, no es partial |

## Reglas críticas / no-tocar
- Sello de calidad = imagen (`Calidad-AyC.png`), NO crear CSS alternativo.
- No pushear sin OK de Javier.

## Punteros al vault
- Hechos del cliente → `../../zk-vault/clientes/FA/FA.md`
- Estado vivo / tareas → `../../zk-vault/clientes/FA/FA-roadmap.md`
- protocolo de actualización → zk-vault/clientes/FA/FA.md
