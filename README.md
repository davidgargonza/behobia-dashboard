# Behobia–San Sebastián 2026 · Dashboard de resultados

**Ver el dashboard:** https://davidgargonza.github.io/behobia-dashboard/ (rama `gh-pages`, que solo contiene `index.html`; tras regenerar, copia `index.html` a esa rama)

`index.html` es un único archivo autocontenido (datos incluidos, sin dependencias externas).
Busca por nombre o dorsal y compara hasta 6 corredores: dónde iba cada uno en cada momento de la carrera (tiempo neto), tiempos de paso, ritmo por tramo y su lugar entre los 26.036 que llegaron.


Datos: clasificación oficial de clasificacion.behobia-sansebastian.com (8/11/2026; la organización aún la marca como provisional).

## Regenerar

```bash
python3 -I scripts/scrape_oficial.py 2026 <total> data/oficial.csv            # clasificación oficial
python3 -I scripts/scrape_oficial.py 2026 <total_mujeres> data/oficial_mujeres.csv 2
python3 -I scripts/merge_oficial.py      # añade la hora de salida del directo (data/directo.csv)
python3 -I scripts/build_data.py
python3 -I scripts/build_html.py         # index.html
python3 -I scripts/build_og.py && node scripts/screenshot_og.js   # og.png
```

Los totales son los que muestra oficial.php en «Número total de resultados». Después, copia `index.html` y `og.png` a la rama `gh-pages`.

Tipografía: Archivo (SIL Open Font License), incrustada en el HTML desde `src/fonts/`.

`data/perfil.json`: altitud cada 100 m, digitalizada del perfil del dossier técnico oficial 2026 (pág. 11). Desnivel positivo resultante: 193 m (oficial: 192 m).

Miniatura para compartir: `python3 -I scripts/build_og.py && node scripts/screenshot_og.js` genera `og.png`; cópiala a la rama `gh-pages` junto a `index.html`.
