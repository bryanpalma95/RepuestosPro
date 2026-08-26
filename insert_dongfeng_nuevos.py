# -*- coding: utf-8 -*-
"""RepuestosPro - Agregar modelos Dongfeng/DFM vendidos en Chile (CIDEF) que faltaban.
Agrega vehiculos nuevos (INSERT OR IGNORE) con componentes por familia de motor.
Familia 1.5T Dongfeng comparte comps de motor con SX5/Forthing.
Rich 6 = motor Nissan ZD25 diesel (plataforma D22). MAGE/EV = electrificados.
Ejecutar: python insert_dongfeng_nuevos.py  (luego export_db.py + regen nav)
Fuentes: cidef.cl, autocosmos.cl, wikipedia (Aeolus, Dongfeng Rich)
"""
import sqlite3, os
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="
CIDEF = "https://cidef.cl/marca/dongfeng/"

def L(t,u): return {"t":t,"u":u}
def P(cat,lab,name,det,brands,refs,interval,links): return (cat,lab,name,det,brands,refs,interval,links)

def motor_15t(neum):
    return [
        P("Motor","Aceite","Aceite 5W-30 sintetico","~4.0-4.5L | 1.5T turbo","Mobil, Shell, Castrol",
          [("5W-30 API SP","confirmed")],"c/10k",[L("CIDEF",CIDEF),L("ML",ML+"aceite+5w30+dongfeng")]),
        P("Motor","Filtro Aceite","Filtro aceite 1.5T","Spin-on, verificar rosca","MANN, Bosch",
          [("Verificar OEM","verify")],"c/10k",[L("CIDEF",CIDEF),L("ML",ML+"filtro+aceite+dongfeng")]),
        P("Motor","Filtro Aire","Filtro aire motor","Panel","MANN, Bosch",
          [("Verificar OEM","verify")],"c/10-15k",[L("CIDEF",CIDEF),L("ML",ML+"filtro+aire+dongfeng")]),
        P("Encendido","Bujias","Bujias x4","1.5T iridio","NGK, Bosch",
          [("Verificar OEM","verify")],"c/30-45k",[L("CIDEF",CIDEF),L("ML",ML+"bujia+dongfeng")]),
        P("Distribucion","Cadena","Cadena de distribucion","1.5T sin cambio programado","Dongfeng",
          [("Cadena","confirmed")],None,[L("CIDEF",CIDEF)]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Disco ventilado","TRW, Bosch",
          [("Verificar OEM","verify")],"c/30-50k",[L("CIDEF",CIDEF),L("ML",ML+"pastillas+freno+dongfeng")]),
        P("Frenos","Liquido Frenos","Liquido de frenos DOT 4","Sistema hidraulico","Bosch, ATE",
          [("DOT 4","confirmed")],"c/2 anios",[L("ML",ML+"liquido+freno+dot4")]),
        P("Neumaticos","Neumatico",neum,"Segun version","Continental, Bridgestone",
          [(neum,"confirmed")],None,[L("ML",ML+"neumatico+"+neum.replace('/','+').replace(' ','+')),L("Continental","https://www.continental-neumaticos.cl/")]),
    ]

def motor_rich6():
    return [
        P("Motor","Aceite","Aceite 15W-40 / 5W-30 diesel","~6.0L | ZD25 diesel (base Nissan)","Shell Rimula, Mobil",
          [("15W-40 CI-4","confirmed")],"c/10k",[L("CIDEF",CIDEF),L("ML",ML+"aceite+15w40+diesel")]),
        P("Motor","Filtro Aceite","Filtro aceite ZD25","Motor Nissan ZD25 diesel","MANN, Bosch",
          [("15208-Serie Nissan (verificar)","verify")],"c/10k",[L("ML",ML+"filtro+aceite+dongfeng+rich"),L("AZ",AZ+"oil+filter+ZD25")]),
        P("Motor","Filtro Aire","Filtro aire motor","Pickup","MANN, Bosch",
          [("Verificar OEM","verify")],"c/15k",[L("ML",ML+"filtro+aire+dongfeng+rich"),L("AZ",AZ+"air+filter+dongfeng+rich")]),
        P("Motor","Filtro Combustible","Filtro combustible diesel","Separador de agua","Bosch, MANN",
          [("Verificar OEM","verify")],"c/10-20k",[L("ML",ML+"filtro+combustible+diesel")]),
        P("Distribucion","Cadena","Cadena distribucion ZD25","Motor diesel","Dongfeng/Nissan",
          [("Cadena (ZD25)","confirmed")],None,[L("ML",ML+"distribucion+zd25")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Pickup","Bosch, TRW",
          [("Verificar OEM","verify")],"c/40k",[L("ML",ML+"pastillas+freno+dongfeng+rich")]),
        P("Neumaticos","Neumatico","245/70 R16","Pickup","BFGoodrich, Bridgestone",
          [("245/70 R16","confirmed")],None,[L("ML",ML+"neumatico+245+70+r16"),L("BFGoodrich","https://www.bfgoodrich.cl/")]),
    ]

def motor_mage_phev():
    return [
        P("Motor","Aceite","Aceite 0W-20 hibrido","Motor 1.5T + electrico","Mobil, Castrol",
          [("0W-20","confirmed")],"c/10k",[L("CIDEF","https://cidef.cl/modelo/mage/"),L("ML",ML+"aceite+0w20+hibrido")]),
        P("Motor","Filtro Aceite","Filtro aceite","Motor combustion del hibrido","MANN, Bosch",
          [("Verificar OEM","verify")],"c/10k",[L("CIDEF","https://cidef.cl/modelo/mage/"),L("ML",ML+"filtro+aceite+dongfeng+mage")]),
        P("Motor","Filtro Aire","Filtro aire motor","Panel","MANN, Bosch",
          [("Verificar OEM","verify")],"c/15k",[L("ML",ML+"filtro+aire+dongfeng+mage")]),
        P("Bateria","Bateria HV","Bateria alta tension (traccion)","Sistema PHEV","Dongfeng",
          [("Bateria HV PHEV","confirmed")],None,[L("CIDEF","https://cidef.cl/modelo/mage/")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Freno regenerativo + disco","TRW, Bosch",
          [("Verificar OEM","verify")],"c/40-60k",[L("ML",ML+"pastillas+freno+dongfeng+mage")]),
        P("Neumaticos","Neumatico","225/55 R19","SUV mediano","Continental, Michelin",
          [("225/55 R19","confirmed")],None,[L("ML",ML+"neumatico+225+55+r19"),L("Michelin","https://www.michelin.cl/")]),
    ]

def motor_mage_ev():
    return [
        P("Motor","Refrigerante","Refrigerante bateria EV","Circuito termico bateria","Dongfeng",
          [("Coolant EV (verificar)","verify")],None,[L("Racing5","https://www.racing5.cl/cidef-chile-presento-el-nuevo-dongfeng-mage-ev-movilidad-100-electrica-en-formato-suv/")]),
        P("Bateria","Bateria HV","Bateria traccion (160hp/120kW, 240Nm)","Motor sincrono imanes permanentes","Dongfeng",
          [("Bateria HV EV","confirmed")],None,[L("Racing5","https://www.racing5.cl/cidef-chile-presento-el-nuevo-dongfeng-mage-ev-movilidad-100-electrica-en-formato-suv/")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Freno regenerativo + disco","TRW, Bosch",
          [("Verificar OEM","verify")],"c/50-70k",[L("ML",ML+"pastillas+freno+dongfeng+mage")]),
        P("Neumaticos","Neumatico","235/50 R19","SUV EV","Michelin, Continental",
          [("235/50 R19","confirmed")],None,[L("ML",ML+"neumatico+235+50+r19"),L("Michelin","https://www.michelin.cl/")]),
    ]

NUEVOS = [
    ("dongfeng-t5-evo","Dongfeng T5 Evo","1.5T/1.6T Forthing Dynamics | Cadena","Plataforma Forthing = T5L/SX5",range(2022,2027),motor_15t,"225/55 R18"),
    ("dongfeng-sx6","Dongfeng SX6","1.5T 7 plazas | Cadena","SUV mediano 7 pasajeros",range(2021,2027),motor_15t,"215/60 R17"),
    ("dongfeng-aeolus-gs-cross","Dongfeng Aeolus GS Cross","1.0T 3cil / 1.5T 4cil | Cadena","Aeolus (Fengshen Yixuan GS)",range(2023,2027),motor_15t,"215/55 R18"),
    ("dongfeng-aeolus-y3","Dongfeng Aeolus Y3","1.5L/1.5T | Cadena","Aeolus (Fengshen)",range(2023,2027),motor_15t,"205/55 R16"),
    ("dongfeng-mage","Dongfeng Mage","1.5T PHEV hibrido enchufable","Aeolus Mage PHEV",range(2024,2027),motor_mage_phev,None),
    ("dongfeng-mage-ev","Dongfeng Mage EV","Electrico 120kW/240Nm","Aeolus Mage 100% EV",range(2024,2027),motor_mage_ev,None),
    ("dongfeng-huge","Dongfeng Huge","Aeolus SUV insignia | 2026","Cuarto Aeolus (Y3/GS Cross/Mage)",range(2026,2027),motor_15t,"235/55 R19"),
    ("dongfeng-rich-6","Dongfeng Rich 6","2.5D ZD25 | Pickup (plataforma Nissan D22)","Base Nissan Navara D22",range(2021,2027),motor_rich6,None),
]

def insert_vehicle(c, vid, name, info, cross, comps):
    c.execute("INSERT OR IGNORE INTO vehicles VALUES (?,?,?,?)", (vid, name, info, cross))
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

def main():
    conn=sqlite3.connect(DB); conn.execute("PRAGMA foreign_keys=ON"); c=conn.cursor()
    n_veh=0
    for base,name,info,cross,years,gen,arg in NUEVOS:
        comps = gen(arg) if arg is not None else gen()
        for y in years:
            vid=f"{base}-{y}"
            fullname=f"{name} — {y}"
            insert_vehicle(c, vid, fullname, info, cross, comps)
            n_veh+=1
    conn.commit()
    total_v=c.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
    total_p=c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print(f"Registros Dongfeng agregados/actualizados: {n_veh}")
    print(f"Vehiculos totales: {total_v} | Componentes totales: {total_p}")
    conn.close()

if __name__=="__main__":
    main()
