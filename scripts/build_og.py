"""Genera og.html (1200x630) para la miniatura al compartir. Después: node scripts/screenshot_og.js -> og.png"""
import base64, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "data/dashboard.json").read_text(encoding="utf-8")); C = D["cols"]
P = json.loads((ROOT / "data/perfil.json").read_text())
N = len(C["d"]); val = [i for i in range(N) if C["t"][i] > 0]
win = [min((i for i in val if C["s"][i] == s), key=lambda i: C["t"][i]) for s in (0, 1)]
def km_at(i, T):
    if T >= C["t"][i]: return 20.0
    pts = [(0, 0)] + [(C[k][i], d) for k, d in (("t5", 5), ("t10", 10), ("t15", 15)) if C[k][i] > 0] + [(C["t"][i], 20)]
    for (t0, d0), (t1, d1) in zip(pts, pts[1:]):
        if T <= t1: return d0 + (d1 - d0) * (T - t0) / (t1 - t0)
def hms(s): return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"
import csv
NOM = {int(r["dorsal"]): (r["nombre"], r["apellidos"]) for r in csv.DictReader(open(ROOT / "data/corredores.csv", encoding="utf-8"))}
def name(i):  # nombre de pila y primer apellido
    n, a = NOM[C["d"][i]]; return " ".join(w.capitalize() for w in (n.split()[0] + " " + a.split()[0]).lower().split())
T = C["t"][win[0]]; kw = km_at(win[1], T)
# perfil en SVG
W, X0, X1, TOP, BASE = 1200, 64, 1136, 330, 560
x = lambda k: X0 + k / 20 * (X1 - X0); y = lambda e: BASE - e / 90 * (BASE - TOP)
elev = lambda k: P[min(200, int(k * 10))] + (P[min(200, int(k * 10) + 1)] - P[min(200, int(k * 10))]) * (k * 10 - int(k * 10))
path = f"M{x(0)},{BASE} " + " ".join(f"L{x(k/10):.1f},{y(P[k]):.1f}" for k in range(201)) + f" L{x(20)},{BASE} Z"
altos = "".join(f'<text x="{x(k):.0f}" y="{y(elev(k)) - 16:.0f}" class="alto">{n} · {round(elev(k))} m</text>' for k, n in ((7.3, "Gaintxurizketa"), (13, "Kaputxinoak"), (16.8, "Miracruz")))
dots = "".join(f'<circle cx="{x(k):.1f}" cy="{y(elev(k)):.1f}" r="13" fill="{c}" stroke="#ECEDE9" stroke-width="4"/>' for k, c in ((20, "#2a78d6"), (kw, "#eb6834")))
dots += f'<text x="{x(kw) + 18:.1f}" y="{y(elev(kw)) - 16:.1f}" class="who">{name(win[1]).split()[0]}</text><text x="{x(20):.1f}" y="{y(elev(20)) - 92:.1f}" class="who" text-anchor="end">{name(win[0]).split()[0]}</text><line x1="{x(20):.1f}" x2="{x(20):.1f}" y1="{y(elev(20)) - 86:.1f}" y2="{y(elev(20)) - 16:.1f}" stroke="#16181B" stroke-width="1.5"/>'
font = lambda f: base64.b64encode((ROOT / "src/fonts" / f).read_bytes()).decode()
caption = f"Cuando {name(win[0])} ganó en {hms(T)}, {name(win[1])} iba por el km {kw:.1f}".replace(".", ",")
html = f"""<!doctype html><html lang="es"><meta charset="utf-8"><style>
@font-face {{ font-family: Archivo; font-weight: 100 900; font-stretch: 62% 125%; src: url(data:font/woff2;base64,{font("archivo-latin.woff2")}) format("woff2"); }}
html, body {{ margin: 0; width: 1200px; height: 630px; background: #ECEDE9; color: #16181B; font-family: Archivo; overflow: hidden; }}
h1 {{ position: absolute; left: 64px; top: 52px; margin: 0; font-size: 92px; line-height: .92; font-weight: 800; font-stretch: 66%; letter-spacing: -0.02em; }}
p {{ position: absolute; left: 64px; top: 224px; margin: 0; font-size: 30px; color: #43474D; max-width: 1000px; }}
.k {{ display: inline-flex; align-items: center; gap: 10px; margin-right: 26px; }}
.k i {{ width: 18px; height: 18px; border-radius: 3px; display: inline-block; }}
svg {{ position: absolute; left: 0; top: 0; }}
text {{ font-family: Archivo; }}
.alto {{ font-size: 22px; font-weight: 650; fill: #16181B; text-anchor: middle; }}
.ax {{ font-size: 20px; fill: #43474D; }}
.who {{ font-size: 20px; font-weight: 650; fill: #16181B; }}
</style><body>
<h1>Behobia – San Sebastián 2026</h1>
<p>{caption}. Compara a quien quieras, kilómetro a kilómetro.</p>
<svg width="1200" height="630" viewBox="0 0 1200 630">
<path d="{path}" fill="#2B2E32"/>
{"".join(f'<line x1="{x(k)}" x2="{x(k)}" y1="{y(elev(k)):.1f}" y2="{BASE}" stroke="#ECEDE9" stroke-width="3" opacity=".6"/>' for k in (5, 10, 15))}
{altos}{dots}
<text x="{X0}" y="{BASE + 34}" class="ax">Behobia</text><text x="{X1}" y="{BASE + 34}" class="ax" text-anchor="end">Donostia</text>
<text x="{x(5)}" y="{BASE + 34}" class="ax" text-anchor="middle">km 5</text><text x="{x(10)}" y="{BASE + 34}" class="ax" text-anchor="middle">km 10</text><text x="{x(15)}" y="{BASE + 34}" class="ax" text-anchor="middle">km 15</text>
</svg></body></html>"""
(ROOT / "og.html").write_text(html, encoding="utf-8")
print(caption)
