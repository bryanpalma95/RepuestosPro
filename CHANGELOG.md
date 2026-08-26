# Changelog

## [0.9.1] - 2026-08-26

### Agregado
- 3,280 vehiculos individuales por ano (expansion completa)
- 348 part numbers OEM verificados en 154 familias de motor
- Selector cascada Marca → Modelo → Ano
- Seccion "Los mas buscados" con 12 modelos populares
- Buscador filtra grid en tiempo real
- Filtro inmediato al seleccionar marca o modelo
- Contador de resultados visible
- Lazy loading: carga inicial 26KB, datos completos solo al ver detalle
- Boton "Volver" en vista detalle
- Logo clickeable → volver al inicio

### Eliminado
- Service Worker / PWA offline (causaba cache problematico)
- Breadcrumb (innecesario)
- 341 vehiculos duplicados (entradas agrupadas reemplazadas por individuales)

### Corregido
- Tiempo de carga: de 2.8MB inicial a 26KB
- Stats en landing actualizados a datos reales

---

## [0.9.0] - 2026-08-26

### Agregado
- 5 vehiculos con datos OEM 100% verificados: Toyota Corolla 2020, Mazda CX-5 2022, Hyundai Tucson 2022, Honda CR-V 2022, VW Golf 2020
- Componentes con part number confirmed: filtro aceite, filtro aire, bujias, filtro cabina
- Links directos a fuentes de compra (Amazon OEM, AutoZone, oempartsonline)
- Notas de compatibilidad cruzada entre modelos
- Versionado en footer de index.html
- README.md y CHANGELOG.md

### Infraestructura
- 3214 VINs de referencia generados y validados contra NHTSA
- 154 familias de motor identificadas con filtro de aceite OEM
- Base de datos auxiliar (componentes.db) con estructura para 100 componentes x 154 familias
- Scripts de insercion por lotes (insert_lote_oem.py)

---

## [0.8.0] - 2026-08 (sesiones anteriores)

### Agregado
- Bloques 1-28 + clasicos: 278 vehiculos, 1085 componentes
- DFM AX4 2019 completo (componentes, fusibles, ficha tecnica)
- Joyear SX5 2022 completo
- Frontend PWA (catalogo.html + index.html)
- Service Worker para offline
- Buscador y filtros en catalogo
