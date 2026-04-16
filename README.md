# fa-ac — A&C Soluciones Agrícolas y Urbanas

Repositorio de producción del sitio web y herramientas digitales de A&C Soluciones (aycmip.cl).

**Cliente:** Francisco Aracena — A&C Soluciones Agrícolas y Urbanas
**Contacto:** ventas@aycmip.cl · +56 9 8154 4036
**URL live:** https://www.aycmip.cl

---

## Estructura

```
fa-ac/
  web/          → Sitio web de producción (www.aycmip.cl)
  docs/         → Vínculos a vault y registros de implementación
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

## v2 — En construcción (PAUSADO — esperando señal de Francisco)

Pendiente de implementar:
- Cotizador interactivo: tipo de plaga + inmueble + comuna + urgencia → cotización estimada + email automático al lead y a A&C
- Google Analytics 4 + Microsoft Clarity (heatmaps)
- SEO técnico mejorado
- Hero con 2 imágenes (rotación)
- Páginas nuevas: Moscas, Garrapatas, Sanitización
- Badge de garantía visual
- Próxima reunión Francisco: OG image 1200×630, Google Business, acceso SII, credenciales IG, número Angelo, WhatsApp Business

**Brief completo v2:** `zk-vault/clientes/FA/FA-cronologico.md`
**Arquitectura CRM+AI (post-v2):** `zk-vault/clientes/FA/FA-crm-ai.md`
**Reunión estratégica:** `zk-vault/clientes/FA/FA-reunion-voz001.md`

### Post-v2 — Proyectos en paralelo (contexto reunión Voz 001)
- **Corpus de voz Francisco:** scrape Instagram/YouTube → agente AI que habla como Francisco (2 bots: comercial + técnico)
- **Go High Level:** Javier tiene cuenta GHL ~2-3 semanas. Construir landing FA + automatizaciones → Francisco compra cuenta propia
- **Contenido video:** plantilla de guión para TikTok/Reels (gancho → problema → solución). Posible collab FA × CG (Chely)
- **Marca personal:** Francisco como especialista/asesor en plagas — cursos, capacitaciones, advisory

---

## Registro de cambios

Ver [CHANGELOG.md](CHANGELOG.md)
