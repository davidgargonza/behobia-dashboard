"""Asigna provincia y comunidad a cada procedencia (municipio) por coincidencia de nombre normalizado."""
import json, re, unicodedata
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"

def norm(s):
    s = unicodedata.normalize("NFD", s.upper())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

ARTS = ("LA", "EL", "LOS", "LAS", "L", "LES", "O", "A", "OS", "AS", "ES", "SA")

def variants(name):
    out = set()
    for part in re.split(r"[/-]| - ", name) + [name]:
        n = norm(part)
        if not n:
            continue
        out.add(n)
        m = re.match(r"(.*) (%s)$" % "|".join(ARTS), n)  # "LASTRILLA LA" -> "LA LASTRILLA"
        if m:
            out.add(f"{m.group(2)} {m.group(1)}")
            out.add(m.group(1))
        m = re.match(r"(%s) (.*)$" % "|".join(ARTS), n)
        if m:
            out.add(m.group(2))
    return out

FRANCE = {"HENDAYE", "HENDAIA", "BAYONNE", "BAIONA", "BIARRITZ", "ANGLET", "URRUGNE", "URRUÑA", "CIBOURE",
          "SAINT JEAN DE LUZ", "DONIBANE LOHIZUNE", "ASCAIN", "BIDART", "GUETHARY", "SAINT PEE SUR NIVELLE",
          "HASPARREN", "USTARITZ", "CAMBO LES BAINS", "PARIS", "BORDEAUX", "TOULOUSE", "PAU", "BOUCAU",
          "TARNOS", "ARCANGUES", "BOUCAU", "MOUGUERRE", "SAINT PIERRE D IRUBE", "VILLEFRANQUE", "BIRIATOU",
          "AHETZE", "ARBONNE", "LAHONCE", "LYON", "MARSEILLE", "LILLE", "NANTES", "MONTPELLIER", "DAX"}

def build():
    provs = {p["code"]: p for p in json.load(open(D / "geo_provincias.json"))}
    ccaa = {c["code"]: c["label"] for c in json.load(open(D / "geo_ccaa.json"))}
    idx = {}
    for m in json.load(open(D / "geo_poblaciones.json")):
        p = provs[m["parent_code"]]
        for v in variants(m["label"]):
            idx.setdefault(v, set()).add((p["label"], ccaa[p["parent_code"]]))
    for p in provs.values():  # capitales con nombre de provincia
        for v in variants(p["label"]):
            idx.setdefault(v, set()).add((p["label"], ccaa[p["parent_code"]]))
    return idx

def lookup(idx, name):
    vs = variants(name)
    if vs & FRANCE:
        return ("Francia", "Francia")
    hits = set()
    for v in vs:
        if v in idx and len(idx[v]) == 1:
            hits |= idx[v]
    if len(hits) == 1:
        return hits.pop()
    for v in vs:  # ambiguos: preferimos el País Vasco / Navarra (sesgo real de la carrera)
        for h in idx.get(v, ()):
            if h[1] in ("País Vasco", "Comunidad Foral de Navarra", "Navarra"):
                return h
    return None
