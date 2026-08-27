# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Haval (grupo GWM).
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_haval_componentes.py  (luego export_db.py + _regen_nav.py)
Fuentes publicas: scribd (manual Haval H6 2022), gwmanz, alibaba/autopart.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
NOTA: Haval comparte mecanica con GWM (familia de motores GW4). Familias usadas aqui:
  - GW4C20B 2.0T gasolina (H6, Dargo, Tank 300)
  - GW4B15/GW4G15 1.5T gasolina (Jolion, H6 1.5T)
  - GW4D20 2.0D diesel (Poer pickup)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
MANUAL_H6 = "https://es.scribd.com/document/717137231/Haval-H6-2022-EN-service-98f4452a68"

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- GW4C20B 2.0T gasolina (H6, Dargo, Tank 300) ----------------
def gw4c20(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 / 5W-40 sintetico", "~5.5L | 2.0T GW4C20B", "GWM Genuine, Mobil, Shell",
          [("5W-30 sintetico", "confirmed"), ("5W-40 (uso severo)", "confirmed")], "c/10-12k / 12 meses",
          [L("Manual H6", MANUAL_H6), L("ML", ML+"aceite+5w30+haval+h6")]),
        P("Motor", "Filtro Aceite", "Filtro aceite GW4C20B", "2.0T (H6/Dargo/Tank 300 comparten)", "GWM Genuine, Mahle",
          [("Verificar OEM", "verify")], "c/10-12k",
          [L("Alibaba", "https://autopart.alibaba.com/product/genuine-gwm-auto-parts"), L("ML", ML+"filtro+aceite+haval+h6")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "2.0T turbo", "GWM Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15k",
          [L("ML", ML+"filtro+aire+haval+h6")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "2.0T turbo (c/50k segun manual)", "NGK iridio, Bosch",
          [("Verificar OEM", "verify")], "c/50k",
          [L("Manual H6", MANUAL_H6), L("Alibaba", "https://autopart.alibaba.com/product/spark-plug-great-wall"), L("ML", ML+"bujia+ngk+haval+h6")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "H6/Dargo/Tank 300", "GWM Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+haval+h6")]),
        P("Transmision", "Aceite DCT", "Fluido caja doble embrague 7DCT", "Transmision humeda 7DCT450", "GWM Genuine",
          [("Verificar OEM", "verify")], "c/60k",
          [L("Manual H6", MANUAL_H6), L("ML", ML+"aceite+dct+haval+h6")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado SUV", "GWM Genuine, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+haval+h6")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, GWM Genuine",
          [("DOT4", "confirmed")], "c/2 anos",
          [L("Manual H6", MANUAL_H6), L("ML", ML+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Continental, Cooper, Bridgestone",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Continental", "https://www.continental-neumaticos.cl/")]),
    ]


# ---------------- GW4B15 / GW4G15 1.5T gasolina (Jolion, H6 1.5T) ----------------
def gw4b15(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 sintetico", "~4.5L | 1.5T GW4B15/GW4G15", "GWM Genuine, Mobil, Shell",
          [("5W-30 sintetico", "confirmed")], "c/10-12k / 12 meses",
          [L("Manual H6", MANUAL_H6), L("ML", ML+"aceite+5w30+haval+jolion")]),
        P("Motor", "Filtro Aceite", "Filtro aceite 1.5T", "Jolion/H6 1.5T", "GWM Genuine, Mahle",
          [("Verificar OEM", "verify")], "c/10-12k",
          [L("Alibaba", "https://autopart.alibaba.com/product/genuine-gwm-auto-parts"), L("ML", ML+"filtro+aceite+haval+jolion")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "1.5T turbo", "GWM Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15k",
          [L("ML", ML+"filtro+aire+haval+jolion")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "1.5T turbo (c/50k segun manual)", "NGK iridio, Bosch",
          [("Verificar OEM", "verify")], "c/50k",
          [L("Manual H6", MANUAL_H6), L("Alibaba", "https://autopart.alibaba.com/product/spark-plug-great-wall"), L("ML", ML+"bujia+ngk+haval+jolion")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Jolion", "GWM Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+haval+jolion")]),
        P("Transmision", "Aceite DCT", "Fluido caja doble embrague 7DCT", "Transmision humeda 7DCT", "GWM Genuine",
          [("Verificar OEM", "verify")], "c/60k",
          [L("Manual H6", MANUAL_H6), L("ML", ML+"aceite+dct+haval+jolion")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado SUV compacto", "GWM Genuine, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+haval+jolion")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, GWM Genuine",
          [("DOT4", "confirmed")], "c/2 anos",
          [L("ML", ML+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Continental, Bridgestone",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- GW4D20 2.0D diesel (Poer pickup) ----------------
def gw4d20(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 / 5W-40 diesel", "~6.0L | 2.0D GW4D20 turbodiesel", "GWM Genuine, Shell Rimula",
          [("5W-30 diesel (ACEA C3)", "confirmed")], "c/10k",
          [L("GWM NZ", "https://www.gwmanz.com/au/"), L("ML", ML+"aceite+5w30+diesel+haval+poer")]),
        P("Motor", "Filtro Aceite", "Filtro aceite diesel GW4D20", "Poer/Cannon 2.0D", "GWM Genuine, MANN",
          [("Verificar OEM", "verify")], "c/10k",
          [L("Alibaba", "https://autopart.alibaba.com/product/genuine-gwm-auto-parts"), L("ML", ML+"filtro+aceite+haval+poer")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Pickup diesel", "GWM Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15k",
          [L("ML", ML+"filtro+aire+haval+poer")]),
        P("Motor", "Filtro Combustible", "Filtro combustible diesel", "Separador de agua", "Bosch, MANN",
          [("Verificar OEM", "verify")], "c/20-40k",
          [L("ML", ML+"filtro+combustible+haval+poer")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Poer/Cannon", "GWM Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+haval+poer")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado pickup", "GWM Genuine, TRW",
          [("Verificar OEM", "verify")], "c/40k",
          [L("ML", ML+"pastillas+freno+haval+poer")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, GWM Genuine",
          [("DOT4", "confirmed")], "c/2 anos",
          [L("ML", ML+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "Pickup 4x4", "BFGoodrich, Cooper, Bridgestone",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("BFGoodrich", "https://www.bfgoodrich.cl/")]),
    ]


HAVAL_MAP = {
    "haval-h6": (gw4c20, "225/60 R18"),
    "haval-dargo": (gw4c20, "235/55 R19"),
    "haval-tank-300": (gw4c20, "265/65 R17"),
    "haval-jolion": (gw4b15, "225/55 R18"),
    "haval-poer": (gw4d20, "265/60 R18"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Haval %'").fetchall()
    n = 0; skipped = []
    for vid, name in rows:
        entry = HAVAL_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        n += 1
    conn.commit()
    print("Haval actualizados:", n)
    if skipped:
        print("Sin mapa (revisar):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
