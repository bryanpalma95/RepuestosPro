# RepuestosPro

Catalogo de repuestos automotrices con referencias OEM verificadas, compatibilidad cruzada y links de compra.

**Live:** https://bryanpalma95.github.io/RepuestosPro/

## Estado actual

- 283 vehiculos en catalogo
- 1,100+ componentes con part numbers OEM
- 49 marcas cubiertas
- PWA instalable (funciona offline)

## Stack

- HTML/CSS/JS vanilla (sin frameworks)
- SQLite local (`db.sqlite`) para gestion de datos
- `db.json` exportado para el frontend (GitHub Pages)
- Python scripts para insercion y exportacion

## Flujo de trabajo

```
1. Editar/insertar datos en db.sqlite (via scripts Python)
2. python export_db.py  →  genera db.json
3. git add db.json && git commit && git push
4. GitHub Pages sirve el sitio actualizado
```

## Scripts principales

| Script | Funcion |
|--------|---------|
| `setup_db.py` | Crear estructura BD inicial |
| `export_db.py` | SQLite → db.json (para frontend) |
| `insert_lote_oem.py` | Insertar vehiculos con datos OEM verificados |
| `generar_vins_full.py` | Generar VINs de referencia (3214 modelos) |
| `setup_componentes_db.py` | BD auxiliar de componentes por familia motor |

## Datos verificados

Los part numbers OEM provienen de fuentes oficiales:
- oempartsonline.com (Toyota, Nissan, Honda, Ford, Hyundai, VW, Subaru)
- parts.vw.com, parts.subaru.com, parts.toyota.com
- store.mopar.com (Jeep/Dodge/Ram/Chrysler)
- amazon.com (listings Genuine OEM)
- Manuales oficiales del fabricante (mazdausa.com, owners-manual.mazda.com)

## Autor

Bryan Palma — [@bryanpalma95](https://github.com/bryanpalma95)
