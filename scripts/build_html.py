"""Inserta datos y tipografía en src/template.html -> index.html (un único archivo, sin dependencias)."""
import base64
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
tpl = (ROOT / "src/template.html").read_text(encoding="utf-8")
data = (ROOT / "data/dashboard.json").read_text(encoding="utf-8").replace("</", "<\\/")
font = lambda f: base64.b64encode((ROOT / "src/fonts" / f).read_bytes()).decode()
out = ROOT / "index.html"
html = (tpl.replace("/*__FONT_LATIN__*/", font("archivo-latin.woff2"))
           .replace("/*__FONT_LATIN_EXT__*/", font("archivo-latin-ext.woff2"))
           .replace("/*__DATA__*/null", data))
out.write_text(html, encoding="utf-8")
print(out, out.stat().st_size // 1024, "KB")
