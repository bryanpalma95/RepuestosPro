# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Hyundai/Kia (BLOQUE 2).
Cubre SUV/medianos gasolina + V6 Lambda. Motor por familia; frenos/neumaticos por modelo.
PN confirmado = confirmed, resto verify. Ejecutar: python insert_hyundai_bloque2_componentes.py
Fuentes publicas: hyundaipartsdeal, kiapartsnow, oempartsonline, amazon.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
Familias:
  - Nu/Theta 1.6/2.0/2.4 gasolina (Tucson, Santa Fe, Sonata, Creta, Seltos, Sportage, Cerato)
  - Lambda 3.5 V6 (Palisade, Telluride, Carnival) [bujias x6, ~5.7L aceite]
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
OEM = "https://hyundai.oempartsonline.com/"

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- Nu/Theta 1.6/2.0/2.4 gasolina (SUV/medianos) ----------------
def nu_theta(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-20 / 5W-30 sintetico", "1.6/2.0/2.4 gasolina Nu/Theta/Gamma", "Hyundai/Kia Genuine, Mobil, Idemitsu",
          [("5W-20 / 5W-30", "confirmed")], "c/10k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"aceite+5w30+hyundai")]),
        P("Motor", "Filtro Aceite", "Filtro aceite cartucho Hyundai/Kia", "Cartucho universal Nu/Theta/Gamma", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed"), ("26300-35504 (antiguo)", "confirmed")], "c/10k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Segun version", "Hyundai/Kia Genuine, MANN, K&N",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"filtro+aire+hyundai")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "1.6/2.0/2.4 gasolina", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/100k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"bujia+ngk+hyundai")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Segun version", "Hyundai/Kia Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"filtro+cabina+hyundai")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Hyundai/Kia Genuine, Akebono",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"pastillas+freno+hyundai")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+hyundai")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Lambda 3.5 V6 (Palisade, Telluride, Carnival) ----------------
def lambda_v6(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 sintetico", "~5.7L | 3.5 V6 Lambda gasolina", "Hyundai/Kia Genuine, Mobil",
          [("5W-30", "confirmed")], "c/10k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"aceite+5w30+hyundai+palisade")]),
        P("Motor", "Filtro Aceite", "Filtro aceite cartucho Hyundai/Kia", "Cartucho universal V6 Lambda", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed"), ("26300-35504 (antiguo)", "confirmed")], "c/10k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "V6 3.5 Lambda", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"filtro+aire+hyundai+palisade")]),
        P("Encendido", "Bujias", "Bujias x6 iridio", "V6 3.5 Lambda", "NGK iridio, Denso",
          [("Verificar OEM", "verify")], "c/100k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"bujia+ngk+hyundai+v6")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "SUV grande / minivan", "Hyundai/Kia Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"filtro+cabina+hyundai+palisade")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado SUV/minivan", "Hyundai/Kia Genuine, Akebono",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("OEMPartsOnline", OEM), L("ML", ML+"pastillas+freno+hyundai+palisade")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+hyundai")]),
        P("Neumaticos", "Neumatico", neum, "SUV/minivan grande", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


HYUNDAI_B2_MAP = {
    "hyundai-tucson": (nu_theta, "235/60 R18"),
    "hyundai-santa-fe": (nu_theta, "235/60 R18"),
    "hyundai-sonata": (nu_theta, "235/45 R18"),
    "hyundai-creta": (nu_theta, "215/60 R17"),
    "hyundai-seltos": (nu_theta, "235/55 R18"),
    "hyundai-sportage": (nu_theta, "235/60 R18"),
    "hyundai-sorento": (nu_theta, "235/60 R18"),
    "hyundai-cerato": (nu_theta, "205/55 R16"),
    "hyundai-palisade": (lambda_v6, "245/50 R20"),
    "hyundai-telluride": (lambda_v6, "245/60 R18"),
    "hyundai-carnival": (lambda_v6, "235/60 R18"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Hyundai %'").fetchall()
    n = 0; skipped = []
    for vid, name in rows:
        entry = HYUNDAI_B2_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        n += 1
    conn.commit()
    print("Hyundai B2 actualizados:", n)
    if skipped:
        print("Sin mapa (otros bloques):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
