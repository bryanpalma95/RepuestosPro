# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Kia.
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_kia_componentes.py  (luego export_db.py + _regen_nav.py)
Fuentes publicas: kiapartsnow, hyundaipartsdeal, amazon.
Regla: solo se marca "confirmed" un PN con fuente publica fiable; sin PN publico = "verify".
Kia comparte mecanica con Hyundai; se reutilizan esas familias.
Familias:
  - D4CB 2.5 CRDi diesel (Frontier pickup/camion) - sin bujias, con filtro combustible
  - Gasolina antiguo 1.5/1.6 (Sephia sedan clasico)
  - Gasolina Nu/Theta 2.0/2.4 (Optima/K5 sedan mediano)
  - Gasolina Gamma 1.5/1.6 (Sonet SUV subcompacto)
  - Gasolina Gamma/Kappa 1.0T/1.4 (Stonic SUV subcompacto)
  - Lambda 3.5 V6 (Telluride SUV grande, bujias x6)
  - Hibrido Kappa 1.6 GDI + motor electrico (Niro)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
KPN = "https://www.kiapartsnow.com/"

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- D4CB 2.5 CRDi diesel (Frontier) ----------------
def kia_frontier(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 diesel sintetico", "Motor D4CB 2.5 CRDi | diesel", "Hyundai/Kia Genuine, MANN",
          [("5W-30 diesel (ACEA C3)", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"aceite+5w30+diesel+kia+frontier")]),
        P("Motor", "Filtro Aceite", "Filtro aceite diesel D4CB", "2.5 CRDi diesel", "Hyundai/Kia Genuine, MANN",
          [("26330-4A001", "confirmed"), ("26330-4A700", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aceite+26330+4a001")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Frontier 2.5 CRDi", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aire+kia+frontier")]),
        P("Motor", "Filtro Combustible", "Filtro combustible diesel", "Sistema CRDi diesel", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+combustible+diesel+kia+frontier")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Frontier", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+cabina+kia+frontier")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado pickup", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("KiaPartsNow", KPN), L("ML", ML+"pastillas+freno+kia+frontier")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia Genuine, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+kia")]),
        P("Neumaticos", "Neumatico", neum, "Pickup/camion", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Gasolina antiguo 1.5/1.6 (Sephia) ----------------
def kia_sephia(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-20 / 5W-30 sintetico", "Motor gasolina 1.5/1.6 | sedan clasico", "Hyundai/Kia Genuine, MANN",
          [("5W-20 / 5W-30", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"aceite+kia+sephia")]),
        P("Motor", "Filtro Aceite", "Filtro aceite gasolina", "Gasolina antiguo 1.5/1.6", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed"), ("26300-35504", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Sephia 1.5/1.6", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aire+kia+sephia")]),
        P("Encendido", "Bujias", "Bujias x4", "Gasolina 1.5/1.6", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/30-60k",
          [L("KiaPartsNow", KPN), L("ML", ML+"bujia+ngk+kia+sephia")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Sephia", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+cabina+kia+sephia")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("KiaPartsNow", KPN), L("ML", ML+"pastillas+freno+kia+sephia")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia Genuine, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+kia")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Bridgestone, Michelin",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- Gasolina Nu/Theta 2.0/2.4 (Optima/K5) ----------------
def kia_optima_k5(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-20 / 5W-30 sintetico", "Motor Nu/Theta 2.0/2.4 gasolina | sedan mediano", "Hyundai/Kia Genuine, MANN",
          [("5W-20 / 5W-30", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"aceite+kia+optima")]),
        P("Motor", "Filtro Aceite", "Filtro aceite gasolina", "Nu/Theta 2.0/2.4", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Optima/K5 2.0/2.4", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aire+kia+optima")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "Nu/Theta 2.0/2.4", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("KiaPartsNow", KPN), L("ML", ML+"bujia+ngk+kia+optima")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Optima/K5", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+cabina+kia+optima")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("KiaPartsNow", KPN), L("ML", ML+"pastillas+freno+kia+optima")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia Genuine, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+kia")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Gasolina Gamma 1.5/1.6 (Sonet) ----------------
def kia_sonet(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-20 / 5W-30 sintetico", "Motor Gamma 1.5/1.6 gasolina | SUV subcompacto", "Hyundai/Kia Genuine, MANN",
          [("5W-20 / 5W-30", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"aceite+kia+sonet")]),
        P("Motor", "Filtro Aceite", "Filtro aceite gasolina", "Gamma 1.5/1.6", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Sonet 1.5/1.6", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aire+kia+sonet")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "Gamma 1.5/1.6", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("KiaPartsNow", KPN), L("ML", ML+"bujia+ngk+kia+sonet")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Sonet", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+cabina+kia+sonet")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("KiaPartsNow", KPN), L("ML", ML+"pastillas+freno+kia+sonet")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia Genuine, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+kia")]),
        P("Neumaticos", "Neumatico", neum, "SUV subcompacto", "Bridgestone, Michelin, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- Gasolina Gamma/Kappa 1.0T/1.4 (Stonic) ----------------
def kia_stonic(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-20 / 5W-30 sintetico", "Motor Gamma/Kappa 1.0T/1.4 gasolina | SUV subcompacto", "Hyundai/Kia Genuine, MANN",
          [("5W-20 / 5W-30", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"aceite+kia+stonic")]),
        P("Motor", "Filtro Aceite", "Filtro aceite gasolina", "Gamma/Kappa 1.0T/1.4", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Stonic 1.0T/1.4", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aire+kia+stonic")]),
        P("Encendido", "Bujias", "Bujias x3/x4 iridio", "Gamma/Kappa 1.0T/1.4", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("KiaPartsNow", KPN), L("ML", ML+"bujia+ngk+kia+stonic")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Stonic", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+cabina+kia+stonic")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("KiaPartsNow", KPN), L("ML", ML+"pastillas+freno+kia+stonic")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia Genuine, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+kia")]),
        P("Neumaticos", "Neumatico", neum, "SUV subcompacto", "Bridgestone, Michelin, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Bridgestone", "https://www.bridgestone.cl/")]),
    ]


# ---------------- Lambda 3.5 V6 (Telluride) ----------------
def kia_telluride(neum):
    return [
        P("Motor", "Aceite", "Aceite 5W-20 / 5W-30 sintetico", "Motor Lambda 3.5 V6 gasolina | SUV grande", "Hyundai/Kia Genuine, MANN",
          [("5W-20 / 5W-30", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"aceite+kia+telluride")]),
        P("Motor", "Filtro Aceite", "Filtro aceite gasolina", "Lambda 3.5 V6", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Telluride 3.5 V6", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aire+kia+telluride")]),
        P("Encendido", "Bujias", "Bujias x6 iridio", "Lambda 3.5 V6", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/100k",
          [L("KiaPartsNow", KPN), L("ML", ML+"bujia+ngk+kia+telluride")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Telluride", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+cabina+kia+telluride")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado SUV grande", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("KiaPartsNow", KPN), L("ML", ML+"pastillas+freno+kia+telluride")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia Genuine, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+kia")]),
        P("Neumaticos", "Neumatico", neum, "SUV grande", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


# ---------------- Hibrido Kappa 1.6 GDI + electrico (Niro) ----------------
def kia_niro(neum):
    return [
        P("Motor", "Aceite", "Aceite 0W-20 sintetico", "Motor Kappa 1.6 GDI hibrido | sistema HEV", "Hyundai/Kia Genuine, MANN",
          [("0W-20", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"aceite+0w20+kia+niro")]),
        P("Motor", "Filtro Aceite", "Filtro aceite gasolina/hibrido", "Kappa 1.6 GDI", "Hyundai/Kia Genuine, MANN",
          [("26300-35505", "confirmed")], "c/10k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aceite+26300+35505")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", "Niro 1.6 GDI hibrido", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+aire+kia+niro")]),
        P("Encendido", "Bujias", "Bujias x4 iridio", "1.6 GDI hibrido", "NGK, Denso",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("KiaPartsNow", KPN), L("ML", ML+"bujia+ngk+kia+niro")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", "Niro", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("KiaPartsNow", KPN), L("ML", ML+"filtro+cabina+kia+niro")]),
        P("Alta Tension", "Sistema HEV", "Sistema hibrido / bateria alta tension", "Sistema hibrido/EV - revisar en concesionario", "Hyundai/Kia Genuine",
          [("Sistema hibrido/EV - revisar en concesionario", "verify")], None,
          [L("KiaPartsNow", KPN), L("ML", ML+"kia+niro+hibrido")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado (freno regenerativo)", "Hyundai/Kia Genuine, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("KiaPartsNow", KPN), L("ML", ML+"pastillas+freno+kia+niro")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Hyundai/Kia Genuine, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+kia")]),
        P("Neumaticos", "Neumatico", neum, "SUV hibrido", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


KIA_MAP = {
    "kia-frontier": (kia_frontier, "195 R15C"),
    "kia-sephia": (kia_sephia, "185/65 R14"),
    "kia-optima-k5": (kia_optima_k5, "215/55 R17"),
    "kia-sonet": (kia_sonet, "215/60 R16"),
    "kia-stonic": (kia_stonic, "205/55 R17"),
    "kia-telluride": (kia_telluride, "245/60 R18"),
    "kia-niro": (kia_niro, "205/60 R16"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Kia %'").fetchall()
    n = 0; skipped = []
    for vid, name in rows:
        entry = KIA_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum = entry
        clear_and_insert(c, vid, gen(neum))
        n += 1
    conn.commit()
    print("Kia actualizados:", n)
    if skipped:
        print("Sin mapa (revisar):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
