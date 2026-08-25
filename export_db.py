"""
RepuestosPro - Exportar SQLite a db.json
Ejecutar despues de modificar la BD para actualizar el frontend.
El archivo db.json es lo que se sube a git y el HTML consume.
"""
import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.json')

def export():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    vehicles = c.execute("SELECT * FROM vehicles ORDER BY id").fetchall()
    data = {}
    for v in vehicles:
        vid = v['id']
        cats = c.execute("SELECT * FROM categories WHERE vehicle_id=? ORDER BY sort_order, name", (vid,)).fetchall()
        categories = {}
        for cat in cats:
            parts = c.execute("SELECT * FROM parts WHERE category_id=? ORDER BY id", (cat['id'],)).fetchall()
            parts_list = []
            for p in parts:
                refs = c.execute("SELECT reference, status FROM part_refs WHERE part_id=? ORDER BY id", (p['id'],)).fetchall()
                links = c.execute("SELECT label, url FROM part_links WHERE part_id=? ORDER BY id", (p['id'],)).fetchall()
                part_obj = {"cat":p['cat_label'],"name":p['name'],"details":p['details'] or "","brands":p['brands'] or "","refs":[{"r":r['reference'],"s":r['status']} for r in refs],"links":[{"t":l['label'],"u":l['url']} for l in links]}
                if p['interval_info']:
                    part_obj["interval"] = p['interval_info']
                parts_list.append(part_obj)
            if parts_list:
                categories[cat['name']] = parts_list
        data[vid] = {"name":v['name'],"info":v['info'] or "","crossNote":v['cross_note'] or "","categories":categories}
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',',':'))
    conn.close()
    count_v = len(data)
    count_p = sum(sum(len(ps) for ps in v['categories'].values()) for v in data.values())
    print(f"Exportado: {JSON_PATH}")
    print(f"Vehiculos: {count_v} | Componentes: {count_p}")

if __name__ == '__main__':
    export()
