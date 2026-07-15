import sqlite3
import os

def migrate():
    # Use database at project root
    db_path = os.path.join(os.path.dirname(__file__), '..', 'Amarakosha.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Creating tables nominal_declension_suffix_elements and tiganta_suffix_elements...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nominal_declension_suffix_elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paradigm_code TEXT,
            position_index INTEGER,
            suffix TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tiganta_suffix_elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suffix_code INTEGER,
            position_index INTEGER,
            suffix TEXT
        )
    """)

    # Clear existing data just in case
    cursor.execute("DELETE FROM nominal_declension_suffix_elements")
    cursor.execute("DELETE FROM tiganta_suffix_elements")

    # 1. Migrate nominal_declension_suffixes
    print("Migrating nominal_declension_suffixes...")
    cursor.execute("SELECT paradigm_code, suffix_patterns FROM nominal_declension_suffixes")
    rows = cursor.fetchall()
    for row in rows:
        code, patterns = row[0], row[1]
        if patterns:
            suffixes = patterns.strip().split(' ')
            for idx, suffix in enumerate(suffixes):
                cursor.execute("""
                    INSERT INTO nominal_declension_suffix_elements (paradigm_code, position_index, suffix)
                    VALUES (?, ?, ?)
                """, (code, idx, suffix))

    # 2. Migrate tiganta_suffixes
    print("Migrating tiganta_suffixes...")
    cursor.execute("SELECT suffix_code, conjugation_suffixes FROM tiganta_suffixes")
    rows = cursor.fetchall()
    for row in rows:
        code, patterns = row[0], row[1]
        if patterns:
            suffixes = patterns.strip().split(' ')
            for idx, suffix in enumerate(suffixes):
                cursor.execute("""
                    INSERT INTO tiganta_suffix_elements (suffix_code, position_index, suffix)
                    VALUES (?, ?, ?)
                """, (code, idx, suffix))

    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == '__main__':
    migrate()
