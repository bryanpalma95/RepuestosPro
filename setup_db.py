"""
RepuestosPro - Setup de Base de Datos SQLite
Ejecutar una vez para crear la BD con la estructura.
Luego usar import_initial.py para poblar y export_db.py para generar db.json
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite')

def create_tables(conn):
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        info TEXT,
        cross_note TEXT
    );
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id TEXT NOT NULL,
        name TEXT NOT NULL,
        sort_order INTEGER DEFAULT 0,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        cat_label TEXT NOT NULL,
        name TEXT NOT NULL,
        details TEXT,
        brands TEXT,
        interval_info TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS part_refs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_id INTEGER NOT NULL,
        reference TEXT NOT NULL,
        status TEXT DEFAULT 'verify' CHECK(status IN ('confirmed','verify')),
        FOREIGN KEY (part_id) REFERENCES parts(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS part_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_id INTEGER NOT NULL,
        label TEXT NOT NULL,
        url TEXT NOT NULL,
        FOREIGN KEY (part_id) REFERENCES parts(id) ON DELETE CASCADE
    );
    ''')
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    create_tables(conn)
    conn.close()
    print(f"BD creada: {DB_PATH}")
    print("Tablas: vehicles, categories, parts, part_refs, part_links")
    print("\nSiguiente paso: python import_initial.py")
