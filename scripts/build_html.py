"""Inserta data/dashboard.json en src/template.html -> index.html (un único archivo)."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
tpl = (ROOT / "src/template.html").read_text(encoding="utf-8")
data = (ROOT / "data/dashboard.json").read_text(encoding="utf-8").replace("</", "<\\/")
out = ROOT / "index.html"
out.write_text(tpl.replace("/*__DATA__*/null", data), encoding="utf-8")
print(out, out.stat().st_size // 1024, "KB")
