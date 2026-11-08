# Behobia–San Sebastián 2026 · Dashboard de resultados

**Ver el dashboard:** https://raw.githack.com/davidgargonza/behobia-dashboard/main/index.html

`index.html` es un único archivo autocontenido (datos incluidos, sin dependencias externas).
Filtros por nombre/dorsal, sexo, categoría y procedencia; distribución de tiempos, edad, procedencia, splits y hora de salida.
El enlace admite parámetros para compartir, p. ej. `index.html#dorsal=1234`.

Datos: clasificación **provisional** en directo de clasificacion.behobia-sansebastian.com (8/11/2026).

## Regenerar (p. ej. con la clasificación oficial)

```bash
python3 -I scripts/scrape.py 1 <total_resultados> data/corredores.csv   # tipoCarrera=1 corredores/as
python3 -I scripts/build_data.py
python3 -I scripts/build_html.py   # escribe index.html
```

`<total_resultados>` es el número que muestra la web en «Número total de resultados».
