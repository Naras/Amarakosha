# Relational Schema Analysis & Normalization Report

This document analyzes the legacy database tables `STINNEW`, `Stinfin`, and `SubFin` in `Amarakosha.db`. We highlight their current structural violations of First Normal Form (1NF) and Second Normal Form (2NF), and propose clean, fully normalized schemas matching modern 3NF guidelines.

---

## 1. Analysis of `STINNEW` (Tiganta Suffix Mappings)

### Current Structure
* **Table Schema**:
  ```sql
  CREATE TABLE "STINNEW" (
      "Field1" TEXT,     -- Verb Base (e.g. 'भव्')
      "Field2" INTEGER,  -- Dhatu ID (e.g. 1)
      "Field3" TEXT      -- Concatenated Space-Separated Suffix Tokens
  );
  ```
* **Example Row**:
  * `Field1` = `'भव्'`
  * `Field2` = `1`
  * `Field3` = `'1A1 1E3 1G4 1I5 1M7 1F27 1H14 1P18'`

### Issues
1. **1NF Violation**: `Field3` contains a space-separated list of tokens.
2. **Concatenated Attributes**: Each token (e.g., `'1A1'`) is a composite string:
   * First Character (`1`): `dhatu_vidha` (conjugation mode: 1 = Kevala-Tiganta, 2 = Nijanta, 3 = Sannanta)
   * Second Character (`A`): `lakara_id` (tense/mood code: A = Lat, B = Lit, etc.)
   * Third/Remaining Characters (`1`): `suffix_code` references `tiganta_suffixes`

### Proposed Normalized Schema
We split the composite tokens and store them as individual rows in a normalized mapping table:

```sql
CREATE TABLE tiganta_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    form TEXT NOT NULL,                  -- Verb Base (e.g. 'भव्')
    dhatu_id INTEGER NOT NULL,           -- Foreign key to dhatu_metadata
    dhatu_vidha INTEGER NOT NULL,        -- Explicit integer (1, 2, or 3)
    lakara_id INTEGER NOT NULL,          -- Explicit integer (0 to 9)
    suffix_code INTEGER NOT NULL         -- Foreign key to tiganta_suffixes
);
```

---

## 2. Analysis of `Stinfin` (Conjugated Verb Forms)

### Current Structure
* **Table Schema**:
  ```sql
  CREATE TABLE "Stinfin" (
      "ID" INTEGER,
      "Field1" TEXT,     -- Fully conjugated verb form (e.g. 'बभ्राम')
      "Field2" INTEGER,  -- Dhatu ID (e.g. 91)
      "Field3" TEXT,     -- Composite Type Code (e.g. '1C')
      "Field4" INTEGER   -- Purusha-Vacana Slot Code (0 to 8)
  );
  ```
* **Example Row**:
  * `Field1` = `'बभ्राम'`
  * `Field2` = `91`
  * `Field3` = `'1C'`
  * `Field4` = `0` (Prathama Purusha Ekavacana)

### Issues
1. **Composite Attribute**: `Field3` combines two distinct metadata fields:
   * First Character (`1`): `dhatu_vidha`
   * Second Character (`C`): `lakara_id` (tense/mood representation)

### Proposed Normalized Schema
Separate the composite column into distinct, indexable integer columns:

```sql
CREATE TABLE tiganta_form_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    form TEXT NOT NULL,                  -- Fully conjugated form (e.g., 'बभ्राम')
    dhatu_id INTEGER NOT NULL,           -- Foreign key to dhatu_metadata
    dhatu_vidha INTEGER NOT NULL,        -- Explicit integer (1, 2, or 3)
    lakara_id INTEGER NOT NULL,          -- Explicit integer (0 to 9)
    purusha_vacana_code INTEGER NOT NULL -- Explicit slot index (0 to 8)
);
```

---

## 3. Analysis of `SubFin` (Fully Declined Nominal Forms)

### Current Structure
* **Table Schema**:
  ```sql
  CREATE TABLE "SubFin" (
      "ID" INTEGER,
      "FinForm" TEXT,    -- Fully declined word form (e.g. 'जरे')
      "Code" TEXT        -- Space-separated list of paradigm and case codes
  );
  ```
* **Example Row**:
  * `FinForm` = `'जरे'`
  * `Code` = `'b007,2 b007,5 b007,22 b007,23'`

### Issues
1. **1NF Violation**: The `Code` column contains a space-separated list of elements.
2. **Composite Format**: Each element is joined by a comma (e.g., `'b007,2'`), where `'b007'` is the paradigm/declension pattern code and `'2'` is the Vibhakti-Vacana index (0 to 23).

### Proposed Normalized Schema
Normalize the mapping into a 1:many relation, splitting the paradigm and case positions:

```sql
CREATE TABLE subanta_declensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fin_form TEXT NOT NULL UNIQUE        -- Inflected form (e.g. 'जरे')
);

CREATE TABLE subanta_declension_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    declension_id INTEGER REFERENCES subanta_declensions(id),
    anta_code TEXT NOT NULL,             -- Pratipadika ending code (e.g., 'b')
    linga_id INTEGER NOT NULL,           -- Gender ID
    paradigm_id INTEGER NOT NULL,        -- Paradigm class identifier
    vibvach INTEGER NOT NULL             -- Case-number index (0 to 23)
);
```
*(Alternatively, `paradigm_code` can be stored directly as a combined string like `'b007'` if preferred for simplicity)*
