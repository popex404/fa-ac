"""
generador/  = herramienta de construccion. NUNCA se le pasa a Miguel.
web/        = lo unico deployable, el .zip que se le manda a Miguel sale de aqui.

Regenera las secciones compartidas (header, footer, analytics, main.js, year-script)
dentro de web/index.html y web/blog/*/index.html, a partir de
generador/_partials/ + generador/_data.json.

Uso: python build.py   (desde generador/, o desde donde sea, la ruta a web/ es fija)
Editar SOLO los archivos en _partials/ (o _data.json para el numero de WhatsApp,
GA4, Clarity, email). Nunca editar a mano el contenido entre los marcadores
<!-- PARTIAL:xxx:start --> ... <!-- PARTIAL:xxx:end --> en web/index.html o
web/blog/*/index.html, se pierde en el proximo build.
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
SERVICIOS = ["exterminio-y-fumigacion-de-plagas-de-termitas"]

DATA = json.loads((HERE / "_data.json").read_text(encoding="utf-8"))

HOME_CTX = dict(DATA, ROOT="", HOME_LINK="#", HOME_ANCHOR="", PLAGA_PREFIX="blog/",
                SERVICIO_PREFIX="servicios/", SERVICIOS_GRID_ANCHOR="#servicios")
BLOG_CTX = dict(DATA, ROOT="../../", HOME_LINK="../../index.html",
                HOME_ANCHOR="../../index.html", PLAGA_PREFIX="../",
                SERVICIO_PREFIX="../../servicios/",
                SERVICIOS_GRID_ANCHOR="../../index.html#servicios")
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
                     SERVICIOS_GRID_ANCHOR="../../index.html#servicios")

PARTIAL_NAMES = ["analytics", "header", "footer", "main-js", "year-script"]
# Partials de contenido: secciones universales (mismo copy en cualquier landing
# de servicio futura), reusadas desde web/index.html pero SOLO inyectadas via
# marcadores en paginas de servicios/ (no en home/blog, que no las declaran).
SERVICE_PARTIAL_NAMES = ["trust-bar", "clientes", "mecanismo", "proof-counters",
                         "para-quien", "value-stack", "garantia",
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
    sync_js_constant("js/main.js", "FA_WA_NUMBER", DATA["WA_DIGITS"])
    sync_js_constant("js/main.js", "FA_TEL_NUMBER", "+" + DATA["WA_DIGITS"])
    print("js/cotizador.js + js/main.js: constantes de telefono sincronizadas")


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

    for slug in SERVICIOS:
        f = WEB / "servicios" / slug / "index.html"
        text = f.read_text(encoding="utf-8")
        text = apply_markers(text, SERVICIO_CTX, partials, PARTIAL_NAMES)
        text = apply_markers(text, SERVICIO_CTX, service_partials, SERVICE_PARTIAL_NAMES)
        f.write_text(text, encoding="utf-8")
        print(f"servicios/{slug}/index.html actualizado")

    sync_contact_fields()
    sync_cotizador_wa_number()


if __name__ == "__main__":
    build()
    print("\nListo. Revisa los cambios con git diff antes de subir.")
