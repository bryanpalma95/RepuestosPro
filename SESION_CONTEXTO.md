# RepuestosPro — Contexto para nueva sesión

## Proyecto
- Catálogo de repuestos automotrices con datos JSON y publicación en GitHub Pages
- Repo: https://github.com/bryanpalma95/RepuestosPro
- Live: https://bryanpalma95.github.io/RepuestosPro/
- Carpeta local: c:\Users\brian\proyecto dominio gratis\DFM\

## Archivos clave
- `index.html` = frontend principal
- `catalogo.html` = vista de catálogo y filtros
- `db.json` = fuente principal del catálogo publicado
- `db-nav.json` = índice ligero para carga rápida
- `db.sqlite` = base interna de trabajo
- `export_db.py` = exporta la base a `db.json`
- `data.js` = fallback legacy

## Estado verificado en la base actual
- 3,246 vehículos
- 13,536 componentes
- 45 marcas
- Segmento más fuerte: Hyundai, Suzuki, Nissan, Volkswagen, Chevrolet, Toyota, Peugeot y Ford

## Flujo actual
- Actualizar la fuente de datos o scripts de importación
- Reconstruir/normalizar la base local
- Exportar a `db.json`
- Revisar cobertura por marca/modelo
- Publicar cambios y validar el frontend

## Estructura del catálogo
- Las entradas están organizadas por vehículo
- Cada vehículo incluye marca, modelo, año y categorías de componentes
- Los componentes contienen referencias, notas y compatibilidades cruzadas

## Web principal
- https://bryanpalma95.github.io/RepuestosPro/catalogo.html
- El catálogo está pensado para navegación rápida por marca, modelo y año
- La base real de referencia para el frontend es `db.json`

## Observaciones importantes
- La documentación antigua tenía métricas obsoletas; la fuente de verdad es la base actual
- El catálogo ya no se basa en dos o tres marcas de ejemplo, sino en una base mucho más amplia
- Los datos deben actualizarse desde la estructura real del proyecto, no desde versiones históricas de pruebas or versiones de sesión

## Regla operativa
1. La base actual debe ser la referencia para cualquier actualización de estado
2. Los cambios de contenido se deben validar con la estructura real del JSON
3. Los documentos del proyecto deben reflejar el estado actual y no cifras históricas obsoletas

## Mis autos y uso práctico
- AX4 Luxury 1.6 2019: motor PSA/DF1
- Joyear SX5 1.6 2022: motor 4A92 / Mitsubishi

## Mejoras pendientes del producto
- Selector más claro por marca/modelo
- Búsqueda predictiva
- Paginación por bloques
- Mejor visibilidad de compatibilidades y botón de detalle por componente
- Mejor organización por marca y por generación
