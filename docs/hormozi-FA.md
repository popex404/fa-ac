# HORMOZI FA — A&C Soluciones Agrícolas y Urbanas
> Cliente: Francisco Arazena (FA / Pancho)
> Fuente: Videollamada 1 (2026-03-05) + Videollamada 3 (Reunión 3) + Imágenes de marca
> Última actualización: 2026-03-21
> Template base: `zk-vault/outputs/sops/SOP_hormozi-landing-page.md`
> ⚠️ Este archivo está vinculado al repo `FA-control-plagas/` (github.com/popex404/fa-ac-demos)
> Cuando modifiques cualquier sección aquí → actualizar la sección correspondiente en el HTML.

---

## IDENTIDAD DE MARCA

| Campo | Valor | Estado |
|---|---|---|
| Nombre empresa | A&C Soluciones Agrícolas y Urbanas | ✅ |
| Marca corta | AyC MiP | ✅ |
| Color primario | `#E8731A` (naranja) | ✅ |
| Color secundario | `#3A6B28` (verde oscuro) | ✅ |
| Color neutro | `#1A1A1A` (negro) | ✅ |
| Logo color | `PUBLICIDAD/Imagenes/Ayc/Logo_ayc@4x-3.png` | ✅ |
| Logo blanco | `PUBLICIDAD/Imagenes/Ayc/logo_ayc_blanco@4x.png` | ✅ |
| Logo vectorial | `PUBLICIDAD/Imagenes/Ayc/LOGO AYC.pdf` | ✅ |
| Sello garantía | `PUBLICIDAD/Imagenes/Ayc/Calidad-AyC.png` | ✅ |
| Medios de pago | `PUBLICIDAD/Imagenes/Ayc/transbank_medios_pago.png` | ✅ |
| Teléfono activo (HTML) | +56 9 8154 4036 | ✅ |
| Teléfono alternativo | +56 9 3629 7390 (registrado — puede reactivarse) | 📝 |
| Email | ventas@aycmip.cl | ✅ |
| Web actual | www.aycmip.cl | ✅ |
| Instagram | @ayc.mip | ✅ |
| WhatsApp link | https://wa.me/56981544036 | ✅ |
| Certificación | Empresa Certificada por SEREMI | ✅ |
| Pago | Efectivo, Transferencia o Transbank | ✅ |
| Medios de pago (texto) | Efectivo, Transferencia o Tarjetas (Transbank) | ✅ |

### Grand Slam Statement
> "La solución a tus plagas desde la primera visita, o volvemos gratis"

---

## SECCIÓN 1 — HERO
> 📄 HTML: `<section id="hero">`
> `emotion: confianza + autoridad inmediata`
> `schema_type: LocalBusiness`

| Campo | Contenido |
|---|---|
| Pre-headline | Empresa Certificada SEREMI · Visita técnica gratuita · Atención 24/7 |
| Headline | Solucionamos tu problema de plagas desde la primera visita, garantizado |
| Subheadline | Técnicos especializados con métodos que funcionan desde la primera sesión, sin repeticiones ni sorpresas |
| CTA principal | "Habla con un técnico ahora" → WhatsApp |
| CTA secundario | "Emergencia 24/7 · Llama ahora" → tel |
| Imagen hero | `PUBLICIDAD/Imagenes/Heroes/hero_main_ayc.png` |
| image_alt | Técnico certificado A&C de frente con brazos cruzados frente a cartel AyC MiP |
| wa_message | "Hola, vi su página y necesito asesoria tecnica de control de plagas." |

**Notas:**
- `hero_main_ayc.png` es la imagen principal — técnico de frente, brazos cruzados, cartel AyC detrás, sello garantía visible. Es la más fuerte porque tiene branding AyC integrado.
- Mobile-first: el CTA debe verse sin hacer scroll
- El sello `Calidad-AyC.png` puede aparecer superpuesto en la esquina del hero

---

## SECCIÓN 2 — PAIN POINTS
> 📄 HTML: `<section id="pain">`
> `emotion: validación del problema — el cliente se tiene que ver reflejado`

| # | Título (pregunta empática) | Descripción |
|---|---|---|
| 1 | ¿Fumigaste y volvieron? | Muchas empresas usan productos que dispersan la plaga en vez de eliminarla. Pagas 3 veces y el problema sigue. |
| 2 | ¿Nadie te responde el formulario? | Cuando hay una plaga, necesitas respuesta inmediata. Los formularios no dan certeza de cuándo te llaman. |
| 3 | ¿Te ofrecen precio sin ver el problema? | Cada plaga es distinta. Sin visita técnica, el diagnóstico puede estar equivocado y la cotización no vale nada. |
| 4 | ¿Te llenaron de papeles que no entienden nada? | Otras empresas te entregan pilas de documentos en papel. Nosotros somos 100% digitales: órdenes, informes y certificados llegan directo a tu correo, sin papeleo. |

**Notas:**
- Títulos en formato pregunta (genera empatía, el cliente se identifica)
- Imágenes de apoyo: `PUBLICIDAD/Imagenes/Plagas/` según tipo de plaga mencionada

---

## SECCIÓN 3 — MECANISMO ÚNICO
> 📄 HTML: `<section id="mecanismo">`
> `emotion: curiosidad + credibilidad técnica`
> `schema_type: HowTo`

El diferenciador técnico que justifica por qué AyC funciona cuando otros no.

| Campo | Contenido |
|---|---|
| Título | Por qué nuestro método funciona cuando los demás fallan |
| Mecanismo | **Sistema MIP (Manejo Integrado de Plagas)** — protocolo certificado que combina diagnóstico de especie + insecticidas no repelentes + seguimiento post-tratamiento |
| Diferenciador 1 | **Insecticidas no repelentes:** eliminan desde adentro en vez de dispersar la plaga. La colonia muere, no se mueve. |
| Diferenciador 2 | **Gestión 100% digitalizada vía CentralMIP:** AyC opera con CentralMIP, el software de control de plagas más usado en Latinoamérica. Cada visita, trampa y tratamiento queda registrado. Los clientes acceden a su portal en tiempo real y reciben certificados digitales de acreditación al instante — válidos para auditorías SEREMI. |
| Diferenciador 3 | **Certificación SEREMI:** no somos un servicio informal — emitimos certificado oficial válido para auditorías sanitarias bajo normativa DS 157/2005. El certificado incluye firma digital. |
| Diferenciador 4 | **Diagnóstico antes de cotizar:** visitamos el lugar, identificamos la especie y el nivel de infestación. La solución es específica, no genérica. |

**Nota de copy:** Mencionar CentralMIP por nombre — añade credibilidad (es el software líder en LatAm para control de plagas). La narrativa es "AyC usa las mejores herramientas disponibles", no "CentralMIP es el protagonista". AyC siempre al frente.

**Pendientes con Francisco:**
- [ ] ¿Qué productos/marcas usan? Deben ser productos con registros ISP
- [ ] ¿Tiempo promedio de resolución real?

---

## SECCIÓN 4 — PRUEBA / CREDIBILIDAD
> 📄 HTML: `<section id="proof">`
> `emotion: reducción de desconfianza`
> `schema_type: Review + Organization`
> ⚠️ Va ANTES de la solución — primero se cree, después se explica

| Elemento | Contenido | Asset |
|---|---|---|
| Hero de marca | Técnico certificado con branding AyC visible | `PUBLICIDAD/Imagenes/Heroes/hero_main_ayc.png` |
| Sello de calidad | Garantía de Calidad A&C (sello dorado oficial) | `PUBLICIDAD/Imagenes/Ayc/Calidad-AyC.png` |
| Certificación | Logo SEREMI + "Empresa Certificada" | `PUBLICIDAD/Imagenes/Ayc/seremi-salud.png` ✅ |
| Medios de pago | Transbank | `PUBLICIDAD/Imagenes/Ayc/transbank_medios_pago.png` |
| Servicios cubiertos | Cucarachas · Roedores · Arañas · Termitas · Avispas · Hormigas · Sanitización · Control Aves | Afiches en `PUBLICIDAD/Afiches/` |
| Testimonios | ⚠️ PENDIENTE — Francisco tiene clientes reales, hay que pedírselos | — |
| Números | ⚠️ PENDIENTE — años de experiencia / clientes atendidos | — |

---

## SECCIÓN 5 — SOLUCIÓN
> 📄 HTML: `<section id="solution">`
> `emotion: alivio + claridad`

| # | Título | Descripción |
|---|---|---|
| 1 | Diagnóstico gratuito | Visitamos, evaluamos y cotizamos sin costo. Sin compromiso. |
| 2 | Insecticidas no repelentes | Tecnología que elimina desde adentro, no desplaza la plaga. Una sesión resuelve. |
| 3 | Resultado en 1 visita | Sin tratamientos repetidos. Nuestro método funciona a la primera. |
| 4 | Garantía de 2 semanas | Si ves alguna plaga después del tratamiento, volvemos sin costo adicional. |
| 5 | Certificado SEREMI | Emitimos certificado oficial para cumplimiento sanitario. Válido para auditorías. |
| 6 | Atención de emergencia 24/7 | ¿Aparece una plaga un domingo a las 2am? Tenemos técnico disponible. |

**Imágenes de servicios disponibles:**
- `PUBLICIDAD/Afiches/rrss_empresarial_control plagas.png`
- `PUBLICIDAD/Afiches/rrss_empresarial_sanitizacionambientes.png`
- `PUBLICIDAD/Afiches/rrss_empresarial_tecnologia-innovacion.png`
- `PUBLICIDAD/Imagenes/Plagas/` — por tipo de plaga

---

## SECCIÓN 6 — PARA QUIÉN ES
> 📄 HTML: `<section id="para-quien">`
> `emotion: identificación — "esto es para mí"`

| Segmento | Descripción | Pain específico |
|---|---|---|
| Dueños de casa | Familias con plaga activa que quieren solución rápida y segura | Miedo a las plagas + niños en casa |
| Restaurantes y PYMES | Necesitan certificado SEREMI para operar. Urgencia alta. | Multa / cierre si no tienen certificado |
| Colegios e instituciones | Contratos recurrentes, alta demanda de documentación | Protocolo sanitario + DS 157/2005 |
| Empresas industriales | Control continuo con trazabilidad digital y documentos de acreditación al instante | Cumplimiento normativo + auditorías |
| Casos de emergencia 24/7 | Plaga aparece fuera de horario hábil | Respuesta inmediata, no formulario |

**Notas:**
- La base de datos `BD Clientes.xlsx` tiene hoja "BD Colegio" — colegios son un segmento activo
- Para empresas industriales: CentralMIP (portal de cliente + trazabilidad + certificados digitales) es el diferenciador clave

---

## SECCIÓN 7 — VALUE STACK
> 📄 HTML: `<section id="value-stack">`
> `emotion: sensación de ganga / valor desproporcionado`

| Ítem | Valor percibido |
|---|---|
| Visita técnica de diagnóstico | Gratis |
| Tratamiento especializado (1 sesión) | Resultado garantizado |
| Certificado sanitario oficial | Viene incluido en todos los servicios |
| Garantía de 2 semanas | Sin costo extra |
| Asesoría en prevención | Incluida en la visita |
| Gestión digitalizada (industrial) | Trazabilidad total de trampas, tratamientos y documentos de acreditación al instante |

**Frase ancla de precio:**
> "Otras empresas te cobran 3 sesiones a $120.000 c/u = $360.000. Nosotros resolvemos en una, con garantía."

---

## SECCIÓN 8 — URGENCIA
> 📄 HTML: `<section id="urgency">`
> `emotion: pérdida inminente — el costo de no actuar hoy`

| Campo | Contenido |
|---|---|
| Mensaje | Las plagas no esperan. Cada día que pasa, la colonia crece. |
| Urgencia real | Visita técnica gratuita con disponibilidad limitada — agenda hoy |
| Consecuencia de esperar | Una colonia de cucarachas se duplica en 30 días. Lo que hoy es un problema manejable, mañana es una infestación. No esperes: cada día que no actúas, el problema se multiplica. |

---

## SECCIÓN 9 — GARANTÍA
> 📄 HTML: `<section id="garantia">`
> `emotion: eliminación del riesgo percibido`

| Campo | Contenido |
|---|---|
| Garantía principal | Si ves alguna plaga en los 14 días siguientes al tratamiento, volvemos sin costo |
| Sello visual | `PUBLICIDAD/Imagenes/Ayc/Calidad-AyC.png` — imagen principal de esta sección |
| Certificación | Respaldo SEREMI — no somos un servicio informal |
| Confianza adicional | Técnico real con foto, no un bot genérico |
| wa_message | "Hola, quiero consultar sobre la garantía del servicio." |

**Notas:**
- El sello `Calidad-AyC.png` es el elemento visual central de esta sección — no reemplazar con CSS genérico

---

## SECCIÓN 10 — FAQ
> 📄 HTML: `<section id="faq">`
> `emotion: eliminación de objeciones finales`
> `schema_type: FAQPage`

| Pregunta | Respuesta |
|---|---|
| ¿Cuánto demora el tratamiento? | Depende del tipo de plaga y el tamaño del espacio. Una visita de diagnóstico suele durar 30-60 min. El tratamiento lo coordinamos en la misma visita. |
| ¿Tengo que salir de mi casa durante el tratamiento? | Para algunos tratamientos sí, por seguridad. Te avisamos con anticipación qué necesitas hacer. |
| ¿El tratamiento es seguro para niños y mascotas? | Sí. Usamos productos autorizados y te indicamos el tiempo de espera seguro antes de volver al espacio. |
| ¿Dan certificado SEREMI? | Sí. Emitimos certificado oficial válido para auditorías sanitarias, requerido por la normativa DS 157/2005. |
| ¿Qué pasa si la plaga vuelve? | Tienes garantía de 2 semanas. Si aparece alguna plaga, volvemos sin costo adicional. |
| ¿Atienden los fines de semana y feriados? | Sí, tenemos atención de emergencia 24/7 los 365 días del año. |
| ¿Cómo pago? | Aceptamos efectivo, transferencia bancaria y tarjetas a través de Transbank (Visa, Mastercard, Amex). |

---

## SECCIÓN 11 — CTA FINAL
> 📄 HTML: `<section id="cta-final">`
> `emotion: decisión — reducir fricción al máximo`

| Campo | Contenido |
|---|---|
| Headline final | ¿Listo para terminar con la plaga hoy? |
| CTA 1 | "Agenda tu visita técnica gratuita" → WhatsApp |
| CTA 2 | "Emergencia 24/7 — Llama ahora" → tel |
| CTA 3 | Formulario simple: nombre + teléfono + tipo de plaga (opcional, secundario) |
| wa_message | "Hola, vi su página y necesito asesoria tecnica de control de plagas." |
| Imagen de apoyo | `PUBLICIDAD/Imagenes/Heroes/hero_tecnico_frente.png` o `hero_tecnico_accion.png` |

---

## NOTAS GLOBALES DE DISEÑO
> Aplican a todo el HTML

- **Mobile-first** — diseñar para 375px primero, escalar a desktop
- **WhatsApp es el canal principal** — CTA más visible siempre
- Sin formularios como canal primario (la gente no sabe cuándo responden)
- Botón flotante WhatsApp en mobile (esquina inferior derecha, siempre visible)
- Fuente: limpia, sans-serif, máx. 20 palabras por frase
- **Hero images:** `hero_main_ayc.png` para sección Hero. `hero_tecnico_frente.png` y `hero_tecnico_accion.png` para secciones internas
- **Sello garantía:** siempre usar `Calidad-AyC.png` — nunca CSS genérico

---

## PENDIENTES (completar con Francisco)

- [x] **Teléfono confirmado** — +56 9 8154 4036 ✅ confirmado por Francisco
- [ ] **Testimonios de clientes reales** con nombre y tipo de servicio
- [ ] **Nombre del número de emergencia** (¿Ángel? ¿un técnico específico?)
- [x] **CentralMIP** — se menciona por nombre como credencial (software líder LatAm que AyC usa). Protagonista sigue siendo AyC. ✅
- [x] **Logo SEREMI** — `PUBLICIDAD/Imagenes/Ayc/seremi-salud.png` ✅
- [x] **Años de experiencia** / número de clientes atendidos — 500+ clientes, 10+ años de experiencia ✅ confirmado
- [ ] **Precio orientativo termitas** (requiere visita — ¿hay rango?)
- [ ] **Videos de Instagram** embebibles
- [ ] **¿Dominio nuevo o se usa aycmip.cl?**
