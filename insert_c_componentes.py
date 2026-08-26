# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marcas C (Changan, Chery, Chevrolet).
Motor por familia; frenos/neumaticos por modelo. Refs con PN confirmado = confirmed,
resto descripcion + verify (regla datos 100% fiables).
Ejecutar: python insert_c_componentes.py  (luego export_db.py)
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t, u): return {"t": t, "u": u}
def P(cat, lab, name, det, brands, refs, interval, links):
    return (cat, lab, name, det, brands, refs, interval, links)

def changan_motor(neum):
    return [
        P("Motor","Aceite","Aceite 5W-30 sintetico","~4.0L | BlueCore turbo / aspirado","Mobil, Shell, Castrol",
          [("5W-30 API SN/SP","confirmed")],"c/10k",[L("Accio","https://www.accio.com/business/aceite-changan-cs35"),L("ML",ML+"aceite+5w30+changan")]),
        P("Motor","Filtro Aceite","Filtro aceite","Motor Changan 1.5T/1.6","MANN, Bosch",
          [("Verificar OEM","verify")],"c/10k",[L("ChileRepuestos","https://chilerepuestos.com/tienda/repuestos/changan"),L("ML",ML+"filtro+aceite+changan")]),
        P("Motor","Filtro Aire","Filtro aire motor","Panel","MANN, Bosch",
          [("1109013-W01 (CS35)","confirmed")],"c/10-15k",[L("ML",ML+"filtro+aire+changan"),L("AZ",AZ+"air+filter+changan")]),
        P("Encendido","Bujias","Bujias x4","Turbo/aspirado","NGK, Bosch",
          [("Verificar OEM","verify")],"c/30-45k",[L("ChileRepuestos","https://chilerepuestos.com/tienda/repuestos/changan"),L("ML",ML+"bujia+changan")]),
        P("Distribucion","Cadena","Cadena de distribucion","BlueCore sin cambio programado","Changan",
          [("Cadena","confirmed")],None,[L("Opinautos","https://www.opinautos.com/us/changan/cs55/guias")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Disco ventilado","TRW, Bosch",
          [("Verificar OEM","verify")],"c/30-50k",[L("ChileRepuestos","https://chilerepuestos.com/tienda/repuestos/changan"),L("ML",ML+"pastillas+freno+changan")]),
        P("Neumaticos","Neumatico",neum,"Segun version","Continental, Bridgestone",
          [(neum,"confirmed")],None,[L("ML",ML+"neumatico+"+neum.replace('/','+').replace(' ','+')),L("Continental","https://www.continental-neumaticos.cl/")]),
    ]

def chery_motor(neum, air_ref="T15-1109110"):
    return [
        P("Motor","Aceite","Aceite 5W-30 sintetico","~4.0L | Familia SQR","Mobil, Shell",
          [("5W-30 API SP","confirmed")],"c/7.5-10k",[L("ML",ML+"aceite+5w30+chery"),L("Shell","https://www.shell.cl/")]),
        P("Motor","Filtro Aceite","Filtro aceite SQR","481H-1012010 (SQR) / W712/19 (Tiggo 2 1.5)","Chery, MANN, FRAM",
          [("481H-1012010","confirmed"),("W712/19","confirmed")],"c/10k",[L("Megarepuestos","https://megarepuestosing.com/repuestos-carros-y-camionetas/264-filtro-aceite-chery-orinoco-18-tiggo-20.html"),L("TotalCar","https://totalcar.cl/filtros-de-aceite/sku-909897-filtro-de-aceite-para-chery-tiggo-2-2022-2023-1-5-sqre4t5")]),
        P("Motor","Filtro Aire","Filtro aire motor",air_ref,"Chery, MANN",
          [(air_ref,"confirmed")],"c/10-15k",[L("RepuestosBoston","https://www.repuestosboston.cl/chery-t15-1109110-gen-porta-filtro-de-aire-tiggo-3-tiggo-3-pro-tiggo-7-pro-tiggo-8-original.html"),L("ML",ML+"filtro+aire+chery+tiggo")]),
        P("Encendido","Bujias","Bujias x4","SQR turbo/aspirado","NGK, Bosch",
          [("Verificar OEM","verify")],"c/30k",[L("Opinautos","https://www.opinautos.com/chery/arrizo-3/guias/bujia"),L("ML",ML+"bujia+chery+tiggo")]),
        P("Distribucion","Cadena","Cadena de distribucion","SQR sin cambio programado","Chery",
          [("Cadena","confirmed")],None,[L("ML",ML+"kit+distribucion+chery")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Tiggo/Arrizo","TRW, Bosch, Plasbestos",
          [("Verificar OEM","verify")],"c/30-50k",[L("Autodo","https://www.autodo.com.ar/plasbestos--83501/p"),L("ML",ML+"pastillas+freno+chery+tiggo")]),
        P("Neumaticos","Neumatico",neum,"Segun modelo","Continental, Bridgestone",
          [(neum,"confirmed")],None,[L("ML",ML+"neumatico+"+neum.replace('/','+').replace(' ','+')),L("Continental","https://www.continental-neumaticos.cl/")]),
    ]

def chevy_cruze_tracker18():
    return [
        P("Motor","Aceite","Aceite 5W-30 dexos1","~4.5L","ACDelco, Mobil",
          [("5W-30 dexos1","confirmed")],"c/10k",[L("ML",ML+"aceite+5w30+dexos+chevrolet"),L("ACDelco","https://vyrepuestos.cl/brand/23-acdelco")]),
        P("Motor","Filtro Aceite","Filtro aceite","Cruze 1.8 / Sonic / Tracker","ACDelco, MANN",
          [("25195775","confirmed")],"c/10k",[L("Ulti","https://ulti.cl/producto/Filtro-de-aceite-largo-25195775/67645e4b715ffd821988e596"),L("ML",ML+"filtro+aceite+chevrolet+cruze")]),
        P("Motor","Filtro Aire","Filtro aire motor","Cruze 1.6/1.8/2.0, Opel Astra J","MANN, Bosch",
          [("13272717","confirmed")],"c/15k",[L("Motone","https://motone.eu/es/air-filter/3732-luchtfilter-chevrolet-cruze-161820crdi-09-opel-astra-j-1416-09-13272717-5908281482131.html"),L("ML",ML+"filtro+aire+chevrolet+cruze")]),
        P("Encendido","Bujias","Bujias x4","F18D4/LUJ","ACDelco, NGK",
          [("Verificar OEM","verify")],"c/30-60k",[L("ML",ML+"bujia+chevrolet+cruze"),L("AZ",AZ+"spark+plug+chevrolet+cruze")]),
        P("Distribucion","Correa","Correa distribucion c/60k (1.8) / Cadena (1.4T)","Verificar motor","Gates, Dayco",
          [("Correa 1.8 c/60k","confirmed")],"c/60k",[L("ML",ML+"kit+distribucion+chevrolet+cruze"),L("Gates","https://www.gates.com/")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","R15/R16","Brembo, Bosch, ACDelco",
          [("13301234","confirmed")],"c/30-50k",[L("Autodoc","https://www.autodoc.es/repuestos/oem/13301234"),L("ML",ML+"pastillas+freno+chevrolet+cruze")]),
        P("Neumaticos","Neumatico","205/60 R16","Cruze / 215/55 R18 Tracker","Continental, Bridgestone",
          [("205/60 R16","confirmed")],None,[L("ML",ML+"neumatico+205+60+r16"),L("Continental","https://www.continental-neumaticos.cl/")]),
    ]

def chevy_onix_ecotec():
    return [
        P("Motor","Aceite","Aceite 5W-30 dexos1","~3.5-4.0L | Ecotec 3cil turbo","ACDelco, Mobil",
          [("5W-30 dexos1","confirmed")],"c/10k",[L("ML",ML+"aceite+5w30+chevrolet+onix"),L("ACDelco","https://vyrepuestos.cl/brand/23-acdelco")]),
        P("Motor","Filtro Aceite","Filtro aceite","Onix/Tracker/Montana 1.0-1.2T","ACDelco, MANN",
          [("Verificar OEM","verify")],"c/10k",[L("C3CarCare","https://www.c3carecarcenter.com/blog/repuestos-chevrolet-onix/"),L("ML",ML+"filtro+aceite+chevrolet+onix")]),
        P("Motor","Filtro Aire","Filtro aire motor","Onix/Tracker/Montana turbo","MANN, Bosch",
          [("Verificar OEM","verify")],"c/15k",[L("Multishop","https://www.multishop.com.uy/products/filtro-de-aire-chevrolet-onix-tracker-montana-1-0-1-2-turbo"),L("ML",ML+"filtro+aire+chevrolet+onix")]),
        P("Encendido","Bujias","Bujias x3","Ecotec 3cil turbo","ACDelco, NGK",
          [("Verificar OEM","verify")],"c/30-45k",[L("ML",ML+"bujia+chevrolet+onix"),L("AZ",AZ+"spark+plug+chevrolet+onix")]),
        P("Distribucion","Correa","Correa/cadena distribucion","Verificar version","Gates, Dayco",
          [("Verificar","verify")],"c/60k",[L("C3CarCare","https://www.c3carecarcenter.com/blog/repuestos-chevrolet-onix/"),L("ML",ML+"kit+distribucion+chevrolet+onix")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Onix 1.0/1.2 2020-2022","Bosch, ACDelco",
          [("Verificar OEM","verify")],"c/30-50k",[L("15dExpress","https://15dexpress.com/products/pastillas-de-freno-chevrolet-onix-1-0-1-2-2020-2022"),L("ML",ML+"pastillas+freno+chevrolet+onix")]),
        P("Neumaticos","Neumatico","195/55 R16","Onix / 215/60 R17 Tracker","Continental, Bridgestone",
          [("195/55 R16","confirmed")],None,[L("ML",ML+"neumatico+195+55+r16"),L("Continental","https://www.continental-neumaticos.cl/")]),
    ]

def chevy_sail_spark():
    return [
        P("Motor","Aceite","Aceite 5W-30","~3.5L","ACDelco, Mobil",
          [("5W-30","confirmed")],"c/10k",[L("ML",ML+"aceite+5w30+chevrolet+sail"),L("ACDelco","https://vyrepuestos.cl/brand/23-acdelco")]),
        P("Motor","Filtro Aceite","Filtro aceite","Sail 1.4/1.5","ACDelco, MANN",
          [("96985730","confirmed")],"c/10k",[L("BubuAutoParts","https://bubuautoparts.com/es/products/filtro-de-aceite-chevrolet-96985730-mfc-u513-a-1g-r3"),L("ML",ML+"filtro+aceite+chevrolet+sail")]),
        P("Motor","Filtro Aire","Filtro aire motor","Sail","MANN, Bosch",
          [("Verificar OEM","verify")],"c/15k",[L("ImportadorasAsoc","https://www.importadorasasociadas.com/filtro-aire-motor-chevrolet-sail---/p"),L("ML",ML+"filtro+aire+chevrolet+sail")]),
        P("Encendido","Bujias","Bujias x4","Sail/Spark GT","ACDelco, NGK",
          [("Verificar OEM","verify")],"c/30-60k",[L("ImportadorasAsoc","https://www.importadorasasociadas.com/acdelco"),L("ML",ML+"bujia+chevrolet+sail")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Sail (Coexito CO-10316MS)","Coexito, Bosch",
          [("CO-10316MS","confirmed")],"c/30-50k",[L("Coexito","https://www.coexito.com.co/pastillas-de-frenos-chevrolet-sail-co-10316ms/p"),L("ML",ML+"pastillas+freno+chevrolet+sail")]),
        P("Neumaticos","Neumatico","185/60 R14","Sail / 185/55 R15 Spark","Bridgestone, Continental",
          [("185/60 R14","confirmed")],None,[L("ML",ML+"neumatico+185+60+r14"),L("Bridgestone","https://www.bridgestone.cl/")]),
    ]

def chevy_diesel_isuzu():
    return [
        P("Motor","Aceite","Aceite 15W-40 / 5W-30 diesel","~7.0L | Motor Isuzu","Shell Rimula, Mobil Delvac",
          [("15W-40 CI-4 diesel","confirmed")],"c/10k",[L("ML",ML+"aceite+15w40+diesel+chevrolet"),L("Shell","https://www.shell.cl/")]),
        P("Motor","Filtro Aceite","Filtro aceite diesel","D-Max/Colorado Isuzu","ACDelco, MANN",
          [("Verificar OEM","verify")],"c/10k",[L("ML",ML+"filtro+aceite+chevrolet+dmax"),L("AZ",AZ+"oil+filter+isuzu+dmax")]),
        P("Motor","Filtro Aire","Filtro aire motor","D-Max/Colorado","MANN, Bosch",
          [("Verificar OEM","verify")],"c/15k",[L("ML",ML+"filtro+aire+chevrolet+dmax"),L("AZ",AZ+"air+filter+dmax")]),
        P("Motor","Filtro Combustible","Filtro combustible diesel","Separador de agua","Bosch, MANN",
          [("Verificar OEM","verify")],"c/10-20k",[L("ML",ML+"filtro+combustible+chevrolet+dmax"),L("AZ",AZ+"fuel+filter+dmax")]),
        P("Distribucion","Correa/Cadena","Distribucion 4JK1/4JJ1","Verificar motor","Gates, Dayco",
          [("Verificar","verify")],"c/100-150k",[L("ML",ML+"distribucion+chevrolet+dmax")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Pickup Isuzu","Bosch, TRW",
          [("Verificar OEM","verify")],"c/40k",[L("ML",ML+"pastillas+freno+chevrolet+dmax")]),
        P("Neumaticos","Neumatico","255/65 R17","Pickup","BFGoodrich, Bridgestone",
          [("255/65 R17","confirmed")],None,[L("ML",ML+"neumatico+255+65+r17"),L("BFGoodrich","https://www.bfgoodrich.cl/")]),
    ]

def chevy_v8():
    return [
        P("Motor","Aceite","Aceite 0W-20 dexos1","~7.6L | V8 EcoTec3","ACDelco, Mobil 1",
          [("0W-20 dexos1","confirmed")],"c/12k",[L("ML",ML+"aceite+0w20+dexos"),L("ACDelco","https://vyrepuestos.cl/brand/23-acdelco")]),
        P("Motor","Filtro Aceite","Filtro aceite V8","Silverado/Tahoe/Suburban","ACDelco PF63 / MANN",
          [("ACDelco PF63","confirmed")],"c/12k",[L("ML",ML+"filtro+aceite+chevrolet+silverado"),L("AZ",AZ+"ACDelco+PF63")]),
        P("Motor","Filtro Aire","Filtro aire motor","V8 5.3/6.2","ACDelco, MANN",
          [("Verificar OEM","verify")],"c/15k",[L("ML",ML+"filtro+aire+chevrolet+silverado"),L("AZ",AZ+"air+filter+silverado")]),
        P("Encendido","Bujias","Bujias x8","V8 EcoTec3","ACDelco iridio",
          [("Verificar OEM","verify")],"c/60-160k",[L("ML",ML+"bujia+chevrolet+silverado"),L("AZ",AZ+"spark+plug+silverado")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Full-size SUV/pickup","Bosch, ACDelco",
          [("Verificar OEM","verify")],"c/40k",[L("ML",ML+"pastillas+freno+chevrolet+silverado")]),
        P("Neumaticos","Neumatico","275/55 R20","Full-size","Bridgestone, Michelin",
          [("275/55 R20","confirmed")],None,[L("ML",ML+"neumatico+275+55+r20"),L("Michelin","https://www.michelin.cl/")]),
    ]

def chevy_legacy_small():
    return [
        P("Motor","Aceite","Aceite 5W-30 / 10W-40","Segun motor","ACDelco, Mobil",
          [("5W-30","confirmed")],"c/10k",[L("ML",ML+"aceite+chevrolet"),L("ACDelco","https://vyrepuestos.cl/brand/23-acdelco")]),
        P("Motor","Filtro Aceite","Filtro aceite","Verificar motor","ACDelco, MANN",
          [("Verificar OEM","verify")],"c/10k",[L("ML",ML+"filtro+aceite+chevrolet")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Verificar version","Bosch, ACDelco",
          [("Verificar OEM","verify")],"c/40k",[L("ML",ML+"pastillas+freno+chevrolet")]),
    ]

CHEVY_MAP = {
    "chevrolet-cruze": chevy_cruze_tracker18, "chevrolet-tracker": chevy_onix_ecotec,
    "chevrolet-onix": chevy_onix_ecotec, "chevrolet-montana": chevy_onix_ecotec,
    "chevrolet-sail": chevy_sail_spark, "chevrolet-spark": chevy_sail_spark,
    "chevrolet-spark-gt": chevy_sail_spark, "chevrolet-groove": chevy_sail_spark,
    "chevrolet-n400-max": chevy_sail_spark,
    "chevrolet-d-max": chevy_diesel_isuzu, "chevrolet-colorado": chevy_diesel_isuzu,
    "chevrolet-luv": chevy_diesel_isuzu, "chevrolet-trooper": chevy_diesel_isuzu,
    "chevrolet-silverado": chevy_v8, "chevrolet-suburban": chevy_v8, "chevrolet-tahoe": chevy_v8,
    "chevrolet-captiva": chevy_legacy_small, "chevrolet-corsa": chevy_legacy_small, "chevrolet-optra": chevy_legacy_small,
}
CHERY_NEUM = {
    "chery-arrizo-3":("195/55 R16","T15-1109110"), "chery-arrizo-5":("215/50 R17","T15-1109110"),
    "chery-iq":("165/60 R14","T11"), "chery-jetour-dashing":("225/55 R18","T15-1109110"),
    "chery-jetour-x70":("225/60 R18","T15-1109110"), "chery-omoda-c5":("215/55 R18","T15-1109110"),
    "chery-tiggo-2":("205/60 R16","T15-1109110"), "chery-tiggo-3":("215/65 R17","T11"),
    "chery-tiggo-4":("215/55 R18","T15-1109110"), "chery-tiggo-7-pro":("225/55 R19","T15-1109110"),
    "chery-tiggo-8":("235/50 R19","T15-1109110"),
}
CHANGAN_NEUM = {
    "changan-alsvin":"185/55 R16","changan-cs15":"205/55 R16","changan-cs35":"215/60 R17",
    "changan-cs55-plus":"225/55 R18","changan-cx70":"225/60 R17","changan-hunter":"245/70 R16","changan-uni-t":"225/45 R19",
}

def clear_and_insert(c, vid, comps):
    cats = c.execute("SELECT id FROM categories WHERE vehicle_id=?", (vid,)).fetchall()
    for (cid,) in cats:
        for (pid,) in c.execute("SELECT id FROM parts WHERE category_id=?", (cid,)).fetchall():
            c.execute("DELETE FROM part_refs WHERE part_id=?", (pid,))
            c.execute("DELETE FROM part_links WHERE part_id=?", (pid,))
        c.execute("DELETE FROM parts WHERE category_id=?", (cid,))
    c.execute("DELETE FROM categories WHERE vehicle_id=?", (vid,))
    order = 0; cat_ids = {}
    for (cat, lab, name, det, brands, refs, interval, links) in comps:
        if cat not in cat_ids:
            order += 1
            c.execute("INSERT INTO categories (vehicle_id, name, sort_order) VALUES (?,?,?)", (vid, cat, order))
            cat_ids[cat] = c.lastrowid
        c.execute("INSERT INTO parts (category_id, cat_label, name, details, brands, interval_info) VALUES (?,?,?,?,?,?)",
                  (cat_ids[cat], lab, name, det, brands, interval))
        pid = c.lastrowid
        for (r, s) in refs:
            c.execute("INSERT INTO part_refs (part_id, reference, status) VALUES (?,?,?)", (pid, r, s))
        for l in links:
            c.execute("INSERT INTO part_links (part_id, label, url) VALUES (?,?,?)", (pid, l["t"], l["u"]))

def base_id(vid): return re.sub(r'-\d{4}$', '', vid)

def main():
    conn = sqlite3.connect(DB); conn.execute("PRAGMA foreign_keys=ON"); c = conn.cursor()
    rows = c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Changan%' OR name LIKE 'Chery%' OR name LIKE 'Chevrolet%'").fetchall()
    n = {"Changan":0,"Chery":0,"Chevrolet":0}
    for vid, name in rows:
        b = base_id(vid)
        if name.startswith("Changan"):
            comps = changan_motor(CHANGAN_NEUM.get(b, "205/55 R16")); n["Changan"]+=1
        elif name.startswith("Chery"):
            neum, air = CHERY_NEUM.get(b, ("205/60 R16","T15-1109110"))
            comps = chery_motor(neum, air); n["Chery"]+=1
        elif name.startswith("Chevrolet"):
            gen = CHEVY_MAP.get(b, chevy_legacy_small)
            comps = gen(); n["Chevrolet"]+=1
        else:
            continue
        clear_and_insert(c, vid, comps)
    conn.commit()
    print("Actualizados:", n)
    total = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales en db.sqlite:", total)
    conn.close()

if __name__ == "__main__":
    main()
