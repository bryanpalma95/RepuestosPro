"""
RepuestosPro - Generador de VINs COMPLETO (3218 modelos)
=========================================================
Lee el archivo modelos_vehiculos.txt y genera 1 VIN por cada
combinacion marca/modelo/ano.

Uso:
    python generar_vins_full.py                     # Todos (3218)
    python generar_vins_full.py --marca Toyota      # Solo una marca
    python generar_vins_full.py --count             # Solo contar modelos

Salida: vins_completo.json (para uso programatico)
        vins_completo.md   (para referencia humana)
"""

import json
import os
import random
import time
import sys

# ============================================================
# WMI (World Manufacturer Identifier) por marca
# ============================================================
WMI_POR_MARCA = {
    "Nissan": ["JN1", "3N1", "1N4", "5N1", "JN8", "MNT"],
    "Toyota": ["JTD", "JTE", "JTN", "2T1", "4T1", "5TD", "5TF", "MR0"],
    "Chevrolet": ["1G1", "1GC", "2G1", "3G1", "KL1", "9BG", "LSG", "MAJ"],
    "Subaru": ["JF1", "JF2", "4S3", "4S4"],
    "Suzuki": ["JS1", "JS2", "JS3", "JSA", "TSM", "MHF"],
    "Kia": ["KNA", "KND", "5XX", "U5Y"],
    "Fiat": ["ZFA", "9BD", "3FA"],
    "Peugeot": ["VF3", "VR3"],
    "Volkswagen": ["WVW", "WV1", "WV2", "3VW", "9BW"],
    "Daewoo": ["KLA", "KLT"],
    "Audi": ["WAU", "WA1"],
    "BMW": ["WBA", "WBS", "WBY", "5UX"],
    "BAIC": ["LA0"],
    "Changan": ["LS4", "LVZ"],
    "Chery": ["LVV", "LWV"],
    "Chrysler": ["1C3", "2C3"],
    "Citroen": ["VF7", "VR7"],
    "DFSK": ["LGJ"],
    "DFM": ["LGJ", "LDC"],
    "Dodge": ["1C4", "2C3", "3C4", "3D7"],
    "Dongfeng": ["LGJ", "LDC"],
    "Ford": ["1FA", "1FD", "1FM", "1FT", "2FM", "3FA", "MAJ", "MNB"],
    "GAC": ["LEA"],
    "Geely": ["L6T"],
    "GWM": ["LGX", "LZG"],
    "Haval": ["LGX"],
    "Honda": ["JHM", "1HG", "2HG", "5J6", "19X", "93H"],
    "Hyundai": ["KMH", "5NP", "5NM", "KMF", "MAL"],
    "JAC": ["LJ1"],
    "Jeep": ["1C4", "1J4", "1J8"],
    "Jetour": ["LVV"],
    "JMC": ["LJZ"],
    "Lexus": ["JTJ", "JTH", "2T2"],
    "Maxus": ["LSG"],
    "Mazda": ["JM1", "JMZ", "3MZ", "1YV"],
    "Mercedes": ["WDB", "WDC", "WDD", "55S", "4JG"],
    "MG": ["LSJ", "LSD"],
    "Mini": ["WMW"],
    "Mitsubishi": ["JA3", "JA4", "JMB", "JMY", "MMB", "MMC"],
    "Omoda": ["LVV"],
    "Opel": ["W0L"],
    "Porsche": ["WP0", "WP1"],
    "Ram": ["1C6", "3C6", "3D7"],
    "Range Rover": ["SAL"],
    "Renault": ["VF1", "VF6", "93Y"],
    "Seat": ["VSS"],
    "Skoda": ["TMB"],
    "SsangYong": ["KPT", "KPA"],
    "Volvo": ["YV1", "YV4"],
    # Citro\u00ebn variante
    "Citro\u00ebn": ["VF7", "VR7"],
}

# Caracteres validos VIN (sin I, O, Q)
VIN_CHARS = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
VIN_NUMERIC = "0123456789"

WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

TRANSLITERATION = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
    'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

YEAR_CODES = {
    1990: 'L', 1991: 'M', 1992: 'N', 1993: 'P', 1994: 'R',
    1995: 'S', 1996: 'T', 1997: 'V', 1998: 'W', 1999: 'X',
    2000: 'Y', 2001: '1', 2002: '2', 2003: '3', 2004: '4',
    2005: '5', 2006: '6', 2007: '7', 2008: '8', 2009: '9',
    2010: 'A', 2011: 'B', 2012: 'C', 2013: 'D', 2014: 'E',
    2015: 'F', 2016: 'G', 2017: 'H', 2018: 'J', 2019: 'K',
    2020: 'L', 2021: 'M', 2022: 'N', 2023: 'P', 2024: 'R',
    2025: 'S', 2026: 'T', 2027: 'V', 2028: 'W', 2029: 'X',
    2030: 'Y',
}


def calcular_checksum(vin):
    """Calcula el digito verificador (posicion 9) de un VIN."""
    total = 0
    for i, char in enumerate(vin):
        if i == 8:
            continue
        value = TRANSLITERATION.get(char, 0)
        total += value * WEIGHTS[i]
    remainder = total % 11
    return 'X' if remainder == 10 else str(remainder)


def generar_vin(marca, year):
    """Genera un VIN sintetico valido para marca y ano."""
    wmis = WMI_POR_MARCA.get(marca, None)
    if not wmis:
        for key in WMI_POR_MARCA:
            if key.lower() == marca.lower():
                wmis = WMI_POR_MARCA[key]
                break
    if not wmis:
        wmis = ["1ZZ"]

    wmi = random.choice(wmis)
    vds = ''.join(random.choice(VIN_CHARS) for _ in range(5))
    check = '0'
    year_code = YEAR_CODES.get(year, 'A')
    plant = random.choice(VIN_CHARS)
    seq = ''.join(random.choice(VIN_NUMERIC) for _ in range(6))

    vin = wmi + vds + check + year_code + plant + seq
    check = calcular_checksum(vin)
    vin = vin[:8] + check + vin[9:]
    return vin


def parsear_modelos_desde_texto(texto):
    """
    Parsea el archivo de modelos con formato TSV:
    Marca  Modelo  Ano  Motor  ...
    Retorna lista de tuplas (marca, modelo, year, motor)
    """
    modelos = []
    for linea in texto.strip().split('\n'):
        linea = linea.strip()
        if not linea:
            continue
        if linea.startswith("Marca") and "Modelo" in linea:
            continue

        partes = linea.split('\t')
        if len(partes) < 3:
            partes = linea.split(None, 3)
            if len(partes) < 3:
                continue

        marca = partes[0].strip()
        modelo = partes[1].strip()
        try:
            year = int(partes[2].strip())
        except ValueError:
            continue

        motor = partes[3].strip() if len(partes) > 3 else "-"

        if marca and modelo and 1980 <= year <= 2030:
            modelos.append((marca, modelo, year, motor))

    return modelos


def main():
    print("=" * 60)
    print("RepuestosPro - Generador VINs COMPLETO")
    print("=" * 60)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Buscar archivo de modelos
    archivo_modelos = None
    posibles = [
        os.path.join(script_dir, "modelos_vehiculos.txt"),
        os.path.join(script_dir, "..", "modelos_vehiculos.txt"),
        os.path.join(script_dir, "modelos.txt"),
    ]
    for p in posibles:
        if os.path.exists(p):
            archivo_modelos = p
            break

    if not archivo_modelos:
        print("ERROR: No se encontro archivo de modelos.")
        print("Guardar la lista como uno de estos archivos:")
        for p in posibles:
            print(f"  - {p}")
        print("\nFormato esperado (TSV):")
        print("  Marca\\tModelo\\tAno\\tMotor")
        print("  Toyota\\tCorolla\\t2020\\t1.8L 2ZR-FE")
        sys.exit(1)

    print(f"Leyendo: {archivo_modelos}")
    with open(archivo_modelos, 'r', encoding='utf-8') as f:
        texto = f.read()

    modelos = parsear_modelos_desde_texto(texto)

    # Filtrar por marca
    marca_filter = None
    if "--marca" in sys.argv:
        idx = sys.argv.index("--marca")
        if idx + 1 < len(sys.argv):
            marca_filter = sys.argv[idx + 1]
            modelos = [(m, mod, y, mot) for m, mod, y, mot in modelos
                       if m.lower() == marca_filter.lower()]

    if "--count" in sys.argv:
        print(f"\nTotal modelos: {len(modelos)}")
        marcas = set(m for m, _, _, _ in modelos)
        print(f"Marcas unicas: {len(marcas)}")
        for marca in sorted(marcas):
            count = sum(1 for m, _, _, _ in modelos if m == marca)
            print(f"  {marca}: {count}")
        return

    print(f"\nTotal modelos a procesar: {len(modelos)}")
    print("-" * 60)

    # Generar 1 VIN por modelo
    resultados = {}
    marcas_sin_wmi = set()

    for i, (marca, modelo, year, motor) in enumerate(modelos, 1):
        if i % 500 == 0 or i == len(modelos):
            print(f"  [{i}/{len(modelos)}] procesando...")

        vin = generar_vin(marca, year)
        key = f"{marca}|{modelo}|{year}"
        resultados[key] = {
            "marca": marca,
            "modelo": modelo,
            "year": year,
            "motor": motor,
            "vin": vin
        }

        if marca not in WMI_POR_MARCA:
            found = False
            for k in WMI_POR_MARCA:
                if k.lower() == marca.lower():
                    found = True
                    break
            if not found:
                marcas_sin_wmi.add(marca)

    # Exportar JSON
    json_path = os.path.join(script_dir, "vins_completo.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    # Exportar Markdown agrupado por marca
    md_path = os.path.join(script_dir, "vins_completo.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# VINs de Referencia - Catalogo Completo RepuestosPro\n\n")
        f.write(f"> Total: {len(resultados)} modelos con VIN de referencia\n")
        f.write(f"> Generado: {time.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")

        por_marca = {}
        for key, data in sorted(resultados.items()):
            marca = data["marca"]
            if marca not in por_marca:
                por_marca[marca] = []
            por_marca[marca].append(data)

        for marca in sorted(por_marca.keys()):
            items = por_marca[marca]
            f.write(f"## {marca} ({len(items)} modelos)\n\n")
            f.write("| Modelo | Ano | Motor | VIN |\n")
            f.write("|--------|-----|-------|-----|\n")

            for item in sorted(items, key=lambda x: (x["modelo"], x["year"])):
                f.write(f"| {item['modelo']} | {item['year']} | {item['motor']} | `{item['vin']}` |\n")

            f.write("\n---\n\n")

        f.write("## Como usar estos VINs\n\n")
        f.write("1. Copiar VIN del modelo deseado\n")
        f.write("2. Decodificar en:\n")
        f.write("   - NHTSA: `https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{VIN}?format=json`\n")
        f.write("   - vindecoderz.com / en.vindecoder.pl\n")
        f.write("3. Buscar componentes en catalogos OEM:\n")
        f.write("   - 7zap.com, partsouq.com, megazip.net (multi-marca)\n")
        f.write("   - parts.toyota.com, parts.nissan.com, epc.hyundai.com\n")
        f.write("4. Marcas chinas: Alibaba, autodoc.co.uk, distribuidores locales\n\n")

        if marcas_sin_wmi:
            f.write("## Marcas sin WMI registrado (VIN generico)\n\n")
            for m in sorted(marcas_sin_wmi):
                f.write(f"- {m}\n")

    print("\n" + "=" * 60)
    print("[OK] COMPLETADO")
    print(f"  > JSON: {json_path}")
    print(f"  > MD:   {md_path}")
    print(f"  > Total modelos: {len(resultados)}")
    print(f"  > Marcas unicas: {len(por_marca)}")
    if marcas_sin_wmi:
        print(f"  > Marcas sin WMI: {', '.join(sorted(marcas_sin_wmi))}")
    print("=" * 60)


if __name__ == "__main__":
    main()
