# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marcas MG y Maxus (grupo SAIC).
Motor por familia; frenos/neumaticos por modelo.
Ejecutar: python insert_mg_maxus_componentes.py  (luego export_db.py + _regen_nav.py)
Regla estricta: MG/Maxus tienen pocos PN OEM de fuente publica fiable.
  Solo se marca "confirmed" el tipo de aceite, el DOT4 y el neumatico.
  TODO PN de filtros/bujias/pastillas va ("Verificar OEM","verify"). NO se inventan part numbers.
Familias:
  - mg_gasolina  1.5 aspirado / 1.5T / 1.0T turbo (MG3, MG5, HS, RX5, ZS) motores SAIC gasolina
  - maxus_diesel 2.0 turbodiesel / gasolina comercial (Deliver 9, G10, T60) SAIC
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- MG gasolina (SUV/sedan 1.5 aspirado, 1.5T, 1.0T) ----------------
def mg_gasolina(neum, motor_nota="motor SAIC"):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 sintetico", "motor SAIC gasolina | " + motor_nota, "MG/SAIC Genuine, MANN",
          [("5W-30 sintetico", "confirmed")], "c/10k",
          [L("ML", ML+"aceite+5w30+mg"), L("Amazon", AZ+"5w30+synthetic+oil")]),
        P("Motor", "Filtro Aceite", "Filtro aceite motor", "motor SAIC | " + motor_nota, "MG/SAIC Genuine, MANN",
          [("Verificar OEM", "verify")], "c/10k",
          [L("ML", ML+"filtro+aceite+mg"), L("Amazon", AZ+"mg+oil+filter")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "motor SAIC | " + motor_nota, "MG/SAIC Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+mg"), L("Amazon", AZ+"mg+air+filter")]),
        P("Encendido", "Bujias", "Bujias iridio", "motor SAIC gasolina | " + motor_nota, "NGK, Bosch",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("ML", ML+"bujia+ngk+mg"), L("Amazon", AZ+"ngk+spark+plug")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "cabina MG", "MG/SAIC Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+mg"), L("Amazon", AZ+"mg+cabin+air+filter")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "disco ventilado", "Bosch, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+mg"), L("Amazon", AZ+"mg+brake+pads")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "sistema hidraulico", "Bosch, TRW",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Maxus diesel (comercial/van/pickup 2.0 turbodiesel) ----------------
def maxus_diesel(neum, motor_nota="2.0 turbodiesel SAIC"):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 diesel (ACEA C3)", "motor SAIC diesel | " + motor_nota, "Maxus/SAIC Genuine, MANN",
          [("5W-30 diesel (ACEA C3)", "confirmed")], "c/10k",
          [L("ML", ML+"aceite+5w30+diesel+acea+c3"), L("Amazon", AZ+"5w30+c3+diesel+oil")]),
        P("Motor", "Filtro Aceite", "Filtro aceite motor", "motor SAIC diesel | " + motor_nota, "Maxus/SAIC Genuine, MANN",
          [("Verificar OEM", "verify")], "c/10k",
          [L("ML", ML+"filtro+aceite+maxus"), L("Amazon", AZ+"maxus+oil+filter")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "motor SAIC diesel | " + motor_nota, "Maxus/SAIC Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+maxus"), L("Amazon", AZ+"maxus+air+filter")]),
        P("Motor", "Filtro Combustible", "Filtro combustible diesel c/separador agua", "diesel con separador de agua | " + motor_nota, "Maxus/SAIC Genuine, MANN",
          [("Verificar OEM", "verify")], "c/20-40k",
          [L("ML", ML+"filtro+combustible+diesel+maxus"), L("Amazon", AZ+"maxus+fuel+filter+diesel")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "cabina Maxus", "Maxus/SAIC Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+maxus"), L("Amazon", AZ+"maxus+cabin+air+filter")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "disco ventilado comercial", "Bosch, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+maxus"), L("Amazon", AZ+"maxus+brake+pads")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "sistema hidraulico", "Bosch, TRW",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "comercial/van/pickup", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


MG_MAXUS_MAP = {
    # MG gasolina (motores SAIC)
    "mg-mg-3":        (lambda n: mg_gasolina(n, "MG3 gasolina 1.5 aspirado, motor SAIC"), "195/55 R16"),
    "mg-saic-mg-3":   (lambda n: mg_gasolina(n, "MG3 gasolina 1.5 aspirado, motor SAIC"), "195/55 R16"),
    "mg-saic-mg-5":   (lambda n: mg_gasolina(n, "MG5 gasolina 1.5, motor SAIC"), "205/55 R16"),
    "mg-saic-mg-hs":  (lambda n: mg_gasolina(n, "MG HS SUV 1.5T turbo, motor SAIC"), "235/50 R18"),
    "mg-saic-mg-rx5": (lambda n: mg_gasolina(n, "MG RX5 SUV 1.5T turbo, motor SAIC"), "235/50 R19"),
    "mg-saic-mg-zs":  (lambda n: mg_gasolina(n, "MG ZS SUV 1.0T/1.5 aspirado, motor SAIC"), "215/55 R17"),
    # Maxus comerciales/diesel (SAIC)
    "maxus-deliver-9":      (lambda n: maxus_diesel(n, "Deliver 9 van/camion 2.0 turbodiesel SAIC"), "235/65 R16C"),
    "maxus-saic-deliver-9": (lambda n: maxus_diesel(n, "Deliver 9 van/camion 2.0 turbodiesel SAIC"), "235/65 R16C"),
    "maxus-g10":            (lambda n: maxus_diesel(n, "G10 van gasolina 2.0T o diesel 2.0 SAIC"), "215/65 R16"),
    "maxus-saic-g10":       (lambda n: maxus_diesel(n, "G10 van gasolina 2.0T o diesel 2.0 SAIC"), "215/65 R16"),
    "maxus-saic-t60":       (lambda n: maxus_diesel(n, "T60 pickup 2.0 turbodiesel SAIC"), "255/60 R18"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'MG %' OR name LIKE 'Maxus %'").fetchall()
    n_mg = 0; n_maxus = 0; skipped = []; mapped_bases = set()
    for vid, name in rows:
        bid = base_id(vid)
        entry = MG_MAXUS_MAP.get(bid)
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        mapped_bases.add(bid)
        if bid.startswith("maxus"):
            n_maxus += 1
        else:
            n_mg += 1
    conn.commit()
    print("MG actualizados:", n_mg)
    print("Maxus actualizados:", n_maxus)
    print("Total actualizados:", n_mg + n_maxus)
    if skipped:
        print("Sin mapa (revisar):", sorted(set(base_id(s) for s in skipped)))
    else:
        print("Sin mapa: (ninguno)")
    print("Base IDs mapeados (%d/%d):" % (len(mapped_bases), len(MG_MAXUS_MAP)), sorted(mapped_bases))
    missing = sorted(set(MG_MAXUS_MAP.keys()) - mapped_bases)
    if missing:
        print("Base IDs del mapa NO encontrados en vehicles:", missing)
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
