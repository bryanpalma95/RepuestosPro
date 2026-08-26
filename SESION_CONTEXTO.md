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

## Estado verificado en la base actual (actualizado)
- 3,275 vehículos
- 16,093 componentes
- 42 marcas (se eliminaron 3 registros fantasma Chrysler_Mopar/Dodge_Mopar/Ram_Mopar)
- Segmento más fuerte: Hyundai, Suzuki, Nissan, Volkswagen, Chevrolet, Toyota, Peugeot y Ford

## Progreso de recopilación de componentes (por marca, alfabético)
Método: componentes de MOTOR por familia (compartidos) + FRENOS/SUSPENSIÓN/NEUMÁTICOS por modelo/generación.
Refs OEM con fuente pública fiable = "confirmed"; sin PN público = "verify" (regla datos 100% fiables).
- A: Audi ✓ COMPLETA
- B: BMW (familia B38/B48, frenos por plataforma F30 vs UKL/G) ✓ · BAIC X55 ✓
- C: Changan ✓ · Chery (familia SQR) ✓ · Chevrolet (6 familias: Ecotec, F18D4, Sail/Spark, Isuzu diesel, V8, legacy) ✓
- D: Dongfeng ✓ (AMPLIADA: +8 modelos CIDEF Chile — T5 Evo, SX6, Aeolus GS Cross, Aeolus Y3, Mage PHEV, Mage EV, Huge, Rich 6) · DFSK Glory 580 ✓ · Daewoo Racer/Heaven ✓
- F: Fiat (Firefly, Fire, MultiJet) ✓ · Ford (Sigma/EcoBoost/Duratorq/Coyote V8) ✓
- SIGUIENTE: **G** → GAC, Geely, GWM (todas en estado mínimo, ~1 comp)
- Pendientes tras G: H (Haval, Honda, Hyundai), J, K (Kia casi vacía, 68 veh), L, M, N, O, P, R, S, T, V

## Flujo de build (IMPORTANTE — así llega a la web)
1. Escribir/ejecutar `insert_<marca>_componentes.py` → inserta en `db.sqlite` (patrón: clear_and_insert por vehículo, categorías→partes→refs→links)
2. `python export_db.py` → regenera `db.json` desde `db.sqlite`
3. Regenerar `db-nav.json` con script inline (reconstruye marca→modelo→años desde db.json)
4. git add db.json db-nav.json insert_*.py → commit → push origin main → GitHub Pages
NOTA: editar `componentes_oem_verificados.json` NO actualiza la web (solo alimenta componentes.db auxiliar). La fuente real de la web es db.sqlite→db.json.
Entorno Python: usar `.venv\Scripts\python.exe` (tiene openpyxl instalado).

## Funcionalidad de la web (ya implementada)
- Búsqueda bidireccional: buscar componente/referencia OEM → ver todos los vehículos compatibles (vista showComponent + db-compat.json con 95 refs del Excel)
- Tarjetas de componentes COLAPSADAS por defecto con botón "Ver compatibilidad"
- Carga rápida: db-nav.json (~30KB) instant + lazy load db.json al ver detalle
- Selector cascada Marca→Modelo→Año, años agrupados si >3
- Versionado en footer v0.9.1

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
