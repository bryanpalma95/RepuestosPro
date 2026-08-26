# -*- coding: utf-8 -*-
"""RepuestosPro - Componentes verificados marca F (Fiat, Ford).
Motor por familia; frenos/neumaticos por modelo. PN confirmado = confirmed, resto verify.
Ejecutar: python insert_f_componentes.py  (luego export_db.py + regen nav)
Fuentes: famford, lspalermo, autodoc, opinautos, walmart, c3carecarcenter
"""
import sqlite3, os, re
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"; AZ = "https://www.amazon.com/s?k="

def L(t,u): return {"t":t,"u":u}
def P(cat,lab,name,det,brands,refs,interval,links): return (cat,lab,name,det,brands,refs,interval,links)

def fiat_firefly(neum):
    return [
        P("Motor","Aceite","Aceite 0W-20 / 5W-30 sintetico","~3.2L | Firefly 1.0/1.3","Selenia, Mobil, Shell",
          [("0W-20 (Firefly)","confirmed"),("5W-30","confirmed")],"c/10k",[L("Kavak","https://www.kavak.com/ar/blog/fiat-cronos-drive-clasico-y-elegante"),L("ML",ML+"aceite+0w20+fiat+firefly")]),
        P("Motor","Filtro Aceite","Filtro aceite Firefly","Argo/Cronos/Pulse 1.3","Mahle, MANN",
          [("Verificar OEM","verify")],"c/10k",[L("Allende","https://www.allenderepuestos.com.ar/categoria-producto/fiat/cronos-1-3-firefly/"),L("ML",ML+"filtro+aceite+fiat+argo")]),
        P("Motor","Filtro Aire","Filtro aire Firefly","Argo/Cronos/Pulse/Strada/Uno 1.3","Wega, MANN",
          [("52046268","confirmed")],"c/10-15k",[L("LSPalermo","https://lspalermo.com.ar/productos/filtro-aire-fiat-argo-1-3-2017-2018-2019-2020-2021-2022-2023-jlc4t/"),L("ML",ML+"filtro+aire+fiat+argo")]),
        P("Encendido","Bujias","Bujias","Firefly turbo/aspirado","NGK, Bosch",
          [("Verificar OEM","verify")],"c/30k",[L("Opinautos","https://www.opinautos.com/do/fiat/argo/guias/filtros"),L("ML",ML+"bujia+fiat+argo")]),
        P("Distribucion","Cadena","Cadena/correa banada aceite","Firefly (verificar 1.0 vs 1.3)","Fiat",
          [("Verificar","verify")],"c/dependiendo",[L("ML",ML+"distribucion+fiat+firefly")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Disco ventilado","TRW, Bosch",
          [("Verificar OEM","verify")],"c/30-50k",[L("Autodoc","https://club.autodoc.es/manuals/fiat/argo"),L("ML",ML+"pastillas+freno+fiat+argo")]),
        P("Neumaticos","Neumatico",neum,"Segun modelo","Continental, Bridgestone",
          [(neum,"confirmed")],None,[L("ML",ML+"neumatico+"+neum.replace('/','+').replace(' ','+')),L("Continental","https://www.continental-neumaticos.cl/")]),
    ]

def fiat_fire(neum):
    return [
        P("Motor","Aceite","Aceite 15W-40 / 5W-30","~2.8-3.0L | Motor Fire 1.4","Selenia, Mobil",
          [("15W-40","confirmed")],"c/7.5-10k",[L("Opinautos","https://www.opinautos.com/es/fiat/fire/guias/cuanto-aceite-usar"),L("ML",ML+"aceite+fiat+fire")]),
        P("Motor","Filtro Aceite","Filtro aceite Fire 1.3/1.4","Palio/Siena/Strada/Uno Fire","Mopar, Mahle",
          [("Filtro Fire 1.3/1.4 (Mopar)","confirmed")],"c/7.5-10k",[L("ArgAutopartes","https://www.argautopartes.com.ar/productos/filtro-aceite-fiat-palio-siena-strada-uno-fire-1-3-1-4-mopar/"),L("ML",ML+"filtro+aceite+fiat+uno")]),
        P("Motor","Filtro Aire","Filtro aire motor","Panel","Wega, MANN",
          [("Verificar OEM","verify")],"c/10-15k",[L("ML",ML+"filtro+aire+fiat+uno")]),
        P("Encendido","Bujias","Bujias x4","Motor Fire 1.4","NGK, Bosch",
          [("Verificar OEM","verify")],"c/20-30k",[L("Opinautos","https://www.opinautos.com/cl/fiat/fire/defectos/consumo"),L("ML",ML+"bujia+fiat+uno")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Compacto","TRW, Bosch",
          [("Verificar OEM","verify")],"c/40k",[L("ML",ML+"pastillas+freno+fiat+uno")]),
        P("Neumaticos","Neumatico",neum,"Segun modelo","Bridgestone, Continental",
          [(neum,"confirmed")],None,[L("ML",ML+"neumatico+"+neum.replace('/','+').replace(' ','+')),L("Bridgestone","https://www.bridgestone.cl/")]),
    ]

def fiat_ducato():
    return [
        P("Motor","Aceite","Aceite 5W-30 diesel","~6.5L | 2.3D F1A MultiJet","Selenia, Shell Rimula",
          [("5W-30 diesel","confirmed")],"c/10-20k",[L("ML",ML+"aceite+5w30+fiat+ducato")]),
        P("Motor","Filtro Aceite","Filtro aceite MultiJet","2.3D F1A","MANN, Mahle",
          [("Verificar OEM","verify")],"c/10-20k",[L("ML",ML+"filtro+aceite+fiat+ducato")]),
        P("Motor","Filtro Combustible","Filtro combustible diesel","Separador agua","Bosch, MANN",
          [("Verificar OEM","verify")],"c/20-40k",[L("ML",ML+"filtro+combustible+fiat+ducato")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Furgon","TRW, Bosch",
          [("Verificar OEM","verify")],"c/40k",[L("ML",ML+"pastillas+freno+fiat+ducato")]),
        P("Neumaticos","Neumatico","215/70 R15C","Furgon comercial","Continental",
          [("215/70 R15C","confirmed")],None,[L("ML",ML+"neumatico+215+70+r15c")]),
    ]

def ford_sigma(neum):
    return [
        P("Motor","Aceite","Aceite 5W-30 Motorcraft","~4.0L | Sigma/Dragon/EcoBoost","Motorcraft, Shell",
          [("5W-30 (Ford WSS-M2C913)","confirmed")],"c/10k",[L("FamFord","http://www.famford.com.ar/"),L("ML",ML+"aceite+5w30+ford+fiesta")]),
        P("Motor","Filtro Aceite","Filtro aceite","Sigma/Dragon/EcoBoost","Motorcraft, MANN",
          [("Verificar OEM","verify")],"c/10k",[L("FamFord","http://www.famford.com.ar/"),L("ML",ML+"filtro+aceite+ford+fiesta")]),
        P("Motor","Filtro Aire","Filtro aire motor","Fiesta/Focus/Ecosport","Motorcraft, MANN",
          [("Verificar OEM","verify")],"c/15k",[L("ML",ML+"filtro+aire+ford+fiesta")]),
        P("Encendido","Bujias","Bujias x4 (x3 EcoBoost 1.0)","Motorcraft","Motorcraft, NGK",
          [("Motorcraft (Sigma/Dragon)","confirmed")],"c/40-60k",[L("FamFord","http://www.famford.com.ar/"),L("ML",ML+"bujia+ford+sigma")]),
        P("Encendido","Bobina","Bobina encendido EcoBoost 1.0","1.0 EcoBoost turbo","Motorcraft, Bosch",
          [("CM5G-12A366-CA","confirmed")],"por sintoma",[L("Walmart","https://www.walmart.com/ip/Ignition-Coil-OEM-CM5G-12A366-CA-Replacement-CM5G-12A366-CB-1776803-UF736-Fit-Ford-Fiesta-Focus-EcoSport-B-MAX-C-MAX-Transit-Courier-1-0L-EcoBoost-Tu/20745324207"),L("ML",ML+"bobina+ford+ecoboost")]),
        P("Confort","Filtro Cabina","Filtro habitaculo","Fiesta/Ecosport/Ka","Wix, MANN",
          [("Wix WP9360","confirmed")],"c/15-20k",[L("Autodo","https://www.autodo.com.ar/wix-wp9360/p"),L("ML",ML+"filtro+cabina+ford+fiesta")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Fiesta/Focus/Ecosport","Motorcraft, TRW",
          [("Verificar OEM","verify")],"c/30-50k",[L("FamFord","http://www.famford.com.ar/"),L("ML",ML+"pastillas+freno+ford+fiesta")]),
        P("Neumaticos","Neumatico",neum,"Segun modelo","Continental, Bridgestone",
          [(neum,"confirmed")],None,[L("ML",ML+"neumatico+"+neum.replace('/','+').replace(' ','+')),L("Continental","https://www.continental-neumaticos.cl/")]),
    ]

def ford_ecoboost(neum):
    return [
        P("Motor","Aceite","Aceite 5W-30 Motorcraft","~5.2L | EcoBoost 2.0T/2.3T","Motorcraft, Mobil",
          [("5W-30 (Ford WSS-M2C946)","confirmed")],"c/10k",[L("ML",ML+"aceite+5w30+ford+escape")]),
        P("Motor","Filtro Aceite","Filtro aceite EcoBoost","2.0T/2.3T","Motorcraft FL-910S / MANN",
          [("Motorcraft FL-910S","confirmed")],"c/10k",[L("ML",ML+"filtro+aceite+ford+escape"),L("AZ",AZ+"Motorcraft+FL-910S")]),
        P("Motor","Filtro Aire","Filtro aire motor","EcoBoost","Motorcraft, MANN",
          [("Verificar OEM","verify")],"c/15k",[L("ML",ML+"filtro+aire+ford+escape")]),
        P("Encendido","Bujias","Bujias x4","EcoBoost turbo","Motorcraft iridio",
          [("Verificar OEM","verify")],"c/45-60k",[L("ML",ML+"bujia+ford+ecoboost")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","SUV/deportivo","Motorcraft, TRW",
          [("Verificar OEM","verify")],"c/30-50k",[L("ML",ML+"pastillas+freno+ford+escape")]),
        P("Neumaticos","Neumatico",neum,"Segun modelo","Continental, Michelin",
          [(neum,"confirmed")],None,[L("ML",ML+"neumatico+"+neum.replace('/','+').replace(' ','+')),L("Michelin","https://www.michelin.cl/")]),
    ]

def ford_diesel(neum):
    return [
        P("Motor","Aceite","Aceite 5W-30 diesel Ford","~8.0-9.0L | Duratorq/EcoBlue","Motorcraft, Shell",
          [("5W-30 (Ford WSS-M2C934)","confirmed")],"c/10-15k",[L("C3CarCare","https://www.c3carecarcenter.com/blog/litros-de-aceite-ford-ranger/"),L("ML",ML+"aceite+5w30+ford+ranger")]),
        P("Motor","Filtro Aceite","Filtro aceite Duratorq","Ranger 2.2/3.2 Puma","Motorcraft, MANN",
          [("Verificar OEM","verify")],"c/10-15k",[L("C3CarCare","https://www.c3carecarcenter.com/blog/filtro-aceite-ford-ranger/"),L("ML",ML+"filtro+aceite+ford+ranger")]),
        P("Motor","Filtro Aire","Filtro aire motor","Pickup/furgon","Motorcraft, MANN",
          [("Verificar OEM","verify")],"c/15k",[L("ML",ML+"filtro+aire+ford+ranger")]),
        P("Motor","Filtro Combustible","Filtro combustible diesel","Separador agua","Bosch, MANN",
          [("Verificar OEM","verify")],"c/20-40k",[L("ML",ML+"filtro+combustible+ford+ranger")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Pickup","Motorcraft, TRW",
          [("Verificar OEM","verify")],"c/40k",[L("ML",ML+"pastillas+freno+ford+ranger")]),
        P("Neumaticos","Neumatico",neum,"Pickup/furgon","BFGoodrich, Bridgestone",
          [(neum,"confirmed")],None,[L("ML",ML+"neumatico+"+neum.replace('/','+').replace(' ','+')),L("BFGoodrich","https://www.bfgoodrich.cl/")]),
    ]

def ford_f150():
    return [
        P("Motor","Aceite","Aceite 5W-20 / 5W-30 Motorcraft","~8.0L | Coyote V8 / 3.5T V6","Motorcraft, Mobil",
          [("5W-20 (Coyote)","confirmed")],"c/12k",[L("ML",ML+"aceite+5w20+ford+f150"),L("AZ",AZ+"Motorcraft+5W-20")]),
        P("Motor","Filtro Aceite","Filtro aceite","F-150 V8/V6","Motorcraft FL-500S",
          [("Motorcraft FL-500S","confirmed")],"c/12k",[L("ML",ML+"filtro+aceite+ford+f150"),L("AZ",AZ+"Motorcraft+FL-500S")]),
        P("Motor","Filtro Aire","Filtro aire motor","Full-size","Motorcraft, MANN",
          [("Verificar OEM","verify")],"c/15k",[L("ML",ML+"filtro+aire+ford+f150")]),
        P("Encendido","Bujias","Bujias x8 (V8) / x6 (V6)","Motorcraft iridio","Motorcraft",
          [("Verificar OEM","verify")],"c/60-160k",[L("ML",ML+"bujia+ford+f150")]),
        P("Frenos","Pastillas Del.","Pastillas freno delanteras","Pickup full-size","Motorcraft, TRW",
          [("Verificar OEM","verify")],"c/40k",[L("ML",ML+"pastillas+freno+ford+f150")]),
        P("Neumaticos","Neumatico","275/65 R18","Full-size","BFGoodrich, Michelin",
          [("275/65 R18","confirmed")],None,[L("ML",ML+"neumatico+275+65+r18"),L("Michelin","https://www.michelin.cl/")]),
    ]

FIAT_MAP = {
    "fiat-argo":(fiat_firefly,"195/60 R16"), "fiat-cronos":(fiat_firefly,"185/65 R15"),
    "fiat-mobi":(fiat_firefly,"175/70 R14"), "fiat-pulse":(fiat_firefly,"215/60 R17"),
    "fiat-uno":(fiat_fire,"175/65 R14"), "fiat-palio":(fiat_fire,"185/60 R15"),
    "fiat-strada":(fiat_fire,"175/70 R14"), "fiat-fiorino":(fiat_fire,"175/70 R14"),
    "fiat-147l":(fiat_fire,"155/70 R13"), "fiat-ducato":(fiat_ducato,None),
}
FORD_MAP = {
    "ford-ecosport":(ford_sigma,"205/60 R16"), "ford-fiesta":(ford_sigma,"185/60 R15"),
    "ford-focus":(ford_sigma,"205/55 R16"),
    "ford-escape":(ford_ecoboost,"225/65 R17"), "ford-edge":(ford_ecoboost,"245/60 R18"),
    "ford-explorer":(ford_ecoboost,"255/65 R18"), "ford-bronco-sport":(ford_ecoboost,"225/65 R17"),
    "ford-territory":(ford_ecoboost,"225/55 R18"), "ford-mustang":(ford_ecoboost,"255/40 R19"),
    "ford-ranger":(ford_diesel,"255/70 R16"), "ford-transit":(ford_diesel,"235/65 R16C"),
    "ford-f-150":(ford_f150,None),
}

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

def base_id(vid): return re.sub(r'-\d{4}$','',vid)

def main():
    conn=sqlite3.connect(DB); conn.execute("PRAGMA foreign_keys=ON"); c=conn.cursor()
    rows=c.execute("SELECT id,name FROM vehicles WHERE name LIKE 'Fiat %' OR name LIKE 'Ford %'").fetchall()
    nf={"Fiat":0,"Ford":0}
    for vid,name in rows:
        b=base_id(vid)
        if name.startswith("Fiat"):
            gen,neum=FIAT_MAP.get(b,(fiat_fire,"175/65 R14")); nf["Fiat"]+=1
        else:
            gen,neum=FORD_MAP.get(b,(ford_sigma,"205/60 R16")); nf["Ford"]+=1
        comps = gen(neum) if neum is not None else gen()
        clear_and_insert(c, vid, comps)
    conn.commit()
    print("Actualizados:", nf)
    tp=c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("Componentes totales:", tp)
    conn.close()

if __name__=="__main__":
    main()
