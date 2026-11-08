"""Descarga la clasificación (provisional en directo) de la Behobia-San Sebastián a CSV."""
import csv, html, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://clasificacion.behobia-sansebastian.com/clasificacion-live.php?lang=es&accion=buscar&tipoCarrera={t}&paginacion={o}&siguiente=1"
COLS = ["pos", "nombre", "apellidos", "tiempo", "dorsal", "sexo", "categoria", "procedencia",
        "hora_salida", "pos_salida", "t5", "p5", "t10", "p10", "t15", "p15"]
ROW = re.compile(r"<tr>(.*?)</tr>", re.S)
TD = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
NAME = re.compile(r'class="name">(.*?)</span>.*?class="surname">(.*?)</span>', re.S)

def fetch(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (behobia-dashboard)"})
            return urllib.request.urlopen(req, timeout=30).read().decode("latin-1")
        except Exception as e:
            time.sleep(2 ** i)
    raise RuntimeError(url)

def parse(page):
    body = page.split("<tbody>", 1)[-1].split("</tbody>", 1)[0]
    out = []
    for r in ROW.findall(body):
        tds = TD.findall(r)
        if len(tds) < 15:
            continue
        m = NAME.search(tds[1])
        nom, ape = (m.group(1), m.group(2)) if m else ("", tds[1])
        vals = [tds[0], nom, ape] + tds[2:15]
        out.append([html.unescape(re.sub("<[^>]+>", "", v)).strip() for v in vals])
    return out

def main(tipo, total, dest):
    offsets = range(0, total + 20, 20)
    def job(o):
        return o, parse(fetch(BASE.format(t=tipo, o=o)))
    rows = {}
    with ThreadPoolExecutor(6) as ex:
        for n, (o, r) in enumerate(ex.map(job, offsets)):
            rows[o] = r
            if n % 100 == 0:
                print(f"{o}/{total}", file=sys.stderr)
    with open(dest, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for o in sorted(rows):
            w.writerows(rows[o])

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
