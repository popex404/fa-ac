# Plan — Landing de venta de Termitas

**Estado:** planeación y base, todavía no se construye. Este documento es la
entrada para la próxima sesión de construcción.

**Contexto completo:** `zk-vault/clientes/FA/FA-roadmap.md` → "En curso ahora".
Decidido en reunión con Francisco y Mario el 2026-07-28. Deadline **viernes
2026-07-31**. Por qué Termitas primero: es el servicio más rentable de AyC.

**Objetivo de la página:** vender el servicio de Termitas específicamente
(no promocionar AyC en general), para usar como destino de campañas SEM.
Estilo Hormozi, mismo lenguaje visual que la landing actual (`web/index.html`)
pero enfocado 100% en un solo servicio.

---

## 1. Fuentes de contenido

| Fuente | Qué se saca de ahí |
|---|---|
| `web/index.html` (landing actual) | Estructura visual, secciones universales (ver tabla abajo), estilo, CSS existente |
| `web/blog/termitas/index.html` | Contenido real de termitas: especies, señales de alerta, y sobre todo el **método de tratamiento** (la parte más importante a traer, según Javier) |
| `generador/_partials/` | header, footer, analytics — se reutilizan tal cual, no se rehacen |

---

## 2. Comparación sección por sección: home actual → landing de Termitas

| # | Sección en `web/index.html` hoy | Acción para la landing de Termitas |
|---|---|---|
| 1 | Hero (título genérico + imagen genérica) | **Adaptar el título, mantener la imagen actual del landing por ahora.** Título específico de termitas (ver §3 SEO para las keywords del H1). La foto real del equipo trabajando con termitas se agrega al final, no bloquea el esqueleto (decisión de Javier: primero armar la estructura completa para compartir con Francisco, la foto es un detalle que se suma después). |
| 2 | Trust bar (SEREMI / V Región / garantía 14 días / 24-7) | **Reusar tal cual** (universal, candidato a partial) |
| 3 | Clientes marquee (logos) | **Reusar tal cual** (universal, candidato a partial) — evaluar si aporta en una landing corta enfocada a un solo servicio, o si se saca por espacio |
| 4 | Pain points ("¿Reconoces alguno de estos problemas?", genéricos) | **Adaptar.** Dolores específicos de termitas: sonido hueco en la madera, alitas cerca de ventanas, gránulos color café, galerías de barro. Base real ya escrita en `blog/termitas/index.html` → sección "ALERT SIGNS" (línea 252) |
| 5 | Mecanismo único (insecticidas no repelentes, CentralMIP, certificación, diagnóstico) | **Reusar tal cual** (universal, candidato a partial). Esto es lo que Javier se refería como "¿por qué elegir AyC?" |
| 6 | Proof — counters + badges (500+ clientes, 10+ años, SEREMI, Transbank) | **Reusar tal cual** (universal, candidato a partial). Esto también es parte del "mostrar credenciales y experiencia" que pidió Javier |
| 7 | Proof — testimonios (3 genéricos: ratones, SEREMI, termitas) | **Incluir la sección, pero marcarla explícitamente como "por arreglar".** Para el esqueleto: dejar el testimonio de termitas (Agrícola Los Naranjos, Limache) como placeholder, y dejar un comentario visible en el HTML (`<!-- TODO: revisar testimonios de termitas con Francisco -->`) para que no se nos olvide antes de publicar de verdad. No curar a fondo todavía, eso es para cuando se trabaje el contenido con Francisco. |
| 8 | Servicios grid (las 9 plagas) | **No incluir.** Es networking de la home, no cabe en una landing de un solo servicio. Como mucho, un link chico al fondo tipo "¿Buscas otro servicio? Ver todos" |
| 9 | Para quién es (dueños de casa, PYMES, colegios, industrial, emergencias) | **Reusar tal cual** (universal, candidato a partial) |
| 10 | Value stack (visita gratis, 1 sesión, certificado, garantía, trazabilidad) | **Reusar tal cual** (universal, candidato a partial) — verificar que el texto no prometa "1 sesión" si termitas es distinto (el cotizador ya trata termitas como caso especial sin precio online, revisar consistencia) |
| 11 | Cotizador | **Reusar el widget.** Mejora posible: al venir de una landing de termitas, saltarse la pregunta "¿qué problema tienes?" y partir directo en tamaño/urgencia. Anotado, no bloqueante |
| 12 | Urgencia ("las plagas no esperan") | **Adaptar levemente.** Mismo mensaje, reforzado con "termitas" en vez de genérico |
| 13 | Garantía (sello + 14 días) | **Reusar tal cual** (universal, candidato a partial) |
| 14 | FAQ (genérico: duración, seguridad, pago, etc.) | **Dos capas.** Base genérica reusable (candidato a partial) + preguntas específicas de termitas con la keyword adentro, ej. "¿Cómo sé si tengo termitas?", "¿Termitas de madera seca o subterránea, cuál tengo?". Ver §4, esto es lo que Javier propuso originalmente para SEO por comuna, aplica igual de bien a SEO por servicio |
| 15 | Contacto / CTA final | **Reusar tal cual** (universal, candidato a partial) |
| 16 | Footer | **Ya es partial**, se reusa sin tocar nada |
| — | **Sección "Cobertura" (nueva, no existe en la home)** | **Agregar.** Lista de comunas de la V Región atendidas, para que esta página empiece a competir en "termitas Quillota" antes de que existan páginas por comuna. Contenido: ver universo de comunas en `zk-vault/clientes/FA/FA.md` (si no está ahí, retomar de la Sesión 2, `FA/reuniones/sesion-2/FA-plan-sesion2-v1.md`) |
| — | **Contenido a traer de `blog/termitas/index.html`** | Sección "TREATMENT METHODS" (línea 268 del archivo actual): intro + 5 métodos (barreras químicas, inyección termiticida, sistemas de cebado IGR, erradicación térmica, informe técnico). Es lo más importante a trasladar, según Javier. La sección "SPECIES SECTION" (línea 208, Cryptotermes brevis / Reticulitermes flavipes) es más informativa que de venta — evaluar si se resume en 2-3 líneas dentro de otra sección, o se deja solo en el blog y la landing linkea ahí para el que quiera el detalle técnico |

---

## 3. SEO — metatags y keywords

Definido por Javier: optimizar para "Termitas", "Problema de Termitas", "Plaga
de Termitas", "Exterminación de Termitas" + variantes asociadas. Al momento de
escribir title/meta description/H1, usar estas frases tal cual aparecen en
búsquedas reales, no solo como palabras sueltas.

Referencia de patrón de competidores (análisis ya hecho en esta conversación,
antes del plan de la Sesión 2): título tipo `Control de Termitas en [zona] |
[gancho] — [Marca]`, H1 corto y directo con la keyword principal.

---

## 4. Infraestructura técnica — qué ya existe, qué falta decidir

**Ya existe (no rehacer):**
- `generador/build.py` + `generador/_partials/` — sistema de partials para header/footer/analytics/main-js/year-script. Ver `generador/README.md`.
- `sync_contact_fields()` — sincroniza teléfono/email en cualquier `.html` nuevo bajo `web/` automáticamente, sin necesidad de registrarlo en ningún lado.
- Tracking de origen del cotizador ya funciona (`data-source` → campo `source` en el webhook), solo falta poner el atributo correcto en la página nueva.

**Decidido:**
1. **Ruta del archivo (confirmado por Javier):** `web/servicios/exterminio-y-fumigacion-de-plagas-de-termitas/index.html`. Nombre largo a propósito, cubre keywords de SEO. Nota técnica: queda a la misma profundidad que `web/blog/[plaga]/` (2 niveles bajo `web/`), así que `{{ROOT}}` es igual (`../../`), pero **no** es el mismo contexto que `BLOG_CTX`: para linkear desde acá hacia `web/blog/termitas/` (o hacia otras páginas de `web/servicios/` que se creen después) la ruta relativa es distinta a como se linkean entre sí las páginas de `blog/`. Al construir, definir un `SERVICIO_CTX` propio en `build.py`, no reusar `BLOG_CTX` a ciegas.

**Falta decidir/hacer al construir:**
2. **Extender `_partials/` con las secciones universales de la tabla §2** (trust-bar, mecanismo, proof-counters+badges, para-quién-es, value-stack, garantía, contacto-final), no solo copiarlas a mano en la landing nueva. Javier: correr el script para agregar esas secciones y otros campos, no reescribirlas HTML a mano. Son universales (mismo contenido en cualquier landing de servicio futura), tiene sentido sacarlas del `web/index.html` actual igual que se hizo con header/footer.
3. **Registrar la página nueva en `build.py`** (hoy la lista de archivos está a mano, ver `generador/README.md` → "Cómo agregar una página nueva al sistema"), o generalizar el script para que descubra solo cualquier `.html` con marcadores. Vale la pena resolverlo ahora que hay un caso real.
4. **Sexto partial para el cotizador** (`_partials/cotizador-embed.html`): el `<div>` del widget/modal + el `<script src="js/cotizador.js">`, para no repetirlo a mano en esta página ni en las futuras. Depende de cómo se decida mostrarlo acá (modal como en la home, o widget inline).
5. **Imagen del hero:** se mantiene la actual por ahora (ver tabla §2, fila 1). Reemplazar por una foto real más adelante, no bloquea el esqueleto.
6. **Testimonios:** incluir la sección con lo que hay, marcada como pendiente de revisar con Francisco (ver tabla §2, fila 7).

---

## 5. Testeo — verificar antes de dar la landing por lista

- **Con Miguel:** confirmar si su servidor sirve `carpeta/` sin mostrar `index.html` en la URL (probado localmente con el servidor de Python, funciona ahí, pero no está confirmado en el hosting real). Afecta si la URL final queda limpia o con `/index.html` visible.
- **Google Apps Script del cotizador:** verificar si la columna `source` del Sheet efectivamente se está escribiendo con el payload actual (no se pudo confirmar desde el repo, ese script vive fuera del código versionado). Importante antes de lanzar la landing nueva, porque ahí es donde vamos a querer medir de dónde vienen los leads.

---

## 6. Fuera de alcance para esta landing (a propósito)

- Páginas por comuna de termitas (`exterminacion-de-plagas-de-termitas-en-[comuna]`) — vienen después, esta landing es la plantilla base para llegar ahí.
- Nuevas landing de otros servicios (ratones, sanitización) — mismo caso, después.
- Distancia/tiempo desde la base de operaciones por comuna — eso es para cuando existan páginas por comuna reales, acá basta con la lista simple de cobertura (§2, última fila).
