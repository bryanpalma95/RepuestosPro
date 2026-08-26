# RepuestosPro

Catálogo de repuestos automotrices con referencias OEM, compatibilidad cruzada y enlaces de compra.

**Live:** https://bryanpalma95.github.io/RepuestosPro/

## Estado actual (verificado contra db.json)

- 3,246 vehículos en el catálogo
- 13,536 entradas de componentes
- 45 marcas cubiertas
- Base de datos principal: `db.json`
- Cobertura más fuerte en Hyundai, Suzuki, Nissan, Volkswagen, Chevrolet, Toyota y Peugeot

## Stack

- HTML/CSS/JS vanilla
- JSON como fuente principal para el frontend
- SQLite local para gestión interna de datos
- Python para importación, generación y exportación

## Flujo de trabajo

```
1. Actualizar la fuente de datos o scripts de importación
2. Reconstruir/normalizar la base local
3. Exportar a db.json
4. Publicar el cambio y actualizar el frontend
```

## Scripts principales

| Script | Función |
|--------|---------|
| `setup_db.py` | Crear la estructura base de datos |
| `export_db.py` | Generar `db.json` desde la base local |
| `insert_lote_oem.py` | Cargar lotes de vehículos y componentes OEM |
| `generar_vins_full.py` | Generar VINs de referencia |
| `setup_componentes_db.py` | Crear la base auxiliar de familias y componentes |

## Datos verificados

Los números y referencias del catálogo se actualizan desde la base real del proyecto. La información contenida en `db.json` es la fuente de verdad para el sitio publicado.

## Nota sobre la calidad de datos

- La base actual incluye vehículos y componentes con referencias cruzadas
- El catálogo está orientado a compatibilidad entre modelos y marcas
- La estructura está diseñada para crecer por familias de motor y generaciones

## Autor

Bryan Palma — [@bryanpalma95](https://github.com/bryanpalma95)
