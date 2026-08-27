# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados Nissan Bloque 3 (diesel / pickup / van).
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_nissan_bloque3_componentes.py
Fuentes publicas: nissan genuine parts, mann, bosch, trw.
Regla: solo se marca "confirmed" un PN/tipo con fuente publica fiable; sin PN publico = "verify".
Diesel: sin bujias. Aceite/DOT4 confirmed por tipo; resto verify (no inventar PN).
Familias:
  - nissan_diesel: turbodiesel Nissan (D21 TD27/TD25, D21 NP300 YD25, NP300 Navara YD25/YS23, Urvan YD25)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- Diesel turbodiesel Nissan (D21 / NP300 / Navara / Urvan) ----------------
def nissan_diesel(neum, det):
    aceite = "15W-40 diesel" if "TD27" in det or "TD25" in det else "5W-30 / 5W-40 diesel"
    return [
        P("Motor", "Aceite", "Aceite " + aceite, det, "Nissan Genuine, MANN",
          [(aceite, "confirmed")], "c/10k",
          [L("ML", ML+"aceite+"+aceite.split()[0].lower()+"+nissan+diesel"), L("Amazon", AZ+"aceite+"+aceite.split()[0].lower()+"+diesel")]),
        P("Motor", "Filtro Aceite", "Filtro aceite motor", det, "Nissan Genuine, MANN",
          [("Verificar OEM", "verify")], "c/10k",
          [L("ML", ML+"filtro+aceite+nissan+diesel"), L("Amazon", AZ+"filtro+aceite+nissan+diesel")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", det, "Nissan Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+nissan+diesel"), L("Amazon", AZ+"filtro+aire+nissan+diesel")]),
        P("Motor", "Filtro Combustible", "Filtro combustible diesel c/separador de agua", det, "Nissan Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+combustible+diesel+nissan+separador+agua"), L("Amazon", AZ+"filtro+combustible+diesel+nissan")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", det, "Nissan Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+nissan"), L("Amazon", AZ+"filtro+cabina+nissan")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado pickup/van", "Bosch, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+nissan"), L("Amazon", AZ+"pastillas+freno+nissan")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, TRW",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+nissan"), L("Amazon", AZ+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, BFGoodrich",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


NISSAN_B3_MAP = {
    "nissan-d21": (nissan_diesel, "235/75 R15", "TD27 / TD25 turbodiesel"),
    "nissan-d21-np300": (nissan_diesel, "245/70 R16", "YD25 DDTi turbodiesel"),
    "nissan-np300-navara": (nissan_diesel, "255/70 R16", "YD25 / YS23 DDTi turbodiesel"),
    "nissan-urvan": (nissan_diesel, "195 R15C", "YD25 DDTi turbodiesel"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Nissan %'").fetchall()
    n = 0; skipped = []
    for vid, name in rows:
        entry = NISSAN_B3_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum, det = entry
        clear_and_insert(c, vid, gen(neum, det))
        n += 1
    conn.commit()
    print("Nissan B3 actualizados:", n)
    if skipped:
        print("Sin mapa (otros bloques, correcto):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
