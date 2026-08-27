# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Jeep.
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_jeep_componentes.py  (luego export_db.py + _regen_nav.py)
Fuentes publicas: mopar, store.mopar, amazon, mercadolibre.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
Familias:
  - Tigershark 2.0/2.4 4cil MultiAir (Compass, Renegade, Cherokee 2.4, Journey 2.4)
  - Pentastar 3.2/3.6 V6 (Grand Cherokee, Wrangler, Gladiator, Durango, Cherokee V6, Pacifica)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
MOPAR = "https://www.mopar.com/"; STORE = "https://store.mopar.com/"

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- Tigershark 2.0/2.4 4cil (Compass, Renegade, Cherokee 2.4, Journey 2.4) ----------------
def tigershark_24(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 / 5W-20 sintetico", "~4.7L | Tigershark 2.0/2.4 MultiAir", "Mopar, Pennzoil",
          [("0W-20 / 5W-20", "confirmed")], "c/10k",
          [L("Mopar", MOPAR), L("ML", ML+"aceite+0w20+jeep")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Mopar", "Tigershark 2.0/2.4 (fits 2.0/2.4)", "Mopar, MANN",
          [("4892339", "confirmed")], "c/10k",
          [L("StoreMopar", STORE), L("ML", ML+"filtro+aceite+mopar+4892339")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Compass/Renegade/Cherokee 2.4", "Mopar, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("StoreMopar", STORE), L("ML", ML+"filtro+aire+jeep+compass")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "Tigershark 2.0/2.4", "NGK, Champion",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("StoreMopar", STORE), L("ML", ML+"bujia+ngk+jeep+compass")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Compass/Renegade/Cherokee/Journey", "Mopar",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("Amazon", AZ+"jeep+cabin+air+filter"), L("ML", ML+"filtro+cabina+jeep")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Mopar, Bosch",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("StoreMopar", STORE), L("ML", ML+"pastillas+freno+jeep+compass")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Mopar, Bosch",
          [("DOT4 (Mopar)", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+jeep")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Pentastar 3.2/3.6 V6 (Grand Cherokee, Wrangler, Gladiator, Durango, Cherokee V6, Pacifica) ----------------
def pentastar_v6(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 sintetico", "~5.7L | Pentastar 3.2/3.6 V6", "Mopar, Pennzoil",
          [("0W-20 (Pentastar)", "confirmed")], "c/10k",
          [L("Mopar", MOPAR), L("ML", ML+"aceite+0w20+jeep+pentastar")]),
        P("Motor", "Filtro Aceite", "Filtro aceite cartucho Mopar", "Pentastar 3.2/3.6 V6", "Mopar",
          [("68191349AC", "confirmed"), ("68191349AB / 68191349AA", "confirmed")], "c/10k",
          [L("StoreMopar", STORE), L("ML", ML+"filtro+aceite+mopar+68191349")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Grand Cherokee/Wrangler/Durango V6", "Mopar, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("StoreMopar", STORE), L("ML", ML+"filtro+aire+jeep+grand+cherokee")]),
        P("Encendido", "Bujias", "Bujias x6 iridio", "Pentastar V6", "NGK, Champion",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("StoreMopar", STORE), L("ML", ML+"bujia+ngk+jeep+pentastar")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Grand Cherokee/Wrangler/Durango", "Mopar",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("Amazon", AZ+"jeep+cabin+air+filter"), L("ML", ML+"filtro+cabina+jeep")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado SUV/pickup", "Mopar, Bosch",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("StoreMopar", STORE), L("ML", ML+"pastillas+freno+jeep+grand+cherokee")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Mopar, Bosch",
          [("DOT4 (Mopar)", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+jeep")]),
        P("Neumaticos", "Neumatico", neum, "SUV/pickup", "Michelin, BFGoodrich, Bridgestone",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


JEEP_MAP = {
    "jeep-compass": (tigershark_24, "225/60 R17"),
    "jeep-renegade": (tigershark_24, "215/60 R17"),
    "jeep-cherokee": (tigershark_24, "225/60 R17"),
    "jeep-grand-cherokee": (pentastar_v6, "265/60 R18"),
    "jeep-wrangler": (pentastar_v6, "255/70 R18"),
    "jeep-gladiator": (pentastar_v6, "255/70 R18"),
    "jeep-durango": (pentastar_v6, "265/60 R18"),
    "jeep-journey": (tigershark_24, "225/55 R19"),
    "jeep-pacifica": (pentastar_v6, "235/65 R17"),
}


def clear_and_insert(c, vid, comps):
    cats = c.execute("SELECT id FROM categories WHERE vehicle_id=?", (vid,)).fetchall()
    for (cid,) in cats:
        for (pid,) in c.execute("SELECT id FROM parts WHERE category_id=?", (cid,)).fetchall():
            c.execute("DELETE FROM part_refs WHERE part_id=?", (pid,)); c.execute("DELETE FROM part_links WHERE part_id=?", (pid,))
        c.execute("DELETE FROM parts WHERE category_id=?", (cid,))
    c.execute("DELETE FROM categories WHERE vehicle_id=?", (vid,))
    order = 0; cat_ids = {}
    for (cat, lab, nm, det, brands, refs, interval, links) in comps:
        if cat not in cat_ids:
            order += 1
            c.execute("INSERT INTO categories (vehicle_id,name,sort_order) VALUES (?,?,?)", (vid, cat, order)); cat_ids[cat] = c.lastrowid
        c.execute("INSERT INTO parts (category_id,cat_label,name,details,brands,interval_info) VALUES (?,?,?,?,?,?)",
                  (cat_ids[cat], lab, nm, det, brands, interval)); pid = c.lastrowid
        for (r, s) in refs: c.execute("INSERT INTO part_refs (part_id,reference,status) VALUES (?,?,?)", (pid, r, s))
        for l in links: c.execute("INSERT INTO part_links (part_id,label,url) VALUES (?,?,?)", (pid, l["t"], l["u"]))


def base_id(vid): return re.sub(r'-\d{4}$', '', vid)


def main():
    conn = sqlite3.connect(DB); conn.execute("PRAGMA foreign_keys=ON"); c = conn.cursor()
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Jeep %'").fetchall()
    n = 0; skipped = []
    for vid, name in rows:
        entry = JEEP_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        n += 1
    conn.commit()
    print("Jeep actualizados:", n)
    if skipped:
        print("Sin mapa (revisar):", sorted(set(base_id(s) for s in skipped)))
    mapped = sorted(set(base_id(vid) for vid, _ in rows if base_id(vid) in JEEP_MAP))
    missing = [k for k in JEEP_MAP if k not in mapped]
    print("Base IDs Jeep mapeados:", mapped)
    if missing:
        print("FALTAN base_id (no encontrados en vehicles):", missing)
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
