"""
RepuestosPro - Bloque 14: VW Jetta, Bora, Tiguan, T-Cross, Nivus, Taos, Vento + Peugeot 3008, 5008, Rifter
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
ML = "https://listado.mercadolibre.cl/"
AZ = "https://www.amazon.com/s?k="

def ins(conn):
    c = conn.cursor()

    vehicles = {
        "vw_jetta": {
            "name": "Volkswagen Jetta 1.4T/2.0 — 2011-2026",
            "info": "EA211 1.4 TSI / EA888 2.0 TSI | Cadena",
            "crossNote": "Comp: Golf, Passat (EA888). 1.4T = Tiguan, Taos",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-40 VW 502.00","details":"API SN | 4.0-4.6L","brands":"Castrol EDGE, Mobil, Liqui Moly",
                     "refs":[{"r":"5W-40 VW 502.00","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w40+vw+502"},{"t":"Amazon","u":AZ+"Castrol+EDGE+5W-40"},{"t":"Liqui Moly","u":"https://www.liqui-moly.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite EA211/EA888","details":"Segun motor","brands":"MANN, Mahle, Bosch",
                     "refs":[{"r":"MANN W 712/94 (1.4T)","s":"confirmed"},{"r":"MANN HU 7012 z (2.0T)","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+volkswagen+jetta"},{"t":"Amazon","u":AZ+"oil+filter+VW+Jetta"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel","brands":"MANN, Mahle",
                     "refs":[{"r":"MANN C 27 009 (1.4T verificar)","s":"verify"},{"r":"MANN C 35 154 (2.0T verificar)","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+volkswagen+jetta"},{"t":"Amazon","u":AZ+"air+filter+VW+Jetta"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4","details":"Iridium TSI","brands":"NGK, Bosch",
                     "refs":[{"r":"NGK PZFR6R (2.0T verificar)","s":"verify"},{"r":"Bosch FR5KPP332S (1.4T verificar)","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+volkswagen+jetta"},{"t":"Amazon","u":AZ+"spark+plug+VW+Jetta+TSI"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~288-312mm","brands":"TRW, Brembo, ATE",
                     "refs":[{"r":"GDB1762 (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+volkswagen+jetta"},{"t":"Amazon","u":AZ+"brake+pads+VW+Jetta"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"TSI cadena","brands":"-",
                     "refs":[{"r":"Cadena EA211/EA888","s":"confirmed"}],
                     "interval":"Tensores c/100-150k",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+volkswagen+jetta"},{"t":"Amazon","u":AZ+"timing+chain+VW+Jetta+TSI"},{"t":"VW","u":"https://www.vw.cl/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"205/55 R16 / 225/45 R17","details":"","brands":"Continental, Michelin, Pirelli",
                     "refs":[{"r":"205/55 R16","s":"confirmed"},{"r":"225/45 R17","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+205+55+r16"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Michelin","u":"https://www.michelin.cl/"}]}
                ]
            }
        },
        "vw_bora": {
            "name": "Volkswagen Bora 2.0/1.8T/2.5 — 2006-2015",
            "info": "2.0 8v / 1.8T / 2.5 5cil | Cadena/Correa segun motor",
            "crossNote": "= Jetta A5/A6. 2.5L 5cil comp. Golf, Beetle",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-40 VW 502.00","details":"API SN | 4.0-5.5L","brands":"Castrol, Mobil, Liqui Moly",
                     "refs":[{"r":"5W-40 VW 502.00","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w40+vw+502"},{"t":"Amazon","u":AZ+"5W-40+VW+502"},{"t":"Liqui Moly","u":"https://www.liqui-moly.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite","details":"Segun motor","brands":"MANN, Mahle, Bosch",
                     "refs":[{"r":"MANN W 719/30 (2.0/2.5)","s":"confirmed"},{"r":"MANN HU 726/2x (1.8T)","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+volkswagen+bora"},{"t":"Amazon","u":AZ+"oil+filter+VW+Bora"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4/x5","details":"Segun motor","brands":"NGK, Bosch",
                     "refs":[{"r":"Bosch FR7HPP332 (2.0 verificar)","s":"verify"},{"r":"NGK PFR7S8EG (1.8T verificar)","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+volkswagen+bora"},{"t":"Amazon","u":AZ+"spark+plug+VW+Bora"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~280-288mm","brands":"TRW, ATE, Brembo",
                     "refs":[{"r":"GDB1550 (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+volkswagen+bora"},{"t":"Amazon","u":AZ+"brake+pads+VW+Bora"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena/Correa","name":"Cadena (2.0/2.5) o Correa (1.8T)","details":"1.8T: correa c/90k","brands":"Gates, Continental",
                     "refs":[{"r":"Cadena 2.0/2.5","s":"confirmed"},{"r":"Correa 1.8T c/90k","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"distribucion+volkswagen+bora"},{"t":"Amazon","u":AZ+"timing+belt+VW+1.8T"},{"t":"Gates","u":"https://www.gates.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"195/65 R15 / 205/55 R16","details":"","brands":"Continental, Pirelli, Bridgestone",
                     "refs":[{"r":"195/65 R15","s":"confirmed"},{"r":"205/55 R16","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+205+55+r16"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Pirelli","u":"https://www.pirelli.com/"}]}
                ]
            }
        },
        "vw_tiguan": {
            "name": "Volkswagen Tiguan 1.4T/2.0T — 2014-2026",
            "info": "EA211 1.4 TSI / EA888 2.0 TSI | Cadena",
            "crossNote": "Motor comp. Jetta, Golf, Taos (EA211/EA888)",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-40 VW 504.00","details":"API SN | 4.0-5.7L","brands":"Castrol EDGE, Liqui Moly, Mobil",
                     "refs":[{"r":"5W-40 VW 504.00/502.00","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w40+vw+504"},{"t":"Amazon","u":AZ+"Castrol+EDGE+5W-40+VW"},{"t":"Liqui Moly","u":"https://www.liqui-moly.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite","details":"Segun motor","brands":"MANN, Mahle",
                     "refs":[{"r":"MANN W 712/94 (1.4T)","s":"confirmed"},{"r":"MANN HU 7012 z (2.0T)","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+volkswagen+tiguan"},{"t":"Amazon","u":AZ+"oil+filter+VW+Tiguan"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel TSI","brands":"MANN, Mahle",
                     "refs":[{"r":"Verificar modelo","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+volkswagen+tiguan"},{"t":"Amazon","u":AZ+"air+filter+VW+Tiguan"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4","details":"Iridium TSI","brands":"NGK, Bosch",
                     "refs":[{"r":"Verificar segun motor","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+volkswagen+tiguan"},{"t":"Amazon","u":AZ+"spark+plug+VW+Tiguan+TSI"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~312mm","brands":"TRW, Brembo, ATE",
                     "refs":[{"r":"GDB1841 (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+volkswagen+tiguan"},{"t":"Amazon","u":AZ+"brake+pads+VW+Tiguan"},{"t":"Brembo","u":"https://www.brembo.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"TSI","brands":"-",
                     "refs":[{"r":"Cadena EA211/EA888","s":"confirmed"}],
                     "interval":"Tensores c/100-150k",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+volkswagen+tiguan"},{"t":"Amazon","u":AZ+"timing+chain+VW+Tiguan"},{"t":"VW","u":"https://www.vw.cl/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"215/65 R17 / 235/55 R18","details":"SUV","brands":"Continental, Michelin, Pirelli",
                     "refs":[{"r":"215/65 R17","s":"confirmed"},{"r":"235/55 R18","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+215+65+r17"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Michelin","u":"https://www.michelin.cl/"}]}
                ]
            }
        },
        "vw_tcross": {
            "name": "Volkswagen T-Cross 1.0T/1.6 — 2019-2026",
            "info": "EA211 1.0 TSI 3cil / 1.6 MSI | Cadena",
            "crossNote": "= Nivus, Polo (plataforma MQB-A0). Motor comp. Virtus",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-40 VW 502.00","details":"API SN | ~3.6L","brands":"Castrol EDGE, Mobil, Liqui Moly",
                     "refs":[{"r":"5W-40 VW 502.00","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w40+vw+502"},{"t":"Amazon","u":AZ+"Castrol+EDGE+5W-40"},{"t":"Liqui Moly","u":"https://www.liqui-moly.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite EA211","details":"= Polo/Virtus","brands":"MANN, Mahle",
                     "refs":[{"r":"MANN W 712/94","s":"confirmed"},{"r":"04E 115 561 H OEM","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+volkswagen+t-cross"},{"t":"Amazon","u":AZ+"oil+filter+VW+T-Cross"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x3 (1.0T) / x4 (1.6)","details":"Iridium","brands":"NGK, Bosch",
                     "refs":[{"r":"Comp. Virtus/Polo","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+volkswagen+t-cross"},{"t":"Amazon","u":AZ+"spark+plug+VW+T-Cross"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~256mm","brands":"TRW, Bosch",
                     "refs":[{"r":"Comp. Polo/Virtus","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+volkswagen+t-cross"},{"t":"Amazon","u":AZ+"brake+pads+VW+T-Cross"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"EA211","brands":"-",
                     "refs":[{"r":"Cadena EA211","s":"confirmed"}],
                     "interval":"Tensores c/120k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+volkswagen+t-cross"},{"t":"Amazon","u":AZ+"timing+chain+VW+EA211"},{"t":"VW","u":"https://www.vw.cl/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"205/60 R16 / 215/50 R18","details":"SUV compacto","brands":"Continental, Pirelli, Bridgestone",
                     "refs":[{"r":"205/60 R16","s":"confirmed"},{"r":"215/50 R18","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+205+60+r16"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Pirelli","u":"https://www.pirelli.com/"}]}
                ]
            }
        },
        "vw_nivus": {
            "name": "Volkswagen Nivus 1.0 TSI — 2021-2026",
            "info": "EA211 1.0 TSI 3cil 116hp | Cadena",
            "crossNote": "= T-Cross coupe. Plataforma MQB-A0. Motor = Polo/Virtus 1.0T",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-40 VW 502.00","details":"API SN | ~3.6L","brands":"Castrol EDGE, Liqui Moly",
                     "refs":[{"r":"5W-40 VW 502.00","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w40+vw+502"},{"t":"Amazon","u":AZ+"Castrol+EDGE+5W-40"},{"t":"Liqui Moly","u":"https://www.liqui-moly.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite = T-Cross","details":"EA211 1.0T","brands":"MANN, Mahle",
                     "refs":[{"r":"MANN W 712/94","s":"confirmed"},{"r":"04E 115 561 H OEM","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+volkswagen+nivus"},{"t":"Amazon","u":AZ+"MANN+W712%2F94"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x3","details":"Iridium 1.0T","brands":"NGK, Bosch",
                     "refs":[{"r":"Comp. T-Cross/Polo 1.0T","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+volkswagen+nivus"},{"t":"Amazon","u":AZ+"spark+plug+VW+Nivus"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"= T-Cross","brands":"TRW, Bosch",
                     "refs":[{"r":"Comp. T-Cross","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+volkswagen+nivus"},{"t":"Amazon","u":AZ+"brake+pads+VW+Nivus"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"EA211 1.0T","brands":"-",
                     "refs":[{"r":"Cadena EA211","s":"confirmed"}],
                     "interval":"Tensores c/120k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+volkswagen+nivus"},{"t":"Amazon","u":AZ+"timing+chain+VW+EA211"},{"t":"VW","u":"https://www.vw.cl/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"195/55 R16 / 205/50 R17","details":"","brands":"Continental, Pirelli, Bridgestone",
                     "refs":[{"r":"195/55 R16","s":"confirmed"},{"r":"205/50 R17","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+205+50+r17"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Pirelli","u":"https://www.pirelli.com/"}]}
                ]
            }
        },
        "vw_taos": {
            "name": "Volkswagen Taos 1.4 TSI — 2021-2026",
            "info": "EA211 1.4 TSI 150hp | Cadena",
            "crossNote": "Plataforma MQB-A1. Motor = Jetta/Tiguan 1.4T",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-40 VW 508.00","details":"API SP | ~4.0L","brands":"Castrol EDGE, Liqui Moly, Mobil",
                     "refs":[{"r":"5W-40 VW 508.00/502.00","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w40+vw+508"},{"t":"Amazon","u":AZ+"Castrol+EDGE+5W-40+VW"},{"t":"Liqui Moly","u":"https://www.liqui-moly.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite 1.4T","details":"= Jetta/Tiguan 1.4","brands":"MANN, Mahle",
                     "refs":[{"r":"MANN W 712/94","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+volkswagen+taos"},{"t":"Amazon","u":AZ+"oil+filter+VW+Taos"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4","details":"Iridium 1.4T","brands":"NGK, Bosch",
                     "refs":[{"r":"Comp. Jetta 1.4T","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+volkswagen+taos"},{"t":"Amazon","u":AZ+"spark+plug+VW+Taos"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~312mm","brands":"TRW, Brembo, ATE",
                     "refs":[{"r":"Comp. Tiguan (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+volkswagen+taos"},{"t":"Amazon","u":AZ+"brake+pads+VW+Taos"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"EA211 1.4T","brands":"-",
                     "refs":[{"r":"Cadena EA211","s":"confirmed"}],
                     "interval":"Tensores c/120k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+volkswagen+taos"},{"t":"Amazon","u":AZ+"timing+chain+VW+EA211+1.4"},{"t":"VW","u":"https://www.vw.cl/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"215/55 R18 / 215/60 R17","details":"SUV compacto","brands":"Continental, Bridgestone, Pirelli",
                     "refs":[{"r":"215/55 R18","s":"confirmed"},{"r":"215/60 R17","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+215+55+r18"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Bridgestone","u":"https://www.bridgestone.cl/"}]}
                ]
            }
        },
        "vw_vento": {
            "name": "Volkswagen Vento 1.6/2.0 — 2014-2022",
            "info": "EA211 1.6 MSI / EA111 2.0 8v | Cadena",
            "crossNote": "= Polo sedan (mercado India). Motor 1.6 = Polo/Virtus",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-40 VW 502.00","details":"API SN | ~3.6-4.0L","brands":"Castrol, Mobil, Liqui Moly",
                     "refs":[{"r":"5W-40 VW 502.00","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w40+vw+502"},{"t":"Amazon","u":AZ+"Castrol+EDGE+5W-40"},{"t":"Liqui Moly","u":"https://www.liqui-moly.com/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite","details":"EA211 1.6","brands":"MANN, Mahle",
                     "refs":[{"r":"MANN W 712/94","s":"confirmed"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+volkswagen+vento"},{"t":"Amazon","u":AZ+"oil+filter+VW+Vento"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4","details":"","brands":"NGK, Bosch",
                     "refs":[{"r":"Comp. Polo 1.6","s":"verify"}],
                     "interval":"c/30k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+volkswagen+vento"},{"t":"Amazon","u":AZ+"spark+plug+VW+Vento"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado","brands":"TRW, Bosch",
                     "refs":[{"r":"Comp. Polo (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+volkswagen+vento"},{"t":"Amazon","u":AZ+"brake+pads+VW+Vento"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"EA211","brands":"-",
                     "refs":[{"r":"Cadena EA211","s":"confirmed"}],
                     "interval":"Tensores c/120k+",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+volkswagen+vento"},{"t":"Amazon","u":AZ+"timing+chain+VW+EA211"},{"t":"VW","u":"https://www.vw.cl/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"185/60 R15 / 195/55 R16","details":"","brands":"Continental, Pirelli, Bridgestone",
                     "refs":[{"r":"185/60 R15","s":"confirmed"},{"r":"195/55 R16","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+195+55+r16"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"},{"t":"Pirelli","u":"https://www.pirelli.com/"}]}
                ]
            }
        },
        "peugeot_3008": {
            "name": "Peugeot 3008 1.6T/2.0D — 2017-2026",
            "info": "PureTech 1.6T / BlueHDi 2.0D | Cadena",
            "crossNote": "Plataforma EMP2. Motor PureTech comp. 308, 508, Citroen C4/C5",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30 PSA B71 2290","details":"ACEA C2 | 4.0-5.0L","brands":"Total Quartz Ineo, Motul",
                     "refs":[{"r":"5W-30 PSA B71 2290","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+peugeot+total+ineo"},{"t":"Amazon","u":AZ+"Total+Quartz+Ineo+5W-30"},{"t":"Total","u":"https://www.totalenergies.cl/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite PureTech","details":"1.6T","brands":"MANN, Purflux, Bosch",
                     "refs":[{"r":"MANN HU 7033 z (verificar)","s":"verify"},{"r":"1109.CK OEM (verificar)","s":"verify"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+peugeot+3008"},{"t":"Amazon","u":AZ+"oil+filter+Peugeot+3008"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Aire","name":"Filtro aire","details":"Panel","brands":"MANN, Purflux",
                     "refs":[{"r":"Verificar OEM","s":"verify"}],
                     "interval":"c/15-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aire+peugeot+3008"},{"t":"Amazon","u":AZ+"air+filter+Peugeot+3008"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4 (1.6T)","details":"Iridium PureTech","brands":"NGK, Bosch",
                     "refs":[{"r":"Comp. 308 1.6T (verificar)","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+peugeot+3008"},{"t":"Amazon","u":AZ+"spark+plug+Peugeot+3008"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~330mm","brands":"TRW, Brembo, Bosch",
                     "refs":[{"r":"Verificar OEM","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+peugeot+3008"},{"t":"Amazon","u":AZ+"brake+pads+Peugeot+3008"},{"t":"Brembo","u":"https://www.brembo.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena distribucion","details":"PureTech 1.6T cadena","brands":"-",
                     "refs":[{"r":"Cadena PureTech","s":"confirmed"}],
                     "interval":"Tensores c/100k",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+peugeot+3008"},{"t":"Amazon","u":AZ+"timing+chain+Peugeot+PureTech"},{"t":"Peugeot","u":"https://www.peugeot.cl/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"225/55 R18 / 235/55 R19","details":"SUV","brands":"Michelin, Continental, Pirelli",
                     "refs":[{"r":"225/55 R18","s":"confirmed"},{"r":"235/55 R19","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+225+55+r18"},{"t":"Michelin","u":"https://www.michelin.cl/"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"}]}
                ]
            }
        },
        "peugeot_5008": {
            "name": "Peugeot 5008 1.6T/2.0D — 2017-2026",
            "info": "PureTech 1.6T / BlueHDi 2.0D | Cadena",
            "crossNote": "= 3008 extendido (7 plazas). Mismo motor y plataforma EMP2",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30 = 3008","details":"PSA B71 2290 | ~4.0-5.0L","brands":"Total Quartz Ineo, Motul",
                     "refs":[{"r":"5W-30 PSA B71 2290","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+peugeot+total+ineo"},{"t":"Amazon","u":AZ+"Total+Quartz+Ineo+5W-30"},{"t":"Total","u":"https://www.totalenergies.cl/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite = 3008","details":"PureTech","brands":"MANN, Purflux",
                     "refs":[{"r":"Comp. 3008 PureTech","s":"verify"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+peugeot+5008"},{"t":"Amazon","u":AZ+"oil+filter+Peugeot+5008"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias","name":"Bujias x4 = 3008","details":"PureTech","brands":"NGK, Bosch",
                     "refs":[{"r":"Comp. 3008","s":"verify"}],
                     "interval":"c/30-60k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+peugeot+5008"},{"t":"Amazon","u":AZ+"spark+plug+Peugeot+5008"},{"t":"NGK","u":"https://www.ngk.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"= 3008","brands":"TRW, Brembo",
                     "refs":[{"r":"Comp. 3008","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+peugeot+5008"},{"t":"Amazon","u":AZ+"brake+pads+Peugeot+5008"},{"t":"Brembo","u":"https://www.brembo.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Cadena","name":"Cadena = 3008","details":"PureTech","brands":"-",
                     "refs":[{"r":"Cadena PureTech","s":"confirmed"}],
                     "interval":"Tensores c/100k",
                     "links":[{"t":"MercadoLibre","u":ML+"cadena+distribucion+peugeot+5008"},{"t":"Amazon","u":AZ+"timing+chain+Peugeot+PureTech"},{"t":"Peugeot","u":"https://www.peugeot.cl/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"225/55 R18 / 235/55 R19","details":"= 3008","brands":"Michelin, Continental, Pirelli",
                     "refs":[{"r":"225/55 R18","s":"confirmed"},{"r":"235/55 R19","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+235+55+r19"},{"t":"Michelin","u":"https://www.michelin.cl/"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"}]}
                ]
            }
        },
        "peugeot_rifter": {
            "name": "Peugeot Rifter 1.5D/1.2T — 2019-2026",
            "info": "BlueHDi 1.5D / PureTech 1.2T | Correa(D)/Cadena(T)",
            "crossNote": "= Citroen Berlingo, Opel Combo. Plataforma EMP2",
            "categories": {
                "Motor y Lubricacion": [
                    {"cat":"Aceite","name":"Aceite 5W-30 PSA B71 2290","details":"ACEA C2 | ~3.8-5.0L","brands":"Total Quartz Ineo, Motul",
                     "refs":[{"r":"5W-30 PSA B71 2290","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"aceite+5w30+peugeot+total+ineo"},{"t":"Amazon","u":AZ+"Total+Quartz+Ineo+5W-30"},{"t":"Total","u":"https://www.totalenergies.cl/"}]},
                    {"cat":"Filtro Aceite","name":"Filtro aceite","details":"1.5D/1.2T","brands":"MANN, Purflux",
                     "refs":[{"r":"Verificar segun motor","s":"verify"}],
                     "interval":"c/10-15k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+aceite+peugeot+rifter"},{"t":"Amazon","u":AZ+"oil+filter+Peugeot+Rifter"},{"t":"MANN","u":"https://www.mann-filter.com/"}]},
                    {"cat":"Filtro Combustible","name":"Filtro petroleo (1.5D)","details":"Con separador agua","brands":"MANN, Purflux, Bosch",
                     "refs":[{"r":"Verificar OEM","s":"verify"}],
                     "interval":"c/10-20k",
                     "links":[{"t":"MercadoLibre","u":ML+"filtro+combustible+peugeot+rifter"},{"t":"Amazon","u":AZ+"fuel+filter+Peugeot+Rifter"},{"t":"MANN","u":"https://www.mann-filter.com/"}]}
                ],
                "Encendido": [
                    {"cat":"Bujias/Precal","name":"Bujias precal (diesel) / Bujias (gasolina)","details":"Segun motor","brands":"Bosch, NGK",
                     "refs":[{"r":"Verificar segun motor","s":"verify"}],
                     "interval":"c/60-100k",
                     "links":[{"t":"MercadoLibre","u":ML+"bujia+peugeot+rifter"},{"t":"Amazon","u":AZ+"glow+plug+Peugeot+Rifter"},{"t":"Bosch","u":"https://www.boschautoparts.com/"}]}
                ],
                "Frenos": [
                    {"cat":"Pastillas Del.","name":"Pastillas delanteras","details":"Disco ventilado ~283mm","brands":"TRW, Bosch, Brembo",
                     "refs":[{"r":"Comp. Berlingo (verificar)","s":"verify"}],
                     "interval":"c/30-50k",
                     "links":[{"t":"MercadoLibre","u":ML+"pastillas+freno+peugeot+rifter"},{"t":"Amazon","u":AZ+"brake+pads+Peugeot+Rifter"},{"t":"TRW","u":"https://www.trwaftermarket.com/"}]}
                ],
                "Distribucion": [
                    {"cat":"Correa/Cadena","name":"Correa (1.5D) / Cadena (1.2T)","details":"1.5D: correa c/150k o 10 anos","brands":"Gates, Dayco",
                     "refs":[{"r":"Correa 1.5D c/150k","s":"confirmed"},{"r":"Cadena 1.2T","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"kit+distribucion+peugeot+rifter"},{"t":"Amazon","u":AZ+"timing+belt+Peugeot+1.5+BlueHDi"},{"t":"Gates","u":"https://www.gates.com/"}]}
                ],
                "Neumaticos": [
                    {"cat":"Neumatico","name":"205/60 R16 / 205/55 R17","details":"Furgoneta","brands":"Michelin, Continental, Bridgestone",
                     "refs":[{"r":"205/60 R16","s":"confirmed"},{"r":"205/55 R17","s":"confirmed"}],
                     "links":[{"t":"MercadoLibre","u":ML+"neumatico+205+60+r16"},{"t":"Michelin","u":"https://www.michelin.cl/"},{"t":"Continental","u":"https://www.continental-neumaticos.cl/"}]}
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
    print(f"Bloque 14 insertado OK")
    print(f"Vehiculos totales: {total} | Componentes totales: {parts_count}")

if __name__ == "__main__":
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    ins(conn)
    conn.close()
