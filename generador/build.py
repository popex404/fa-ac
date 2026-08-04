"""
generador/  = herramienta de construccion. NUNCA se le pasa a Miguel.
web/        = lo unico deployable, el .zip que se le manda a Miguel sale de aqui.

Regenera las secciones compartidas (header, footer, analytics, main.js, year-script)
dentro de web/index.html y web/blog/*/index.html, a partir de
generador/_partials/ + generador/_data.json. Ademas sincroniza el JSON-LD
(tipo de negocio, direccion, areaServed) en todo .html bajo web/, y regenera
robots.txt + sitemap.xml a partir de PLAGAS/SERVICIOS.

Uso: python build.py   (desde generador/, o desde donde sea, la ruta a web/ es fija)
Editar SOLO los archivos en _partials/ (o _data.json para el numero de WhatsApp,
GA4, Clarity, email, SITE_URL). Nunca editar a mano el contenido entre los
marcadores <!-- PARTIAL:xxx:start --> ... <!-- PARTIAL:xxx:end --> en
web/index.html o web/blog/*/index.html, ni web/robots.txt, ni web/sitemap.xml:
se pierde en el proximo build.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
WEB = HERE.parent / "web"
PARTIALS = HERE / "_partials"
PLAGAS = ["aranas", "avispas", "chinche", "cucarachas", "hormigas",
          "mosquito", "palomas", "ratones", "termitas"]
# Cada servicio es un slug + overrides propios de esa pagina (ej. la garantia
# de termitas es distinta a la generica). Lo que no se sobreescribe usa el
# default de SERVICIO_CTX (14 dias, igual que el resto del sitio). Este es el
# patron a seguir cuando se agreguen mas paginas de servicios/: parametrizar
# por diccionario en vez de tocar los partials compartidos a mano por pagina.
SERVICIOS = [
    {
        "slug": "exterminio-y-fumigacion-de-plagas-de-termitas",
        "GARANTIA_DIAS": "1 año",
        "GARANTIA_PERIODO": "durante el año siguiente al tratamiento",
        # Mismo espiritu que WA_HEADER_TEXT: mensajes distintos por CTA para
        # poder distinguir, por el texto que llega a WhatsApp, de cual boton
        # especifico de la landing vino el lead (no solo que vino de aca).
        "WA_HEADER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28men%C3%BA%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20termitas.",
        "WA_VALUESTACK_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28detalle%20del%20servicio%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20termitas.",
        "WA_CONTACTOFINAL_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28contacto%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20termitas.",
        "WA_FOOTER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28pie%20de%20p%C3%A1gina%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20termitas.",
        # Esta landing recibe la campaña de Google Ads de Termitas (2026-08-04):
        # usa el gtag de conversion de Ads en vez del GA4 generico del resto del
        # sitio. "analytics" (nombre del partial default) -> override propio.
        "ANALYTICS_PARTIAL": "analytics-ads-termitas",
    },
    # Fase 2 (2026-08-04): 5 landings mas, mismo patron que Termitas. Orden
    # de esta lista = orden del dropdown "Servicios" en header.html (Javier:
    # Termitas, Desratizacion, Predemolicion, Desinsectacion, Sanitizacion,
    # Palomas). WA_HEADER_TEXT explicito en las 6 a proposito: el default de
    # SERVICIO_CTX quedo hardcodeado a "una plaga de termitas" (bug latente
    # si un servicio nuevo no lo pisa), asi que ninguna entrada de aca debe
    # omitirlo.
    {
        "slug": "exterminio-y-fumigacion-de-plagas-de-ratones",
        "WA_HEADER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28men%C3%BA%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20ratones.",
        "WA_VALUESTACK_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28detalle%20del%20servicio%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20ratones.",
        "WA_CONTACTOFINAL_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28contacto%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20ratones.",
        "WA_FOOTER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28pie%20de%20p%C3%A1gina%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20ratones.",
    },
    {
        "slug": "exterminio-y-fumigacion-de-plagas-de-predemolicion",
        "WA_HEADER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28men%C3%BA%29%20y%20necesito%20una%20inspecci%C3%B3n%20de%20predemolici%C3%B3n.",
        "WA_VALUESTACK_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28detalle%20del%20servicio%29%20y%20necesito%20una%20inspecci%C3%B3n%20de%20predemolici%C3%B3n.",
        "WA_CONTACTOFINAL_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28contacto%29%20y%20necesito%20una%20inspecci%C3%B3n%20de%20predemolici%C3%B3n.",
        "WA_FOOTER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28pie%20de%20p%C3%A1gina%29%20y%20necesito%20una%20inspecci%C3%B3n%20de%20predemolici%C3%B3n.",
    },
    {
        "slug": "exterminio-y-fumigacion-de-plagas-de-desinsectacion",
        "WA_HEADER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28men%C3%BA%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20ara%C3%B1as%2C%20avispas%20u%20hormigas.",
        "WA_VALUESTACK_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28detalle%20del%20servicio%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20ara%C3%B1as%2C%20avispas%20u%20hormigas.",
        "WA_CONTACTOFINAL_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28contacto%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20ara%C3%B1as%2C%20avispas%20u%20hormigas.",
        "WA_FOOTER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28pie%20de%20p%C3%A1gina%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20ara%C3%B1as%2C%20avispas%20u%20hormigas.",
    },
    {
        "slug": "exterminio-y-fumigacion-de-plagas-de-sanitizacion",
        "WA_HEADER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28men%C3%BA%29%20y%20necesito%20un%20servicio%20de%20sanitizaci%C3%B3n.",
        "WA_VALUESTACK_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28detalle%20del%20servicio%29%20y%20necesito%20un%20servicio%20de%20sanitizaci%C3%B3n.",
        "WA_CONTACTOFINAL_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28contacto%29%20y%20necesito%20un%20servicio%20de%20sanitizaci%C3%B3n.",
        "WA_FOOTER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28pie%20de%20p%C3%A1gina%29%20y%20necesito%20un%20servicio%20de%20sanitizaci%C3%B3n.",
    },
    {
        "slug": "exterminio-y-fumigacion-de-plagas-de-palomas",
        "WA_HEADER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28men%C3%BA%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20palomas.",
        "WA_VALUESTACK_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28detalle%20del%20servicio%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20palomas.",
        "WA_CONTACTOFINAL_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28contacto%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20palomas.",
        "WA_FOOTER_TEXT": "Hola%2C%20vi%20su%20p%C3%A1gina%20%28pie%20de%20p%C3%A1gina%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20palomas.",
    },
]

DATA = json.loads((HERE / "_data.json").read_text(encoding="utf-8"))

# Cobertura geografica (comuna + provincia + region) para el JSON-LD
# (areaServed). Misma informacion que ya vive en
# generador/_partials/cobertura.html (mapa interactivo) - duplicada aca a
# proposito, son capas distintas (esta alimenta schema.org, la otra la UI).
# Si cambia la cobertura real hay que actualizar las dos.
# Juan Fernandez queda afuera a proposito: esta en SIN_COBERTURA en
# cobertura.html (isla sin cobertura de terreno confirmada), no se declara
# como area servida.
COBERTURA_JSONLD = {
    "Quillota": ["Quillota", "La Cruz", "Nogales", "Calera", "Hijuelas"],
    "Valparaíso": ["Valparaíso", "Viña del Mar", "Concón", "Quintero",
                   "Puchuncaví", "Casablanca"],
    "Marga Marga": ["Quilpué", "Villa Alemana", "Limache", "Olmué"],
    "San Antonio": ["San Antonio", "Cartagena", "El Tabo", "El Quisco",
                    "Algarrobo", "Santo Domingo"],
    "Petorca": ["La Ligua", "Cabildo", "Petorca", "Zapallar", "Papudo"],
    "San Felipe de Aconcagua": ["San Felipe", "Putaendo", "Santa María",
                                "Panquehue", "Llay-Llay", "Catemu"],
    "Los Andes": ["Los Andes", "San Esteban", "Calle Larga", "Rinconada"],
}


def build_area_served():
    """areaServed a los 3 niveles (region + cada provincia + cada comuna),
    con containedInPlace para que quede la jerarquia real, no una lista
    plana sin relacion entre si."""
    region = {"@type": "State", "name": "Región de Valparaíso"}
    areas = [region]
    for provincia, comunas in COBERTURA_JSONLD.items():
        prov = {"@type": "AdministrativeArea", "name": provincia, "containedInPlace": region}
        areas.append(prov)
        for comuna in comunas:
            areas.append({"@type": "City", "name": comuna, "containedInPlace": prov})
    return areas


AREA_SERVED = build_area_served()

# Mensaje generico del header (boton flotante de WhatsApp + "Agenda gratis"
# desktop/mobile). Cada servicio_CTX puede pisarlo con uno mas especifico (ver
# WA_HEADER_TEXT en SERVICIO_CTX) para poder distinguir, en el mensaje que
# llega, si el lead entro por el header o por un CTA del cuerpo de la pagina.
WA_HEADER_TEXT_GENERICO = "Hola%2C%20vi%20su%20p%C3%A1gina%20y%20necesito%20asesoria%20tecnica%20de%20control%20de%20plagas."

HOME_CTX = dict(DATA, ROOT="", HOME_LINK="#", HOME_ANCHOR="", PLAGA_PREFIX="blog/",
                SERVICIO_PREFIX="servicios/", SERVICIOS_GRID_ANCHOR="#servicios",
                WA_HEADER_TEXT=WA_HEADER_TEXT_GENERICO,
                WA_FOOTER_TEXT=WA_HEADER_TEXT_GENERICO)
BLOG_CTX = dict(DATA, ROOT="../../", HOME_LINK="../../index.html",
                HOME_ANCHOR="../../index.html", PLAGA_PREFIX="../",
                SERVICIO_PREFIX="../../servicios/",
                SERVICIOS_GRID_ANCHOR="../../index.html#servicios",
                WA_HEADER_TEXT=WA_HEADER_TEXT_GENERICO,
                WA_FOOTER_TEXT=WA_HEADER_TEXT_GENERICO)
# Las paginas de servicios/ (landings de venta, ej. Termitas) viven a la misma
# profundidad que blog/[plaga]/ (2 niveles bajo web/), pero HOME_ANCHOR queda
# vacio (local, no "../../index.html"): a diferencia de blog/, estas landings
# SI traen sus propias secciones #para-quien/#garantia/#faq/#contact (reusadas
# como partials de contenido), asi que esos anchors deben scrollear dentro de
# la misma pagina, no mandar de vuelta al home. La unica excepcion es el link
# "Plagas" del header, que apunta a la grilla de plagas del home: por eso usa
# el token aparte SERVICIOS_GRID_ANCHOR en vez de HOME_ANCHOR.
SERVICIO_CTX = dict(DATA, ROOT="../../", HOME_LINK="../../index.html",
                     HOME_ANCHOR="", PLAGA_PREFIX="../../blog/",
                     SERVICIO_PREFIX="../",
                     SERVICIOS_GRID_ANCHOR="../../index.html#servicios",
                     GARANTIA_DIAS="14 días",
                     GARANTIA_PERIODO="en los 14 días siguientes al tratamiento",
                     # Default pensado para la landing de Termitas (unica hoy).
                     # El "(menu)" es a proposito: distingue este boton del
                     # botón "Habla con un especialista" del hero, que manda
                     # el mismo mensaje sin esa palabra.
                     WA_HEADER_TEXT="Hola%2C%20vi%20su%20p%C3%A1gina%20%28men%C3%BA%29%20y%20necesito%20ayuda%20con%20una%20plaga%20de%20termitas.",
                     # Defaults genericos (por si una futura pagina de servicio
                     # no los sobreescribe) - la landing de Termitas SI los
                     # sobreescribe, ver overrides en SERVICIOS arriba.
                     WA_VALUESTACK_TEXT=WA_HEADER_TEXT_GENERICO,
                     WA_CONTACTOFINAL_TEXT=WA_HEADER_TEXT_GENERICO,
                     WA_FOOTER_TEXT=WA_HEADER_TEXT_GENERICO)

PARTIAL_NAMES = ["analytics", "header", "footer", "main-js", "year-script"]
# Partials de contenido: secciones universales (mismo copy en cualquier landing
# de servicio futura), reusadas desde web/index.html pero SOLO inyectadas via
# marcadores en paginas de servicios/ (no en home/blog, que no las declaran).
SERVICE_PARTIAL_NAMES = ["trust-bar", "clientes", "mecanismo", "proof-counters",
                         "para-quien", "value-stack", "garantia", "cobertura",
                         "contacto-final", "cotizador-embed"]


def render(tpl, ctx):
    out = tpl
    for k, v in ctx.items():
        out = out.replace("{{%s}}" % k, v)
    return out


def load_partials(names):
    return {name: (PARTIALS / f"{name}.html").read_text(encoding="utf-8")
            for name in names}


def apply_markers(text, ctx, partials, names):
    for name in names:
        start = f"<!-- PARTIAL:{name}:start -->"
        end = f"<!-- PARTIAL:{name}:end -->"
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
        if not pattern.search(text):
            print(f"  [!] no encontre el marcador '{name}', lo salto (revisar a mano)")
            continue
        rendered = render(partials[name], ctx).rstrip("\n")
        replacement = f"{start}\n{rendered}\n{end}"
        text = pattern.sub(lambda _m, r=replacement: r, text, count=1)
    return text


CONTACT_PATTERNS = [
    (re.compile(r"tel:\+\d{10,11}"), lambda: f"tel:+{DATA['WA_DIGITS']}"),
    (re.compile(r"wa\.me/\d{10,11}"), lambda: f"wa.me/{DATA['WA_DIGITS']}"),
    (re.compile(r'"telephone":\s*"\+\d{10,11}"'), lambda: f'"telephone": "+{DATA["WA_DIGITS"]}"'),
    (re.compile(r"\+56\s9\s\d{4}\s\d{4}"), lambda: DATA["WA_DISPLAY"]),  # espacios OBLIGATORIOS: no debe tocar tel:+56936678897
    (re.compile(r"[\w.+-]+@aycmip\.cl"), lambda: DATA["EMAIL"]),
]


def sync_contact_fields():
    """Telefono/email no viven solo en header/footer: tambien aparecen sueltos
    en contenido unico de cada pagina (el CTA de cada blog/[plaga], los JSON-LD,
    etc). Estos son VALORES reconocibles por su formato (numero de telefono,
    email @aycmip.cl), no bloques identicos, asi que no se resuelven con el
    mecanismo de partials. Se buscan por patron (no por el valor viejo) y se
    normalizan al valor actual de _data.json, asi funciona aunque el numero ya
    haya cambiado varias veces. Recorre TODO .html bajo web/ automaticamente
    (no hay que registrar archivos nuevos aca, a diferencia de los partials)."""
    changed = []
    for f in sorted(WEB.rglob("*.html")):
        text = f.read_text(encoding="utf-8")
        new_text = text
        for pattern, repl in CONTACT_PATTERNS:
            new_text = pattern.sub(lambda _m, r=repl: r(), new_text)
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            changed.append(f.relative_to(WEB))
    if changed:
        print("contacto sincronizado en:", ", ".join(str(c) for c in changed))
    else:
        print("contacto: sin cambios de valor (ya estaba al dia)")


BUSINESS_TYPE_PATTERN = re.compile(r'"@type": "PestControlService"')

# El "name" del JSON-LD debe calzar con el nombre real de la ficha de Google
# Business Profile ("AYC MIP Manejo Integrado de Plagas") para consistencia
# NAP (name-address-phone) en SEO local - la marca visible del sitio se
# renombro a "A&C Control de Plagas" (2026-07-31), pero el schema.org se deja
# apuntando al nombre oficial de Google Business, que es un sistema aparte.
BUSINESS_NAME_PATTERN = re.compile(r'"name": "A&C Soluciones Agrícolas y Urbanas",')

# Direccion actual del LocalBusiness principal (solo aparece en home). Se
# saca streetAddress a proposito: FA prefiere representar la ubicacion via
# areaServed + addressLocality, no una direccion precisa (evita el problema
# de una direccion que solo existia en el JSON-LD y en ningun lado visible
# de la pagina). addressLocality queda en Quillota (no Calera, que es lo que
# hoy dice el perfil de Google Business por un tema de verificacion por
# carta que no se ha podido completar - son sistemas distintos, el schema
# del sitio no tiene por que arrastrar ese error).
HOME_ADDRESS_PATTERN = re.compile(
    r'"address": \{\s*"@type": "PostalAddress",\s*'
    r'"streetAddress": "San Martín #1106",\s*'
    r'"addressLocality": "Quillota",\s*'
    r'"addressRegion": "Valparaíso",\s*'
    r'"addressCountry": "CL"\s*\},'
)

SERVICE_AREA_PATTERN = re.compile(
    r'"areaServed": \{\s*"@type": "State",\s*"name": "Región de Valparaíso"\s*\}'
)


def sync_business_jsonld():
    """Normaliza 3 cosas en el JSON-LD, en TODO .html bajo web/ (por patron,
    igual que sync_contact_fields, no por partial - el bloque de home es
    unico y el de blog/servicios va anidado dentro de un Service que si
    varia por pagina, asi que no calzan con el mecanismo de partials):

    1. "@type": "PestControlService" -> "HomeAndConstructionBusiness". Ese
       tipo no existe en schema.org (404 en schema.org/PestControlService,
       no aparece como subtipo de HomeAndConstructionBusiness ni de ningun
       otro LocalBusiness) - HomeAndConstructionBusiness es el subtipo real
       mas cercano (LocalBusiness que presta servicios en/alrededor de
       casas y edificios, calza con control de plagas).
    2. address del LocalBusiness principal (solo en home, ver
       HOME_ADDRESS_PATTERN arriba).
    3. areaServed: de solo "Región de Valparaíso" (State) a region + las 7
       provincias + sus comunas (ver AREA_SERVED arriba).
    4. name: al nombre de la ficha de Google Business Profile (ver
       BUSINESS_NAME_PATTERN arriba) - queda distinto de la marca visible
       del sitio a propósito, para no romper la consistencia NAP.
    """
    changed = []
    area_served_json = json.dumps(AREA_SERVED, ensure_ascii=False, indent=4)
    new_home_address = (
        '"address": {\n'
        '    "@type": "PostalAddress",\n'
        '    "addressLocality": "Quillota",\n'
        '    "addressRegion": "Valparaíso",\n'
        '    "addressCountry": "CL"\n'
        '  },\n'
        '  "areaServed": ' + area_served_json + ','
    )
    for f in sorted(WEB.rglob("*.html")):
        text = f.read_text(encoding="utf-8")
        new_text = BUSINESS_TYPE_PATTERN.sub('"@type": "HomeAndConstructionBusiness"', text)
        new_text = HOME_ADDRESS_PATTERN.sub(lambda _m, r=new_home_address: r, new_text)
        new_text = SERVICE_AREA_PATTERN.sub(lambda _m, r='"areaServed": ' + area_served_json: r, new_text)
        new_text = BUSINESS_NAME_PATTERN.sub('"name": "AYC MIP Manejo Integrado de Plagas",', new_text)
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            changed.append(f.relative_to(WEB))
    if changed:
        print("JSON-LD (tipo/direccion/areaServed) sincronizado en:", ", ".join(str(c) for c in changed))
    else:
        print("JSON-LD: sin cambios (ya estaba al dia)")


def build_page_urls():
    """Lista de URLs canonicas del sitio, para robots.txt/sitemap.xml. Se
    arma sola a partir de PLAGAS y SERVICIOS (las mismas listas que ya
    gobiernan que paginas genera build()), asi que una pagina nueva
    agregada a esas listas entra aca sola, sin tocar nada mas."""
    urls = [DATA["SITE_URL"] + "/"]
    for plaga in PLAGAS:
        urls.append(f"{DATA['SITE_URL']}/blog/{plaga}/")
    for servicio in SERVICIOS:
        urls.append(f"{DATA['SITE_URL']}/servicios/{servicio['slug']}/")
    return urls


def write_seo_files():
    """robots.txt + sitemap.xml, generados enteros en cada build (no se
    editan a mano, mismo espiritu que los PARTIAL:xxx). Permite explicitamente
    a todos los bots, incluidos los de IA (GPTBot, ClaudeBot, PerplexityBot,
    Google-Extended, etc.) via el wildcard "User-agent: *" - no hay que
    listarlos uno por uno, el wildcard ya los cubre."""
    urls = build_page_urls()

    robots = (
        "# Generado por generador/build.py - no editar a mano, se pierde en el proximo build.\n"
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {DATA['SITE_URL']}/sitemap.xml\n"
    )
    (WEB / "robots.txt").write_text(robots, encoding="utf-8")

    entries = "\n".join(f"  <url>\n    <loc>{u}</loc>\n  </url>" for u in urls)
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!-- Generado por generador/build.py - no editar a mano, se pierde en el proximo build. -->\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
    (WEB / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"robots.txt + sitemap.xml regenerados ({len(urls)} URLs)")


def sync_js_constant(relpath, var_name, value, quote="'"):
    """Sincroniza una constante 'var NOMBRE = valor;' dentro de un .js. No es un
    partial (no es HTML), pero es otra fuente de verdad del telefono que hay
    que mantener igual a _data.json o queda desactualizada en silencio."""
    f = WEB / relpath
    text = f.read_text(encoding="utf-8")
    pattern = re.compile(r"var\s+" + re.escape(var_name) + r"\s*=\s*'[^']*';")
    new_text, n = pattern.subn(f"var {var_name} = {quote}{value}{quote};", text, count=1)
    if n == 0:
        print(f"  [!] no encontre 'var {var_name}' en {relpath}, revisar a mano")
    else:
        f.write_text(new_text, encoding="utf-8")


def sync_cotizador_wa_number():
    """cotizador.js:7 (WA_NUMBER) y main.js:12-13 (FA_WA_NUMBER, FA_TEL_NUMBER)
    son 2 archivos JS con su propia copia del telefono, ademas de todo lo que
    ya cubre sync_contact_fields() en el HTML. main.js ademas reescribe en el
    navegador (al cargar la pagina) cualquier <a href="wa.me/..."> o
    <a href="tel:..."> que encuentre, es una segunda red de seguridad en
    tiempo de ejecucion que ya existia antes de este build.py, se deja tal cual."""
    sync_js_constant("js/cotizador.js", "WA_NUMBER", DATA["WA_DIGITS"])
    sync_js_constant("js/cotizador-termitas.js", "WA_NUMBER", DATA["WA_DIGITS"])
    sync_js_constant("js/main.js", "FA_WA_NUMBER", DATA["WA_DIGITS"])
    sync_js_constant("js/main.js", "FA_TEL_NUMBER", "+" + DATA["WA_DIGITS"])
    print("js/cotizador*.js + js/main.js: constantes de telefono sincronizadas")


def build():
    partials = load_partials(PARTIAL_NAMES)
    service_partials = load_partials(SERVICE_PARTIAL_NAMES)

    home = WEB / "index.html"
    home_text = home.read_text(encoding="utf-8")
    home.write_text(apply_markers(home_text, HOME_CTX, partials, PARTIAL_NAMES), encoding="utf-8")
    print("index.html actualizado")

    for plaga in PLAGAS:
        f = WEB / "blog" / plaga / "index.html"
        text = f.read_text(encoding="utf-8")
        f.write_text(apply_markers(text, BLOG_CTX, partials, PARTIAL_NAMES), encoding="utf-8")
        print(f"blog/{plaga}/index.html actualizado")

    for servicio in SERVICIOS:
        slug = servicio["slug"]
        overrides = {k: v for k, v in servicio.items() if k not in ("slug", "ANALYTICS_PARTIAL")}
        ctx = dict(SERVICIO_CTX, **overrides)
        # Permite que una landing use un partial de analytics distinto al
        # generico (ej. tag de conversion de Google Ads en vez de GA4) sin
        # tocar el analytics.html compartido por las otras 10 paginas.
        analytics_name = servicio.get("ANALYTICS_PARTIAL", "analytics")
        page_partials = partials if analytics_name == "analytics" else \
            dict(partials, analytics=load_partials([analytics_name])[analytics_name])
        f = WEB / "servicios" / slug / "index.html"
        text = f.read_text(encoding="utf-8")
        text = apply_markers(text, ctx, page_partials, PARTIAL_NAMES)
        text = apply_markers(text, ctx, service_partials, SERVICE_PARTIAL_NAMES)
        f.write_text(text, encoding="utf-8")
        print(f"servicios/{slug}/index.html actualizado")

    sync_contact_fields()
    sync_cotizador_wa_number()
    sync_business_jsonld()
    write_seo_files()


if __name__ == "__main__":
    build()
    print("\nListo. Revisa los cambios con git diff antes de subir.")
