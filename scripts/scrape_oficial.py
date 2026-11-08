"""Descarga la clasificación oficial (oficial.php) de un año a CSV. Uso: scrape_oficial.py AÑO TOTAL destino.csv [sexo]"""
import csv, html, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = ("https://clasificacion.behobia-sansebastian.com/oficial.php?lang=es&accion=buscar&tipo=1&ano={y}&categoria=&sexo={s}"
        "&nombre=&apellido=&localidad=&dorsal=&paginacion={o}&siguiente=1")
COLS = ["pos", "nombre", "apellidos", "tiempo", "t5", "t10", "t15", "dorsal", "categoria", "pos_cat", "procedencia"]
ROW = re.compile(r"<tr>(.*?)</tr>", re.S); TD = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
NAME = re.compile(r'class="name">(.*?)</span>.*?class="surname">(.*?)</span>', re.S)

def fetch(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (behobia-dashboard)"})
            return urllib.request.urlopen(req, timeout=30).read().decode("latin-1")
        except Exception:
            time.sleep(2 ** i)
    raise RuntimeError(url)

def parse(page):
    body = page.split("<tbody>", 1)[-1].split("</tbody>", 1)[0]; out = []
    for r in ROW.findall(body):
        tds = [html.unescape(re.sub("<[^>]+>", "", t)).strip() for t in TD.findall(r)]
        if len(tds) < 11: continue
        m = NAME.search(TD.findall(r)[2]); nom, ape = (html.unescape(m.group(1)).strip(), html.unescape(m.group(2)).strip()) if m else ("", tds[2])
        out.append([tds[1], nom, ape, tds[3], tds[4], tds[5], tds[6], tds[7], tds[8], tds[9], tds[10]])
    return out

def main(year, total, dest, sexo=""):
    rows = {}
    with ThreadPoolExecutor(6) as ex:
        for o, r in ex.map(lambda o: (o, parse(fetch(BASE.format(y=year, s=sexo, o=o)))), range(0, total + 20, 20)):
            rows[o] = r
    with open(dest, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(COLS)
        for o in sorted(rows): w.writerows(rows[o])

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
