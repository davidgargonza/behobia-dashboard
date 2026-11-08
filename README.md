# Behobia–San Sebastián 2026 · Dashboard de resultados

**Ver el dashboard:** https://raw.githack.com/davidgargonza/behobia-dashboard/main/index.html

`index.html` es un único archivo autocontenido (datos incluidos, sin dependencias externas).
Busca por nombre o dorsal y compara hasta 6 corredores: dónde iba cada uno en cada momento de la carrera (tiempo neto), tiempos de paso, ritmo por tramo y su lugar entre los 26.036 que llegaron.
El enlace admite parámetros para compartir, p. ej. `index.html#d=2,463,9200` (dorsales separados por comas).

Datos: clasificación **provisional** en directo de clasificacion.behobia-sansebastian.com (8/11/2026).

## Regenerar (p. ej. con la clasificación oficial)

```bash
python3 -I scripts/scrape.py 1 <total_resultados> data/corredores.csv   # tipoCarrera=1 corredores/as
python3 -I scripts/build_data.py
python3 -I scripts/build_html.py   # escribe index.html
```

`<total_resultados>` es el número que muestra la web en «Número total de resultados».

Tipografía: Archivo (SIL Open Font License), incrustada en el HTML desde `src/fonts/`.
