# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca G (GAC, Geely, GWM).
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_g_componentes.py  (luego export_db.py + regen nav)
Fuentes publicas: amazon, chinaautoparts.info, accio, scribd (manual Haval H6), gwmanz.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
NOTA: GWM (Great Wall) y Haval comparten mecanica (grupo GWM). Aqui solo se cubre GWM;
Haval se completa en su propia tanda (letra H).
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- GAC (Trumpchi) — GS4 motor 4B15J1 1.5T turbo ----------------
def gac_gs4(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 / 5W-40 sintetico", "~4.0L | 1.5T turbo 4B15J1", "GAC Genuine, Mobil, Shell",
          [("5W-30 sintetico", "confirmed"), ("5W-40 (uso severo)", "confirmed")], "c/10k",
          [L("Alibaba", "https://smartbuy.alibaba.com/buyingguides/original-oil-filter-gac"), L("ML", ML+"aceite+5w30+gac+gs4")]),
        P("Motor", "Filtro Aceite", "Filtro aceite GS4 1.5T", "Trumpchi GS3/GS4/GS8/GA6", "GAC Genuine, Mahle",
          [("Verificar OEM", "verify")], "c/10k",
          [L("Alibaba", "https://smartbuy.alibaba.com/buyingguides/original-oil-filter-gac"), L("ML", ML+"filtro+aceite+gac+gs4")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "GS4 1.5T", "GAC Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15k",
          [L("ML", ML+"filtro+aire+gac+gs4")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "1.5T turbo", "NGK, Bosch",
          [("Verificar OEM", "verify")], "c/40-60k",
          [L("ML", ML+"bujia+gac+gs4")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "GS3/GS4/GS8/GA6", "GAC Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("AZ", AZ+"GAC+Trumpchi+GS4+cabin+air+filter"), L("ML", ML+"filtro+cabina+gac+gs4")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "GAC Genuine, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+gac+gs4")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Continental, Bridgestone",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Continental", "https://www.continental-neumaticos.cl/")]),
    ]


# ---------------- Geely — Coolray motor JLH-3G15TD 1.5T turbo 3-cil (plataforma BMA) ----------------
def geely_coolray(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 / 5W-40", "~4.2L | 1.5T JLH-3G15TD (VCC RBS0-2AE)", "Geely Genuine, Mobil, Shell",
          [("0W-20 (VCC RBS0-2AE)", "confirmed"), ("5W-40 API SN Plus", "confirmed")], "c/10k",
          [L("Scribd (fluidos)", "https://www.scribd.com/document/822182458/Recommended-fluids-for-Geely-Coolray"), L("ML", ML+"aceite+0w20+geely+coolray")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Coolray SX11", "1.5T JLH-3G15TD (Emgrand/GC9/Tugella comparten)", "Geely Genuine, Mahle",
          [("1016056847", "confirmed"), ("1056022300", "confirmed")], "c/10k",
          [L("ChinaAutoParts", "https://www.chinaautoparts.info/"), L("ML", ML+"filtro+aceite+geely+coolray")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Coolray SX11 1.5T", "Geely Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15k",
          [L("ML", ML+"filtro+aire+geely+coolray")]),
        P("Encendido", "Bujias", "Bujias x4 iridio NGK", "1.5T JLH-3G15TD (Coolray/Emgrand/GC9/Tugella/Lynk&Co 01-06)", "NGK",
          [("NGK ILKFR8B7G (91602)", "confirmed")], "c/40-60k",
          [L("AZ", AZ+"NGK+ILKFR8B7G+91602"), L("ML", ML+"bujia+ngk+geely+coolray")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Coolray SX11", "Geely Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+geely+coolray")]),
        P("Transmision", "Aceite DCT", "Fluido caja doble embrague DCT", "7DCT | Shell Spirax S5 DCT10", "Shell, Geely Genuine",
          [("Shell Spirax S5 DCT10", "confirmed")], "c/60k",
          [L("Scribd (fluidos)", "https://www.scribd.com/document/822182458/Recommended-fluids-for-Geely-Coolray"), L("ML", ML+"aceite+dct+geely+coolray")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado (comparte Binyue SX11/Coolray Pro)", "Geely Genuine, TRW",
          [("4048046400", "confirmed")], "c/30-50k",
          [L("Accio", "https://www.accio.com/plp/geely-coolray-spare-parts"), L("ML", ML+"pastillas+freno+geely+coolray")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, Geely Genuine",
          [("DOT4", "confirmed")], "c/2 anos",
          [L("Scribd (fluidos)", "https://www.scribd.com/document/822182458/Recommended-fluids-for-Geely-Coolray"), L("ML", ML+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Continental, Michelin",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- GWM — motor GW4C20B 2.0T (Tank 300, Dargo). Comparte con Haval ----------------
def gwm_gw4c20(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 / 5W-40 sintetico", "~5.5L | 2.0T GW4C20B", "GWM Genuine, Mobil, Shell",
          [("5W-30 sintetico", "confirmed"), ("5W-40 (uso severo)", "confirmed")], "c/10-12k / 12 meses",
          [L("Scribd (manual H6)", "https://es.scribd.com/document/717137231/Haval-H6-2022-EN-service-98f4452a68"), L("ML", ML+"aceite+5w30+gwm+tank+300")]),
        P("Motor", "Filtro Aceite", "Filtro aceite GW4C20B", "2.0T (Tank 300/Dargo/H6 comparten)", "GWM Genuine, Mahle",
          [("Verificar OEM", "verify")], "c/10-12k",
          [L("Alibaba", "https://autopart.alibaba.com/product/genuine-gwm-auto-parts"), L("ML", ML+"filtro+aceite+gwm+tank+300")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "2.0T turbo", "GWM Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15k",
          [L("ML", ML+"filtro+aire+gwm+tank+300")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "2.0T turbo (c/50k segun manual)", "NGK iridio, Bosch",
          [("Verificar OEM", "verify")], "c/50k",
          [L("Scribd (manual H6)", "https://es.scribd.com/document/717137231/Haval-H6-2022-EN-service-98f4452a68"), L("Alibaba", "https://autopart.alibaba.com/product/spark-plug-great-wall"), L("ML", ML+"bujia+ngk+gwm+tank+300")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Tank 300/Dargo", "GWM Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+gwm+tank+300")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado SUV/pickup", "GWM Genuine, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+gwm+tank+300")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, GWM Genuine",
          [("DOT4", "confirmed")], "c/2 anos",
          [L("ML", ML+"liquido+frenos+dot4")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Cooper, BFGoodrich, Bridgestone",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("BFGoodrich", "https://www.bfgoodrich.cl/")]),
    ]


GAC_MAP = {
    "gac-gs4": (gac_gs4, "225/60 R18"),
}
GEELY_MAP = {
    "geely-coolray": (geely_coolray, "215/55 R18"),
}
GWM_MAP = {
    "gwm-tank-300": (gwm_gw4c20, "265/65 R17"),
    "gwm-dargo": (gwm_gw4c20, "235/55 R19"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'GAC %' OR name LIKE 'Geely %' OR name LIKE 'GWM %'").fetchall()
    nf = {"GAC": 0, "Geely": 0, "GWM": 0}
    skipped = []
    for vid, name in rows:
        b = base_id(vid)
        if name.startswith("GAC"):
            entry = GAC_MAP.get(b); brand = "GAC"
        elif name.startswith("Geely"):
            entry = GEELY_MAP.get(b); brand = "Geely"
        else:
            entry = GWM_MAP.get(b); brand = "GWM"
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        comps = gen(neum) if neum is not None else gen()
        clear_and_insert(c, vid, comps)
        nf[brand] += 1
    conn.commit()
    print("Actualizados:", nf)
    if skipped:
        print("Sin mapa (revisar):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
