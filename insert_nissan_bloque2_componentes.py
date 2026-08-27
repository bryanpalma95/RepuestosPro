# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Nissan - BLOQUE 2 (SUV/CROSSOVER GASOLINA + V6).
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_nissan_bloque2_componentes.py
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
Bloque 2 (SUV/crossover):
  - nissan-juke       (HR16 1.6 / MR16DDT 1.6T turbo)
  - nissan-qashqai    (MR20 2.0 / HR13 1.3T turbo)
  - nissan-x-trail    (MR20 2.0 / QR25 2.5)
  - nissan-murano     (VQ35 3.5 V6 - bujias x6)
  - nissan-pathfinder (VQ35 3.5 V6 - bujias x6)
db.sqlite compartida con procesos paralelos; clear_and_insert borra solo por vehicle_id.
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- Familia SUV/crossover Nissan ----------------
def nissan_suv(neum, det, bujias_n=4):
    aire_ref = ("16546-17B00", "confirmed") if det == "juke" else ("Verificar OEM", "verify")
    motor_nota = {
        "juke": "HR16 1.6 / MR16DDT 1.6T turbo",
        "qashqai": "MR20 2.0 / HR13 1.3T turbo",
        "x-trail": "MR20 2.0 / QR25 2.5",
        "murano": "VQ35 3.5 V6",
        "pathfinder": "VQ35 3.5 V6",
    }[det]
    q = det if det != "x-trail" else "x+trail"
    return [
        P("Motor", "Aceite", "Aceite 5W-30 / 0W-20 sintetico", motor_nota, "Nissan Genuine, MANN",
          [("5W-30 / 0W-20", "confirmed")], "c/10k",
          [L("ML", ML+"aceite+5w30+nissan+"+q)]),
        P("Motor", "Filtro Aceite", "Filtro aceite Nissan", motor_nota, "Nissan Genuine, MANN",
          [("15208-65F0E", "confirmed")], "c/10k",
          [L("Amazon", AZ+"15208-65F0E"), L("ML", ML+"filtro+aceite+15208+65f0e")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", motor_nota, "Nissan Genuine, MANN",
          [aire_ref], "c/15-30k",
          [L("Amazon", AZ+("16546-17B00" if det == "juke" else "filtro+aire+nissan+"+q)), L("ML", ML+"filtro+aire+nissan+"+q)]),
        P("Encendido", "Bujias", "Bujias x%d iridio" % bujias_n, motor_nota, "NGK, Denso",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("ML", ML+"bujia+ngk+nissan+"+q)]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", motor_nota, "Nissan Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+nissan+"+q)]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado SUV/crossover", "Nissan Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+nissan+"+q)]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Nissan, Bosch",
          [("DOT4", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+dot4+nissan")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


NISSAN_B2_MAP = {
    "nissan-juke": (nissan_suv, "215/55 R17", "juke", 4),
    "nissan-qashqai": (nissan_suv, "215/60 R17", "qashqai", 4),
    "nissan-x-trail": (nissan_suv, "225/60 R18", "x-trail", 4),
    "nissan-murano": (nissan_suv, "235/55 R20", "murano", 6),
    "nissan-pathfinder": (nissan_suv, "255/60 R18", "pathfinder", 6),
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
    n = 0; skipped = []; mapped = []
    for vid, name in rows:
        entry = NISSAN_B2_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum, det, bujias_n = entry
        clear_and_insert(c, vid, gen(neum, det, bujias_n))
        n += 1; mapped.append(base_id(vid))
    conn.commit()
    print("Nissan (bloque 2) actualizados:", n)
    print("Base_id mapeados:", sorted(set(mapped)))
    if skipped:
        print("Sin mapa (otros bloques Nissan, correcto):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
