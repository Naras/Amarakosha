# Relational Database Migration Scripts

This folder contains the utility scripts designed to normalize legacy space-separated structures in `Amarakosha.db` into 1:many relational mappings.

---

## 1. [migrate_suffixes_1_m.py](file:///Users/narasimhanm.g./Desktop/Playground/Amarakosha/migration_scripts/migrate_suffixes_1_m.py)

### Description
Splits space-separated suffixes in `nominal_declension_suffixes` and `tiganta_suffixes` into clean, indexed child tables.

* **Target Tables Populated**:
  * `nominal_declension_suffix_elements`
  * `tiganta_suffix_elements`
* **Why it was used**:
  To achieve First Normal Form (1NF) alignment. The code in `MorphologicalAnalysis.py` previously loaded the entire space-separated list string and split it dynamically in memory. By populating element tables, we query exact slot-indexed suffixes directly via SQLite.
* **Usage**:
  Run from the project root:
  ```bash
  venv/bin/python migration_scripts/migrate_suffixes_1_m.py
  ```

---

## 2. [migrate_subanta_declensions.py](file:///Users/narasimhanm.g./Desktop/Playground/Amarakosha/migration_scripts/migrate_subanta_declensions.py)

### Description
Parses the concatenated, space-separated code mappings (e.g. `'b007,2'`) inside `subanta_declensions` and creates normalized entries in `subanta_declension_mappings`.

* **Target Table Populated**:
  * `subanta_declension_mappings`
* **Why it was used**:
  The legacy `SubFin` (now `subanta_declensions`) table stored comma-separated values inside space-separated string values. This script parses each mapping, separating `anta_code`, `linga_id`, `paradigm_id`, and `vibvach` (Vibhakti-Vacana index) into distinct, indexable integer and string columns.
* **Usage**:
  Run from the project root:
  ```bash
  venv/bin/python migration_scripts/migrate_subanta_declensions.py
  ```

---

## 3. [migrate_upasarga_mappings.py](file:///Users/narasimhanm.g./Desktop/Playground/Amarakosha/migration_scripts/migrate_upasarga_mappings.py)

### Description
Parses character-encoded prefix sequences (e.g. `'dajklqrs'`) in `dhatu_upasarga_mappings` and populates `dhatu_upasarga_sequence_elements`.

* **Target Table Populated**:
  * `dhatu_upasarga_sequence_elements`
* **Why it was used**:
  The legacy codebase stored list references inside a string (characters mapped to prefix IDs relative to `'a'`). This script normalizes them into atomic, sequential entries (`dhatu_id`, `position_index`, `upasarga_id`), enabling joining directly with `Upasarga` and completely removing the character-decoding logic from Python.
* **Usage**:
  Run from the project root:
  ```bash
  venv/bin/python migration_scripts/migrate_upasarga_mappings.py
  ```
