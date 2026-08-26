"""
Inserta un lote de vehiculos con componentes OEM verificados en db.sqlite.
Primer lote: 5 vehiculos populares para validar en la web.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')

LOTE = [
    {"id": "corolla-2020", "name": "Toyota Corolla 1.8 — 2020", "info": "1.8L 2ZR-FE / 2.0L M20A-FKS | Cadena", "cross_note": "Comp: RAV4, Prius, C-HR, Auris (mismo motor 2ZR/M20A)", "categories": [{"name": "Filtros y Lubricacion", "parts": [{"cat_label": "Filtro Aceite", "name": "Filtro de Aceite", "details": "Spin-on | Cambio: 10,000 km", "brands": "Toyota Genuine, MANN W 68/3, Wix, Fram", "refs": [("90915-YZZF2", "confirmed"), ("90915-YZZN1", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=90915-YZZF2"), ("AutoZone", "https://www.autozone.com/p/toyota-engine-oil-filter-90915-yzzf2/128800")]}, {"cat_label": "Filtro Aire", "name": "Filtro de Aire Motor", "details": "Panel | Cambio: 20,000 km", "brands": "Toyota Genuine, MANN C 26 011, Wix", "refs": [("17801-21060", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=17801-21060+toyota"), ("OEMParts", "https://toyota.oempartsonline.com/oem-parts/toyota-air-filter-1780121060")]}, {"cat_label": "Bujias", "name": "Bujias de Encendido", "details": "Iridium | Cantidad: 4 | Cambio: 60,000 km", "brands": "Denso, NGK", "refs": [("90919-01253 (Denso FK16HR-A8)", "confirmed")], "links": [("Amazon", "https://www.amazon.com/s?k=90919-01253+toyota+corolla")]}]}]},
    {"id": "cx5-2022", "name": "Mazda CX-5 2.5 — 2022", "info": "2.5L PY-VPS Skyactiv-G | Cadena", "cross_note": "Comp: Mazda 3, 6, CX-30, CX-3 (mismo filtro Skyactiv)", "categories": [{"name": "Filtros y Lubricacion", "parts": [{"cat_label": "Filtro Aceite", "name": "Filtro de Aceite", "details": "Cartucho | Cambio: 12,000 km", "brands": "Mazda Genuine, MANN HU 6007 z", "refs": [("PE01-14-302A", "confirmed"), ("1WPE-14-302 (supersede)", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=PE01-14-302A"), ("MazdaShop", "https://mazdashopusa.com/products/mazda-original-engine-oil-filter-gasket-replacement-mazda-cx-5-2013-2026")]}, {"cat_label": "Filtro Aire", "name": "Filtro de Aire Motor", "details": "Panel | Cambio: 30,000 km", "brands": "Mazda Genuine", "refs": [("PE07-13-3A0A", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=PE07-13-3A0A"), ("MazdaSwag", "https://www.mazdaswag.com/oem-parts/mazda-air-filter-pe07133a0a")]}, {"cat_label": "Bujias", "name": "Bujias de Encendido", "details": "Iridium | Cantidad: 4 | Cambio: 75,000 km", "brands": "Mazda Genuine, NGK", "refs": [("PE5R-18-110", "confirmed"), ("PE5S-18-110", "confirmed")], "links": [("Manual Mazda", "https://owners-manual.mazda.com/gen/es/cx-5/cx-5_8fy6sp17e/contents/10020108.html")]}]}]},
    {"id": "tucson-2022", "name": "Hyundai Tucson 2.0 — 2022", "info": "2.0L G4NA / 1.6T G4FP | Cadena", "cross_note": "Comp: Kia Sportage, Elantra, i30 (filtro 26300-35505 universal Hyundai/Kia)", "categories": [{"name": "Filtros y Lubricacion", "parts": [{"cat_label": "Filtro Aceite", "name": "Filtro de Aceite", "details": "Spin-on | Cambio: 10,000 km", "brands": "Hyundai/Kia Genuine, MANN W 811/80", "refs": [("26300-35505", "confirmed"), ("26300-35504 (version anterior)", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=26300-35505"), ("AutoZone", "https://www.autozone.com/p/hyundai-engine-oil-filter-26300-35505/127897")]}, {"cat_label": "Filtro Aire", "name": "Filtro de Aire Motor", "details": "Panel | Cambio: 20,000 km", "brands": "Hyundai Genuine", "refs": [("28113-D3300", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=28113-D3300")]}, {"cat_label": "Filtro Cabina", "name": "Filtro de Habitaculo", "details": "Carbon activado | Cambio: 15,000 km", "brands": "Hyundai Genuine", "refs": [("97133-D1000", "confirmed")], "links": [("Amazon", "https://www.amazon.com/s?k=97133-D1000")]}]}]},
    {"id": "crv-2022", "name": "Honda CR-V 1.5T — 2022", "info": "1.5L Turbo L15B | Cadena", "cross_note": "Comp: Civic 1.5T, Accord (filtro 15400-PLM-A02 universal Honda)", "categories": [{"name": "Filtros y Lubricacion", "parts": [{"cat_label": "Filtro Aceite", "name": "Filtro de Aceite", "details": "Spin-on | Cambio: 12,000 km", "brands": "Honda Genuine, MANN W 610/6, Wix", "refs": [("15400-PLM-A02", "confirmed"), ("15400-RTA-003", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=15400-PLM-A02"), ("Honda Parts", "https://honda.oempartsonline.com/oem-parts/honda-oil-filter-15400plma02")]}, {"cat_label": "Filtro Aire", "name": "Filtro de Aire Motor", "details": "Panel | Cambio: 20,000 km | Solo 1.5T", "brands": "Honda Genuine", "refs": [("17220-5AA-A00", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=17220-5AA-A00"), ("Honda Parts", "https://honda.oempartsonline.com/oem-parts/honda-air-filter-172205aaa00")]}, {"cat_label": "Filtro Cabina", "name": "Filtro de Habitaculo", "details": "Cambio: 15,000 km", "brands": "Honda Genuine", "refs": [("80292-TF0-G01", "confirmed")], "links": [("Amazon", "https://www.amazon.com/s?k=80292-TF0-G01")]}]}]},
    {"id": "golf-2020", "name": "Volkswagen Golf 1.4T — 2020", "info": "1.4L TSI EA211 | Cadena", "cross_note": "Comp: Jetta, Polo, Tiguan, Audi A3, Q3, Seat Leon, Skoda Octavia (grupo VAG EA211)", "categories": [{"name": "Filtros y Lubricacion", "parts": [{"cat_label": "Filtro Aceite", "name": "Filtro de Aceite", "details": "Cartucho | Cambio: 15,000 km", "brands": "VW Genuine, MANN HU 6002 z", "refs": [("04E115561H", "confirmed"), ("04E115561T (supersede)", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=04E115561H"), ("VW Parts", "https://vw.oempartsonline.com/oem-parts/volkswagen-oil-filter-4e115561t")]}, {"cat_label": "Filtro Aire", "name": "Filtro de Aire Motor", "details": "Panel | Cambio: 30,000 km", "brands": "VW Genuine, MANN", "refs": [("04E129620", "confirmed")], "links": [("Amazon OEM", "https://www.amazon.com/s?k=04E129620"), ("VW Parts", "https://vw.oempartsonline.com/oem-parts/volkswagen-air-filter-4e129620")]}, {"cat_label": "Bujias", "name": "Bujias de Encendido", "details": "Iridium/Double Platinum | Cantidad: 4 | Cambio: 60,000 km", "brands": "Bosch (OE supplier VW)", "refs": [("04E905612C", "confirmed")], "links": [("Amazon", "https://www.amazon.com/s?k=04E905612C"), ("UroTuning", "https://www.urotuning.com/products/spark-plug-vw-audi-mk6-jetta-hybrid-a3-e-tron-04e905612c-bos")]}]}]},
]

def insertar_lote(conn):
    for veh in LOTE:
        exists = conn.execute("SELECT id FROM vehicles WHERE id = ?", (veh["id"],)).fetchone()
        if exists:
            print("  SKIP %s (ya existe)" % veh["id"])
            continue
        conn.execute("INSERT INTO vehicles (id, name, info, cross_note) VALUES (?, ?, ?, ?)",
                     (veh["id"], veh["name"], veh["info"], veh["cross_note"]))
        for cat in veh["categories"]:
            conn.execute("INSERT INTO categories (vehicle_id, name, sort_order) VALUES (?, ?, ?)",
                         (veh["id"], cat["name"], 1))
            cat_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            for part in cat["parts"]:
                conn.execute("INSERT INTO parts (category_id, cat_label, name, details, brands, interval_info) VALUES (?, ?, ?, ?, ?, ?)",
                    (cat_id, part["cat_label"], part["name"], part["details"], part["brands"], None))
                part_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
                for ref, status in part.get("refs", []):
                    conn.execute("INSERT INTO part_refs (part_id, reference, status) VALUES (?, ?, ?)", (part_id, ref, status))
                for label, url in part.get("links", []):
                    conn.execute("INSERT INTO part_links (part_id, label, url) VALUES (?, ?, ?)", (part_id, label, url))
        print("  OK: %s" % veh["name"])
    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    print("Insertando lote 1 (5 vehiculos OEM verificados)...")
    insertar_lote(conn)
    total_v = conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
    total_p = conn.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    print("\nTotal vehiculos en BD: %d" % total_v)
    print("Total parts en BD: %d" % total_p)
    conn.close()
    print("\n[OK] Lote insertado. Ejecuta: python export_db.py")
