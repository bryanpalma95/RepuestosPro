"""RepuestosPro - Bloque 28 FINAL: ~48 vehiculos restantes"""
import sqlite3,os
DB=os.path.join(os.path.dirname(os.path.abspath(__file__)),'db.sqlite')
ML="https://listado.mercadolibre.cl/";AZ="https://www.amazon.com/s?k="
def make(name,info,cross,cats):
    return {"name":name,"info":info,"crossNote":cross,"categories":cats}
def mot(aceite,det,brands,ref,filt_ref,neum,neum_ref):
    return {"Motor":[{"cat":"Aceite","name":aceite,"details":det,"brands":brands,"refs":[{"r":ref,"s":"confirmed"}],"links":[{"t":"ML","u":ML+"aceite+"+ref.split()[0].lower()+"+"+ref.split()[1].lower() if len(ref.split())>1 else ML+"aceite+5w30"},{"t":"AZ","u":AZ+ref.replace(" ","+")},{"t":"Web","u":"https://www.mann-filter.com/"}]},{"cat":"Filtro Aceite","name":"Filtro aceite","details":"","brands":"MANN, Bosch","refs":[{"r":filt_ref,"s":"verify"}],"interval":"c/10-15k","links":[{"t":"ML","u":ML+"filtro+aceite"},{"t":"AZ","u":AZ+"oil+filter"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}],"Neumaticos":[{"cat":"Neumatico","name":neum,"details":"","brands":"Michelin, Continental, Bridgestone","refs":[{"r":neum_ref,"s":"confirmed"}],"links":[{"t":"ML","u":ML+"neumatico+"+neum_ref.replace("/","+").replace(" ","+")},{"t":"Michelin","u":"https://www.michelin.cl/"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"}]}]}
def ins(conn):
    c=conn.cursor()
    V={
"bmw_serie1":make("BMW Serie 1 118i/120i — 2015-2026","B38/B48 1.5T/2.0T | Cadena","Motor B48 comp. Serie 3, X1",mot("5W-30 BMW LL-04","~4.5L","BMW, Castrol, Liqui Moly","5W-30 BMW LL-04","Verificar OEM","225/45 R17","225/45 R17")),
"bmw_serie3":make("BMW Serie 3 320i/330i — 2015-2026","B48 2.0T | Cadena","Comp. X1, X3 (B48)",mot("5W-30 BMW LL-04","~5.0L","BMW, Castrol, Liqui Moly","5W-30 BMW LL-04","Verificar OEM","225/45 R18","225/45 R18")),
"bmw_x1":make("BMW X1 sDrive18i/20i — 2016-2026","B38/B48 1.5T/2.0T | Cadena","= Serie 1/3 motor",mot("5W-30 BMW LL-04","~4.5L","BMW, Castrol","5W-30 BMW LL-04","Verificar OEM","225/50 R18","225/50 R18")),
"bmw_x3":make("BMW X3 xDrive20i/30i — 2017-2026","B48 2.0T / B58 3.0T | Cadena","B48 = Serie 3. B58 = Supra",mot("5W-30 BMW LL-04","~5.5L","BMW, Castrol, Liqui Moly","5W-30 BMW LL-04","Verificar OEM","245/50 R19","245/50 R19")),
"bmw_x5":make("BMW X5 xDrive40i — 2019-2026","B58 3.0T I6 | Cadena","B58 = X3 M40i, Supra",mot("5W-30 BMW LL-04","~6.5L","BMW, Castrol, Liqui Moly","5W-30 BMW LL-04","Verificar OEM","275/40 R20","275/40 R20")),
"mercedes_a":make("Mercedes Clase A 200/250 — 2018-2026","M282 1.3T / M260 2.0T | Cadena","MFA2. 1.3T = Renault",mot("5W-30 MB 229.52","~5.0L","Mercedes, Mobil, Castrol","5W-30 MB 229.52","Verificar OEM","225/45 R17","225/45 R17")),
"mercedes_c":make("Mercedes Clase C 200/300 — 2015-2026","M264/M254 2.0T | Cadena","Comp. E-Class, GLC",mot("5W-30 MB 229.52","~5.5L","Mercedes, Mobil","5W-30 MB 229.52","Verificar OEM","225/45 R18","225/45 R18")),
"mercedes_e":make("Mercedes Clase E 200/300 — 2016-2026","M264/M254 2.0T | Cadena","Comp. Clase C motor",mot("5W-30 MB 229.52","~5.5L","Mercedes, Mobil","5W-30 MB 229.52","Verificar OEM","245/45 R18","245/45 R18")),
"mercedes_gla":make("Mercedes GLA 200/250 — 2020-2026","M282 1.3T / M260 2.0T | Cadena","= Clase A SUV",mot("5W-30 MB 229.52","~5.0L","Mercedes, Mobil","5W-30 MB 229.52","Verificar OEM","235/55 R18","235/55 R18")),
"mercedes_glc":make("Mercedes GLC 200/300 — 2016-2026","M254 2.0T | Cadena","Motor = Clase C/E",mot("5W-30 MB 229.52","~5.5L","Mercedes, Mobil","5W-30 MB 229.52","Verificar OEM","235/55 R19","235/55 R19")),
"mercedes_sprinter":make("Mercedes Sprinter 2.1D — 2014-2026","OM651 2.1D | Cadena","Furgon comercial",mot("5W-30 MB 229.51","~7.0L","Mercedes, Shell Rimula","5W-30 MB 229.51","Verificar OEM","235/65 R16C","235/65 R16C")),
"audi_a3":make("Audi A3 1.4T/2.0T — 2014-2026","EA211/EA888 | Cadena","= VW Golf MQB",mot("5W-40 VW 502.00","~4.0-4.6L","Castrol, Liqui Moly","5W-40 VW 502.00","MANN W 712/94","225/45 R17","225/45 R17")),
"audi_a4":make("Audi A4 2.0T — 2016-2026","EA888 2.0T | Cadena","Comp. Q5",mot("5W-40 VW 502.00","~5.0L","Castrol, Liqui Moly","5W-40 VW 502.00","MANN HU 7012 z (verificar)","245/40 R18","245/40 R18")),
"audi_q3":make("Audi Q3 1.4T/2.0T — 2015-2026","EA211/EA888 | Cadena","= A3 SUV",mot("5W-40 VW 502.00","~4.0-4.6L","Castrol, Liqui Moly","5W-40 VW 502.00","MANN W 712/94","235/50 R19","235/50 R19")),
"audi_q5":make("Audi Q5 2.0T — 2017-2026","EA888 2.0T | Cadena","Comp. A4",mot("5W-40 VW 502.00","~5.7L","Castrol, Liqui Moly","5W-40 VW 502.00","MANN HU 7012 z (verificar)","235/55 R19","235/55 R19")),
"volvo_xc40":make("Volvo XC40 T4/T5 — 2018-2026","B4204T 2.0T | Cadena","CMA",mot("0W-20 Volvo","~5.0L","Volvo, Castrol","0W-20 Volvo","Verificar OEM","235/50 R19","235/50 R19")),
"volvo_xc60":make("Volvo XC60 T5/T6 — 2018-2026","B4204T 2.0T/SC | Cadena","SPA",mot("0W-20 Volvo","~5.5L","Volvo, Castrol","0W-20 Volvo","Verificar OEM","235/55 R19","235/55 R19")),
"lexus_nx":make("Lexus NX 250/350h — 2022-2026","A25A 2.5/Hybrid | Cadena","= RAV4 TNGA-K",mot("0W-20","~4.5L","Toyota/Lexus, Mobil","0W-20","90915-YZZD4 (verificar)","225/60 R18","225/60 R18")),
"porsche_macan":make("Porsche Macan 2.0T/3.0T — 2014-2026","EA888 2.0T / 3.0T | Cadena","2.0T = Audi Q5",mot("5W-40","~6.0-7.0L","Mobil 1, Porsche","5W-40","Verificar OEM","235/55 R19","235/55 R19")),
"porsche_cayenne":make("Porsche Cayenne 3.0T V6 — 2018-2026","EA839 3.0T V6 | Cadena","= Touareg/Q7 plataforma",mot("5W-40","~8.0L","Mobil 1, Porsche","5W-40","Verificar OEM","255/55 R19","255/55 R19")),
"land_rover_evoque":make("Range Rover Evoque 2.0T — 2020-2026","Ingenium 2.0T | Cadena","Comp. Discovery Sport",mot("5W-30 A5/B5","~5.0L","Castrol, Land Rover","5W-30 A5/B5","Verificar OEM","235/50 R20","235/50 R20")),
"seat_ibiza":make("Seat Ibiza 1.0T — 2018-2026","EA211 1.0 TSI | Cadena","= VW Polo",mot("5W-40 VW 502.00","~3.6L","Castrol, Liqui Moly","5W-40 VW 502.00","MANN W 712/94","215/45 R17","215/45 R17")),
"seat_leon":make("Seat Leon 1.4T/2.0T — 2014-2026","EA211/EA888 | Cadena","= VW Golf",mot("5W-40 VW 502.00","~4.0-4.6L","Castrol, Liqui Moly","5W-40 VW 502.00","MANN W 712/94","225/45 R17","225/45 R17")),
"skoda_octavia":make("Skoda Octavia 1.4T/2.0T — 2014-2026","EA211/EA888 | Cadena","= VW Jetta MQB",mot("5W-40 VW 502.00","~4.0-4.6L","Castrol, Liqui Moly","5W-40 VW 502.00","MANN W 712/94","225/45 R18","225/45 R18")),
"opel_corsa":make("Opel Corsa 1.2T — 2020-2026","PureTech 1.2T | Cadena","= Peugeot 208 PSA",mot("5W-30 PSA B71 2290","~3.5L","Total, Motul","5W-30 PSA B71 2290","Verificar OEM","205/45 R17","205/45 R17")),
"mini_cooper":make("Mini Cooper 1.5T/2.0T — 2014-2026","B38/B48 BMW | Cadena","= BMW Serie 1 motor",mot("5W-30 BMW LL-04","~4.2L","BMW, Castrol, Liqui Moly","5W-30 BMW LL-04","Verificar OEM","205/45 R17","205/45 R17")),
"fiat_500":make("Fiat 500 1.2/0.9T — 2014-2023","Fire 1.2 / TwinAir 0.9T | Correa/Cadena","City car",mot("5W-30","~2.8-3.0L","Selenia, Mobil","5W-30","Verificar OEM","195/45 R16","195/45 R16")),
"ford_bronco_sport":make("Ford Bronco Sport 1.5T/2.0T — 2021-2026","EcoBoost 1.5T/2.0T | Cadena","= Escape plataforma",mot("5W-30","~4.5-5.0L","Motorcraft, Mobil","5W-30","Verificar OEM","225/65 R17","225/65 R17")),
"ford_mustang":make("Ford Mustang 2.3T/5.0 V8 — 2015-2026","EcoBoost 2.3T / Coyote 5.0 V8 | Cadena","Iconico",mot("5W-30","~5.0-8.0L","Motorcraft, Mobil 1","5W-30","Verificar OEM","255/40 R19","255/40 R19")),
"ford_transit":make("Ford Transit 2.2D/2.0D — 2014-2026","Duratorq/EcoBlue | Correa/Cadena","Furgon comercial",mot("5W-30 diesel","~6.0-7.0L","Motorcraft, Shell Rimula","5W-30 diesel","Verificar OEM","235/65 R16C","235/65 R16C")),
"ford_edge":make("Ford Edge 2.0T — 2015-2024","EcoBoost 2.0T | Cadena","Comp. Escape motor",mot("5W-30","~5.0L","Motorcraft, Mobil","5W-30","Verificar OEM","245/50 R20","245/50 R20")),
"jetour_x70":make("Jetour X70 1.5T — 2020-2026","SQRF4J16 1.5T | Cadena","Chery. = Tiggo 7 motor",mot("5W-30","~4.2L","Mobil, Shell","5W-30 API SP","Verificar OEM","225/55 R18","225/55 R18")),
"jetour_dashing":make("Jetour Dashing 1.5T/1.6T — 2022-2026","1.5T/1.6T | Cadena","Chery premium",mot("5W-30","~4.2L","Mobil, Shell","5W-30 API SP","Verificar OEM","235/50 R19","235/50 R19")),
"omoda_c5":make("Omoda C5 1.5T — 2023-2026","SQRF4J16 1.5T | Cadena","Chery",mot("5W-30","~4.0L","Mobil, Shell","5W-30 API SP","Verificar OEM","225/45 R19","225/45 R19")),
"maxus_g10":make("Maxus G10 2.0T — 2018-2026","SAIC 2.0T | Cadena","Van SAIC",mot("5W-30","~5.5L","Mobil, Shell","5W-30","Verificar OEM","215/65 R16C","215/65 R16C")),
"maxus_deliver9":make("Maxus Deliver 9 2.0D — 2021-2026","VM 2.0D | Cadena","Furgon",mot("5W-30 diesel","~6.0L","Shell Rimula","5W-30 diesel","Verificar OEM","235/65 R16C","235/65 R16C")),
"dfsk_glory580":make("DFSK Glory 580 1.5T — 2018-2026","SFG15T 1.5T | Cadena","SUV Dongfeng Sokon",mot("5W-30","~4.0L","Mobil, Shell","5W-30","Verificar OEM","215/55 R18","215/55 R18")),
"baic_x55":make("BAIC X55 1.5T — 2020-2026","A151T 1.5T | Cadena","SUV Beijing Auto",mot("5W-30","~4.0L","Mobil, Shell","5W-30","Verificar OEM","225/55 R18","225/55 R18")),
"dongfeng_t5l":make("Dongfeng Forthing T5L 1.5T — 2021-2026","TD15M 1.5T | Cadena","= SX5 evolucion",mot("5W-30","~4.0L","Mobil, Shell","5W-30","Verificar OEM","225/55 R18","225/55 R18")),
"jmc_vigus":make("JMC Vigus Pro 2.0D — 2021-2026","JX4D20 2.0D | Cadena","Pickup JMC Ford China",mot("5W-30 diesel","~5.5L","Shell Rimula","5W-30 diesel","Verificar OEM","245/65 R17","245/65 R17")),
"gac_gs4":make("GAC GS4 1.5T — 2019-2026","4B15J 1.5T | Cadena","SUV GAC Motor",mot("5W-30","~4.0L","Mobil, Shell","5W-30","Verificar OEM","225/55 R18","225/55 R18")),
    }
    for vid, vdata in V.items():
        c.execute("INSERT OR IGNORE INTO vehicles VALUES (?,?,?,?)", (vid, vdata["name"], vdata["info"], vdata["crossNote"]))
        order=0
        for cat_name, parts in vdata["categories"].items():
            order+=1
            c.execute("INSERT INTO categories (vehicle_id, name, sort_order) VALUES (?,?,?)", (vid, cat_name, order))
            cat_id=c.lastrowid
            for p in parts:
                c.execute("INSERT INTO parts (category_id, cat_label, name, details, brands, interval_info) VALUES (?,?,?,?,?,?)",
                    (cat_id, p.get("cat",""), p["name"], p.get("details",""), p.get("brands",""), p.get("interval",None)))
                pid=c.lastrowid
                for r in p.get("refs",[]):
                    c.execute("INSERT INTO part_refs (part_id, reference, status) VALUES (?,?,?)", (pid, r["r"], r["s"]))
                for l in p.get("links",[]):
                    c.execute("INSERT INTO part_links (part_id, label, url) VALUES (?,?,?)", (pid, l["t"], l["u"]))
    conn.commit()
    total=c.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
    parts_count=c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print(f"Bloque 28 FINAL insertado OK")
    print(f"Vehiculos totales: {total} | Componentes totales: {parts_count}")
if __name__=="__main__":
    conn=sqlite3.connect(DB);conn.execute("PRAGMA foreign_keys = ON");ins(conn);conn.close()
