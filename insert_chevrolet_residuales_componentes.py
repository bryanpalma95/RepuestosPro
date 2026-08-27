# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca Chevrolet (residuales incompletos).
Completa modelos Chevrolet que quedaron con <5 componentes en tandas anteriores.
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_chevrolet_residuales_componentes.py
Fuentes publicas: gmpartsdirect, acdelco, amazon.
Regla: solo se marca "confirmed" un PN/spec con fuente publica fiable; sin PN publico = "verify".
Solo se procesan los base_id del mapa; el resto de Chevrolet ya esta completo y NO se toca.
Familias:
  - GM gasolina (Captiva 2.4 Ecotec, Corsa 1.4/1.6/1.8, Optra 1.6/1.8 Daewoo/Holden)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
GMP = "https://www.gmpartsdirect.com/"

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links): return (cat, lab, name, det, brands, refs, interval, links)


# ---------------- GM gasolina (Captiva 2.4, Corsa 1.4/1.6/1.8, Optra 1.6/1.8) ----------------
def gm_gasolina(neum, det):
    return [
        P("Motor", "Aceite", "Aceite 5W-30 dexos1 sintetico", det + " gasolina", "Chevrolet/GM Genuine, ACDelco, MANN",
          [("5W-30 dexos1", "confirmed")], "c/10k",
          [L("GMPartsDirect", GMP), L("ML", ML+"aceite+5w30+dexos1+chevrolet")]),
        P("Motor", "Filtro Aceite", "Filtro aceite GM", det, "Chevrolet/GM Genuine, ACDelco, MANN",
          [("Verificar OEM", "verify")], "c/10k",
          [L("GMPartsDirect", GMP), L("ML", ML+"filtro+aceite+chevrolet")]),
        P("Motor", "Filtro Aire", "Filtro aire motor", det, "Chevrolet/GM Genuine, ACDelco, MANN",
          [("Verificar OEM", "verify")], "c/15-30k",
          [L("GMPartsDirect", GMP), L("ML", ML+"filtro+aire+chevrolet")]),
        P("Encendido", "Bujias", "Bujias iridio/platino", det, "NGK, ACDelco",
          [("Verificar OEM", "verify")], "c/60-100k",
          [L("GMPartsDirect", GMP), L("ML", ML+"bujia+ngk+chevrolet")]),
        P("Confort", "Filtro Cabina", "Filtro habitaculo A/C", det, "Chevrolet/GM Genuine, ACDelco, MANN",
          [("Verificar OEM", "verify")], "c/15-20k",
          [L("GMPartsDirect", GMP), L("ML", ML+"filtro+cabina+chevrolet")]),
        P("Frenos", "Pastillas Del.", "Pastillas freno delanteras", "Disco ventilado", "Chevrolet/GM Genuine, ACDelco, MANN",
          [("Verificar OEM", "verify")], "c/30-50k",
          [L("GMPartsDirect", GMP), L("ML", ML+"pastillas+freno+chevrolet")]),
        P("Frenos", "Liquido Frenos", "Liquido de frenos DOT4", "Sistema hidraulico", "Chevrolet/GM, ACDelco, Bosch",
          [("DOT4", "confirmed")], "c/2-3 anos",
          [L("ML", ML+"liquido+frenos+dot4+chevrolet")]),
        P("Neumaticos", "Neumatico", neum, "Segun version", "Michelin, Bridgestone, Continental",
          [(neum, "confirmed")], None,
          [L("ML", ML+"neumatico+"+neum.replace('/', '+').replace(' ', '+')), L("Michelin", "https://www.michelin.cl/")]),
    ]


CHEVROLET_MAP = {
    "chevrolet-captiva": (gm_gasolina, "235/60 R17", "2.4 Ecotec"),
    "chevrolet-corsa": (gm_gasolina, "185/65 R14", "1.4/1.6/1.8"),
    "chevrolet-optra": (gm_gasolina, "195/60 R15", "1.6/1.8 Daewoo/Holden"),
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
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Chevrolet %'").fetchall()
    n = 0; skipped = []
    for vid, name in rows:
        entry = CHEVROLET_MAP.get(base_id(vid))
        if entry is None:
            skipped.append(vid); continue
        gen, neum, det = entry
        clear_and_insert(c, vid, gen(neum, det))
        n += 1
    conn.commit()
    print("Chevrolet actualizados:", n)
    if skipped:
        print("Sin mapa (no tocados):", sorted(set(base_id(s) for s in skipped)))
    tp = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()


if __name__ == "__main__":
    main()
