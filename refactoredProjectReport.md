# Amarakosha Refactored Project Report

This report summarizes the major architectural improvements, database normalization efforts, migration script executions, and codebase enhancements undertaken in the **Amarakosha** project. These changes improve database performance, guarantee data integrity, align with modern relational schema practices, and ensure smooth deployments across local dev and Amazon Lightsail server environments.

---

## 1. Database Schema Refactoring & Normalization

The legacy database (`Amarakosha.db`) contained several denormalized structures that violated standard relational hygiene rules (First Normal Form (1NF) and Second Normal Form (2NF)).

### Legacy Tables Normalization

#### A. `STINNEW` (Tiganta Suffix Mappings)
* **Issues (1NF & 2NF)**: The legacy `Field3` column contained a space-separated string of composite codes (e.g. `'1A1 1E3 1G4'`). Each token combined the conjugation mode (`dhatu_vidha`), tense/mood (`lakara_id`), and a suffix reference.
* **Refactoring**: Split composite tokens into atomic elements and mapped them to individual rows in the new `tiganta_mappings` table:
  ```sql
  CREATE TABLE tiganta_mappings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      form TEXT NOT NULL,
      dhatu_id INTEGER REFERENCES dhatu_metadata(dhatu_id),
      dhatu_vidha INTEGER NOT NULL,
      lakara_id INTEGER REFERENCES lakara_lookup(id),
      suffix_code TEXT NOT NULL
  );
  ```

#### B. `Stinfin` (Conjugated Verb Forms)
* **Issues (2NF)**: The legacy `Field3` combined the conjugation mode and tense/mood into a 2-character string (e.g. `'1C'`).
* **Refactoring**: Split the composite field into explicit, indexed integer columns in `tiganta_form_mappings`:
  ```sql
  CREATE TABLE tiganta_form_mappings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      form TEXT NOT NULL,
      dhatu_id INTEGER REFERENCES dhatu_metadata(dhatu_id),
      dhatu_vidha INTEGER NOT NULL,
      lakara_id INTEGER REFERENCES lakara_lookup(id),
      purusha_vacana_code INTEGER NOT NULL
  );
  ```

#### C. `SubFin` (Declined Nominal Forms)
* **Issues (1NF)**: The legacy `Code` column contained space-separated composite codes like `'b007,2 b007,5'`. The code combined the declension pattern and the vibvach index, separated by a comma.
* **Refactoring**: Normalized into a 1-to-many relationship using a master-child layout:
  ```sql
  CREATE TABLE subanta_declensions (
      id INTEGER PRIMARY KEY,
      fin_form TEXT NOT NULL,
      code_list TEXT NOT NULL
  );

  CREATE TABLE subanta_declension_mappings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      declension_id INTEGER REFERENCES subanta_declensions(id),
      anta_code TEXT NOT NULL,
      linga_id INTEGER,
      paradigm_id INTEGER,
      vibvach INTEGER NOT NULL
  );
  ```

---

## 2. Structural Feasibility: Can `dhatuNo` be Replaced by `dhatu`?

> [!WARNING]
> **No. Replacing the unique identifier `dhatuNo` with the literal Sanskrit spelling (`dhatu`) is linguistically and structurally impossible.**

### Grammatical Homonymy in Sanskrit
In Paninian grammar, many verbal roots share the exact same characters/spelling but have completely different grammatical properties depending on their conjugational class (*Gana*), suffix class (*Padi*), or semantics.
1. **Example 1: `कृ` (kṛ)**
   - **Tanadi Gana** (8th class) $\rightarrow$ conjugates to *karoti* (करोति - "to do").
   - **Kryadi Gana** (9th class) $\rightarrow$ conjugates to *kriṇāti* (क्रीणाति - "to buy").
2. **Example 2: `भृ` (bhṛ)**
   - Produces entirely distinct conjugation paradigms depending on whether it belongs to the Bhvadi, Juhotyadi, or Kryadi Gana.

### Relational Database Impact
Querying by a string literal like `'कृ'` instead of a unique ID like `1.12` (represented as `dhatu_id` or `dhatuNo`) would return duplicate matching rows. The database layer would merge separate roots, leading to incorrect verb conjugation tables and morphological analyses. Therefore, retaining a unique identifier (`dhatuNo` / `dhatu_id`) is essential to preserve grammatical accuracy.

---

## 3. Database Migration Scripts

Four main Python utility scripts were executed to implement the schema renovations:

1. **[migrate_db.py](file:///Users/narasimhanm.g./Desktop/Playground/Amarakosha/migrate_db.py)**:
   - Drops legacy tables and recreates fully normalized schemas with standard foreign keys.
   - Creates and populates lookup tables for `gana_lookup`, `padi_lookup`, `it_lookup`, `transitivity_lookup`, `lakara_lookup`, and `voice_lookup`.
   - Extracts metadata from legacy table `Sdhatu` to populate `dhatu_metadata` and `dhatu_meanings`.
   - Populates `krdanta_dictionary` from `KRUD`, `krdanta_indeclinables` from `KRUDAV`, and inflected nominals into `subanta_forms`.
2. **[migrate_suffixes_1_m.py](file:///Users/narasimhanm.g./Desktop/Playground/Amarakosha/migration_scripts/migrate_suffixes_1_m.py)**:
   - Normalizes the legacy `Sufcode` (nominal suffixes) and `stinsuf` (verbal suffixes) tables.
   - Splits space-separated list strings (previously loaded and split dynamically in Python memory) into individual records in `nominal_declension_suffix_elements` and `tiganta_suffix_elements`.
3. **[migrate_subanta_declensions.py](file:///Users/narasimhanm.g./Desktop/Playground/Amarakosha/migration_scripts/migrate_subanta_declensions.py)**:
   - Parses space-separated comma configurations (e.g. `'b007,2'`) in `subanta_declensions`.
   - Populates `subanta_declension_mappings` with individual columns for `anta_code` (e.g. `'b'`), `linga_id` (e.g., `0`), `paradigm_id` (e.g. `7`), and `vibvach` (e.g. `2`).
4. **[migrate_upasarga_mappings.py](file:///Users/narasimhanm.g./Desktop/Playground/Amarakosha/migration_scripts/migrate_upasarga_mappings.py)**:
   - Parses character-encoded prefix sequences (e.g. `'dajklqrs'`) in `dhatu_upasarga_mappings`.
   - Normalizes character index listings (`ord(char) - ord('a') + 1`) into atomic database rows inside `dhatu_upasarga_sequence_elements`. This removes complex character-offset parsing from client Python code.

---

## 4. Frontend & Backend Codebase Enhancements

A series of enhancements were made to make the application reliable in local development and Amazon Lightsail server environments.

### Unified API URL Resolution
* **Dynamic Config (`config.js`)**: Abstracted the backend API endpoints. Dynamic domain detection was implemented; when hosted on `iyengarlabs.org`, the application automatically requests `https://app.iyengarlabs.org/amarakosha-rest-api`. Otherwise, it defaults to the local development environment (`http://127.0.0.1:5002/Amarakosha/api/v1.0`).
* **Session Validation**: Added `getScriptParam()` to prevent sending `"null"` or `"undefined"` query parameters when language options aren't pre-configured in session storage.
* **Refactored Frontend**: Updated HTML pages (Synonyms, Subanta, Tiganta, Krdanta, and Sentence Analyser) to construct endpoint URLs through `getApiUrl()` and encode path parameters via `encodeURIComponent` to prevent parsing breaks.

### Backend Improvements
* **`/healthz` Endpoint**: Added health ping routes `/healthz` and `/Amarakosha/api/v1.0/healthz` to Flask `restService.py` to allow Docker and Lightsail load balancer checks.
* **Mojibake Param Decoding**: Standard WSGI containers decode URL parameters as ISO-8859-1 (Latin-1). Sanskrit path parameters (e.g. `%E0%A4%85%E0%A4%82%E0%A4%B6%E0%A4%95%E0%A5%8D`) would corrupt into mojibake and cause service crashes. Added `decode_param()` inside `restService.py` to encode parameters back to Latin-1 bytes and decode them properly into UTF-8 Devanagari.

### Containerization
* **Dynamic Docker Entrypoint**: Added `docker-entrypoint.sh` inside `source/View/Webclient` to inject the runtime container environment variable `API_URL` directly into `config.js` on startup. This decouples the frontend code build from target deployment URLs.

---

## 5. Verification & Testing

* **Backend Health Checks**: Tested health endpoints return `200 OK` with `{"status": "healthy"}` and appropriate CORS headers.
* **Transliteration Encoding**: Sent Devanagari path query `Subanta/अंशक` to local REST APIs. The mojibake decoder successfully recovered the characters, generated the declensions, and returned correct JSON paradigms without errors.
