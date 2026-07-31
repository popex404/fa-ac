# generador/ — qué es esto

**Esta carpeta es herramienta, no se sube al hosting.** Lo único que se le pasa a
Miguel es `../web/` completo. Si algún día empaquetas un `.zip` para el hosting,
`generador/` no va adentro.

Existe porque el header, el footer y el bloque de analítica (GA4 + Clarity)
vivían copiados y pegados, idénticos, en los 10 archivos HTML del sitio
(`web/index.html` + los 9 de `web/blog/`). Cambiar el número de WhatsApp, por
ejemplo, significaba editar 10 archivos a mano. Ahora se edita una vez acá y se
regenera solo.

## Qué hay adentro

| Archivo | Qué es |
|---|---|
| `build.py` | El script. Lee `_partials/` + `_data.json` y reescribe `../web/index.html` y `../web/blog/*/index.html`. |
| `_data.json` | Los valores que cambian: número de WhatsApp, email, IDs de GA4/Clarity, `SITE_URL` (dominio de producción, para `robots.txt`/`sitemap.xml` y el JSON-LD). |
| `_partials/header.html` | Botón flotante de WhatsApp + menú mobile + navbar completa. |
| `_partials/footer.html` | El `<footer>` completo (SEREMI, nav, contacto, copyright). |
| `_partials/analytics.html` | El bloque de GA4 + Microsoft Clarity que va en el `<head>`. |
| `_partials/main-js.html` | La línea `<script src="...js/main.js">`. |
| `_partials/year-script.html` | El script que pone el año actual en el copyright. |

Los partials son HTML normal (o casi, ver "Tokens" abajo), no una plantilla con
sintaxis especial. Se pueden abrir y editar como cualquier HTML.

## Cómo usarlo

```
cd generador
python build.py
```

Reescribe los archivos de `web/` (home, blog, servicios) y además:
1. Sincroniza teléfono/email en **todo** `.html` bajo `web/` (no solo header/footer, también el contenido único de cada página y los JSON-LD), buscando por patrón (`tel:`, `wa.me/`, `"telephone"`, formato visible, `@aycmip.cl`), no por el valor viejo, así funciona aunque el número ya haya cambiado varias veces antes.
2. Sincroniza las 3 copias del teléfono que viven en JS aparte del HTML: `cotizador.js` (`WA_NUMBER`) y `main.js` (`FA_WA_NUMBER`, `FA_TEL_NUMBER`).
3. Normaliza el JSON-LD en todo `.html` bajo `web/` (`sync_business_jsonld()`):
   tipo de negocio (`HomeAndConstructionBusiness`), dirección del `LocalBusiness`
   principal (solo en home) y `areaServed` (región + provincias + comunas, ver
   `AREA_SERVED`/`COBERTURA_JSONLD` al principio de `build.py`). Por patrón,
   igual que el punto 1, no por partial.
4. Regenera `web/robots.txt` y `web/sitemap.xml` enteros (`write_seo_files()`),
   a partir de `PLAGAS` + `SERVICIOS` + `SITE_URL` — una página nueva agregada
   a esas listas entra sola al sitemap la próxima vez que se corra `build.py`.

Correrlo sin haber cambiado nada en `_partials/` o `_data.json` no modifica
ningún archivo (es idempotente, probado con checksums). Probado también de
punta a punta con un número/email de prueba: cero rastros del valor viejo en
ningún archivo después de correrlo.

**Regla de oro: nunca editar a mano el contenido entre**
`<!-- PARTIAL:xxx:start -->` **y** `<!-- PARTIAL:xxx:end -->` **dentro de
`web/index.html` o `web/blog/*/index.html`.** Se pierde en el próximo build. Si
hay que cambiar algo ahí, se cambia en el partial correspondiente y se corre
`build.py`. Lo mismo aplica a `web/robots.txt` y `web/sitemap.xml`: se
regeneran enteros en cada build, cualquier edición a mano se pierde.

## Tokens

Los partials tienen espacios en blanco tipo `{{ROOT}}` en vez de rutas
escritas a mano, porque el mismo `header.html` se usa en la home (en la raíz)
y en las páginas de `blog/` (un nivel más adentro), y las rutas relativas no
son las mismas.

| Token | Para qué | Valor en home | Valor en `blog/*` |
|---|---|---|---|
| `{{ROOT}}` | Prefijo hacia `css/`, `js/`, `img/` | `` (vacío) | `../../` |
| `{{HOME_LINK}}` | Link al logo / "Inicio" | `#` | `../../index.html` |
| `{{HOME_ANCHOR}}` | Prefijo de anclas `#servicios`, `#faq`, etc. | `` (vacío) | `../../index.html` |
| `{{PLAGA_PREFIX}}` | Prefijo hacia las páginas hermanas de plaga | `blog/` | `../` |
| `{{WA_DIGITS}}` | Número sin `+` ni espacios, para `tel:` y `wa.me/` | igual en ambas, viene de `_data.json` |
| `{{WA_DISPLAY}}` | Número con formato, para texto visible | igual en ambas |
| `{{EMAIL}}` | Email de contacto | igual en ambas |
| `{{GA4_ID}}` / `{{CLARITY_ID}}` | IDs de analítica | igual en ambas |

Los valores por contexto (home vs. blog) están al principio de `build.py`, en
`HOME_CTX` y `BLOG_CTX`.

## Cómo agregar una página nueva al sistema (ej. futuras páginas de comuna)

**Hoy `build.py` tiene la lista de archivos escrita a mano**: la home + las 9
plagas (variable `PLAGAS`) para header/footer/analytics, y las páginas de
`servicios/` (variable `SERVICIOS`, lista de diccionarios `{slug, overrides...}`)
para eso más los partials de contenido (`SERVICE_PARTIAL_NAMES`). La landing de
Termitas ya usa este segundo patrón — es el ejemplo a seguir para la próxima
página de servicio. Para que una página nueva reciba el mismo header/footer
automático:

1. En su HTML, dejar los mismos marcadores `<!-- PARTIAL:header:start -->` /
   `:end` (y los de footer, analytics, main-js, year-script) en el lugar
   correcto, en vez de escribir esos bloques a mano.
2. Definir qué contexto le corresponde (`ROOT`, `HOME_LINK`, etc. según en qué
   carpeta vive) — si es un caso nuevo de profundidad, hay que agregar un
   contexto nuevo tipo `HOME_CTX`/`BLOG_CTX`.
3. Agregar el archivo a la función `build()` en `build.py`, y agregar su slug
   a `PLAGAS` o `SERVICIOS` (según corresponda) — eso además la mete sola en
   `sitemap.xml` (ver `write_seo_files()`), sin tocar nada más.

Si esto se vuelve frecuente (va a pasar pronto, con la landing de Termitas y
después las páginas por comuna), vale la pena generalizar `build.py` para que
**busque solo** cualquier `.html` bajo `web/` que tenga esos marcadores, en vez
de tener la lista a mano. No se hizo todavía porque el contexto (`ROOT`,
`PLAGA_PREFIX`, etc.) depende de la profundidad y tipo de página, y eso hay que
decidirlo cuando se sepa cómo se van a organizar las carpetas nuevas.

## El cotizador es un caso aparte

`web/js/cotizador.js` **no** es un partial, es un solo archivo JS que las
páginas enlazan (`<script src=".../js/cotizador.js">`). Cambiar su lógica
(precios, preguntas, textos) es editar ese archivo directo, sin build, aplica
solo en cualquier página que lo enlace. Hoy `web/index.html` lo enlaza, y la
landing de Termitas usa su propio `web/js/cotizador-termitas.js` (separado a
propósito, para que futuras plagas tengan el suyo sin pisarse).

Su número de WhatsApp (`WA_NUMBER` en la línea 7) es una excepción: no es un
bloque de HTML así que no puede ser un partial, pero sí depende del mismo dato
que `_data.json`, así que `build.py` lo sincroniza al final de cada corrida
(función `sync_cotizador_wa_number` → `sync_js_constant`).

**Ojo con `js/main.js`:** ya traía, de antes de este trabajo, su propio
mini-sistema (`FA_WA_NUMBER` / `FA_TEL_NUMBER`, líneas 12-13, con un comentario
que literalmente dice "cambiar número aquí actualiza todos los links del
sitio"). Reescribe en el navegador, al cargar la página, cualquier
`<a href="wa.me/...">` o `<a href="tel:...">` que encuentre. Es una segunda
red de seguridad en tiempo de ejecución, redundante ahora con lo que hace
`build.py` en el HTML fuente, pero no molesta y se dejó tal cual (no se borró
código que ya funcionaba). `build.py` también sincroniza estas 2 constantes.

Para embeber el cotizador en una página de servicio nueva ya existe el partial
`_partials/cotizador-embed.html` (el `<div>` del widget/modal + el `<script>`,
parte de `SERVICE_PARTIAL_NAMES`) — se agregó para la landing de Termitas, se
reusa tal cual para la próxima página de servicio.

## Lo que este sistema NO cubre todavía (actualizado 2026-07-29)

**Resuelto (ya no es limitación):**
- El número de WhatsApp y el email dentro del contenido único de cada página
  (CTAs, JSON-LD) — antes solo se cubría header/footer, ahora
  `sync_contact_fields()` recorre todo `web/*.html`.
- Las clases CSS `.btn-primary` / `.btn-secondary` / `.btn-sistema` duplicadas
  entre `css/styles.css` y `css/subpages.css`: eran código muerto (`subpages.css`
  carga antes que `styles.css`, así que `styles.css` ya ganaba en la cascada).
  Se borró la copia de `subpages.css`, cero cambio visual. Ya no hay que
  duplicar nada ahí.
- El **tipo de negocio, dirección y área servida del JSON-LD** vivían escritos
  a mano en 11 archivos (el tipo era además inválido, `PestControlService` no
  existe en schema.org). Ahora `sync_business_jsonld()` los normaliza desde un
  solo lugar en `build.py` (`AREA_SERVED`/`COBERTURA_JSONLD`), igual patrón
  que `sync_contact_fields()`.
- `robots.txt` / `sitemap.xml` no existían — ahora los genera
  `write_seo_files()` en cada build, a partir de `PLAGAS`/`SERVICIOS`.

**Decidido no tokenizar (a propósito, no es un olvido):**
- El **nombre de la empresa** ("A&C Soluciones Agrícolas y Urbanas") dentro de
  los JSON-LD. Javier: es muy improbable que cambie, cambiar el nombre legal de
  una empresa es complicado, no vale la pena la abstracción para algo que
  casi no va a cambiar.

**Resuelto parcialmente:**
- La **garantía** (`GARANTIA_DIAS` / `GARANTIA_PERIODO`) ya es un token con
  default "14 días" en `SERVICIO_CTX`, sobreescribible por página vía el
  diccionario `SERVICIOS` — la landing de Termitas lo usa para su garantía de
  1 año sin tocar el default del resto del sitio. Ese es el patrón a repetir
  para cualquier otro valor que varíe por página de servicio.

**Sigue pendiente (más grande, no es de este ajuste puntual):**
- El resto del **texto de contenido** (menciones SEREMI, copy del
  hero/FAQ/etc.) sigue siendo HTML fijo por página, no un dato en `_data.json`.
  Tokenizar contenido de verdad (no solo contacto/garantía) es del tamaño del
  generador de comunas/servicios que viene después de la landing de Termitas.
- **`alt` descriptivo y `width`/`height` en imágenes**, en las 11 páginas —
  hoy el 91% de las `<img>` del sitio no tiene dimensiones (riesgo de CLS).
  Queda a propósito para el final del roadmap SEO (ver `FA-roadmap.md` en el
  vault), toca página por página, no es centralizable en `build.py` como el
  resto de esta limpieza.
