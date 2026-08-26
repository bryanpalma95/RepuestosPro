# -*- coding: utf-8 -*-
"""RepuestosPro - Cierre marca D: DFSK Glory 580 + Daewoo Racer/Heaven.
Ademas elimina 3 registros basura (notas de trabajo mal insertadas como vehiculos
con años falsos: Chrysler_Mopar-1000, Dodge_Mopar-1500, Ram_Mopar-2500).
La info util (HEMI/Pentastar/Cummins) ya esta en los Ram 1500/2500 reales.
Ejecutar: python insert_d_componentes.py  (luego export_db.py + regen nav)
"""
import sqlite3, os
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t,u): return {"t":t,"u":u}
def P(cat,lab,name,det,brands,refs,interval,links): return (cat,lab,name,det,brands,refs,interval,links)

def comps_dfsk_glory580():
    return [
        P("Motor","Aceite","Aceite 5W-30 sintetico","~4.0L | 1.5T SFG15T (137-148 HP)","Mobil, Shell",
          [("5W-30 API SP","confirmed")],"c/10k",[L("Scegliauto","https://www.scegliauto.com/es/cerca/cambio-de-aceite-glory-580/"),L("ML",ML+"aceite+5w30+dfsk+glory")]),
        P("Motor","Filtro Aceite","Filtro aceite 1.5T","Spin-on","MANN, Bosch",
          [("Verificar OEM","verify")],"c/10k",[L("Opinautos","https://www.opinautos.com/dfsk/580/guias"),L("ML",ML+"filtro+aceite+dfsk+glory+580")]),
        P("Motor","Filtro Aire","Filtro aire motor","Panel","MANN, Bosch",
          [("Verificar OEM","verify")],"c/10-15k",[L("ML",ML+"filtro+aire+dfsk+glory+580")]),
        P("Encendido","Bujias","Bujias x4","1.5T turbo","NGK, Bosch",
          [("Verificar OEM","verify")],"c/30-45k",[L("ML",ML+"bujia+dfsk+glory+580")]),
        P("Distribucion","Cadena","Cadena de distribucion","1.5T sin cambio programado","DFSK",
          [("Cadena","confirmed")],None,[L("Wikipedia","https://en.wikipedia.org/wiki/Fengon_580")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","SUV 7 plazas","TRW, Bosch",
          [("Verificar OEM","verify")],"c/30-50k",[L("ML",ML+"pastillas+freno+dfsk+glory+580")]),
        P("Neumaticos","Neumatico","215/60 R17","SUV 7 plazas","Continental, Bridgestone",
          [("215/60 R17","confirmed")],None,[L("ML",ML+"neumatico+215+60+r17"),L("Continental","https://www.continental-neumaticos.cl/")]),
    ]

def comps_daewoo():
    return [
        P("Motor","Aceite","Aceite 10W-40 / 5W-30","~3.5L | Motor GM/Opel Family 1.5-1.6","Mobil, Shell",
          [("10W-40","confirmed")],"c/8-10k",[L("Opinautos","https://static.opinautos.com/daewoo/heaven/guias/lubricacion"),L("ML",ML+"aceite+10w40+daewoo")]),
        P("Motor","Filtro Aceite","Filtro aceite","Motor Family GM","MANN, Bosch",
          [("Verificar OEM","verify")],"c/8-10k",[L("Autodoc","https://www.autodoc.es/repuestos/motor/daewoo/racer"),L("ML",ML+"filtro+aceite+daewoo")]),
        P("Encendido","Bujias","Bujias x4","Motor Family 1.5-1.6","NGK",
          [("NGK BPR6ES","confirmed")],"c/20-30k",[L("TotalCar","https://totalcar.cl/repuestos/daewoo"),L("ML",ML+"bujia+ngk+bpr6es")]),
        P("Distribucion","Correa","Correa de distribucion","Motor Family c/60k","Gates, Dayco",
          [("Correa c/60k","confirmed")],"c/60k",[L("ML",ML+"correa+distribucion+daewoo"),L("Gates","https://www.gates.com/")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Compacto","Bosch, TRW",
          [("Verificar OEM","verify")],"c/40k",[L("Mundorepuestos","https://mundorepuestos.com/marca/daewoo/racer"),L("ML",ML+"pastillas+freno+daewoo")]),
        P("Neumaticos","Neumatico","175/70 R13","Compacto clasico","Bridgestone",
          [("175/70 R13","confirmed")],None,[L("ML",ML+"neumatico+175+70+r13"),L("Bridgestone","https://www.bridgestone.cl/")]),
    ]

BASURA = [
    "chrysler-mopar-nota-reutilizar-en-dodge-durango-journey-jeep-grand-cherokee-wrangler-gladiator-compass-ram-1000",
    "dodge-mopar-nota-reutilizar-en-ram-1500",
    "ram-mopar-ram-2500",
]

def clear_and_insert(c, vid, comps):
    cats=c.execute("SELECT id FROM categories WHERE vehicle_id=?", (vid,)).fetchall()
    for (cid,) in cats:
        for (pid,) in c.execute("SELECT id FROM parts WHERE category_id=?", (cid,)).fetchall():
            c.execute("DELETE FROM part_refs WHERE part_id=?", (pid,)); c.execute("DELETE FROM part_links WHERE part_id=?", (pid,))
        c.execute("DELETE FROM parts WHERE category_id=?", (cid,))
    c.execute("DELETE FROM categories WHERE vehicle_id=?", (vid,))
    order=0; cat_ids={}
    for (cat,lab,nm,det,brands,refs,interval,links) in comps:
        if cat not in cat_ids:
            order+=1
            c.execute("INSERT INTO categories (vehicle_id,name,sort_order) VALUES (?,?,?)", (vid,cat,order)); cat_ids[cat]=c.lastrowid
        c.execute("INSERT INTO parts (category_id,cat_label,name,details,brands,interval_info) VALUES (?,?,?,?,?,?)",
                  (cat_ids[cat],lab,nm,det,brands,interval)); pid=c.lastrowid
        for (r,s) in refs: c.execute("INSERT INTO part_refs (part_id,reference,status) VALUES (?,?,?)", (pid,r,s))
        for l in links: c.execute("INSERT INTO part_links (part_id,label,url) VALUES (?,?,?)", (pid,l["t"],l["u"]))

def delete_vehicle(c, vid):
    cats=c.execute("SELECT id FROM categories WHERE vehicle_id=?", (vid,)).fetchall()
    for (cid,) in cats:
        for (pid,) in c.execute("SELECT id FROM parts WHERE category_id=?", (cid,)).fetchall():
            c.execute("DELETE FROM part_refs WHERE part_id=?", (pid,)); c.execute("DELETE FROM part_links WHERE part_id=?", (pid,))
        c.execute("DELETE FROM parts WHERE category_id=?", (cid,))
    c.execute("DELETE FROM categories WHERE vehicle_id=?", (vid,))
    c.execute("DELETE FROM vehicles WHERE id=?", (vid,))

def main():
    conn=sqlite3.connect(DB); conn.execute("PRAGMA foreign_keys=ON"); c=conn.cursor()
    borrados=0
    for vid in BASURA:
        if c.execute("SELECT 1 FROM vehicles WHERE id=?", (vid,)).fetchone():
            delete_vehicle(c, vid); borrados+=1
    n=0
    for vid,name in c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'DFSK%' OR name LIKE 'Daewoo%'").fetchall():
        if name.startswith("DFSK"):
            clear_and_insert(c, vid, comps_dfsk_glory580())
        else:
            clear_and_insert(c, vid, comps_daewoo())
        n+=1
    conn.commit()
    print(f"Registros basura eliminados: {borrados} | DFSK/Daewoo actualizados: {n}")
    tv=c.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
    tp=c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print(f"Vehiculos totales: {tv} | Componentes: {tp}")
    conn.close()

if __name__=="__main__":
    main()
