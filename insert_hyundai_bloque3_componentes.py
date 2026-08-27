# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Hyundai (BLOQUE 3: diesel comercial + hibrido/EV).
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_hyundai_bloque3_componentes.py
Fuentes publicas: oempartsonline, hyundaipartsdeal, amazon, mercadolibre.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
Familias BLOQUE 3:
  - D4CB 2.5 CRDi turbodiesel (Porter, H-1, Kia Frontier/K2500 gemelo)
  - Ioniq HEV Kappa 1.6 GDI hibrido + motor electrico
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
HOP = "https://hyundai.oempartsonline.com/"

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- D4CB 2.5 CRDi turbodiesel (Porter, H-1, Kia Frontier/K2500) ----------------
def diesel_d4cb(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 diesel sintetico", "~7L | D4CB 2.5 CRDi turbodiesel (ACEA C3)", "Hyundai/Kia, Mobil, Total",
          [("5W-30 diesel (ACEA C3)", "confirmed")], "c/10k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"aceite+5w30+diesel+d4cb")]),
        P("Motor", "Filtro Aceite", "Filtro aceite diesel D4CB", "Porter/H-1/H100/Starex/Kia K2500-Frontier", "Hyundai/Kia Genuine, MANN",
          [("26330-4A001", "confirmed"), ("26330-4A700", "confirmed")], "c/10k",
          [L("Amazon", AZ+"26330-4A001"), L("ML", ML+"filtro+aceite+26330+4a001")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "D4CB 2.5 CRDi", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"filtro+aire+hyundai+porter+diesel")]),
        P("Motor", "Filtro Combustible", "Filtro combustible diesel c/separador agua", "D4CB CRDi common-rail", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/20-40k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"filtro+combustible+diesel+hyundai+porter")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Porter/H-1/Frontier", "Hyundai/Kia Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"filtro+cabina+hyundai+h1")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado comercial", "Hyundai/Kia Genuine, Akebono",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"pastillas+freno+hyundai+porter")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+hyundai")]),
        P("Neumaticos", "Neumatico", neum, "Segun version comercial", "Bridgestone, Michelin, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- Ioniq HEV Kappa 1.6 GDI hibrido + motor electrico ----------------
def ioniq_hev(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 sintetico", "Kappa 1.6 GDI hibrido Atkinson", "Hyundai/Kia, Mobil, Shell",
          [("0W-20", "confirmed")], "c/10k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"aceite+0w20+hyundai+ioniq")]),
        P("Motor", "Filtro Aceite", "Filtro aceite gasolina/hibrido", "Hyundai/Kia 1.6 GDI", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed")], "c/10k",
          [L("Amazon", AZ+"26300-35505"), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Ioniq 1.6 GDI HEV", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"filtro+aire+hyundai+ioniq")]),
        P("Encendido", "Bujias", "Bujias iridio", "1.6 GDI hibrido", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"bujia+ngk+hyundai+ioniq")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Ioniq", "Hyundai/Kia Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"filtro+cabina+hyundai+ioniq")]),
        P("Alta Tension", "Sistema Hibrido/EV", "Bateria y sistema de alta tension", "Sistema hibrido/EV - revisar en concesionario", "Hyundai/Kia (servicio oficial)",
          [("Sistema hibrido/EV - revisar en concesionario", "verify")], None,
          [L("OEMPartsOnline", HOP), L("Hyundai", "https://www.hyundai.com/cl/es")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado - frenado regenerativo alarga vida util", "Hyundai/Kia Genuine, Akebono",
          [("Verificar OEM", "verify")], "c/50-80k",
          [L("OEMPartsOnline", HOP), L("ML", ML+"pastillas+freno+hyundai+ioniq")]),
        P("Neumaticos", "Neumatico", neum, "Segun version (eco/sport)", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


HYUNDAI_B3_MAP = {
    "hyundai-porter": (diesel_d4cb, "195 R14C"),
    "hyundai-h-1": (diesel_d4cb, "215/70 R16"),
    "hyundai-kia-frontier": (diesel_d4cb, "195 R15C"),
    "hyundai-ioniq": (ioniq_hev, "195/65 R15"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Hyundai %'").fetchall()
    n = 0; skipped = []
    for vid, name in rows:
        entry = HYUNDAI_B3_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        n += 1
    conn.commit()
    print("Hyundai B3 actualizados:", n)
    if skipped:
        print("Sin mapa (otro bloque):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
