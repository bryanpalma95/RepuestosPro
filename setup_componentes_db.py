"""
RepuestosPro - Setup Base de Datos de Componentes
===================================================
Crea la estructura SQLite para 154 familias x 495 componentes.
Luego se llena progresivamente desde busquedas web y APIs.

Estructura:
  - motor_families: 154 familias de motor
  - components: 495 componentes (del archivo componentes.txt)
  - family_components: relacion familia <-> componente con OEM data
  - vehicles: 3218 vehiculos mapeados a su familia

Uso:
    python setup_componentes_db.py          # Crear BD
    python setup_componentes_db.py --stats  # Ver stats
"""

import sqlite3
import json
import os
import sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "componentes.db")


def crear_tablas(conn):
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS motor_families (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        family_key TEXT UNIQUE NOT NULL,
        marca TEXT NOT NULL,
        motor TEXT NOT NULL,
        modelos_json TEXT,
        notas TEXT
    );
    CREATE TABLE IF NOT EXISTS components (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        categoria TEXT,
        subcategoria TEXT,
        aplica_a TEXT DEFAULT 'todos',
        prioridad INTEGER DEFAULT 99
    );
    CREATE TABLE IF NOT EXISTS family_components (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        family_id INTEGER NOT NULL,
        component_id INTEGER NOT NULL,
        oem_number TEXT,
        alt_numbers TEXT,
        aftermarket TEXT,
        brands TEXT,
        interval_km INTEGER,
        interval_months INTEGER,
        quantity INTEGER DEFAULT 1,
        notes TEXT,
        source TEXT,
        verified INTEGER DEFAULT 0,
        updated_at TEXT,
        FOREIGN KEY (family_id) REFERENCES motor_families(id),
        FOREIGN KEY (component_id) REFERENCES components(id),
        UNIQUE(family_id, component_id)
    );
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        year INTEGER NOT NULL,
        motor TEXT,
        vin TEXT,
        family_id INTEGER,
        FOREIGN KEY (family_id) REFERENCES motor_families(id)
    );
    CREATE INDEX IF NOT EXISTS idx_fc_family ON family_components(family_id);
    CREATE INDEX IF NOT EXISTS idx_fc_component ON family_components(component_id);
    CREATE INDEX IF NOT EXISTS idx_fc_verified ON family_components(verified);
    CREATE INDEX IF NOT EXISTS idx_vehicles_family ON vehicles(family_id);
    CREATE INDEX IF NOT EXISTS idx_vehicles_marca ON vehicles(marca);
    ''')
    conn.commit()


def cargar_componentes(conn):
    top50 = [
        ("Filtro de Aceite", "Motor", "Lubricacion", 1),
        ("Filtro de Aire", "Motor", "Admision", 2),
        ("Filtro de Combustible", "Motor", "Combustible", 3),
        ("Filtro de Habitaculo", "Habitaculo", "Climatizacion", 4),
        ("Bujias", "Motor", "Encendido", 5),
        ("Bobina de Encendido", "Motor", "Encendido", 6),
        ("Correa de Distribucion", "Motor", "Distribucion", 7),
        ("Cadena de Distribucion", "Motor", "Distribucion", 8),
        ("Correa de Accesorios", "Motor", "Accesorios", 9),
        ("Bomba de Agua", "Motor", "Refrigeracion", 10),
        ("Pastillas de Freno Delanteras", "Frenos", "Delantera", 11),
        ("Pastillas de Freno Traseras", "Frenos", "Trasera", 12),
        ("Discos de Freno Delanteros", "Frenos", "Delantera", 13),
        ("Discos de Freno Traseros", "Frenos", "Trasera", 14),
        ("Zapatas de Freno", "Frenos", "Trasera", 15),
        ("Liquido de Frenos", "Frenos", "General", 16),
        ("Sensor de Velocidad de Rueda (ABS)", "Frenos", "Electronica", 17),
        ("Flexible de Freno", "Frenos", "Hidraulica", 18),
        ("Amortiguador Delantero", "Suspension", "Delantera", 19),
        ("Amortiguador Trasero", "Suspension", "Trasera", 20),
        ("Rotula de Bandeja", "Suspension", "Delantera", 21),
        ("Bieleta de la Barra Estabilizadora", "Suspension", "General", 22),
        ("Brazo de Control (Bandeja)", "Suspension", "Delantera", 23),
        ("Extremo de Direccion (Axial)", "Direccion", "General", 24),
        ("Cojinete de Rueda", "Suspension", "General", 25),
        ("Resorte de Suspension", "Suspension", "General", 26),
        ("Cremallera de Direccion", "Direccion", "General", 27),
        ("Buje de Bandeja", "Suspension", "Delantera", 28),
        ("Bateria", "Electrico", "General", 29),
        ("Alternador", "Electrico", "Carga", 30),
        ("Motor de Arranque", "Electrico", "Arranque", 31),
        ("Sensor de Ciguenal (CKP)", "Motor", "Sensores", 32),
        ("Sensor de Levas (CMP)", "Motor", "Sensores", 33),
        ("Sonda Lambda", "Motor", "Escape", 34),
        ("Sensor de Flujo de Aire (MAF)", "Motor", "Sensores", 35),
        ("Termostato", "Motor", "Refrigeracion", 36),
        ("Radiador", "Refrigeracion", "General", 37),
        ("Ventilador del Radiador", "Refrigeracion", "General", 38),
        ("Mangueras del Radiador", "Refrigeracion", "General", 39),
        ("Bomba de Direccion Asistida", "Direccion", "Hidraulica", 40),
        ("Kit de Embrague", "Transmision", "Embrague", 41),
        ("Junta Homocinetica", "Transmision", "Palier", 42),
        ("Fuelle de Junta Homocinetica", "Transmision", "Palier", 43),
        ("Rodamiento de Embrague", "Transmision", "Embrague", 44),
        ("Aceite Transmision", "Transmision", "Lubricacion", 45),
        ("Inyectores de Combustible", "Motor", "Combustible", 46),
        ("Bomba de Combustible", "Motor", "Combustible", 47),
        ("Catalizador", "Escape", "General", 48),
        ("Valvula EGR", "Motor", "Escape", 49),
        ("Cuerpo de Acelerador", "Motor", "Admision", 50),
    ]
    for nombre, cat, subcat, prio in top50:
        conn.execute('INSERT OR IGNORE INTO components (nombre, categoria, subcategoria, prioridad) VALUES (?, ?, ?, ?)',
                     (nombre, cat, subcat, prio))

    adicionales = [
        "Tensor de Correa de Distribucion", "Junta de Culata",
        "Sello del Ciguenal Delantero", "Sello del Ciguenal Trasero",
        "Soporte de Motor", "Sensor de Presion de Aceite",
        "Cables de Bujias", "Sensor de Presion de Aire (MAP)",
        "Silenciador", "Cilindro Maestro de Embrague",
        "Cilindro Esclavo de Embrague", "Sello del Diferencial",
        "Cilindro de Rueda (Bombin)", "Compresor de Aire Acondicionado",
        "Valvula de Expansion del A/C", "Tornillo de Rueda",
        "Tuerca de Rueda", "Limpiaparabrisas (Escobillas)",
        "Faro Delantero", "Faro Trasero",
        "Parachoques Delantero", "Parachoques Trasero",
        "Espejo Retrovisor Lateral", "Bocina (Claxon)",
        "Caja de Fusibles", "Sensor de Estacionamiento",
        "Radio / Multimedia", "Airbag del Conductor",
        "Cinturon de Seguridad del Conductor", "Sensor de Temperatura del Motor",
        "Sensor de Temperatura del Refrigerante", "Valvula de Control de Aire (IAC)",
        "Multiple de Admision", "Multiple de Escape",
        "Turbo (para motores turbo)", "Intercooler",
        "Filtro de Particulas (DPF)", "Modulo ABS",
        "Bomba de ABS", "Sensor de Presion de Neumaticos",
        "Condensador del A/C", "Evaporador del A/C",
        "Polea del Ciguenal", "Volante del Motor (Dual Mass)",
        "Disco de Embrague", "Plato de Presion de Embrague",
        "Cable de Embrague", "Sensor de Velocidad Caja",
        "Bomba de Aceite", "Carter de Aceite",
    ]
    prio = 51
    for nombre in adicionales:
        conn.execute('INSERT OR IGNORE INTO components (nombre, categoria, prioridad) VALUES (?, ?, ?)',
                     (nombre, "General", prio))
        prio += 1
    conn.commit()


def cargar_familias(conn):
    oem_path = os.path.join(SCRIPT_DIR, "componentes_oem_verificados.json")
    with open(oem_path, 'r', encoding='utf-8') as f:
        oem = json.load(f)
    for fkey, fdata in oem.items():
        conn.execute('INSERT OR IGNORE INTO motor_families (family_key, marca, motor, modelos_json) VALUES (?, ?, ?, ?)',
                     (fkey, fdata['marca'], fdata['motor'], json.dumps(fdata['modelos'], ensure_ascii=False)))
    conn.commit()


def codigos_motor(texto):
    return set(c for c in re.findall(r'[A-Z0-9][A-Z0-9]{2,}[-]?[A-Z0-9]*', texto.upper())
               if len(c) >= 3 and c not in ('V6', 'V8', 'TSI', 'TDI', 'GDI', 'VVT', 'DOHC', 'OHC'))


def cargar_vehiculos(conn):
    cat_path = os.path.join(SCRIPT_DIR, "vins_catalogo_final.json")
    with open(cat_path, 'r', encoding='utf-8') as f:
        catalogo = json.load(f)

    cursor = conn.execute("SELECT id, family_key, motor, marca FROM motor_families")
    families_db = cursor.fetchall()

    idx_code = {}
    idx_str = {}
    for fid, fkey, motor, marca in families_db:
        for c in codigos_motor(motor):
            idx_code[c] = fid
        for m in [x.strip().lower() for x in marca.split('/')]:
            idx_str[m + '|' + motor] = fid
            for seg in motor.split(','):
                seg = seg.strip()
                if seg:
                    idx_str[m + '|' + seg] = fid

    for key, data in catalogo.items():
        motor = data.get('motor', '-')
        marca_l = data['marca'].lower()
        family_id = None
        for c in codigos_motor(motor):
            if c in idx_code:
                family_id = idx_code[c]
                break
        if not family_id:
            family_id = idx_str.get(marca_l + '|' + motor)
        if not family_id:
            for oem_key in idx_str:
                if oem_key.startswith(marca_l + '|'):
                    oem_motor = oem_key.split('|', 1)[1]
                    if motor in oem_motor or oem_motor in motor:
                        family_id = idx_str[oem_key]
                        break
        conn.execute('INSERT INTO vehicles (marca, modelo, year, motor, vin, family_id) VALUES (?, ?, ?, ?, ?, ?)',
                     (data['marca'], data['modelo'], data['year'], motor, data['vin'], family_id))
    conn.commit()


def cargar_oem_existentes(conn):
    oem_path = os.path.join(SCRIPT_DIR, "componentes_oem_verificados.json")
    with open(oem_path, 'r', encoding='utf-8') as f:
        oem = json.load(f)

    for fkey, fdata in oem.items():
        cursor = conn.execute("SELECT id FROM motor_families WHERE family_key = ?", (fkey,))
        row = cursor.fetchone()
        if not row:
            continue
        family_id = row[0]

        for comp_name, comp_data in fdata.get('componentes', {}).items():
            base = comp_name.split('(')[0].strip()
            cursor = conn.execute("SELECT id FROM components WHERE nombre LIKE ?", ('%' + base[:15] + '%',))
            row = cursor.fetchone()
            if not row:
                if 'aceite' in comp_name.lower() and 'filtro' in comp_name.lower():
                    cursor = conn.execute("SELECT id FROM components WHERE nombre = 'Filtro de Aceite'")
                    row = cursor.fetchone()
                elif 'aire' in comp_name.lower() and 'filtro' in comp_name.lower():
                    cursor = conn.execute("SELECT id FROM components WHERE nombre = 'Filtro de Aire'")
                    row = cursor.fetchone()
                elif 'buj' in comp_name.lower():
                    cursor = conn.execute("SELECT id FROM components WHERE nombre = 'Bujias'")
                    row = cursor.fetchone()
            if not row:
                continue
            component_id = row[0]
            oem_num = comp_data.get('oem', comp_data.get('info', ''))
            alt = comp_data.get('alt', comp_data.get('supersede', ''))
            aftermarket = comp_data.get('aftermarket', '')
            source = comp_data.get('fuente', '')
            notes = comp_data.get('nota', '')
            conn.execute('''INSERT OR REPLACE INTO family_components
                (family_id, component_id, oem_number, alt_numbers, aftermarket, source, verified, notes, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, 1, ?, datetime('now'))''',
                         (family_id, component_id, oem_num, alt, aftermarket, source, notes))
    conn.commit()


def mostrar_stats(conn):
    print("=" * 50)
    print("ESTADISTICAS BD COMPONENTES")
    print("=" * 50)
    r = conn.execute("SELECT COUNT(*) FROM motor_families").fetchone()[0]
    print(f"  Familias de motor: {r}")
    r = conn.execute("SELECT COUNT(*) FROM components").fetchone()[0]
    print(f"  Componentes maestro: {r}")
    r = conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
    print(f"  Vehiculos: {r}")
    r = conn.execute("SELECT COUNT(*) FROM family_components").fetchone()[0]
    print(f"  Datos OEM cargados: {r}")
    r2 = conn.execute("SELECT COUNT(*) FROM family_components WHERE verified = 1").fetchone()[0]
    print(f"  Datos verificados: {r2}")
    f_con = conn.execute("SELECT COUNT(DISTINCT family_id) FROM family_components").fetchone()[0]
    f_tot = conn.execute("SELECT COUNT(*) FROM motor_families").fetchone()[0]
    print(f"\n  Familias con datos: {f_con}/{f_tot}")
    potencial = f_tot * 50
    print(f"  Llenado top50: {r}/{potencial} ({100*r/max(potencial,1):.1f}%)")
    print(f"\n  Archivo: {DB_PATH} ({os.path.getsize(DB_PATH)//1024} KB)")


def main():
    if "--stats" in sys.argv and os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        mostrar_stats(conn)
        conn.close()
        return

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")

    print("Creando tablas...")
    crear_tablas(conn)
    print("Cargando componentes (top 50 + 50 adicionales)...")
    cargar_componentes(conn)
    print("Cargando familias de motor (154)...")
    cargar_familias(conn)
    print("Cargando vehiculos (3218)...")
    cargar_vehiculos(conn)
    print("Cargando datos OEM verificados...")
    cargar_oem_existentes(conn)

    print()
    mostrar_stats(conn)
    conn.close()
    print("\n[OK] BD creada.")


if __name__ == "__main__":
    main()
