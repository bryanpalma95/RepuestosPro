# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marcas Mercedes-Benz y Mitsubishi.
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_mb_mitsubishi_componentes.py  (luego export_db.py + _regen_nav.py)
Fuentes publicas: mercadolibre, amazon, catalogos MANN/Bosch/NGK.
Regla: solo se marca "confirmed" un dato con fuente publica fiable (aceite por spec, DOT4);
sin PN publico concreto = "verify". NO se inventan part numbers.
Familias:
  - mb_gasolina: Clase A, GLA + version gasolina de Clase C / Clase E / GLC (M282 1.3T / M260-M264 2.0T)
  - mb_diesel: Sprinter + opcion diesel (OM651/OM642 / OM654) - sin bujias, con Filtro Combustible
  - mitsu_gasolina: ASX, Eclipse Cross, Lancer, Mirage, Outlander (4B10/4B11/4B12/4B40/3A92)
  - mitsu_diesel: L200, L300, Montero Sport (4N15 2.4 DI-D / 4D56) - sin bujias, con Filtro Combustible
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- Mercedes-Benz gasolina (Clase A, GLA, C/E/GLC gasolina) ----------------
def mb_gasolina(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 / 0W-40 sintetico", "M282 1.3T / M260-M264 2.0T gasolina", "Mercedes-Benz Genuine, Mobil",
          [("5W-30 / 0W-40 MB 229.5", "confirmed")], "c/10-15k",
          [L("ML", ML+"aceite+5w30+mb+229.5"), L("Amazon", AZ+"mercedes+229.5+oil")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Mercedes-Benz", "Motor gasolina M282/M260/M264", "Mercedes-Benz Genuine, MANN",
          [("Verificar OEM", "verify")], "c/10-15k",
          [L("ML", ML+"filtro+aceite+mercedes+benz"), L("Amazon", AZ+"mann+filtro+aceite+mercedes")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Gasolina turbo M282/M260/M264", "Mercedes-Benz Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+mercedes+benz"), L("Amazon", AZ+"mann+filtro+aire+mercedes")]),
        P("Encendido", "Bujias", "Bujias iridio", "Gasolina turbo M282/M260/M264", "NGK, Bosch",
          [("Verificar OEM", "verify")], "c/40-60k",
          [L("ML", ML+"bujia+mercedes+benz"), L("Amazon", AZ+"ngk+bujia+mercedes")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C carbon activo", "Cabina gasolina", "Mercedes-Benz Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+mercedes+benz"), L("Amazon", AZ+"mann+filtro+cabina+mercedes")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Bosch, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+mercedes+benz"), L("Amazon", AZ+"bosch+pastillas+mercedes")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, Mercedes-Benz Genuine",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+mercedes")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Continental, Pirelli",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Mercedes-Benz diesel (Sprinter + opcion diesel C/E/GLC) ----------------
def mb_diesel(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 diesel sintetico", "OM651/OM642 / OM654 diesel", "Mercedes-Benz Genuine, Mobil",
          [("5W-30 diesel MB 229.51", "confirmed")], "c/10-15k",
          [L("ML", ML+"aceite+5w30+mb+229.51+diesel"), L("Amazon", AZ+"mercedes+229.51+diesel+oil")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Mercedes-Benz", "Diesel OM651/OM642/OM654", "Mercedes-Benz Genuine, MANN",
          [("Verificar OEM", "verify")], "c/10-15k",
          [L("ML", ML+"filtro+aceite+mercedes+diesel"), L("Amazon", AZ+"mann+filtro+aceite+mercedes+diesel")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Diesel OM651/OM642/OM654", "Mercedes-Benz Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+mercedes+diesel"), L("Amazon", AZ+"mann+filtro+aire+mercedes+diesel")]),
        P("Motor", "Filtro Combustible", "Filtro combustible diesel", "Diesel c/separador de agua", "Mercedes-Benz Genuine, MANN",
          [("Verificar OEM", "verify")], "c/20-40k",
          [L("ML", ML+"filtro+combustible+mercedes+diesel"), L("Amazon", AZ+"mann+filtro+combustible+mercedes")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C carbon activo", "Cabina diesel", "Mercedes-Benz Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+mercedes+benz"), L("Amazon", AZ+"mann+filtro+cabina+mercedes")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado van/comercial", "Bosch, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+mercedes+sprinter"), L("Amazon", AZ+"bosch+pastillas+mercedes+sprinter")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, Mercedes-Benz Genuine",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+mercedes")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Continental, Pirelli",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Mitsubishi gasolina (ASX, Eclipse Cross, Lancer, Mirage, Outlander) ----------------
def mitsu_gasolina(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 / 5W-30 sintetico", "4B10/4B11/4B12/4B40/3A92 gasolina", "Mitsubishi Genuine, Mobil",
          [("0W-20 / 5W-30", "confirmed")], "c/10k",
          [L("ML", ML+"aceite+0w20+mitsubishi"), L("Amazon", AZ+"mitsubishi+0w20+oil")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Mitsubishi", "Motor gasolina 4B/3A", "Mitsubishi Genuine, MANN",
          [("Verificar OEM (ej. 1230A182 / MZ690115)", "verify")], "c/10k",
          [L("ML", ML+"filtro+aceite+mitsubishi"), L("Amazon", AZ+"mann+filtro+aceite+mitsubishi")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Gasolina 4B/3A", "Mitsubishi Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+mitsubishi"), L("Amazon", AZ+"mann+filtro+aire+mitsubishi")]),
        P("Encendido", "Bujias", "Bujias iridio", "Gasolina 4B/3A/4B40 turbo", "NGK, Bosch",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("ML", ML+"bujia+mitsubishi"), L("Amazon", AZ+"ngk+bujia+mitsubishi")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Cabina gasolina", "Mitsubishi Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+mitsubishi"), L("Amazon", AZ+"mann+filtro+cabina+mitsubishi")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Bosch, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+mitsubishi"), L("Amazon", AZ+"bosch+pastillas+mitsubishi")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, TRW",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+mitsubishi")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Bridgestone, Michelin, Yokohama",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- Mitsubishi diesel (L200, L300, Montero Sport) ----------------
def mitsu_diesel(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 diesel / 10W-30 sintetico", "4N15 2.4 DI-D / 4D56 diesel", "Mitsubishi Genuine, Mobil",
          [("5W-30 diesel / 10W-30 (4D56)", "confirmed")], "c/10k",
          [L("ML", ML+"aceite+5w30+diesel+mitsubishi"), L("Amazon", AZ+"mitsubishi+diesel+oil")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Mitsubishi", "Diesel 4N15/4D56", "Mitsubishi Genuine, MANN",
          [("Verificar OEM", "verify")], "c/10k",
          [L("ML", ML+"filtro+aceite+mitsubishi+diesel"), L("Amazon", AZ+"mann+filtro+aceite+mitsubishi+diesel")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Diesel 4N15/4D56", "Mitsubishi Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("ML", ML+"filtro+aire+mitsubishi+diesel"), L("Amazon", AZ+"mann+filtro+aire+mitsubishi+diesel")]),
        P("Motor", "Filtro Combustible", "Filtro combustible diesel", "Diesel c/separador de agua", "Mitsubishi Genuine, MANN",
          [("Verificar OEM", "verify")], "c/20-40k",
          [L("ML", ML+"filtro+combustible+mitsubishi+diesel"), L("Amazon", AZ+"mann+filtro+combustible+mitsubishi")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Cabina diesel", "Mitsubishi Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("ML", ML+"filtro+cabina+mitsubishi"), L("Amazon", AZ+"mann+filtro+cabina+mitsubishi")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado pickup/SUV/van", "Bosch, TRW",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("ML", ML+"pastillas+freno+mitsubishi+l200"), L("Amazon", AZ+"bosch+pastillas+mitsubishi")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Bosch, TRW",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+mitsubishi")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Bridgestone, Michelin, Yokohama",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


MB_MITSU_MAP = {
    # Mercedes-Benz
    "mercedes-benz-clase-a": (mb_gasolina, "205/55 R16"),
    "mercedes-benz-clase-c": (mb_gasolina, "225/50 R17"),
    "mercedes-benz-clase-e": (mb_gasolina, "245/45 R18"),
    "mercedes-benz-gla": (mb_gasolina, "235/55 R18"),
    "mercedes-benz-glc": (mb_gasolina, "235/60 R18"),
    "mercedes-benz-sprinter": (mb_diesel, "235/65 R16C"),
    # Mitsubishi
    "mitsubishi-asx": (mitsu_gasolina, "215/60 R17"),
    "mitsubishi-eclipse-cross": (mitsu_gasolina, "225/55 R18"),
    "mitsubishi-lancer": (mitsu_gasolina, "205/60 R16"),
    "mitsubishi-mirage": (mitsu_gasolina, "175/55 R15"),
    "mitsubishi-outlander": (mitsu_gasolina, "225/55 R18"),
    "mitsubishi-l200": (mitsu_diesel, "245/70 R16"),
    "mitsubishi-l300": (mitsu_diesel, "195 R14C"),
    "mitsubishi-montero-sport": (mitsu_diesel, "265/60 R18"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Mercedes-Benz %' OR name LIKE 'Mitsubishi %'").fetchall()
    n_mb = 0; n_mitsu = 0; skipped = []
    for vid, name in rows:
        entry = MB_MITSU_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        if name.startswith("Mercedes-Benz "):
            n_mb += 1
        else:
            n_mitsu += 1
    conn.commit()
    print("Mercedes-Benz actualizados:", n_mb)
    print("Mitsubishi actualizados:", n_mitsu)
    if skipped:
        print("Sin mapa (revisar):", sorted(set(base_id(s) for s in skipped)))
    else:
        print("Sin mapa: (ninguno)")
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
