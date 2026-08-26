"""
RepuestosPro - Bloque 13: Chevrolet Optra, D-Max, Onix, Cavalier, Tahoe, Suburban, Montana, Spin, Prisma + VW Virtus
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"
AZ = "https://www.amazon.com/s?k="

def ins(conn):
    c = conn.cursor()

    vehicles = {
        "chevrolet_optra": {
            "name": "Chevrolet Optra 1.6/1.8 — 2004-2012",
            "info": "E-TEC II 1.6 F16D3 / 1.8 T18SED | Correa",
            "crossNote": "= Daewoo Lacetti/Nubira. Motor F16D3 = Aveo 1.6",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30","details":"API SN | 3.75L","brands":"Mobil, Castrol, Shell",
                     "refs":[{"r":"5W-30 API SN","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+sintetico"},{"t":"Amazon","u":AZ+"5W-30+synthetic"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite F16D3","details":"Rosca M20","brands":"MANN, ACDelco, Wix",
                     "refs":[{"r":"MANN W 7015","s":"confirmed"},{"r":"PF48","s":"confirmed"},{"r":"93185674 OEM","s":"verify"}],
                     "interval":"c/5-10k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+chevrolet+optra"},{"t":"Amazon","u":AZ+"MANN+W7015"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire panel","details":"F16D3","brands":"MANN, Wix, ACDelco",
                     "refs":[{"r":"MANN C 2565","s":"confirmed"},{"r":"96553450 OEM","s":"confirmed"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+chevrolet+optra"},{"t":"Amazon","u":AZ+"air+filter+Chevrolet+Optra"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Cabina","name":"Filtro cabina","details":"Carbon activado disp.","brands":"MANN, Bosch",
                     "refs":[{"r":"MANN CU 2442","s":"confirmed"},{"r":"96554378 OEM","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+cabina+chevrolet+optra"},{"t":"Amazon","u":AZ+"cabin+filter+Chevrolet+Optra"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4","details":"Gap 0.8-1.0mm","brands":"NGK, Denso, Bosch",
                     "refs":[{"r":"NGK BKR6E-11","s":"confirmed"},{"r":"Denso K20TT","s":"confirmed"},{"r":"Bosch FR7DC+","s":"confirmed"}],
                     "interval":"c/20-30k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+chevrolet+optra"},{"t":"Amazon","u":AZ+"NGK+BKR6E-11"},{"t":"NGK","u":"https://www.ngk.com/"}]},
                    {"cat":"Bobina","name":"Bobina encendido","details":"Cassette 4 salidas","brands":"Delphi, ACDelco",
                     "refs":[{"r":"96453420","s":"confirmed"},{"r":"Delphi GN10362","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"bobina+encendido+chevrolet+optra"},{"t":"Amazon","u":AZ+"ignition+coil+Chevrolet+Optra"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Cables Bujia","name":"Cables bujia x4","details":"F16D3","brands":"NGK, ACDelco",
                     "refs":[{"r":"96497773 OEM","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"cables+bujia+chevrolet+optra"},{"t":"Amazon","u":AZ+"spark+plug+wires+Chevrolet+Optra"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado 256mm","brands":"TRW, Bosch, Sangsin",
                     "refs":[{"r":"GDB3286","s":"confirmed"},{"r":"96534653 OEM","s":"confirmed"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+chevrolet+optra"},{"t":"Amazon","u":AZ+"brake+pads+Chevrolet+Optra"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]},
                    {"cat":"Pastillas Tras.","name":"Pastillas/Balatas traseras","details":"Tambor","brands":"TRW, Bosch",
                     "refs":[{"r":"GS8634","s":"verify"}],
                     "interval":"c/50-70k",
                     "links":[{"t":"MercadoLibre","u":ML+"balatas+traseras+chevrolet+optra"},{"t":"Amazon","u":AZ+"rear+brake+shoes+Chevrolet+Optra"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Kit Correa","name":"Kit distribucion","details":"Correa + tensor + bomba agua","brands":"Gates, Dayco, Continental",
                     "refs":[{"r":"Gates K015603XS","s":"confirmed"},{"r":"96417177 correa OEM","s":"confirmed"}],
                     "interval":"c/60k km",
                     "links":[{"t":"MercadoLibre","u":ML+"kit+distribucion+chevrolet+optra"},{"t":"Amazon","u":AZ+"timing+belt+kit+Chevrolet+Optra"},{"t":"Gates","u":"https://www.gates.com/"}]}
                ],
                "Refrigeracion": [
                    {"cat":"Refrigerante","name":"Dex-Cool naranja","details":"OAT GM","brands":"ACDelco, Prestone",
                     "refs":[{"r":"Dex-Cool OAT","s":"confirmed"}],
                     "interval":"c/4-5 anos",
                     "links":[{"t":"MercadoLibre","u":ML+"refrigerante+dex+cool"},{"t":"Amazon","u":AZ+"ACDelco+Dex-Cool"},{"t":"Prestone","u":"https://prestone.com/"}]}
                ],
                "Transmision": [
                    {"cat":"Aceite Caja","name":"75W-90 GL-4","details":"Manual ~1.8L","brands":"ACDelco, Motul",
                     "refs":[{"r":"75W-90 GL-4","s":"confirmed"}],
                     "interval":"c/40-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+transmision+75w90"},{"t":"Amazon","u":AZ+"75W-90+GL-4"},{"t":"Motul","u":"https://www.motul.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"195/55 R15","details":"","brands":"Hankook, Kumho, Continental",
                     "refs":[{"r":"195/55 R15","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+195+55+r15"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Michelin","u":"https://www.michelin.cl/"}]}
                ]
            }
        },
        "chevrolet_dmax": {
            "name": "Chevrolet D-Max 2.5D/3.0D — 2014-2026",
            "info": "4JK1-TC 2.5D / 4JJ1-TC 3.0D Isuzu | Cadena",
            "crossNote": "= Isuzu D-Max. Motor Isuzu 4JK1/4JJ1",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30 diesel","details":"CI-4/CK-4 | 5.5-7.0L","brands":"Mobil Delvac, Shell Rimula, Castrol",
                     "refs":[{"r":"5W-30 CI-4","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+diesel"},{"t":"Amazon","u":AZ+"5W-30+diesel+oil"},{"t":"Shell","u":"https://www.shell.cl/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite diesel","details":"4JK1/4JJ1","brands":"MANN, Isuzu, Bosch",
                     "refs":[{"r":"MANN W 950/38","s":"confirmed"},{"r":"8-98165071-0 OEM","s":"confirmed"}],
                     "interval":"c/5-10k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+chevrolet+dmax"},{"t":"Amazon","u":AZ+"oil+filter+Isuzu+D-Max"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Cilindrico","brands":"MANN, Wix, Sakura",
                     "refs":[{"r":"8-98140266-0 OEM","s":"confirmed"},{"r":"MANN C 16 012","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+chevrolet+dmax"},{"t":"Amazon","u":AZ+"air+filter+Isuzu+D-Max"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Combustible","name":"Filtro petroleo","details":"Con separador agua","brands":"MANN, Bosch, Sakura",
                     "refs":[{"r":"MANN WK 8019","s":"confirmed"},{"r":"8-98149983-0 OEM","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+combustible+chevrolet+dmax"},{"t":"Amazon","u":AZ+"fuel+filter+Isuzu+D-Max"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias Precal.","name":"Bujias precalentamiento x4","details":"Diesel","brands":"Bosch, NGK, Denso",
                     "refs":[{"r":"Bosch GLP 194 (verificar)","s":"verify"},{"r":"8-98186806-0 OEM","s":"verify"}],
                     "interval":"c/80-100k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+precalentamiento+dmax"},{"t":"Amazon","u":AZ+"glow+plug+Isuzu+D-Max"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado 280-300mm","brands":"TRW, Bosch, Brembo",
                     "refs":[{"r":"8-98080077-0 OEM","s":"confirmed"},{"r":"GDB3548","s":"confirmed"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+chevrolet+dmax"},{"t":"Amazon","u":AZ+"brake+pads+Isuzu+D-Max"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]},
                    {"cat":"Pastillas Tras.","name":"Pastillas traseras","details":"Disco solido","brands":"TRW, Bosch",
                     "refs":[{"r":"8-98079104-0 OEM","s":"confirmed"}],
                     "interval":"c/40-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+traseras+dmax"},{"t":"Amazon","u":AZ+"rear+brake+pads+Isuzu+D-Max"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"NO cambio programado","brands":"-",
                     "refs":[{"r":"Cadena 4JK1","s":"confirmed"}],
                     "interval":"Tensores c/150k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+isuzu+dmax"},{"t":"Amazon","u":AZ+"timing+chain+Isuzu+4JK1"},{"t":"Isuzu","u":"https://www.isuzu.cl/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"245/70 R16 / 255/65 R17","details":"4x4","brands":"BFGoodrich, General Tire, Bridgestone",
                     "refs":[{"r":"245/70 R16","s":"confirmed"},{"r":"255/65 R17","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+245+70+r16"},{"t":"BFGoodrich","u":"https://www.bfgoodrich.cl/"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"}]}
                ]
            }
        },
        "chevrolet_onix": {
            "name": "Chevrolet Onix 1.0T/1.2 — 2020-2026",
            "info": "1.0T Ecotec 3cil / 1.2 4cil | Cadena",
            "crossNote": "Plataforma GEM. Comp: Tracker 1.0T, Onix Plus",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30 Dexos1","details":"API SP | 3.5-4.0L","brands":"Mobil, ACDelco, Castrol",
                     "refs":[{"r":"5W-30 Dexos1 Gen3","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+dexos1"},{"t":"Amazon","u":AZ+"ACDelco+dexos1+5W-30"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite 1.0T","details":"Ecotec 3cil","brands":"ACDelco, MANN, Wix",
                     "refs":[{"r":"55594651 OEM","s":"confirmed"},{"r":"MANN W 712/95","s":"confirmed"}],
                     "interval":"c/10k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+chevrolet+onix"},{"t":"Amazon","u":AZ+"oil+filter+Chevrolet+Onix"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel 1.0T","brands":"ACDelco, MANN",
                     "refs":[{"r":"42675534 OEM (verificar)","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+chevrolet+onix"},{"t":"Amazon","u":AZ+"air+filter+Chevrolet+Onix"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Cabina","name":"Filtro cabina","details":"Panel","brands":"ACDelco, MANN",
                     "refs":[{"r":"52187011 OEM (verificar)","s":"verify"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+cabina+chevrolet+onix"},{"t":"Amazon","u":AZ+"cabin+filter+Chevrolet+Onix"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x3 (1.0T)","details":"Iridium turbo","brands":"NGK, ACDelco",
                     "refs":[{"r":"LKAR7BI-9S (verificar)","s":"verify"},{"r":"55598693 OEM","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+chevrolet+onix+1.0+turbo"},{"t":"Amazon","u":AZ+"spark+plug+Chevrolet+Onix"},{"t":"NGK","u":"https://www.ngk.com/"}]},
                    {"cat":"Bobina","name":"Bobina x3 (1.0T)","details":"Individual","brands":"Delphi, ACDelco",
                     "refs":[{"r":"55585539 OEM (verificar)","s":"verify"}],
                     "links":[{"t":"MercadoLibre","u":ML+"bobina+encendido+chevrolet+onix"},{"t":"Amazon","u":AZ+"ignition+coil+Chevrolet+Onix"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~276mm","brands":"TRW, Bosch, ACDelco",
                     "refs":[{"r":"GDB3594 (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+chevrolet+onix"},{"t":"Amazon","u":AZ+"brake+pads+Chevrolet+Onix"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]},
                    {"cat":"Pastillas Tras.","name":"Pastillas traseras","details":"Tambor/Disco segun version","brands":"TRW, Bosch",
                     "refs":[{"r":"Verificar version","s":"verify"}],
                     "interval":"c/50-70k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+traseras+chevrolet+onix"},{"t":"Amazon","u":AZ+"rear+brake+Chevrolet+Onix"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"NO cambio","brands":"-",
                     "refs":[{"r":"Cadena 1.0T","s":"confirmed"}],
                     "interval":"Tensores c/100k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+chevrolet+onix"},{"t":"Amazon","u":AZ+"timing+chain+Chevrolet+Onix"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"195/55 R16 / 185/65 R15","details":"Segun version","brands":"Continental, Bridgestone, Pirelli",
                     "refs":[{"r":"195/55 R16","s":"confirmed"},{"r":"185/65 R15","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+195+55+r16"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Pirelli","u":"https://www.pirelli.com/"}]}
                ]
            }
        },
        "chevrolet_cavalier": {
            "name": "Chevrolet Cavalier 1.5 — 2018-2026",
            "info": "L2B 1.5L SAIC | Cadena",
            "crossNote": "Motor L2B SAIC. Comp: Sail 1.5 (mismo bloque)",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30 Dexos1","details":"API SN | ~4.0L","brands":"Mobil, ACDelco, Shell",
                     "refs":[{"r":"5W-30 Dexos1","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+dexos1"},{"t":"Amazon","u":AZ+"5W-30+Dexos1"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite L2B","details":"Comp. Sail 1.5","brands":"ACDelco, MANN, Wix",
                     "refs":[{"r":"MANN W 712/95","s":"confirmed"},{"r":"24109353 OEM (verificar)","s":"verify"}],
                     "interval":"c/7.5-10k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+chevrolet+cavalier"},{"t":"Amazon","u":AZ+"oil+filter+Chevrolet+Cavalier+1.5"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel","brands":"ACDelco, MANN",
                     "refs":[{"r":"Verificar OEM","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+chevrolet+cavalier"},{"t":"Amazon","u":AZ+"air+filter+Chevrolet+Cavalier"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4","details":"Iridium","brands":"NGK, ACDelco, Denso",
                     "refs":[{"r":"ILKAR7B11 (verificar)","s":"verify"}],
                     "interval":"c/30k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+chevrolet+cavalier"},{"t":"Amazon","u":AZ+"spark+plug+Chevrolet+Cavalier"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado","brands":"TRW, Bosch, ACDelco",
                     "refs":[{"r":"Verificar OEM","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+chevrolet+cavalier"},{"t":"Amazon","u":AZ+"brake+pads+Chevrolet+Cavalier"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"NO cambio","brands":"-",
                     "refs":[{"r":"Cadena L2B","s":"confirmed"}],
                     "interval":"Tensores c/100k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+chevrolet+cavalier"},{"t":"Amazon","u":AZ+"timing+chain+Chevrolet+Cavalier"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"195/55 R16 / 185/60 R15","details":"","brands":"Continental, Hankook, Pirelli",
                     "refs":[{"r":"195/55 R16","s":"confirmed"},{"r":"185/60 R15","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+195+55+r16"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Pirelli","u":"https://www.pirelli.com/"}]}
                ]
            }
        },
        "chevrolet_tahoe": {
            "name": "Chevrolet Tahoe 5.3 V8 — 2014-2026",
            "info": "EcoTec3 5.3L V8 L83/L84 | Cadena",
            "crossNote": "= Suburban, Silverado (mismo motor). Comp: GMC Yukon",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30 Dexos1","details":"API SP | ~7.5L","brands":"Mobil 1, ACDelco, Valvoline",
                     "refs":[{"r":"5W-30 Dexos1 Gen3","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+dexos1"},{"t":"Amazon","u":AZ+"Mobil+1+5W-30+5+quart"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite V8","details":"5.3L EcoTec3","brands":"ACDelco, MANN, Wix",
                     "refs":[{"r":"ACDelco PF63E","s":"confirmed"},{"r":"MANN W 950/26","s":"confirmed"}],
                     "interval":"c/10-12k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+chevrolet+tahoe"},{"t":"Amazon","u":AZ+"ACDelco+PF63E"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel grande V8","brands":"ACDelco, K&N, MANN",
                     "refs":[{"r":"A3181C (verificar)","s":"verify"}],
                     "interval":"c/15-25k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+chevrolet+tahoe"},{"t":"Amazon","u":AZ+"air+filter+Chevrolet+Tahoe"},{"t":"K&N","u":"https://www.knfilters.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x8","details":"Iridium V8","brands":"ACDelco, NGK",
                     "refs":[{"r":"ACDelco 41-114 Iridium","s":"confirmed"},{"r":"41-110 (gen anterior)","s":"confirmed"}],
                     "interval":"c/60-100k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+chevrolet+tahoe+5.3"},{"t":"Amazon","u":AZ+"ACDelco+41-114"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado grande","brands":"ACDelco, Wagner, Brembo",
                     "refs":[{"r":"ACDelco 171-1074 (verificar)","s":"verify"}],
                     "interval":"c/40-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+chevrolet+tahoe"},{"t":"Amazon","u":AZ+"brake+pads+Chevrolet+Tahoe"},{"t":"Wagner","u":"https://www.wagnerbrake.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"V8 doble cadena","brands":"-",
                     "refs":[{"r":"Cadena EcoTec3","s":"confirmed"}],
                     "interval":"Tensores c/150k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+chevrolet+tahoe"},{"t":"Amazon","u":AZ+"timing+chain+kit+5.3+V8+Chevrolet"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Transmision": [
                    {"cat":"Fluido ATF","name":"ATF Dexron VI","details":"Automatica 6/8/10 vel","brands":"ACDelco, Valvoline",
                     "refs":[{"r":"Dexron VI","s":"confirmed"},{"r":"ACDelco 10-9395","s":"confirmed"}],
                     "interval":"c/60-80k",
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+transmision+dexron+vi"},{"t":"Amazon","u":AZ+"ACDelco+Dexron+VI"},{"t":"Valvoline","u":"https://www.valvoline.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"265/65 R18 / 275/55 R20","details":"SUV grande","brands":"BFGoodrich, Michelin, Bridgestone",
                     "refs":[{"r":"265/65 R18","s":"confirmed"},{"r":"275/55 R20","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+265+65+r18"},{"t":"BFGoodrich","u":"https://www.bfgoodrich.cl/"},{"t":"Michelin","u":"https://www.michelin.cl/"}]}
                ]
            }
        },
        "chevrolet_suburban": {
            "name": "Chevrolet Suburban 5.3 V8 — 2014-2026",
            "info": "EcoTec3 5.3L V8 L83/L84 | Cadena",
            "crossNote": "= Tahoe (mismo motor y tren). Mas largo. Comp: GMC Yukon XL",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30 Dexos1","details":"API SP | ~7.5L","brands":"Mobil 1, ACDelco, Valvoline",
                     "refs":[{"r":"5W-30 Dexos1 Gen3","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+dexos1"},{"t":"Amazon","u":AZ+"Mobil+1+5W-30"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite V8 = Tahoe","details":"5.3L EcoTec3","brands":"ACDelco, MANN, Wix",
                     "refs":[{"r":"ACDelco PF63E","s":"confirmed"},{"r":"MANN W 950/26","s":"confirmed"}],
                     "interval":"c/10-12k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+chevrolet+suburban"},{"t":"Amazon","u":AZ+"ACDelco+PF63E"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x8 = Tahoe","details":"Iridium V8","brands":"ACDelco, NGK",
                     "refs":[{"r":"ACDelco 41-114","s":"confirmed"}],
                     "interval":"c/60-100k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+chevrolet+suburban+5.3"},{"t":"Amazon","u":AZ+"ACDelco+41-114"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"= Tahoe","brands":"ACDelco, Wagner, Brembo",
                     "refs":[{"r":"ACDelco 171-1074 (verificar)","s":"verify"}],
                     "interval":"c/40-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+chevrolet+suburban"},{"t":"Amazon","u":AZ+"brake+pads+Chevrolet+Suburban"},{"t":"Wagner","u":"https://www.wagnerbrake.com/"}]}
                ],
                "Transmision": [
                    {"cat":"Fluido ATF","name":"ATF Dexron VI = Tahoe","details":"Automatica","brands":"ACDelco, Valvoline",
                     "refs":[{"r":"Dexron VI","s":"confirmed"}],
                     "interval":"c/60-80k",
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+transmision+dexron+vi"},{"t":"Amazon","u":AZ+"ACDelco+Dexron+VI"},{"t":"Valvoline","u":"https://www.valvoline.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"265/65 R18 / 275/55 R20","details":"SUV grande = Tahoe","brands":"BFGoodrich, Michelin, Bridgestone",
                     "refs":[{"r":"265/65 R18","s":"confirmed"},{"r":"275/55 R20","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+275+55+r20"},{"t":"BFGoodrich","u":"https://www.bfgoodrich.cl/"},{"t":"Michelin","u":"https://www.michelin.cl/"}]}
                ]
            }
        },
        "chevrolet_montana": {
            "name": "Chevrolet Montana 1.2T — 2023-2026",
            "info": "1.2T Ecotec 3cil Turbo | Cadena",
            "crossNote": "Plataforma GEM. Motor comp. Onix 1.0T (mismo bloque 3cil turbo)",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30 Dexos1","details":"API SP | ~4.0L","brands":"Mobil, ACDelco, Castrol",
                     "refs":[{"r":"5W-30 Dexos1 Gen3","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+dexos1"},{"t":"Amazon","u":AZ+"ACDelco+Dexos1+5W-30"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite 1.2T","details":"Comp. Onix turbo","brands":"ACDelco, MANN",
                     "refs":[{"r":"55594651 OEM","s":"confirmed"},{"r":"MANN W 712/95","s":"confirmed"}],
                     "interval":"c/10k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+chevrolet+montana"},{"t":"Amazon","u":AZ+"oil+filter+Chevrolet+Montana"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel turbo","brands":"ACDelco, MANN",
                     "refs":[{"r":"Verificar OEM","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+chevrolet+montana"},{"t":"Amazon","u":AZ+"air+filter+Chevrolet+Montana+2023"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x3","details":"Iridium 1.2T","brands":"NGK, ACDelco",
                     "refs":[{"r":"Comp. Onix 1.0T (verificar)","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+chevrolet+montana"},{"t":"Amazon","u":AZ+"spark+plug+Chevrolet+Montana"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado","brands":"TRW, Bosch, ACDelco",
                     "refs":[{"r":"Verificar OEM","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+chevrolet+montana"},{"t":"Amazon","u":AZ+"brake+pads+Chevrolet+Montana+2023"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"NO cambio","brands":"-",
                     "refs":[{"r":"Cadena 1.2T","s":"confirmed"}],
                     "interval":"Tensores c/100k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+chevrolet+montana"},{"t":"Amazon","u":AZ+"timing+chain+Chevrolet+Montana"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"205/65 R16 / 215/55 R17","details":"Pickup compacta","brands":"Continental, Pirelli, Bridgestone",
                     "refs":[{"r":"205/65 R16","s":"confirmed"},{"r":"215/55 R17","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+205+65+r16"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Pirelli","u":"https://www.pirelli.com/"}]}
                ]
            }
        },
        "chevrolet_spin": {
            "name": "Chevrolet Spin 1.8 — 2014-2022",
            "info": "Ecotec 1.8L 4cil | Cadena",
            "crossNote": "Motor Ecotec 1.8 comp. Cobalt/Prisma 1.8. Plataforma GM Gamma II",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30","details":"API SN | ~4.0L","brands":"Mobil, ACDelco, Shell",
                     "refs":[{"r":"5W-30 API SN","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+sintetico"},{"t":"Amazon","u":AZ+"5W-30+synthetic"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite 1.8","details":"Ecotec","brands":"ACDelco, MANN, Wix",
                     "refs":[{"r":"MANN W 712/95","s":"confirmed"},{"r":"93313927 OEM","s":"confirmed"}],
                     "interval":"c/10k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+chevrolet+spin"},{"t":"Amazon","u":AZ+"MANN+W712%2F95"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel","brands":"ACDelco, MANN",
                     "refs":[{"r":"MANN C 2598 (verificar)","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+chevrolet+spin"},{"t":"Amazon","u":AZ+"air+filter+Chevrolet+Spin"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4","details":"Iridium","brands":"NGK, ACDelco, Denso",
                     "refs":[{"r":"NGK ILTR5A-13G (verificar)","s":"verify"}],
                     "interval":"c/30k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+chevrolet+spin"},{"t":"Amazon","u":AZ+"spark+plug+Chevrolet+Spin"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~256mm","brands":"TRW, Bosch, Cobreq",
                     "refs":[{"r":"N1432 (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+chevrolet+spin"},{"t":"Amazon","u":AZ+"brake+pads+Chevrolet+Spin"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"NO cambio","brands":"-",
                     "refs":[{"r":"Cadena Ecotec 1.8","s":"confirmed"}],
                     "interval":"Tensores c/100k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+chevrolet+spin"},{"t":"Amazon","u":AZ+"timing+chain+Chevrolet+Spin"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"195/55 R15 / 185/65 R15","details":"Minivan","brands":"Continental, Bridgestone, Pirelli",
                     "refs":[{"r":"195/55 R15","s":"confirmed"},{"r":"185/65 R15","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+195+55+r15"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Bridgestone","u":"https://www.bridgestone.cl/"}]}
                ]
            }
        },
        "chevrolet_prisma": {
            "name": "Chevrolet Prisma 1.4/1.8 — 2014-2020",
            "info": "Ecotec 1.4 SPE/4 / 1.8 | Cadena",
            "crossNote": "= Onix sedan 1ra gen. Motor comp. Cobalt/Spin 1.8",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30","details":"API SN | ~3.5-4.0L","brands":"Mobil, ACDelco, Shell",
                     "refs":[{"r":"5W-30 API SN","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+sintetico"},{"t":"Amazon","u":AZ+"5W-30+synthetic"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite","details":"= Spin/Cobalt","brands":"ACDelco, MANN",
                     "refs":[{"r":"MANN W 712/95","s":"confirmed"},{"r":"93313927 OEM","s":"confirmed"}],
                     "interval":"c/10k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+chevrolet+prisma"},{"t":"Amazon","u":AZ+"MANN+W712%2F95"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel","brands":"ACDelco, MANN",
                     "refs":[{"r":"MANN C 2598 (verificar)","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+chevrolet+prisma"},{"t":"Amazon","u":AZ+"air+filter+Chevrolet+Prisma"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4","details":"Iridium","brands":"NGK, ACDelco",
                     "refs":[{"r":"NGK ILTR5A-13G (verificar)","s":"verify"}],
                     "interval":"c/30k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+chevrolet+prisma"},{"t":"Amazon","u":AZ+"spark+plug+Chevrolet+Prisma"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado","brands":"TRW, Bosch, Cobreq",
                     "refs":[{"r":"N1432 (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+chevrolet+prisma"},{"t":"Amazon","u":AZ+"brake+pads+Chevrolet+Prisma"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"NO cambio","brands":"-",
                     "refs":[{"r":"Cadena Ecotec","s":"confirmed"}],
                     "interval":"Tensores c/100k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+chevrolet+prisma"},{"t":"Amazon","u":AZ+"timing+chain+Chevrolet+Prisma"},{"t":"ACDelco","u":"https://www.acdelco.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"185/65 R15 / 185/70 R14","details":"Sedan compacto","brands":"Continental, Bridgestone, Pirelli",
                     "refs":[{"r":"185/65 R15","s":"confirmed"},{"r":"185/70 R14","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+185+65+r15"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Bridgestone","u":"https://www.bridgestone.cl/"}]}
                ]
            }
        },
        "vw_virtus": {
            "name": "Volkswagen Virtus 1.6 MSI / 1.0 TSI — 2018-2026",
            "info": "EA211 1.6 MSI / 1.0 TSI 3cil | Cadena",
            "crossNote": "= Polo sedan. Motor EA211 comp. Polo, T-Cross, Nivus",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-40 VW 502.00","details":"API SN | ~3.6L","brands":"Castrol EDGE, Mobil, Liqui Moly",
                     "refs":[{"r":"5W-40 VW 502.00","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w40+vw+502"},{"t":"Amazon","u":AZ+"Castrol+EDGE+5W-40"},{"t":"Liqui Moly","u":"https://www.liqui-moly.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite EA211","details":"= Polo/T-Cross","brands":"MANN, Mahle, Bosch",
                     "refs":[{"r":"MANN W 712/94","s":"confirmed"},{"r":"04E 115 561 H OEM","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+volkswagen+virtus"},{"t":"Amazon","u":AZ+"MANN+W712%2F94"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel EA211","brands":"MANN, Mahle",
                     "refs":[{"r":"MANN C 27 009 (verificar)","s":"verify"},{"r":"04E 129 620 D OEM","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+volkswagen+virtus"},{"t":"Amazon","u":AZ+"air+filter+VW+Virtus"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Cabina","name":"Filtro cabina","details":"Carbon act.","brands":"MANN, Mahle, Bosch",
                     "refs":[{"r":"MANN CUK 2545 (verificar)","s":"verify"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+cabina+volkswagen+virtus"},{"t":"Amazon","u":AZ+"cabin+filter+VW+Polo+2018"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4 (1.6) / x3 (1.0T)","details":"Iridium","brands":"NGK, Bosch",
                     "refs":[{"r":"NGK LKAR7BI-9S (1.0T verificar)","s":"verify"},{"r":"Bosch FR6KI332S (1.6 verificar)","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+volkswagen+virtus"},{"t":"Amazon","u":AZ+"spark+plug+VW+Polo+EA211"},{"t":"NGK","u":"https://www.ngk.com/"}]},
                    {"cat":"Bobina","name":"Bobina encendido","details":"Individual x4/x3","brands":"Bosch, Beru",
                     "refs":[{"r":"04C 905 110 D (verificar)","s":"verify"}],
                     "links":[{"t":"MercadoLibre","u":ML+"bobina+encendido+volkswagen+virtus"},{"t":"Amazon","u":AZ+"ignition+coil+VW+Polo+EA211"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~256mm","brands":"TRW, Bosch, Brembo",
                     "refs":[{"r":"GDB2082 (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+volkswagen+virtus"},{"t":"Amazon","u":AZ+"brake+pads+VW+Virtus"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]},
                    {"cat":"Pastillas Tras.","name":"Pastillas traseras","details":"Tambor/Disco segun version","brands":"TRW, Bosch",
                     "refs":[{"r":"Verificar version","s":"verify"}],
                     "interval":"c/50-70k",
                     "links":[{"t":"MercadoLibre","u":ML+"freno+trasero+volkswagen+virtus"},{"t":"Amazon","u":AZ+"rear+brake+VW+Virtus"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"NO cambio EA211","brands":"-",
                     "refs":[{"r":"Cadena EA211","s":"confirmed"}],
                     "interval":"Tensores c/120k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+volkswagen+virtus"},{"t":"Amazon","u":AZ+"timing+chain+VW+EA211"},{"t":"Volkswagen","u":"https://www.vw.cl/"}]}
                ],
                "Transmision": [
                    {"cat":"Aceite Caja","name":"ATF / Manual","details":"Automatica 6AT o Manual 5vel","brands":"VW, Mobil",
                     "refs":[{"r":"G 055 025 A2 ATF (verificar)","s":"verify"},{"r":"75W-90 GL-4 manual","s":"confirmed"}],
                     "interval":"c/60k",
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+caja+volkswagen+virtus"},{"t":"Amazon","u":AZ+"VW+ATF+G055025"},{"t":"Motul","u":"https://www.motul.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"185/60 R15 / 195/55 R16","details":"","brands":"Continental, Pirelli, Bridgestone",
                     "refs":[{"r":"185/60 R15","s":"confirmed"},{"r":"195/55 R16","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+185+60+r15"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Pirelli","u":"https://www.pirelli.com/"}]}
                ]
            }
        }
    }

    for vid, vdata in vehicles.items():
        c.execute("INSERT OR IGNORE INTO vehicles VALUES (?,?,?,?)",
                  (vid, vdata["name"], vdata["info"], vdata["crossNote"]))
        order = 0
        for cat_name, parts in vdata["categories"].items():
            order += 1
            c.execute("INSERT INTO categories (vehicle_id, name, sort_order) VALUES (?,?,?)",
                      (vid, cat_name, order))
            cat_id = c.lastrowid
            for p in parts:
                c.execute("INSERT INTO parts (category_id, cat_label, name, details, brands, interval_info) VALUES (?,?,?,?,?,?)",
                          (cat_id, p.get("cat",""), p["name"], p.get("details",""), p.get("brands",""), p.get("interval",None)))
                pid = c.lastrowid
                for r in p.get("refs",[]):
                    c.execute("INSERT INTO part_refs (part_id, reference, status) VALUES (?,?,?)",
                              (pid, r["r"], r["s"]))
                for l in p.get("links",[]):
                    c.execute("INSERT INTO part_links (part_id, label, url) VALUES (?,?,?)",
                              (pid, l["t"], l["u"]))

    conn.commit()
    total = c.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
    parts_count = c.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print(f"Bloque 13 insertado OK")
    print(f"Vehiculos totales: {total} | Componentes totales: {parts_count}")

if __name__ == "__main__":
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    ins(conn)
    conn.close()
