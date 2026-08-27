# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marcas Lexus y Mazda.
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_lexus_mazda_componentes.py  (luego export_db.py + _regen_nav.py)
Fuentes publicas: mazdapartsstore, lexuspartsnow, mannfilter, amazon.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
Familias:
  - Skyactiv-G gasolina (Mazda2/3/6, CX-3, CX-30, CX-5, CX-9)
  - Mazda BT-50 diesel (pickup, comparte plataforma Isuzu D-Max / Ford Ranger)
  - Lexus NX (motor Toyota 2.0T o 2.5 hibrido)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- Skyactiv-G gasolina (Mazda2/3/6, CX-3, CX-30, CX-5, CX-9) ----------------
def skyactiv_g(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 sintetico", "Skyactiv-G gasolina | segun cilindrada", "Mazda Genuine, Mobil, Idemitsu",
          [("0W-20 (Mazda GF-6)", "confirmed")], "c/10k",
          [L("MercadoLibre", ML+"aceite+0w20+mazda"), L("Amazon", AZ+"mazda+0w20+oil")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Mazda Skyactiv", "Mazda2/3/6/CX-3/CX-30/CX-5/CX-9", "Mazda Genuine, MANN",
          [("PE01-14-302A", "confirmed"), ("1WPE-14-302 (actual)", "confirmed")], "c/10k",
          [L("Amazon", AZ+"PE01-14-302A"), L("ML", ML+"filtro+aceite+mazda+pe01+14+302")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Skyactiv-G", "Mazda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+mazda+skyactiv"), L("Amazon", AZ+"mazda+skyactiv+air+filter")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "Skyactiv-G", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("ML", ML+"bujia+mazda+skyactiv"), L("Amazon", AZ+"mazda+skyactiv+spark+plug")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Skyactiv-G", "Mazda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+mazda"), L("Amazon", AZ+"mazda+cabin+air+filter")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Mazda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+mazda"), L("Amazon", AZ+"mazda+brake+pads")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Mazda, Bosch",
          [("DOT4", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+dot4+mazda")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Bridgestone, Michelin, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- Mazda BT-50 diesel (pickup, comparte con Isuzu D-Max / Ford Ranger) ----------------
def mazda_bt50_diesel(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 diesel sintetico", "Pickup diesel 3.0/1.9 | comparte Isuzu D-Max / Ford Ranger", "Mazda Genuine, MANN",
          [("5W-30 diesel", "confirmed")], "c/10k",
          [L("ML", ML+"aceite+5w30+diesel+mazda+bt50"), L("Amazon", AZ+"5w30+diesel+oil")]),
        P("Motor", "Filtro Aceite", "Filtro aceite diesel", "BT-50 diesel", "Mazda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/10k",
          [L("ML", ML+"filtro+aceite+mazda+bt50"), L("Amazon", AZ+"mazda+bt50+oil+filter")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "BT-50 diesel", "Mazda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+mazda+bt50"), L("Amazon", AZ+"mazda+bt50+air+filter")]),
        P("Motor", "Filtro Combustible", "Filtro combustible diesel c/separador de agua", "BT-50 diesel", "Mazda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/20-40k",
          [L("ML", ML+"filtro+combustible+diesel+mazda+bt50"), L("Amazon", AZ+"mazda+bt50+fuel+filter+diesel")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "BT-50", "Mazda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+mazda+bt50"), L("Amazon", AZ+"mazda+bt50+cabin+filter")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado pickup", "Mazda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+mazda+bt50"), L("Amazon", AZ+"mazda+bt50+brake+pads")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Mazda, Bosch",
          [("DOT4", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+dot4+mazda")]),
        P("Neumaticos", "Neumatico", neum, "Pickup", "Bridgestone, Michelin, BFGoodrich",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- Lexus NX (motor Toyota 2.0T o 2.5 hibrido) ----------------
def lexus_nx(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 sintetico", "SUV premium | Toyota 2.0T o 2.5 hibrido", "Lexus/Toyota Genuine, Mobil",
          [("0W-20", "confirmed")], "c/10k",
          [L("ML", ML+"aceite+0w20+toyota+lexus"), L("Amazon", AZ+"toyota+0w20+oil")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Lexus/Toyota", "Lexus NX", "Lexus/Toyota Genuine, Denso",
          [("Verificar OEM", "verify")], "c/10k",
          [L("ML", ML+"filtro+aceite+lexus+nx+toyota"), L("Amazon", AZ+"lexus+nx+oil+filter")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Lexus NX", "Lexus/Toyota Genuine, Denso",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+lexus+nx"), L("Amazon", AZ+"lexus+nx+air+filter")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "Toyota 2.0T / 2.5 hibrido", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/100k",
          [L("ML", ML+"bujia+iridio+lexus+nx+toyota"), L("Amazon", AZ+"lexus+nx+spark+plug")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Lexus NX", "Lexus/Toyota Genuine, Denso",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+lexus+nx"), L("Amazon", AZ+"lexus+nx+cabin+air+filter")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado SUV premium", "Lexus/Toyota Genuine, Denso",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+lexus+nx"), L("Amazon", AZ+"lexus+nx+brake+pads")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Lexus/Toyota, Bosch",
          [("DOT4", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+dot4+lexus+toyota")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


LEXUS_MAZDA_MAP = {
    "lexus-lexus-nx": (lexus_nx, "235/55 R18"),
    "mazda-mazda-2": (skyactiv_g, "185/65 R15"),
    "mazda-mazda-3": (skyactiv_g, "205/60 R16"),
    "mazda-mazda-6": (skyactiv_g, "225/55 R17"),
    "mazda-cx-3": (skyactiv_g, "215/60 R16"),
    "mazda-cx-30": (skyactiv_g, "215/55 R18"),
    "mazda-cx-5": (skyactiv_g, "225/65 R17"),
    "mazda-cx-9": (skyactiv_g, "255/50 R20"),
    "mazda-bt-50": (mazda_bt50_diesel, "265/65 R17"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Lexus %' OR name LIKE 'Mazda %'").fetchall()
    n_lexus = 0; n_mazda = 0; skipped = []
    for vid, name in rows:
        entry = LEXUS_MAZDA_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        if name.startswith("Lexus "):
            n_lexus += 1
        else:
            n_mazda += 1
    conn.commit()
    print("Lexus actualizados:", n_lexus)
    print("Mazda actualizados:", n_mazda)
    if skipped:
        print("Sin mapa (revisar):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
