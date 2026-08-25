# RepuestosPro — Contexto para nueva sesión

## Proyecto
- Catálogo repuestos automotrices, HTML estático + JSON, GitHub Pages
- Repo: https://github.com/bryanpalma95/RepuestosPro
- Live: https://bryanpalma95.github.io/RepuestosPro/
- Carpeta local: c:\Users\brian\proyecto dominio gratis\DFM\

## Archivos clave
- index.html = Frontend (carga db.json con fetch)
- db.json = Datos para frontend (SE SUBE a git)
- db.sqlite = BD local (NO se sube, .gitignore)
- export_db.py = SQLite a db.json
- data.js = Fallback legacy

## Flujo: insertar en sqlite → python export_db.py → git add db.json → git commit → git push

## Estado: 267 vehiculos, 1043 componentes (bloques 1-28 COMPLETOS)

## Pendiente: CATALOGO COMPLETO. Enriquecer datos existentes (mas refs confirmadas, mas categorias por vehiculo)

## Bloques pendientes (13-28):
- 13: Chevrolet Optra, D-Max, Onix, Cavalier, Tahoe, Suburban, Montana, Spin, Prisma + VW Virtus
- 14: VW Jetta, Bora, Tiguan, T-Cross, Nivus, Taos, Vento + Peugeot 3008, 5008, Rifter
- 15: Renault Captur, Arkana, Oroch, Koleos, Alaskan, Megane + Fiat Mobi, Argo, Cronos, Pulse
- 16: Fiat Ducato, Jeep Wrangler, Gladiator, Renegade, Cherokee, Dodge Durango, Journey + Chrysler Pacifica, Kia Carnival, Ram 700
- 17: Ram 1000, 1500, 2500 + Toyota Raize, Rush, Avanza, Auris, Prius, C-HR, Yaris Sport
- 18: Nissan Murano, Juke, V16, D21, Urvan + Toyota Hiace + Hyundai H-1, Verna, Atos, Veloster
- 19: Hyundai Sonata, Venue, Palisade, Ioniq + Kia Optima, Stonic, Seltos, Niro, Telluride + Chevrolet Silverado
- 20: Suzuki Ignis, S-Cross, Ertiga, XL7, Dzire + Mazda CX-3, CX-30, CX-9 + Subaru Legacy, WRX
- 21: Subaru Evoltis + Mitsubishi Lancer, ASX, Eclipse Cross, L300 + Honda Pilot, Ridgeline + Chery Tiggo 4, 7, Arrizo 3, 5
- 22: MG 5, 6, Marvel R, ZX Plus + Changan UNI-T, UNI-K, CS55, Hunter, Alsvin + Haval Jolion, Dargo
- 23: GWM Tank 300 + JAC S2, S3, JS2, JS3, JS4, JS8, T6, Sunray + Jetour X70
- 24: Jetour Dashing, Omoda C5, Exeed LX, TXL + Maxus G10, V80, Deliver 9 + DFSK Glory 580, 560 + BAIC X35, X55
- 25: Shineray G01, KYC Mamut, JMC Vigus + Dongfeng Joyear X3, T5L + BMW Serie 1, 3, X1, X3, X5
- 26: Mercedes A, C, E, GLA, GLC, Sprinter + Audi A3, A4, Q3, Q5 + Volvo V40, XC40, XC60
- 27: Lexus NX, Porsche Macan/Cayenne + Land Rover Evoque + Seat Ibiza/Leon + Skoda Fabia/Octavia + Opel Corsa/Astra/Mokka
- 28: Mini Cooper, Fiat 500, Alfa Giulietta + Ford Edge, Bronco Sport, Mustang, Transit + Samsung SM3 + Brilliance + GAC GS3/GS4

## Cruces clave:
- Kappa (Hyundai/Kia): Morning=i10=Eon → filtro MANN W 811/80
- Gamma: Accent=Rio=Soluto=Elantra=Creta=i30=Cerato → filtro 26300-35504
- HR16DE (Nissan): Versa=Tiida=March=Kicks=Qashqai → filtro 15208-65F0E, bujia LZKAR6AP-11 = DFM
- Skyactiv (Mazda): 3=CX-5=6 → filtro SH01-14-302A
- PSA: 208=2008=308=301=Partner=Berlingo=C3=DFM AX4 → filtro 1109.CK
- K serie (Suzuki): Swift=Baleno=Ignis → filtro MANN W 67/2
- Fire (Fiat): Palio=Uno=Fiorino=Strada → correa 50-60k
- 4A9x (Mitsubishi): SX5=Mirage=Lancer=ASX → filtro MZ690115

## Mis autos:
- AX4 Luxury 1.6 2019: LCVT13, Motor J0247199, 215/50R17, PSA/DF1
- Joyear SX5 1.6 2022: RTJX69, Motor S3MP284 (4A92), 215/60R16, bomba 1300A095, CKP 1865A126

## Reglas:
1. Nunca excluir info existente
2. Min 3 enlaces por componente
3. Indicar compatibilidades cruzadas
4. confirmed/verify en refs
5. Export+commit+push post cada bloque
6. Push autorizado libremente


## MEJORAS UI/UX PENDIENTES (implementar al inicio próxima sesión):

### Prioridad 1 (hacer primero):
1. **Selector en cascada Marca → Modelo** (reemplazar dropdown de 122+ opciones)
2. **Buscador predictivo** con autocompletado (mostrar sugerencias al escribir)
3. **Paginación** (20 tarjetas + botón "Cargar más")

### Prioridad 2:
4. **Botón "Ver Repuestos"** visible en cada tarjeta
5. **Hover mejorado** en cards (sombra + escala sutil)
6. **Contraste** en notas de compatibilidad (texto más oscuro o fondo coloreado)

### Prioridad 3:
7. Logos de marcas en tarjetas
8. Iconos para cadena/correa/motor/diesel
9. Filtros sidebar (diesel/gasolina, cadena/correa, tipo vehículo)
10. "Vehículos vistos recientemente" en sidebar
