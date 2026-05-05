# fa-ac — A&C Soluciones Agrícolas y Urbanas

Repositorio de producción del sitio web y herramientas digitales de A&C Soluciones (aycmip.cl).

**Cliente:** Francisco Aracena — A&C Soluciones Agrícolas y Urbanas
**Email:** ventas@aycmip.cl
**URL live:** https://www.aycmip.cl

---

## Número activo (WhatsApp CTAs)

Número en uso: **+56 9 8154 4036** (personal Francisco)

Para cambiar el número en el sitio:
- **Cotizador:** actualizar `WA_NUMBER` en `web/js/cotizador.js` línea 7
- **HTML:** grep+replace `wa.me/56981544036` en todos los archivos HTML

---

## Estructura

```
fa-ac/
  web/          → Sitio web de producción (www.aycmip.cl)
```

---

## v1 — Deploy actual

**Estado:** Live en producción (www.aycmip.cl)
**Stack:** HTML + CSS + JS vanilla. Sin dependencias de build.

Incluye:
- Landing page principal con copy Hormozi (11 secciones: Hero, Pain Points, Mecanismo, Prueba, Solución, Para Quién Es, Value Stack, Urgencia, Garantía, FAQ, CTA Final)
- 9 páginas de servicios individuales: Arañas, Avispas, Chinches, Cucarachas, Mosquitos, Hormigas, Palomas, Roedores, Termitas
- Schema JSON-LD: LocalBusiness (PestControlService), FAQPage, BreadcrumbList, Service en subpáginas
- Meta SEO en todas las páginas
- Sistema de animaciones unificado (`.reveal/.revealed` via IntersectionObserver)
- Navbar con dropdown de servicios + menú móvil expandible
- Grand Slam: "La solución a tus plagas desde la primera visita, o volvemos gratis"
- Certificación DS 157/2005, garantía 14 días, atención 24/7
- Portal Sistema para Clientes: sistema.centralmip.com/login
- Testimoniales Swiper v11 (placeholders — pendiente reales de Francisco)

---

## v2 — En repo, pendiente deploy

**Estado:** Completa en repositorio. Pendiente que Miguel haga pull al servidor.

Implementado en repo:
- Cotizador interactivo (`/cotizar`): inmueble → plaga → tamaño → urgencia → contacto → presupuesto estimado + CTA WhatsApp
- Google Analytics 4 + Microsoft Clarity (heatmaps)
- SEO técnico mejorado (keywords, meta-tags, alt-text)

Pendiente futuro (no bloqueante para deploy):
- Subpáginas: Moscas, Garrapatas, Sanitización
- Backlinks internos: termitas → home → cucarachas

---

## Vault FA

Fuente de verdad del cliente: `zk-vault/clientes/FA/FA.json`
Historial y loops: `zk-vault/clientes/FA/FA.md`
