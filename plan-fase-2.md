# Plan — Fase 2 (nuevos servicios de venta)

Sucesor de `plan-landing-termitas.md` (eliminado, contenido repartido: lo
vigente quedó acá, la referencia técnica pasó a `referencia-ctas-y-previews.md`).

**Estado: Termitas (v3.0) completa y pusheada** (`db3146e` + `04a3a79`,
2026-07-31). Pendiente que Javier suba el `.zip` de `web/` al hosting de
Miguel. Detalle de decisiones y sesiones de construcción →
`zk-vault/clientes/FA/FA-roadmap.md` → `## Logrado`.

---

## Servicios construidos (2026-08-04) — mismo patrón que Termitas

Reunión 2026-08-03 (Pancho + Mario). **Las 5 páginas ya están construidas**
(local, sin pushear). Cada una sigue el mismo esquema que la landing de
Termitas: partial de `generador/_partials/`, overrides propios en la lista
`SERVICIOS` de `generador/build.py` (garantía, mensajes de WhatsApp por CTA,
cotizador propio), y backlink a su página de blog/plaga correspondiente.
Detalle técnico completo (slugs, cotizadores, decisiones de contenido a
revisar) → `referencia-ctas-y-previews.md` → "Fase 2 — 5 landings nuevas".

1. **Derratización** (roedores) — `exterminio-y-fumigacion-de-plagas-de-ratones`
2. **Predemolición** — servicio propio, separado de Derratización (ajuste
   2026-08-04: en la reunión salió mezclado con derratizado, pero Pancho/Mario
   lo tratan como servicio aparte) — `exterminio-y-fumigacion-de-plagas-de-predemolicion`
3. **Desinsectación** — cubre hormigas, arañas, avispas ("voladores y
   rastreros"). Chinches de cama NO entra acá, se queda en su página de blog.
   `exterminio-y-fumigacion-de-plagas-de-desinsectacion`
4. **Sanitización** — `exterminio-y-fumigacion-de-plagas-de-sanitizacion`
5. **Control de palomas** — `exterminio-y-fumigacion-de-plagas-de-palomas`

Usar en el copy los términos que la gente realmente busca (ej. "control de
ratones"), no solo el nombre técnico — mismo criterio que ya se aplicó en
Termitas.

**Pendiente antes de pushear:**
- Revisar con Francisco el contenido de Predemolición y Sanitización (sin
  blog fuente, redactado con criterio general — ver TODOs marcados en el
  HTML y detalle en `referencia-ctas-y-previews.md`).
- Reemplazar los 5 testimonios genéricos por reseñas reales cuando existan.
- Grabar/conseguir video propio por servicio (hoy las 5 landings reusan el
  video de Termitas a modo de placeholder, a pedido de Javier).
- Confirmar orden y nombres del dropdown "Servicios" del header con Javier
  antes de pushear (ya aplicado: Termitas, Desratización, Predemolición,
  Desinsectación, Sanitización, Palomas).

**Nota sobre el botón "Servicios" de la home (resuelto):** el link directo
del dropdown ahora apunta a la grilla de "Nuestros Servicios" del home
(antes iba directo a Termitas, único servicio que existía).

---

## Pendiente heredado de la landing de Termitas (sin urgencia)

- Revisar con Francisco los textos/mensajes de WhatsApp/títulos del sitio —
  detalle y antes/después en `referencia-ctas-y-previews.md`.
- Seguir mejorando SEO y `alt` de imágenes (candidatos ya anotados en
  `referencia-ctas-y-previews.md`), y decidir cuándo convertir a WebP/AVIF.
- Links internos del sitio muestran `index.html` en la URL al navegar (ej.
  `.../blog/aranas/index.html`) — cosmético, el `canonical` de cada página
  ya está limpio, no afecta SEO. **En pausa (2026-08-03):** Pancho pidió
  mantener el `index.html` explícito en la URL de la landing de Termitas por
  ahora, no está seguro si el redirect sin él funciona bien en el hosting de
  Miguel — confirmar con él antes de tocar los `href` internos.
- Decisión estratégica de páginas por comuna (landings completas vs. páginas
  delgadas) — propuesta técnica completa en `FA-roadmap.md` → Largo plazo,
  Javier no ha decidido todavía.

---

## Referencia técnica

Paths, arquitectura de `build.py`/partials, cotizadores y comando de testing
local → `referencia-ctas-y-previews.md`, sección "Dónde está todo".

No pushear a GitHub sin confirmación explícita de Javier.
