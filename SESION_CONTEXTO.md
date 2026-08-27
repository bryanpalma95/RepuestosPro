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
- 16,867 componentes
- 42 marcas (se eliminaron 3 registros fantasma Chrysler_Mopar/Dodge_Mopar/Ram_Mopar)
- Avance global: ~53% vehículos completos (>=5 comps). Marcas 100%: 14/42 (A-G + Haval + Honda).
- Segmento más fuerte: Hyundai, Suzuki, Nissan, Volkswagen, Chevrolet, Toyota, Peugeot y Ford

## Progreso de recopilación de componentes (por marca, alfabético)
Método: componentes de MOTOR por familia (compartidos) + FRENOS/SUSPENSIÓN/NEUMÁTICOS por modelo/generación.
Refs OEM con fuente pública fiable = "confirmed"; sin PN público = "verify" (regla datos 100% fiables).
- A: Audi ✓ COMPLETA
- B: BMW (familia B38/B48, frenos por plataforma F30 vs UKL/G) ✓ · BAIC X55 ✓
- C: Changan ✓ · Chery (familia SQR) ✓ · Chevrolet (6 familias: Ecotec, F18D4, Sail/Spark, Isuzu diesel, V8, legacy) ✓
- D: Dongfeng ✓ (AMPLIADA: +8 modelos CIDEF Chile — T5 Evo, SX6, Aeolus GS Cross, Aeolus Y3, Mage PHEV, Mage EV, Huge, Rich 6) · DFSK Glory 580 ✓ · Daewoo Racer/Heaven ✓
- F: Fiat (Firefly, Fire, MultiJet) ✓ · Ford (Sigma/EcoBoost/Duratorq/Coyote V8) ✓
- G: GAC (GS4 1.5T 4B15J1) ✓ · Geely (Coolray 1.5T JLH-3G15TD, plataforma BMA) ✓ · GWM (Tank 300 + Dargo, motor GW4C20B 2.0T — comparte mecánica con Haval) ✓
  └─ Refs confirmed clave: Geely filtro aceite OEM 1016056847/1056022300, bujía NGK ILKFR8B7G (91602), pastillas OE 4048046400, DCT Shell Spirax S5 DCT10. GAC/GWM PN sin fuente pública = verify.
  └─ Script: insert_g_componentes.py. Resultado: GAC 8 veh, Geely 7 veh, GWM 10 veh actualizados. Totales 16,093 → 16,260 (+167).
- H (por marca, un script cada una):
  └─ Haval ✓ COMPLETA (32 veh) — familias GW4: GW4C20B 2.0T (H6/Dargo/Tank 300), GW4B15 1.5T (Jolion), GW4D20 2.0D diesel (Poer). Script: insert_haval_componentes.py. Totales 16,260 → 16,445 (+185).
  └─ Honda ✓ COMPLETA (98 veh, 8 comps c/u) — familias: L15B7 1.5T turbo (Civic/CR-V/Accord), L15 1.5 aspirado (City/Fit/HR-V), J35 3.5 V6 (Pilot/Ridgeline). K24 disponible en script pero no mapeada. Script: insert_honda_componentes.py. Totales 16,445 → 16,867 (+422). Refs confirmed: aceite 15400-PLM-A02 / 15400-RTA-003, aire 17220-5AA-A00 / 17220-R5A-A00, bujia NGK DXE22HCR11S / DILKAR8P8SY, cabina 80292-SDA-407 / 80292-TF0-G01.
  └─ SIGUIENTE en H: Hyundai (291 veh, 25 modelos; varios ya en 9 comps). Refs confirmed listas: filtro aceite Hyundai/Kia 26300-35505, aire Elantra 28113-AA100, cabina 97133-L1000. OJO: hay gemelos Kia mezclados (Carnival, Cerato, Morning, Sorento, Sportage, Seltos, Frontier) — al hacer Kia (letra K) reutilizar familias.
- Pendientes tras H: J, K (Kia casi vacía, 68 veh), L, M, N, O, P, R, S, T, V
- Nota: `_regen_nav.py` automatiza el paso 3 del build (regenera db-nav.json desde db.json; marca = primera palabra del nombre). Reutilizable en próximas tandas.

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

## Excel dinámico (SOLO LOCAL, no se sube a git)
- `RepuestosPro_Catalogo_Dinamico.xlsx` (~870 KB) generado por `generar_excel_dinamico.py`
- Regenerar: `.venv\Scripts\python.exe generar_excel_dinamico.py` (acepta nombre de salida opcional como arg)
- Hojas: INICIO (portada/guía, sin fórmulas) · Componentes (20.152 filas, 1 por ref OEM) · Compatibilidad OEM (95) · Indice Referencias (305, cruces >=2 veh) · Resumen por Marca (42)
- Buscador = AutoFiltro nativo de cada tabla (compatible con todo Excel/LibreOffice/Sheets)
- IMPORTANTE: NO usar fórmulas FILTER/array dinámico con openpyxl — Excel las marca como corruptas y las elimina (openpyxl no escribe la metadata de spill). Por eso INICIO es texto puro y la búsqueda va por AutoFiltro.
- Ambos archivos (.xlsx y generador) quedan untracked a propósito.

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
