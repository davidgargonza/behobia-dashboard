"""Une la clasificación oficial con datos que solo da el directo (hora de salida) -> data/corredores.csv"""
import csv
from pathlib import Path
D = Path(__file__).resolve().parent.parent / "data"
live = {r["dorsal"]: r for r in csv.DictReader(open(D / "directo.csv", encoding="utf-8"))}
women = {r["dorsal"] for r in csv.DictReader(open(D / "oficial_mujeres.csv", encoding="utf-8"))}
clean = lambda t: "" if t in ("*", "-", "") else t
COLS = ["pos", "nombre", "apellidos", "tiempo", "dorsal", "sexo", "categoria", "procedencia", "hora_salida", "pos_salida", "t5", "p5", "t10", "p10", "t15", "p15"]
with open(D / "corredores.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, COLS); w.writeheader()
    for r in csv.DictReader(open(D / "oficial.csv", encoding="utf-8")):
        lv = live.get(r["dorsal"], {})
        w.writerow({"pos": r["pos"], "nombre": r["nombre"], "apellidos": r["apellidos"], "tiempo": clean(r["tiempo"]) if r["pos"] else "",
                    "dorsal": r["dorsal"], "sexo": "MUJER" if r["dorsal"] in women else "HOMBRE", "categoria": r["categoria"],
                    "procedencia": r["procedencia"], "hora_salida": lv.get("hora_salida", ""), "pos_salida": lv.get("pos_salida", ""),
                    "t5": clean(r["t5"]), "p5": "", "t10": clean(r["t10"]), "p10": "", "t15": clean(r["t15"]), "p15": ""})
