# Analysis of Database Queries & Schema Improvements

This document provides a detailed analysis of the database queries utilized by [MorphologicalAnalysis.py](file:///Users/narasimhanm.g./Desktop/Playground/Amarakosha/source/Controller/MorphologicalAnalysis.py), proposes clean column/table renaming strategies for legacy structures, and addresses the linguistic and structural feasibility of replacing `dhatuNo` with `dhatu`.

---

## Part A: Analysis of Database Queries

Below is the summary of database queries executed in each of the core morphological functions:

| Function | Primary Database Queries | Purpose |
| :--- | :--- | :--- |
| `subanta_Generation` | `select * from subanta_forms where base=?`<br>`select * from Sufcode where code=?` | 1. Looks up the declension paradigm and starting base mapping for a nominal root.<br>2. Retrieves the suffix strings associated with the paradigm code. |
| `krdanta_Generation` | `select * from krdanta_dictionary where krd_suffix_code=? and dhatu_id=?`<br>`select * from Sufcode where code=?` | 1. Locates the derived krdanta pratipadika (base form) for a specific verb root and suffix class.<br>2. Fetches the corresponding declension suffixes. |
| `tiganta_Generation` | `select * from upacode where DhatuNo=?`<br>`select * from upasarga`<br>`select * from tiganta_mappings where dhatu_id=? and dhatu_vidha=? and lakara_id=?` | 1. Retrieves prefix (upasarga) associations for a verb root.<br>2. Identifies conjugation templates, voices, and modes mapping to the lakara. |
| `subanta_Analysis` | `select * from subanta_declensions where fin_form=?`<br>`select * from fincode where code like ?`<br>`select * from subanta_forms where erb=?`<br>`select * from sufcode where code=?` | 1. Searches directly for matched fully declensed forms.<br>2. Resolves root word candidates and ending structures to construct analysis metadata. |
| `krdanta_Analysis` | `select * from krdanta_dictionary where sabda_base=?`<br>`select * from Sufcode where code=?` | Reverse-engineers word endings and maps potential base forms back to krdanta suffix classes and verb root IDs. |
| `tiganta_Analysis` | `select * from tiganta_form_mappings where form=?`<br>`select * from tiganta_mappings where form=?`<br>`select * from stinsuf where Field1=?` | 1. Inspects active conjugated verb forms to resolve root ID and tense (lakara).<br>2. Resolves phonetic endings/suffixes using custom verb suffix rule collections. |

---

## Part B: Suggested Schema Name Improvements

Several tables and columns still carry legacy, non-descriptive names (e.g., `Field1`, `Field2`, `Sufcode`). Below is the recommended clean database mapping to align with modern database hygiene:

### 1. `Sufcode` Table
* **Suggested Table Name**: `nominal_declension_suffixes`
* **Suggested Columns**:
  * `code` / `Code` $\rightarrow$ `paradigm_code` (Unique class identifier)
  * `SufStr` $\rightarrow$ `suffix_patterns` (Space-separated list of declension suffixes)

### 2. `fincode` Table
* **Suggested Table Name**: `nominal_base_patterns`
* **Suggested Columns**:
  * `code` $\rightarrow$ `pattern_code`
  * `finroot` $\rightarrow$ `pratipadika_base`

### 3. `upacode` Table
* **Suggested Table Name**: `dhatu_upasarga_mappings`
* **Suggested Columns**:
  * `DhatuNo` $\rightarrow$ `dhatu_id`
  * `UpaCode` $\rightarrow$ `upasarga_sequence_code`

### 4. `stinsuf` Table
* **Suggested Table Name**: `tiganta_suffixes`
* **Suggested Columns**:
  * `Field1` $\rightarrow$ `suffix_code`
  * `Field2` $\rightarrow$ `conjugation_suffixes` (Slash/space-separated verb endings)

---

## Part C: Can `dhatuNo` be Replaced by `dhatu`?

> [!WARNING]
> **No, replacing `dhatuNo` with the literal `dhatu` spelling is not linguistically or structurally feasible.**

### 1. Homonymy in Sanskrit Grammar
In Sanskrit (and Panini's Dhatupatha), there are numerous **homonymous verb roots**—meaning roots that share the exact same spelling/characters, but belong to different conjugational classes (*Ganas*), take different suffixes/conjugations (*Padi*), or have completely different meanings.

* **Example 1: `कृ` (kṛ)**
  * Belonging to **Tanadi Gana** (8th class): Conjugates to *karoti* (करोति - "to do").
  * Belonging to **Kryadi Gana** (9th class): Conjugates to *kriṇāti* (क्रीणाति - "to buy/scatter").
* **Example 2: `भ्रस्ज्` (bhrasj) / `भृ` (bhṛ)**
  * Shared spellings across different classes (Bhvadi vs. Juhotyadi vs. Kryadi) produce entirely distinct conjugation trees.

### 2. Database Primary Key Integrity
If we query using `dhatu` (e.g., `'कृ'`) instead of `dhatuNo` (e.g., `'1.12'`), the query will return records for **all homonymous roots**. This would cause the morphological generator to mix forms from different Ganas or return incorrect declensions.

`dhatuNo` functions as a unique **Primary Key / Foreign Key** mapping to a specific semantic/grammatical entry in the Dhatupatha. Therefore, it must be retained to maintain accurate and unambiguous morphological results.

## Part D: Analysis and Normalization of STINNEW, Stinfin, and SubFin

Below is the normalization analysis for the legacy tables `STINNEW`, `Stinfin`, and `SubFin` to align with relational database hygiene standards:

### 1. `STINNEW` Table (Tiganta Suffix Mappings)
* **Status**: Fully normalized and migrated to `tiganta_mappings`.
* **Issue**: Legacy `Field3` contained space-separated composite codes like `'1A1'`, which violated 1NF.
* **Proposed & Implemented Normalization**:
  * Expanded into the `tiganta_mappings` table:
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

### 2. `Stinfin` Table (Conjugated Verb Forms)
* **Status**: Fully normalized and migrated to `tiganta_form_mappings`.
* **Issue**: Legacy `Field3` combined conjugation mode (`dhatu_vidha`) and tense/mood (`lakara_id`) into a single 2-character string (e.g., `'1C'`), violating 2NF.
* **Proposed & Implemented Normalization**:
  * Separated into explicit fields in `tiganta_form_mappings`:
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

### 3. `SubFin` Table (Declined Nominal Forms)
* **Status**: Fully normalized and migrated to `subanta_declensions` and `subanta_declension_mappings`.
* **Issue**: Legacy `Code` column contained space-separated codes like `'b007,2'`, violating 1NF and combining the paradigm code and vibvach index with a comma.
* **Proposed & Implemented Normalization**:
  * Created `subanta_declensions` and a child relation table `subanta_declension_mappings`:
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
  * **Codebase Cleanup**: The legacy direct lookup loop in `subanta_Analysis` was identified as dead code and was completely removed, simplifying lookup routing.
