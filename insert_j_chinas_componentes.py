# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes marcas chinas de la "J": JAC, JMC, Jetour.
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_j_chinas_componentes.py  (luego export_db.py + _regen_nav.py)
Regla estricta: JAC/JMC/Jetour tienen pocos PN OEM de fuente publica fiable.
  Solo se marca "confirmed" el tipo de aceite (5W-30) y el liquido de frenos (DOT4).
  TODO PN de filtros/bujias/pastillas va como ("Verificar OEM","verify"). No se inventan part numbers.
Familias:
  - suv_gasolina : JAC JS4 (1.5T/1.6 motor JAC HFC), JAC S2 (1.5), JAC S3 (1.6),
                   Jetour Dashing (1.5T/1.6T motor Chery SQRF4J turbo, plataforma Chery/Kunpeng)
  - pickup_diesel: JAC T6 (2.0 diesel HFC4DA), JAC T8 (2.0 turbodiesel HFC4DA),
                   JMC Vigus Pro (motor Ford Puma 2.0 TDCi / JX4D)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- SUV gasolina (JS4, S2, S3, Jetour Dashing) ----------------
def suv_gasolina(neum, det_motor="SUV gasolina", brands_motor="JAC Genuine, MANN", det_aceite="~4.0L | motor gasolina"):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 sintetico", det_aceite, brands_motor,
          [("5W-30 sintetico", "confirmed")], "c/10k",
          [L("ML", ML+"aceite+5w30+sintetico"), L("Amazon", AZ+"aceite+5w30+sintetico")]),
        P("Motor", "Filtro Aceite", "Filtro aceite motor", det_motor, brands_motor,
          [("Verificar OEM", "verify")], "c/10k",
          [L("ML", ML+"filtro+aceite+"+det_motor.replace('/', '+').replace(' ', '+')), L("Amazon", AZ+"filtro+aceite+motor")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", det_motor, brands_motor,
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+"+det_motor.replace('/', '+').replace(' ', '+')), L("Amazon", AZ+"filtro+aire+motor")]),
        P("Encendido", "Bujias", "Bujias iridio", det_motor, "NGK, Bosch",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("ML", ML+"bujia+ngk+"+det_motor.replace('/', '+').replace(' ', '+')), L("Amazon", AZ+"bujia+ngk")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", det_motor, brands_motor,
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+"+det_motor.replace('/', '+').replace(' ', '+')), L("Amazon", AZ+"filtro+cabina")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Bosch, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+delanteras"), L("Amazon", AZ+"pastillas+freno+delanteras")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, TRW",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4"), L("Amazon", AZ+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Pickup diesel (T6, T8, JMC Vigus Pro) ----------------
def pickup_diesel(neum, det_motor="pickup diesel", brands_motor="JAC Genuine, MANN", det_aceite="~6.0L | motor diesel turbo"):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 diesel", det_aceite+" | ACEA C3", brands_motor,
          [("5W-30 diesel (ACEA C3)", "confirmed")], "c/10k",
          [L("ML", ML+"aceite+5w30+diesel+acea+c3"), L("Amazon", AZ+"aceite+5w30+diesel+acea+c3")]),
        P("Motor", "Filtro Aceite", "Filtro aceite motor", det_motor, brands_motor,
          [("Verificar OEM", "verify")], "c/10k",
          [L("ML", ML+"filtro+aceite+"+det_motor.replace('/', '+').replace(' ', '+')), L("Amazon", AZ+"filtro+aceite+diesel")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", det_motor, brands_motor,
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+"+det_motor.replace('/', '+').replace(' ', '+')), L("Amazon", AZ+"filtro+aire+diesel")]),
        P("Motor", "Filtro Combustible", "Filtro combustible diesel c/separador agua", det_motor, brands_motor,
          [("Verificar OEM", "verify")], "c/20-40k",
          [L("ML", ML+"filtro+combustible+diesel+separador+agua"), L("Amazon", AZ+"filtro+combustible+diesel+separador")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", det_motor, brands_motor,
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+"+det_motor.replace('/', '+').replace(' ', '+')), L("Amazon", AZ+"filtro+cabina")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado pickup", "Bosch, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+delanteras+pickup"), L("Amazon", AZ+"pastillas+freno+delanteras")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, TRW",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4"), L("Amazon", AZ+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Bridgestone, Michelin, BFGoodrich",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# Wrappers de familia por modelo (para pasar detalles/marcas especificas sin romper el patron)
def jac_js4(neum): return suv_gasolina(neum, "JAC JS4 1.5T/1.6", "JAC Genuine, MANN", "~4.0L | JAC JS4 1.5T/1.6 (motor JAC HFC)")
def jac_s2(neum):  return suv_gasolina(neum, "JAC S2 1.5", "JAC Genuine, MANN", "~3.8L | JAC S2 1.5 gasolina")
def jac_s3(neum):  return suv_gasolina(neum, "JAC S3 1.6", "JAC Genuine, MANN", "~4.0L | JAC S3 1.6 gasolina")
def jetour_dashing(neum): return suv_gasolina(neum, "Jetour Dashing 1.5T/1.6T", "Jetour/Chery Genuine, MANN", "~4.0L | Jetour Dashing 1.5T/1.6T (comparte motor turbo Chery SQRF4J, plataforma Chery/Kunpeng)")
def jac_t6(neum):  return pickup_diesel(neum, "JAC T6 2.0 diesel", "JAC Genuine, MANN", "~6.0L | JAC T6 2.0 diesel HFC4DA (o 2.0T gasolina)")
def jac_t8(neum):  return pickup_diesel(neum, "JAC T8 2.0 turbodiesel", "JAC Genuine, MANN", "~6.0L | JAC T8 2.0 turbodiesel HFC4DA")
def jmc_vigus_pro(neum): return pickup_diesel(neum, "JMC Vigus Pro 2.0 TDCi", "JMC Genuine, MANN", "~6.0L | JMC Vigus Pro (motor Ford Puma 2.0 TDCi / JX4D)")


J_CHINAS_MAP = {
    "jac-js4": (jac_js4, "215/55 R18"),
    "jac-s2": (jac_s2, "205/60 R16"),
    "jac-s3": (jac_s3, "215/60 R17"),
    "jac-t6": (jac_t6, "245/70 R16"),
    "jac-t8": (jac_t8, "265/65 R17"),
    "jmc-vigus-pro": (jmc_vigus_pro, "255/65 R17"),
    "jetour-dashing": (jetour_dashing, "225/55 R18"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'JAC %' OR name LIKE 'JMC %' OR name LIKE 'Jetour %'").fetchall()
    n = 0; skipped = []
    by_brand = {"JAC": 0, "JMC": 0, "Jetour": 0}
    for vid, name in rows:
        entry = J_CHINAS_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        n += 1
        if name.startswith("JAC "): by_brand["JAC"] += 1
        elif name.startswith("JMC "): by_brand["JMC"] += 1
        elif name.startswith("Jetour "): by_brand["Jetour"] += 1
    conn.commit()
    print("Vehiculos actualizados:", n)
    print("  Por marca -> JAC:", by_brand["JAC"], "| JMC:", by_brand["JMC"], "| Jetour:", by_brand["Jetour"])
    if skipped:
        print("Sin mapa (revisar):", sorted(set(base_id(s) for s in skipped)))
    else:
        print("Sin mapa: ninguno")
    mapped_bases = sorted(set(base_id(vid) for vid, _ in rows if base_id(vid) in J_CHINAS_MAP))
    print("Base_id mapeados (", len(mapped_bases), "):", mapped_bases)
    conn.close()


if __name__ == "__main__":
    main()
