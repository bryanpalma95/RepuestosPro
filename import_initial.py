"""
RepuestosPro - Importar datos iniciales a SQLite
Ejecutar despues de setup_db.py para poblar la BD desde data.js
"""
import sqlite3, json, os, re

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')
DATA_JS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.js')

def parse_data_js():
    with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    # Extraer constantes
    constants = {}
    for m in re.finditer(r'const (\w+)="([^"]*)"', content):
        constants[m.group(1)] = m.group(2)
    # Extraer DATA
    dm = re.search(r'const DATA=(\{.+\});', content, re.DOTALL)
    if not dm:
        return None
    s = dm.group(1)
    # Resolver concatenaciones variable+"texto"
    for name, val in constants.items():
        s = re.sub(re.escape(name) + r'\+"([^"]*)"', lambda m: f'"{val}{m.group(1)}"', s)
        s = re.sub(r'(?<!["\w])' + re.escape(name) + r'(?!["\w])', f'"{val}"', s)
    # JS -> JSON
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'(\{|,)\s*([a-zA-Z_]\w*)\s*:', r'\1"\2":', s)
    s = re.sub(r',\s*([}\]])', r'\1', s)
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        print(f"Parse error: {e}")
        with open(os.path.join(os.path.dirname(__file__), '_debug.txt'), 'w', encoding='utf-8') as f:
            f.write(s[:3000])
        return None

def import_data(conn, data):
    c = conn.cursor()
    c.execute("DELETE FROM part_links"); c.execute("DELETE FROM part_refs")
    c.execute("DELETE FROM parts"); c.execute("DELETE FROM categories"); c.execute("DELETE FROM vehicles")
    for vid, vd in data.items():
        c.execute("INSERT INTO vehicles VALUES (?,?,?,?)", (vid, vd.get('name',''), vd.get('info',''), vd.get('crossNote','')))
        order = 0
        for cat_name, parts in vd.get('categories',{}).items():
            order += 1
            c.execute("INSERT INTO categories (vehicle_id, name, sort_order) VALUES (?,?,?)", (vid, cat_name, order))
            cat_id = c.lastrowid
            for p in parts:
                c.execute("INSERT INTO parts (category_id, cat_label, name, details, brands, interval_info) VALUES (?,?,?,?,?,?)",
                    (cat_id, p.get('cat',''), p.get('name',''), p.get('details',''), p.get('brands',''), p.get('interval')))
                pid = c.lastrowid
                for r in p.get('refs',[]):
                    c.execute("INSERT INTO part_refs (part_id, reference, status) VALUES (?,?,?)", (pid, r.get('r',''), r.get('s','verify')))
                for l in p.get('links',[]):
                    c.execute("INSERT INTO part_links (part_id, label, url) VALUES (?,?,?)", (pid, l.get('t',''), l.get('u','')))
    conn.commit()
    print(f"Importados: {len(data)} vehiculos")

if __name__ == '__main__':
    print("Parseando data.js...")
    data = parse_data_js()
    if not data:
        print("Fallo. Revisa _debug.txt"); exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    import_data(conn, data)
    conn.close()
    print("Exportando db.json...")
    os.system(f'python "{os.path.join(os.path.dirname(os.path.abspath(__file__)), "export_db.py")}"')
