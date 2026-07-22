import sqlite3
import os

def migrate():
    # Use database at project root
    db_path = os.path.join(os.path.dirname(__file__), '..', 'Amarakosha.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Creating table dhatu_upasarga_sequence_elements...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dhatu_upasarga_sequence_elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dhatu_id INTEGER REFERENCES dhatu_metadata(dhatu_id),
            position_index INTEGER,
            upasarga_id INTEGER REFERENCES Upasarga(ID)
        )
    """)

    cursor.execute("DELETE FROM dhatu_upasarga_sequence_elements")

    print("Reading dhatu_upasarga_mappings...")
    cursor.execute("SELECT dhatu_id, upasarga_sequence_code FROM dhatu_upasarga_mappings")
    rows = cursor.fetchall()

    print("Migrating records...")
    insert_count = 0
    for dhatu_id, code in rows:
        if code:
            for idx, ch in enumerate(code):
                upasarga_id = ord(ch) - ord('a') + 1
                cursor.execute("""
                    INSERT INTO dhatu_upasarga_sequence_elements (dhatu_id, position_index, upasarga_id)
                    VALUES (?, ?, ?)
                """, (dhatu_id, idx, upasarga_id))
                insert_count += 1

    conn.commit()
    conn.close()
    print(f"Migration complete! Inserted {insert_count} mapping entries.")

if __name__ == '__main__':
    migrate()
