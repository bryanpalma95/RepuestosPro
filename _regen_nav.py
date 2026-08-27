# -*- coding: utf-8 -*-
"""Regenera db-nav.json desde db.json: marca -> modelo -> [anios].
Nombre de vehiculo esperado: 'Marca Modelo — AAAA'."""
import json, os, re

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, 'db.json'), encoding='utf-8') as f:
    data = json.load(f)

# Convencion del proyecto: la marca es SIEMPRE la primera palabra del nombre
# (p.ej. 'BMW Mini Cooper' -> marca BMW / modelo 'Mini Cooper'; 'Range Rover ...' -> marca Range).
nav = {}
for vid, v in data.items():
    name = v.get("name", "")
    # separar "Marca Modelo — AAAA"
    m = re.match(r'^(.*?)\s+[—-]\s+(\d{4})$', name)
    if not m:
        continue
    left, year = m.group(1).strip(), m.group(2)
    parts = left.split()
    brand = parts[0]
    model = " ".join(parts[1:]) if len(parts) > 1 else brand
    nav.setdefault(brand, {}).setdefault(model, [])
    if year not in nav[brand][model]:
        nav[brand][model].append(year)

for brand in nav:
    for model in nav[brand]:
        nav[brand][model].sort()

# ordenar marcas y modelos alfabeticamente para salida estable
nav_sorted = {b: {mdl: nav[b][mdl] for mdl in sorted(nav[b])} for b in sorted(nav)}

with open(os.path.join(base, 'db-nav.json'), 'w', encoding='utf-8') as f:
    json.dump(nav_sorted, f, ensure_ascii=False)

print("Marcas:", len(nav_sorted))
print("Modelos:", sum(len(m) for m in nav_sorted.values()))
for b in ("GAC", "Geely", "GWM"):
    print(b, "->", nav_sorted.get(b))
