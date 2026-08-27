# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Honda.
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_honda_componentes.py  (luego export_db.py + _regen_nav.py)
Fuentes publicas: hondapartsnow, oempartsonline, filterbuy, amazon.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
Familias:
  - L15B7 1.5T Earth Dreams turbo (Civic, CR-V, Accord base, HR-V turbo)
  - L15/LEA 1.5 i-VTEC aspirado (City, Fit, HR-V aspirado)
  - K24 2.4 i-VTEC (Accord 2.4, CR-V 2.4) [familia disponible, no mapeada por defecto]
  - J35 3.5 V6 SOHC i-VTEC (Pilot, Ridgeline, Accord V6)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
HPN = "https://www.hondapartsnow.com/"

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- L15B7 1.5T turbo (Civic, CR-V, Accord base, HR-V turbo) ----------------
def honda_l15_turbo(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 sintetico", "~3.7L | 1.5T L15B7 Earth Dreams", "Honda HTO-06, Mobil, Idemitsu",
          [("0W-20 (Honda HTO-06)", "confirmed")], "c/10k",
          [L("HondaPartsNow", HPN), L("ML", ML+"aceite+0w20+honda+civic")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Honda", "1.5T (comparte con 1.5/1.8)", "Honda Genuine, Fram",
          [("15400-PLM-A02", "confirmed")], "c/10k",
          [L("HondaPartsNow", HPN), L("ML", ML+"filtro+aceite+15400+plm+a02")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Civic/CR-V 1.5T turbo", "Honda Genuine, K&N",
          [("17220-5AA-A00", "confirmed")], "c/15-30k",
          [L("Amazon", AZ+"17220-5AA-A00"), L("ML", ML+"filtro+aire+honda+civic+turbo")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "1.5T turbo", "NGK, Denso",
          [("NGK DXE22HCR11S", "confirmed")], "c/60-100k",
          [L("HondaPartsNow", HPN), L("ML", ML+"bujia+ngk+honda+civic+turbo")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Civic/CR-V gen10+", "Honda Genuine",
          [("80292-TF0-G01", "confirmed"), ("80292-TBA-A11 (Civic 16-21)", "confirmed")], "c/15-20k",
          [L("Amazon", AZ+"80292-TF0-G01"), L("ML", ML+"filtro+cabina+honda+civic")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Honda Genuine, Akebono",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("HondaPartsNow", HPN), L("ML", ML+"pastillas+freno+honda+civic")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT3/DOT4", "Sistema hidraulico", "Honda, Bosch",
          [("DOT3 (Honda)", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+honda")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- L15/LEA 1.5 i-VTEC aspirado (City, Fit, HR-V aspirado) ----------------
def honda_l15_na(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 / 5W-30 sintetico", "~3.6L | 1.5 i-VTEC aspirado", "Honda HTO-06, Mobil",
          [("0W-20 (Honda HTO-06)", "confirmed")], "c/10k",
          [L("HondaPartsNow", HPN), L("ML", ML+"aceite+0w20+honda+fit")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Honda", "1.5 i-VTEC (Fit/City/HR-V)", "Honda Genuine, Fram",
          [("15400-PLM-A02", "confirmed")], "c/10k",
          [L("HondaPartsNow", HPN), L("ML", ML+"filtro+aceite+15400+plm+a02")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Fit/City/HR-V 1.5", "Honda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("HondaPartsNow", HPN), L("ML", ML+"filtro+aire+honda+fit")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "1.5 i-VTEC", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/100k",
          [L("HondaPartsNow", HPN), L("ML", ML+"bujia+honda+fit")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Fit/City/HR-V", "Honda Genuine",
          [("80292-SDA-407", "confirmed")], "c/15-20k",
          [L("OEMPartsOnline", "https://honda.oempartsonline.com/oem-parts/honda-cabin-air-filter-80292sda407"), L("ML", ML+"filtro+cabina+honda+fit")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado compacto", "Honda Genuine, Akebono",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("HondaPartsNow", HPN), L("ML", ML+"pastillas+freno+honda+fit")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT3/DOT4", "Sistema hidraulico", "Honda, Bosch",
          [("DOT3 (Honda)", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+honda")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Bridgestone, Michelin",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- K24 2.4 i-VTEC (Accord 2.4, CR-V 2.4) ----------------
def honda_k24(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 / 5W-30 sintetico", "~4.2L | 2.4 K24 i-VTEC", "Honda HTO-06, Mobil",
          [("0W-20 (Honda HTO-06)", "confirmed"), ("5W-30", "confirmed")], "c/10k",
          [L("HondaPartsNow", HPN), L("ML", ML+"aceite+honda+accord+2.4")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Honda (grande)", "2.4 K24 / V6 J35", "Honda Genuine, Fram",
          [("15400-RTA-003", "confirmed")], "c/10k",
          [L("HondaPartsNow", HPN), L("ML", ML+"filtro+aceite+15400+rta+003")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "CR-V/Accord 2.4", "Honda Genuine, MANN",
          [("17220-R5A-A00 (CR-V)", "confirmed")], "c/15-30k",
          [L("HondaPartsNow", "https://www.hondapartsnow.com/oem-honda-cr_v-air_filter.html"), L("ML", ML+"filtro+aire+honda+crv")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "2.4 K24", "NGK iridio, Denso",
          [("NGK DILKAR8P8SY (CR-V)", "confirmed")], "c/100k",
          [L("HondaPartsNow", "https://www.hondapartsnow.com/oem-honda-cr_v-spark_plug.html"), L("ML", ML+"bujia+ngk+honda+crv")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Accord/CR-V", "Honda Genuine",
          [("80292-SDA-407", "confirmed")], "c/15-20k",
          [L("OEMPartsOnline", "https://honda.oempartsonline.com/oem-parts/honda-cabin-air-filter-80292sda407"), L("ML", ML+"filtro+cabina+honda+accord")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Honda Genuine, Akebono",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("HondaPartsNow", HPN), L("ML", ML+"pastillas+freno+honda+accord")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT3/DOT4", "Sistema hidraulico", "Honda, Bosch",
          [("DOT3 (Honda)", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+honda")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- J35 3.5 V6 (Pilot, Ridgeline, Accord V6) ----------------
def honda_j35(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 sintetico", "~4.5L | 3.5 V6 J35 SOHC i-VTEC", "Honda HTO-06, Mobil",
          [("0W-20 (Honda HTO-06)", "confirmed")], "c/10k",
          [L("HondaPartsNow", HPN), L("ML", ML+"aceite+0w20+honda+pilot")]),
        P("Motor", "Filtro Aceite", "Filtro aceite Honda (grande)", "V6 J35 / 2.4 K24", "Honda Genuine, Fram",
          [("15400-RTA-003", "confirmed")], "c/10k",
          [L("HondaPartsNow", HPN), L("ML", ML+"filtro+aceite+15400+rta+003")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Pilot/Ridgeline V6", "Honda Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("HondaPartsNow", HPN), L("ML", ML+"filtro+aire+honda+pilot")]),
        P("Encendido", "Bujias", "Bujias x6 iridio", "V6 J35", "NGK iridio, Denso",
          [("Verificar OEM", "verify")], "c/100k",
          [L("HondaPartsNow", HPN), L("ML", ML+"bujia+ngk+honda+pilot")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Pilot/Ridgeline", "Honda Genuine",
          [("80292-SDA-407", "confirmed")], "c/15-20k",
          [L("OEMPartsOnline", "https://honda.oempartsonline.com/oem-parts/honda-cabin-air-filter-80292sda407"), L("ML", ML+"filtro+cabina+honda+pilot")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado SUV/pickup", "Honda Genuine, Akebono",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("HondaPartsNow", HPN), L("ML", ML+"pastillas+freno+honda+pilot")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT3/DOT4", "Sistema hidraulico", "Honda, Bosch",
          [("DOT3 (Honda)", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+honda")]),
        P("Neumaticos", "Neumatico", neum, "SUV/pickup", "Michelin, BFGoodrich, Bridgestone",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


HONDA_MAP = {
    "honda-civic": (honda_l15_turbo, "215/50 R17"),
    "honda-cr-v": (honda_l15_turbo, "235/60 R18"),
    "honda-accord": (honda_l15_turbo, "235/45 R18"),
    "honda-hr-v": (honda_l15_na, "215/55 R17"),
    "honda-city": (honda_l15_na, "185/60 R15"),
    "honda-fit": (honda_l15_na, "185/60 R15"),
    "honda-pilot": (honda_j35, "245/60 R18"),
    "honda-ridgeline": (honda_j35, "245/60 R18"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Honda %'").fetchall()
    n = 0; skipped = []
    for vid, name in rows:
        entry = HONDA_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        n += 1
    conn.commit()
    print("Honda actualizados:", n)
    if skipped:
        print("Sin mapa (revisar):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
