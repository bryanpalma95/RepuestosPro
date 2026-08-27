# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Hyundai - BLOQUE 1.
City car / compactos gasolina. Motor por familia; frenos/neumaticos por modelo.
PN confirmado = confirmed, resto verify.
Ejecutar: python insert_hyundai_bloque1_componentes.py  (luego export_db.py + _regen_nav.py)
Fuentes publicas: hyundaipartsdeal, kiapartsnow, oempartsonline, amazon.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
Familias (Bloque 1):
  - Kappa 1.0/1.2 (Atos/i10, Grand i10, Morning/Picanto)
  - Gamma 1.4/1.6 MPI (Accent, Rio, Soluto, Verna, Elantra 1.6, i30 1.6)
  - Nu 2.0 (Elantra 2.0, i30 2.0)
  - Gamma 1.6 T-GDI turbo (Veloster)
Notas: filtro aceite cartucho universal Gamma/Nu/Kappa 26300-35505 (antiguo 26300-35504).
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
HPD = "https://www.hyundaipartsdeal.com/"

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- Kappa 1.0/1.2 (Atos/i10, Grand i10, Morning) ----------------
def hyundai_kappa(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-20 / 5W-30 sintetico", "~3.3L | Kappa 1.0/1.2 MPI", "Hyundai Genuine, Mobil, Shell",
          [("5W-20 / 5W-30", "confirmed")], "c/10k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"aceite+5w30+hyundai+i10")]),
        P("Motor", "Filtro Aceite", "Filtro aceite cartucho", "Cartucho universal Kappa/Gamma/Nu", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed"), ("26300-35504 (antiguo)", "confirmed")], "c/10k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Kappa 1.0/1.2 city car", "Hyundai Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+aire+hyundai+i10")]),
        P("Encendido", "Bujias", "Bujias x3/x4 iridio", "Kappa 1.0 (3 cil) / 1.2 (4 cil)", "NGK, Denso, Hyundai",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"bujia+ngk+hyundai+i10")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Atos/i10/Grand i10/Morning", "Hyundai Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+cabina+hyundai+i10")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado city car", "Hyundai Genuine, Frixa",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"pastillas+freno+hyundai+i10")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT3/DOT4", "Sistema hidraulico", "Hyundai, Bosch",
          [("DOT3 / DOT4", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+hyundai")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Bridgestone, Michelin, Goodyear",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- Gamma 1.4/1.6 MPI (Accent, Rio, Soluto, Verna, Elantra 1.6, i30 1.6) ----------------
def hyundai_gamma(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-20 / 5W-30 sintetico", "~3.6L | Gamma 1.4/1.6 MPI", "Hyundai Genuine, Mobil, Shell",
          [("5W-20 / 5W-30", "confirmed")], "c/10k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"aceite+5w30+hyundai+accent")]),
        P("Motor", "Filtro Aceite", "Filtro aceite cartucho", "Cartucho universal Gamma/Nu/Kappa", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed"), ("26300-35504 (antiguo)", "confirmed")], "c/10k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Gamma 1.4/1.6 MPI", "Hyundai Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+aire+hyundai+accent")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "Gamma 1.4/1.6 MPI", "NGK, Denso, Hyundai",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"bujia+ngk+hyundai+accent")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Accent/Rio/Soluto/Verna", "Hyundai Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+cabina+hyundai+accent")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado compacto", "Hyundai Genuine, Frixa",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"pastillas+freno+hyundai+accent")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT3/DOT4", "Sistema hidraulico", "Hyundai, Bosch",
          [("DOT3 / DOT4", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+hyundai")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Bridgestone, Michelin, Goodyear",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Nu 2.0 / Gamma 1.6 (Elantra, i30) ----------------
def hyundai_elantra(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-20 / 5W-30 sintetico", "~4.0L | Nu 2.0 MPI / Gamma 1.6", "Hyundai Genuine, Mobil, Shell",
          [("5W-20 / 5W-30", "confirmed")], "c/10k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"aceite+5w30+hyundai+elantra")]),
        P("Motor", "Filtro Aceite", "Filtro aceite cartucho", "Cartucho universal Gamma/Nu/Kappa", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed"), ("26300-35504 (antiguo)", "confirmed")], "c/10k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Elantra AD/CN7", "Hyundai Genuine, MANN",
          [("28113-AA100", "confirmed")], "c/15-30k",
          [L("Amazon", AZ+"28113-AA100"), L("ML", ML+"filtro+aire+hyundai+elantra")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "Nu 2.0 / Gamma 1.6", "NGK, Denso, Hyundai",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"bujia+ngk+hyundai+elantra")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Elantra AD/CN7", "Hyundai Genuine",
          [("97133-L1000", "confirmed")], "c/15-20k",
          [L("Amazon", AZ+"97133-L1000"), L("ML", ML+"filtro+cabina+hyundai+elantra")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Hyundai Genuine, Frixa",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"pastillas+freno+hyundai+elantra")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT3/DOT4", "Sistema hidraulico", "Hyundai, Bosch",
          [("DOT3 / DOT4", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+hyundai")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Gamma 1.6 T-GDI turbo (Veloster) ----------------
def hyundai_veloster(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 sintetico", "~4.2L | Gamma 1.6 T-GDI turbo", "Hyundai Genuine, Mobil, Shell",
          [("5W-30", "confirmed")], "c/10k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"aceite+5w30+hyundai+veloster")]),
        P("Motor", "Filtro Aceite", "Filtro aceite cartucho", "Cartucho universal Gamma/Nu/Kappa", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed"), ("26300-35504 (antiguo)", "confirmed")], "c/10k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Veloster 1.6 T-GDI", "Hyundai Genuine, K&N",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+aire+hyundai+veloster")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "1.6 T-GDI turbo", "NGK, Denso, Hyundai",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"bujia+ngk+hyundai+veloster")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Veloster", "Hyundai Genuine",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"filtro+cabina+hyundai+veloster")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado deportivo", "Hyundai Genuine, Frixa",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("HyundaiPartsDeal", HPD), L("ML", ML+"pastillas+freno+hyundai+veloster")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT3/DOT4", "Sistema hidraulico", "Hyundai, Bosch",
          [("DOT3 / DOT4", "confirmed")], "c/3 anos",
          [L("ML", ML+"liquido+frenos+hyundai")]),
        P("Neumaticos", "Neumatico", neum, "Deportivo", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


HYUNDAI_B1_MAP = {
    "hyundai-atos-i10": (hyundai_kappa, "155/70 R13"),
    "hyundai-grand-i10": (hyundai_kappa, "175/60 R15"),
    "hyundai-morning": (hyundai_kappa, "175/50 R15"),
    "hyundai-accent": (hyundai_gamma, "185/65 R15"),
    "hyundai-rio": (hyundai_gamma, "185/65 R15"),
    "hyundai-soluto": (hyundai_gamma, "185/65 R15"),
    "hyundai-verna-accent": (hyundai_gamma, "185/65 R15"),
    "hyundai-elantra": (hyundai_elantra, "205/55 R16"),
    "hyundai-i30": (hyundai_elantra, "205/55 R16"),
    "hyundai-veloster": (hyundai_veloster, "215/40 R18"),
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
        entry = HYUNDAI_B1_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        n += 1
    conn.commit()
    print("Hyundai (Bloque 1) actualizados:", n)
    if skipped:
        print("Sin mapa (otros bloques / revisar):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
