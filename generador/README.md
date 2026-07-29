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
| `_data.json` | Los valores que cambian: número de WhatsApp, email, IDs de GA4/Clarity. |
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

Reescribe los 10 archivos de `web/` y también sincroniza `web/js/cotizador.js`
(tiene su propio número de WhatsApp, ver "Lo que NO cubre" abajo). Correrlo sin
haber cambiado nada en `_partials/` o `_data.json` no modifica ningún archivo
(es idempotente, probado con checksums).

**Regla de oro: nunca editar a mano el contenido entre**
`<!-- PARTIAL:xxx:start -->` **y** `<!-- PARTIAL:xxx:end -->` **dentro de
`web/index.html` o `web/blog/*/index.html`.** Se pierde en el próximo build. Si
hay que cambiar algo ahí, se cambia en el partial correspondiente y se corre
`build.py`.

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

## Cómo agregar una página nueva al sistema (ej. la landing de Termitas, futuras páginas de comuna)

**Hoy `build.py` tiene la lista de archivos escrita a mano** (la home + las 9
plagas, variable `PLAGAS`). Para que una página nueva reciba el mismo
header/footer automático:

1. En su HTML, dejar los mismos marcadores `<!-- PARTIAL:header:start -->` /
   `:end` (y los de footer, analytics, main-js, year-script) en el lugar
   correcto, en vez de escribir esos bloques a mano.
2. Definir qué contexto le corresponde (`ROOT`, `HOME_LINK`, etc. según en qué
   carpeta vive) — si es un caso nuevo de profundidad, hay que agregar un
   contexto nuevo tipo `HOME_CTX`/`BLOG_CTX`.
3. Agregar el archivo a la función `build()` en `build.py`.

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
solo en cualquier página que lo enlace. Hoy solo `web/index.html` lo enlaza.

Su número de WhatsApp (`WA_NUMBER` en la línea 7) es una excepción: no es un
bloque de HTML así que no puede ser un partial, pero sí depende del mismo dato
que `_data.json`, así que `build.py` lo sincroniza al final de cada corrida
(función `sync_cotizador_wa_number`).

Si se quiere embeber el cotizador en una página nueva (la landing de Termitas,
por ejemplo), falta un sexto partial (`cotizador-embed.html`, el `<div>` del
widget/modal + el `<script>`), todavía no existe porque depende de cómo se
decida mostrarlo ahí (modal vs. widget inline).

## Lo que este sistema NO cubre todavía (auditado 2026-07-29)

- **El número de WhatsApp sigue apareciendo a mano dentro del contenido único
  de cada página** (CTAs del hero, sección de garantía, urgencia, contacto en
  la home; el CTA de servicio en cada página de `blog/`). El build solo cubre
  header/footer/analytics, no el body completo. Si el número cambia, esas
  ocurrencias hay que buscarlas y cambiarlas a mano (`grep -rn "56936678897"
  web/`), o esperar al generador completo (fase de comunas) que sí va a
  tokenizar el contenido entero.
- **Los bloques JSON-LD** (`Service`, `BreadcrumbList` en cada página de
  `blog/`; `PestControlService`, `FAQPage` en la home) tienen el nombre y
  teléfono de la empresa escritos a mano por página, no están centralizados.
- **Las clases CSS `.btn-primary` / `.btn-secondary` / `.btn-sistema`** siguen
  duplicadas entre `css/styles.css` y `css/subpages.css` (no se heredan), esto
  ya estaba documentado en `../CLAUDE.md` antes de este trabajo, sigue igual.

No se resolvieron ahora a propósito: son cambios más grandes que tocan
contenido único por página, no solo lo compartido, y se solapan con el
generador de comunas que se viene después de la landing de Termitas.
