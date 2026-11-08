"""Limpia data/corredores.csv y genera data/dashboard.json (formato columnar compacto)."""
import csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import geo

ROOT = Path(__file__).resolve().parent.parent
CCAA_NAME = {"Asturias, Principado de": "Asturias", "Balears, Illes": "Illes Balears", "Cataluńa": "Cataluña",
             "Castilla - La Mancha": "Castilla-La Mancha", "Madrid, Comunidad de": "C. de Madrid",
             "Murcia, Región de": "Región de Murcia", "Navarra, Comunidad Foral de": "Navarra",
             "Rioja, La": "La Rioja", "Comunitat Valenciana": "C. Valenciana"}
PROV_NAME = {"Gipuzkoa/Guipúzcoa": "Gipuzkoa", "Bizkaia/Vizcaya": "Bizkaia", "Araba/Álava": "Araba/Álava"}
MANUAL = {  # municipios/barrios frecuentes que no casan con el INE
    "ALGORTA": ("Bizkaia", "País Vasco"), "SOPELANA": ("Bizkaia", "País Vasco"), "SODUPE": ("Bizkaia", "País Vasco"),
    "USANSOLO": ("Bizkaia", "País Vasco"), "PASAI ANTXO": ("Gipuzkoa", "País Vasco"),
    "PASAI SAN PEDRO": ("Gipuzkoa", "País Vasco"), "PASAI DONIBANE": ("Gipuzkoa", "País Vasco"),
    "RENTERIA": ("Gipuzkoa", "País Vasco"), "AÑORGA": ("Gipuzkoa", "País Vasco"), "AKARTEGI": ("Gipuzkoa", "País Vasco"),
    "AGINAGA (USURBIL)": ("Gipuzkoa", "País Vasco"),
    "SARRIGUREN": ("Navarra", "Navarra"), "GORRAIZ": ("Navarra", "Navarra"), "ELIZONDO": ("Navarra", "Navarra"),
    "MUTILVA ALTA": ("Navarra", "Navarra"), "MUTILVA BAJA": ("Navarra", "Navarra"), "CIZUR MENOR": ("Navarra", "Navarra"),
    "ORCOYEN": ("Navarra", "Navarra"), "IRURITA": ("Navarra", "Navarra"), "ARTICA": ("Navarra", "Navarra"),
    "ERRATZU": ("Navarra", "Navarra"), "ELBETE": ("Navarra", "Navarra"), "LEGASA": ("Navarra", "Navarra"),
    "MENDILLORRI": ("Navarra", "Navarra"), "CASTEJON": ("Navarra", "Navarra"),
    "PALMA DE MALLORCA": ("Illes Balears", "Illes Balears"), "ALCUDIA": ("Illes Balears", "Illes Balears"),
    "CORRO D'AVALL": ("Illes Balears", "Illes Balears"), "MATAS, LAS": ("Madrid", "C. de Madrid"),
    "ALCOBENDAS Y LA MORALEJA": ("Madrid", "C. de Madrid"), "VALDEMORO": ("Madrid", "C. de Madrid"),
    "ARROYOMOLINOS": ("Madrid", "C. de Madrid"), "SAN AGUSTIN DE GUADALIX": ("Madrid", "C. de Madrid"),
    "BUITRAGO DE LOZOYA": ("Madrid", "C. de Madrid"), "SANTA COLOMA DE GRAMANET": ("Barcelona", "Cataluña"),
    "CALAHORRA": ("La Rioja", "La Rioja"), "TORRENT": ("Valencia/València", "C. Valenciana"),
    "VINAR?S": ("Castellón/Castelló", "C. Valenciana"), "VILLARREAL": ("Castellón/Castelló", "C. Valenciana"),
    "PUERTO DE SAGUNTO": ("Valencia/València", "C. Valenciana"), "GRANADA": ("Granada", "Andalucía"),
    "LAPUEBLA DE LABARKA": ("Araba/Álava", "País Vasco"), "LAGUNA,LA": ("Santa Cruz de Tenerife", "Canarias"),
    "VIRGEN DEL CAMINO, LA": ("León", "Castilla y León"), "VILLARCAYO": ("Burgos", "Castilla y León"),
    "POLA DE SIERO": ("Asturias", "Asturias"), "LUANCO": ("Asturias", "Asturias"), "MIERES": ("Asturias", "Asturias"),
    "GARRAPINILLOS": ("Zaragoza", "Aragón"),
}
FR = {"LEOGNAN", "TALENCE", "BRISCOUS", "BASSUSSARRY", "MERIGNAC", "BEGLES", "SANGUINET", "LARRESSORE", "LABENNE",
      "PESSAC", "URCUIT", "CAPBRETON", "MONT-DE-MARSAN", "CASTANET-TOLOSAN", "LIBOURNE", "BILLERE", "IDRON",
      "ONDRES", "LA TESTE-DE-BUCH", "LONS", "ESPELETTE", "LEVIGNAC", "MIMIZAN"}
ABROAD = {"LONDON": "Reino Unido", "LONDRES": "Reino Unido", "FIRENZE": "Italia", "ESCALDES": "Andorra",
          "ANDORRA LA VELLA": "Andorra", "ENCAMP": "Andorra"}
# Orden por edad (de menor a mayor). Los rangos exactos dependen del reglamento de cada edición.
CAT_ORDER = ["JUNIOR", "PROMESA", "SENIOR", "VETERANO/A", "VETERANO/A II", "VETERANO/A III", "VETERANO/A IV"]
CAT_MAP = {"JUNIOR M": "JUNIOR", "JUNIOR F": "JUNIOR", "PROMESA M": "PROMESA", "PROMESA F": "PROMESA",
           "SENIOR M": "SENIOR", "SENIOR F": "SENIOR", "VETERANO": "VETERANO/A", "VETERANA": "VETERANO/A",
           "VETERANO II": "VETERANO/A II", "VETERANA II": "VETERANO/A II", "VETERANO III": "VETERANO/A III",
           "VETERANA III": "VETERANO/A III", "VETERANO IV": "VETERANO/A IV", "VETERANA IV": "VETERANO/A IV"}

def sec(t):
    if not t or t == "00:00:00":
        return 0
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s

def main():
    idx = geo.build()
    rows = list(csv.DictReader(open(ROOT / "data/corredores.csv", encoding="utf-8")))
    cats, towns, provs, ccaas = [], [], [], []
    def code(lst, v):
        if v not in lst:
            lst.append(v)
        return lst.index(v)
    for c in CAT_ORDER:
        code(cats, c)
    cols = {k: [] for k in ["d", "n", "s", "c", "g", "o", "p", "a", "t", "t5", "t10", "t15", "st", "pos"]}
    for r in rows:
        t = sec(r["tiempo"])
        st = sec(r["hora_salida"])
        valid = 0 < t < 4 * 3600 and st > 0
        town = r["procedencia"].strip() or "(sin dato)"
        if town in MANUAL:
            prov, ccaa = MANUAL[town]
        elif town in FR:
            prov, ccaa = "Francia", "Francia"
        elif town in ABROAD:
            prov = ccaa = ABROAD[town]
        else:
            h = geo.lookup(idx, town)
            prov, ccaa = (PROV_NAME.get(h[0], h[0]), CCAA_NAME.get(h[1], h[1])) if h else ("Sin identificar", "Sin identificar")
        cols["d"].append(int(r["dorsal"]))
        cols["n"].append(f'{r["nombre"]} {r["apellidos"]}'.replace("  ", " ").strip())
        cols["s"].append(0 if r["sexo"] == "HOMBRE" else 1)
        cols["c"].append(code(cats, CAT_MAP.get(r["categoria"], r["categoria"])))
        cols["g"].append(r["categoria"])  # categoría original
        cols["o"].append(code(towns, town))
        cols["p"].append(code(provs, prov))
        cols["a"].append(code(ccaas, ccaa))
        cols["t"].append(t if valid else 0)
        for k in ("t5", "t10", "t15"):
            v = sec(r[k])
            cols[k].append(v if valid and 0 < v < t else 0)
        cols["st"].append(st)
        cols["pos"].append(int(r["pos"]) if r["pos"] not in ("", "0") else 0)
    gcats = sorted(set(cols["g"]))
    cols["g"] = [gcats.index(g) for g in cols["g"]]
    out = {"meta": {"edicion": 61, "fecha": "2026-11-08", "distancia_km": 20,
                    "fuente": "clasificacion.behobia-sansebastian.com (clasificación provisional en directo)"},
           "cats": cats, "gcats": gcats, "towns": towns, "provs": provs, "ccaas": ccaas, "cols": cols}
    (ROOT / "data/dashboard.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    import collections
    print(len(rows), "válidos:", sum(1 for t in cols["t"] if t))
    print(collections.Counter(ccaas[a] for a in cols["a"]).most_common())

main()
