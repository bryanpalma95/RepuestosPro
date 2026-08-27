# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Nissan - BLOQUE 1 (gasolina compactos).
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_nissan_bloque1_componentes.py
Fuentes publicas: nissanpartsdeal, amazon, mercadolibre.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
Bloque 1 (motores HR/MR/QG/GA gasolina compactos):
  - nissan-versa   (HR16 1.6)
  - nissan-tiida   (HR16 1.6 / MR18)
  - nissan-march   (HR12 1.2 / HR16 1.6)
  - nissan-sentra  (MRA8 1.8 / MR20 2.0)
  - nissan-kicks   (HR16 1.6)
  - nissan-v16     (GA16 1.6 clasico - sedan antiguo muy popular en Chile/taxis)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
NPN = "https://www.nissanpartsdeal.com/"

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- Nissan gasolina (compactos HR/MR/QG) ----------------
def nissan_gasolina(neum, det):
    aceite = det.get("aceite", "5W-30 / 0W-20")
    aceite_status = det.get("aceite_status", "confirmed")
    fa_ref = det.get("filtro_aire_ref", "Verificar OEM")
    fa_status = det.get("filtro_aire_status", "verify")
    q = det.get("q", "nissan")
    return [
        P("Motor", "Aceite", "Aceite " + aceite + " sintetico", "Motor gasolina compacto", "Nissan Genuine, Mobil",
          [(aceite, aceite_status)], "c/10k",
          [L("NissanPartsDeal", NPN), L("ML", ML+"aceite+"+aceite.split(' ')[0].lower()+"+nissan+"+q)]),
        P("Motor", "Filtro Aceite", "Filtro aceite Nissan", "Universal Nissan 1995-2020", "Nissan Genuine, MANN",
          [("15208-65F0E", "confirmed")], "c/10k",
          [L("NissanPartsDeal", NPN), L("ML", ML+"filtro+aceite+15208+65f0e")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Motor gasolina compacto", "Nissan Genuine, MANN",
          [(fa_ref, fa_status)], "c/15-30k",
          [L("NissanPartsDeal", NPN), L("ML", ML+"filtro+aire+nissan+"+q)]),
        P("Encendido", "Bujias", "Bujias x4", "Motor gasolina", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("NissanPartsDeal", NPN), L("ML", ML+"bujia+ngk+nissan+"+q)]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Filtro polen", "Nissan Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("NissanPartsDeal", NPN), L("ML", ML+"filtro+cabina+nissan+"+q)]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Nissan Genuine, Akebono",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("NissanPartsDeal", NPN), L("ML", ML+"pastillas+freno+nissan+"+q)]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Nissan, Bosch",
          [("DOT4", "confirmed")], "c/2 anos",
          [L("ML", ML+"liquido+frenos+dot4+nissan")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Bridgestone, Michelin, Goodyear",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


NISSAN_B1_MAP = {
    "nissan-versa":  (nissan_gasolina, "185/65 R15", {"q": "versa"}),
    "nissan-tiida":  (nissan_gasolina, "185/65 R15", {"q": "tiida"}),
    "nissan-march":  (nissan_gasolina, "175/60 R15", {"q": "march"}),
    "nissan-sentra": (nissan_gasolina, "205/55 R16", {"q": "sentra", "filtro_aire_ref": "16546-17B00", "filtro_aire_status": "confirmed"}),
    "nissan-kicks":  (nissan_gasolina, "205/60 R16", {"q": "kicks"}),
    "nissan-v16":    (nissan_gasolina, "175/70 R13", {"q": "v16", "aceite": "10W-30 / 15W-40", "aceite_status": "confirmed"}),
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
        entry = NISSAN_B1_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum, det = entry
        clear_and_insert(c, vid, gen(neum, det))
        n += 1
    conn.commit()
    print("Nissan Bloque 1 actualizados:", n)
    if skipped:
        print("Sin mapa (otros bloques Nissan):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
