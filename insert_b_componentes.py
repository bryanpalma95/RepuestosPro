# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marcas B (BMW familia B48 + BAIC X55).
Actualiza los registros existentes en db.sqlite con componentes OEM verificados.
Motor B38/B48/B58 compartido -> mismos comps de MOTOR en todos los BMW.
Frenos/suspension difieren por plataforma (F20/F30 vs UKL/G).
Ejecutar: python insert_b_componentes.py  (luego export_db.py)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; BW = "https://www.bimmerworld.com/"

def link(t, u): return {"t": t, "u": u}

def motor_bmw_b48():
    return [
        ("Motor", "Aceite", "Aceite 5W-30 LL-04", "~5.2-6.5L segun motor", "BMW, Castrol Edge",
         [("5W-30 BMW LL-04", "confirmed")], "c/15k",
         [link("ML", ML+"aceite+5w30+bmw+ll04"), link("Castrol", "https://www.castrol.com/")]),
        ("Motor", "Filtro Aceite", "Filtro aceite B38/B46/B48", "Motor 4cil turbo", "MANN, Mahle, BMW",
         [("11428593186", "confirmed"), ("11428583898", "confirmed")], "c/15k",
         [link("BimmerWorld", BW+"Engine/Engine-Maintenance/Engine-Oil-Filter-OEM-B46-B48-11428593186.html"), link("ML", ML+"filtro+aceite+bmw")]),
        ("Motor", "Filtro Aire", "Filtro aire motor", "F30 320i/328i / U11", "MANN, BMW",
         [("13718511668", "confirmed"), ("13718513944", "confirmed")], "c/30-60k",
         [link("BimmerWorld", BW+"About-Us/BMW-2-Series-Parts/OEM-BMW-Air-Filter-13718511668.html"), link("ML", ML+"filtro+aire+bmw")]),
        ("Encendido", "Bujias", "Bujias x4 B46A/B48A/B58A", "NGK/Champion iridio", "NGK, Bosch, BMW",
         [("12120040551", "confirmed")], "c/45-60k",
         [link("BimmerWorld", BW+"About-Us/BMW-2-Series-Parts/Spark-Plug-NGK-B46-B58-12120040551.html"), link("ML", ML+"bujia+bmw")]),
        ("Encendido", "Bobina", "Bobina de encendido", "Coil-on-plug (1 por cilindro)", "Delphi, Bosch, BMW",
         [("12138616153", "confirmed")], "por sintoma",
         [link("OEMparts", "https://bmw.oempartsonline.com/oem-parts/bmw-ignition-coil-12138616153"), link("ML", ML+"bobina+encendido+bmw")]),
        ("Refrigeracion", "Bomba Agua", "Bomba agua electrica + termostato", "N20/B-series electrica", "Pierburg, BMW",
         [("11518635089", "confirmed")], "por sintoma",
         [link("OEMbimmer", "https://oembimmerparts.com/products/bmw-f30-328i-water-pump-kit-11518635089"), link("ML", ML+"bomba+agua+bmw")]),
        ("Distribucion", "Cadena", "Cadena de distribucion", "Sin cambio programado", "BMW",
         [("Cadena (B-series)", "confirmed")], None,
         [link("BimmerWorld", BW)]),
    ]

def frenos_f30():
    return [
        ("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "F20/F30", "TRW, Textar, BMW",
         [("34106859181", "confirmed")], "c/30-50k",
         [link("OEMparts", "https://parts.bmwofsouthatlanta.com/oem-parts/bmw-brake-pads-front-34106859181"), link("ML", ML+"pastillas+freno+bmw+serie+3")]),
        ("Frenos", "Disco Tras.", "Disco freno trasero", "F30 4cil", "Zimmermann, ATE, BMW",
         [("34216864900", "confirmed")], "c/60-80k",
         [link("OEMbimmer", "https://oembimmerparts.com/products/bmw-f30-stage1-rear-brake-kit"), link("ML", ML+"disco+freno+bmw")]),
        ("Confort", "Filtro Cabina", "Filtro habitaculo carbon", "F20/F30/F32", "MANN, Bosch, BMW",
         [("64119237555", "confirmed")], "c/15-30k",
         [link("OEMparts", "https://bmw.oempartsonline.com/oem-parts/bmw-cabin-air-filter-64119237555"), link("ML", ML+"filtro+cabina+bmw")]),
        ("Suspension", "Amortiguador Del.", "Amortiguador delantero", "31316873803 izq / 31316873804 der (F30 LCI)", "Sachs, Bilstein, BMW",
         [("31316873803", "confirmed"), ("31316873804", "confirmed")], "por sintoma",
         [link("BimmerWorld", BW+"Suspension-Steering/OEM-BMW-Shocks-Struts/Front-Left-Strut-BMW-F30-328d-328i-330i-xDrive-LCI.html"), link("ML", ML+"amortiguador+bmw+serie+3")]),
    ]

def frenos_ukl():
    return [
        ("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "F48/F39/G20/G01 28i-30i", "TRW, Textar, BMW",
         [("34106888778", "confirmed"), ("34106898307", "confirmed")], "c/30-50k",
         [link("BimmerWorld", BW+"About-Us/BMW-2-Series-Parts/OEM-Front-Brake-Pad-Set-34106888778.html"), link("ML", ML+"pastillas+freno+bmw+x1")]),
        ("Frenos", "Pastillas Tras.", "Pastillas freno traseras", "F48 X1/F39 X2 (TRW)", "TRW, BMW",
         [("34216859917", "confirmed")], "c/40-60k",
         [link("BimmerWorld", BW+"About-Us/i3-60Ah-Rex/Rear-Brake-Pad-Set-TRW-i3-34216859917.html"), link("ML", ML+"pastillas+freno+trasera+bmw+x1")]),
        ("Confort", "Filtro Cabina", "Filtro habitaculo carbon", "F48 X1/F39 X2", "MANN, Bosch, BMW",
         [("64316835405", "confirmed")], "c/15-30k",
         [link("BimmerWorld", BW+"BMW-Interior/Microfilter-Charcoal-OEM-F44-Gran-Coupe-64316835405.html"), link("ML", ML+"filtro+cabina+bmw+x1")]),
        ("Suspension", "Amortiguador Del.", "Amortiguador delantero", "31316861671 izq / 31316861672 der (F48 X1)", "Sachs, BMW",
         [("31316861671", "confirmed"), ("31316861672", "confirmed")], "por sintoma",
         [link("Amazon", "https://www.amazon.com/2016-2022-xDrive28i-31316861671-31306886755-31316882849/dp/B0DYHZ7KVT"), link("ML", ML+"amortiguador+bmw+x1")]),
    ]

def comps_baic_x55():
    return [
        ("Motor", "Aceite", "Aceite 5W-30 sintetico", "~4.0L | Motor 1.5T Magic Core", "Mobil, Shell, Castrol",
         [("5W-30 API SP", "confirmed")], "c/10k",
         [link("Opinautos", "https://www.opinautos.com/baic/x55/guias/lubricacion"), link("ML", ML+"aceite+5w30+baic+x55")]),
        ("Motor", "Filtro Aceite", "Filtro aceite 1.5T", "Tipo spin-on, verificar rosca", "MANN, Bosch",
         [("Verificar OEM", "verify")], "c/10k",
         [link("Opinautos", "https://www.opinautos.com/baic/x55/guias/filtros"), link("ML", ML+"filtro+aceite+baic+x55")]),
        ("Motor", "Filtro Aire", "Filtro aire motor", "Panel", "MANN, Bosch",
         [("Verificar OEM", "verify")], "c/10-15k",
         [link("Opinautos", "https://www.opinautos.com/baic/x55/guias/filtros"), link("ML", ML+"filtro+aire+baic+x55")]),
        ("Distribucion", "Cadena", "Cadena de distribucion", "Motor 1.5T turbo, sin cambio programado", "BAIC",
         [("Cadena (A151T/A156T2H)", "confirmed")], None,
         [link("Opinautos", "https://www.opinautos.com/baic/x55/guias"), link("BAIC", "https://www.baicglobal.com/es/models/26")]),
        ("Frenos", "Liquido Frenos", "Liquido de frenos DOT 4", "Sistema hidraulico", "Bosch, ATE",
         [("DOT 4", "confirmed")], "c/2 anios",
         [link("Opinautos", "https://www.opinautos.com/us/baic/x55/guias/liquido-de-frenos"), link("ML", ML+"liquido+freno+dot4")]),
    ]

def clear_and_insert(c, vid, comps):
    cats = c.execute("SELECT id FROM categories WHERE vehicle_id=?", (vid,)).fetchall()
    for (cid,) in cats:
        parts = c.execute("SELECT id FROM parts WHERE category_id=?", (cid,)).fetchall()
        for (pid,) in parts:
            c.execute("DELETE FROM part_refs WHERE part_id=?", (pid,))
            c.execute("DELETE FROM part_links WHERE part_id=?", (pid,))
        c.execute("DELETE FROM parts WHERE category_id=?", (cid,))
    c.execute("DELETE FROM categories WHERE vehicle_id=?", (vid,))
    order = 0; cat_ids = {}
    for (cat, catlabel, name, details, brands, refs, interval, links) in comps:
        if cat not in cat_ids:
            order += 1
            c.execute("INSERT INTO categories (vehicle_id, name, sort_order) VALUES (?,?,?)", (vid, cat, order))
            cat_ids[cat] = c.lastrowid
        c.execute("INSERT INTO parts (category_id, cat_label, name, details, brands, interval_info) VALUES (?,?,?,?,?,?)",
                  (cat_ids[cat], catlabel, name, details, brands, interval))
        pid = c.lastrowid
        for (r, s) in refs:
            c.execute("INSERT INTO part_refs (part_id, reference, status) VALUES (?,?,?)", (pid, r, s))
        for l in links:
            c.execute("INSERT INTO part_links (part_id, label, url) VALUES (?,?,?)", (pid, l["t"], l["u"]))

def main():
    conn = sqlite3.connect(DB); conn.execute("PRAGMA foreign_keys=ON"); c = conn.cursor()
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'BMW%' OR name LIKE 'BAIC%'").fetchall()
    n_bmw = n_baic = 0
    for vid, name in rows:
        if name.startswith("BAIC"):
            clear_and_insert(c, vid, comps_baic_x55()); n_baic += 1
        elif name.startswith("BMW"):
            comps = motor_bmw_b48()[:]
            mm = re.search(r'(\d{4})$', vid); year = int(mm.group(1)) if mm else 2020
            if vid.startswith("bmw-serie-3") and year >= 2020:
                comps += frenos_ukl()
            elif vid.startswith("bmw-serie-1") or vid.startswith("bmw-serie-3") or vid.startswith("bmw-x5"):
                comps += frenos_f30()
            else:
                comps += frenos_ukl()
            clear_and_insert(c, vid, comps); n_bmw += 1
    conn.commit()
    print(f"Actualizados: BMW={n_bmw}, BAIC={n_baic}")
    total_parts = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales en db.sqlite:", total_parts)
    conn.close()

if __name__ == "__main__":
    main()
