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

DATA = json.loads((HERE / "_data.json").read_text(encoding="utf-8"))

HOME_CTX = dict(DATA, ROOT="", HOME_LINK="#", HOME_ANCHOR="", PLAGA_PREFIX="blog/")
BLOG_CTX = dict(DATA, ROOT="../../", HOME_LINK="../../index.html",
                HOME_ANCHOR="../../index.html", PLAGA_PREFIX="../")

PARTIAL_NAMES = ["analytics", "header", "footer", "main-js", "year-script"]


def render(tpl, ctx):
    out = tpl
    for k, v in ctx.items():
        out = out.replace("{{%s}}" % k, v)
    return out


def load_partials():
    return {name: (PARTIALS / f"{name}.html").read_text(encoding="utf-8")
            for name in PARTIAL_NAMES}


def apply_markers(text, ctx, partials):
    for name in PARTIAL_NAMES:
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


def build():
    partials = load_partials()

    home = WEB / "index.html"
    home_text = home.read_text(encoding="utf-8")
    home.write_text(apply_markers(home_text, HOME_CTX, partials), encoding="utf-8")
    print("index.html actualizado")

    for plaga in PLAGAS:
        f = WEB / "blog" / plaga / "index.html"
        text = f.read_text(encoding="utf-8")
        f.write_text(apply_markers(text, BLOG_CTX, partials), encoding="utf-8")
        print(f"blog/{plaga}/index.html actualizado")


if __name__ == "__main__":
    build()
    print("\nListo. Revisa los cambios con git diff antes de subir.")
