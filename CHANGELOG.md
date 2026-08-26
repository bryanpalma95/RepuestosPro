# Changelog

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
