import sqlite3
import os

def migrate():
    # Use database at project root
    db_path = os.path.join(os.path.dirname(__file__), '..', 'Amarakosha.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Clearing subanta_declension_mappings...")
    cursor.execute("DELETE FROM subanta_declension_mappings")

    print("Reading subanta_declensions...")
    cursor.execute("SELECT id, code_list FROM subanta_declensions")
    rows = cursor.fetchall()
    
    print("Migrating records...")
    insert_count = 0
    for declension_id, code_list in rows:
        if code_list:
            codesets = code_list.strip().split(' ')
            for codeset in codesets:
                if ',' in codeset:
                    parts = codeset.split(',')
                    code_part = parts[0]
                    vibvach_part = int(parts[1])
                    
                    anta_code = code_part[0]
                    linga_id = int(code_part[1])
                    paradigm_id = int(code_part[2:])
                    
                    cursor.execute("""
                        INSERT INTO subanta_declension_mappings (declension_id, anta_code, linga_id, paradigm_id, vibvach)
                        VALUES (?, ?, ?, ?, ?)
                    """, (declension_id, anta_code, linga_id, paradigm_id, vibvach_part))
                    insert_count += 1

    conn.commit()
    conn.close()
    print(f"Migration complete! Inserted {insert_count} mapping entries.")

if __name__ == '__main__':
    migrate()
