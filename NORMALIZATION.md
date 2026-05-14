# NORMALIZATION.md

## Part I — Normalization Audit (3rd Normal Form)

---

## Normalization Audit

The table below evaluates every table in the original schema against each normal form and identifies exactly which tables violate 3NF and why.

| Table       | 1NF | 2NF | 3NF | Violation Reason                                                                 |
|-------------|-----|-----|-----|----------------------------------------------------------------------------------|
| Customers   | ✅  | ✅  | ❌  | `metadata_created_by` depends on the data-entry process, not on `customer_id`   |
| Sellers     | ✅  | ✅  | ❌  | `metadata_source` depends on the ingestion process, not on `seller_id`          |
| Products    | ✅  | ✅  | ⚠️  | `metadata_note` is a business attribute with a misleading name — must be renamed |
| Orders      | ✅  | ✅  | ❌  | `metadate_status` is misspelled and misclassified; mixed casing causes inconsistency |
| Order_Items | ✅  | ✅  | ❌  | `metadata_flag` is `'ok'` in every row — carries no information, violates clean design |

**Why 1NF is satisfied:** All columns hold atomic (single) values. No repeating groups exist. Every table has a defined primary key.

**Why 2NF is satisfied:** Every table uses a single-column primary key, so partial dependency (where a non-key attribute depends on only part of a composite key) is structurally impossible.

**Why 3NF is violated:** 3NF requires that every non-key attribute depend *only* on the primary key — not on any external factor. The `metadata_created_by` and `metadata_source` columns depend on the data entry or ingestion system (an external process), not on the customer or seller. The `metadata_flag` column is a meaningless constant. The `metadate_status` column is misspelled and misclassified. These must all be resolved for the schema to reach 3NF.

**Reduction to 3NF is achieved by:**
1. Extracting `metadata_created_by` and `metadata_source` into a new `Audit_Log` table
2. Renaming `metadata_note` to `category` in Products
3. Correcting `metadate_status` to `order_status` in Orders and adding a CHECK constraint
4. Dropping `metadata_flag` from Order_Items entirely

The full step-by-step decomposition and the final schema are shown in Sections 3 and 4 below.

---

## 1. Original Functional Dependencies

Below are all functional dependencies found in the original schema from the DDL.

**Customers**
```
customer_id → name, email, created_at, metadata_created_by
```

**Sellers**
```
seller_id → seller_name, join_date, metadata_source
```

**Products**
```
product_id → product_name, price, seller_id, metadata_note
```

**Orders**
```
order_id → customer_id, order_date, metadate_status
```

**Order_Items**
```
order_item_id → order_id, product_id, quantity, metadata_flag
```

In every table, the primary key is the only determinant. No non-key attribute determines another non-key attribute, so there are no transitive dependencies among business columns. However, each table contains embedded metadata columns that do not describe the entity itself — they describe how or by whom the record was created. These are identified and resolved below.

---

## 2. Anomaly Identification

### Customers — `metadata_created_by`
This column stores `'admin'` or `'system'`, indicating who entered the record — not a customer property.

- **Update Anomaly:** If the entry source is renamed (e.g., `'admin'` → `'superuser'`), every affected row must be updated individually. Missing one row leaves the table inconsistent.
- **Insertion Anomaly:** A new customer cannot be inserted without knowing or fabricating a value for `metadata_created_by`, even though it has nothing to do with the customer.
- **Deletion Anomaly:** Deleting a customer destroys the audit information (who created it) along with the business data — both are lost together.

### Sellers — `metadata_source`
This column stores `'import'` or `'manual'`, describing how the seller record was loaded.

- **Update Anomaly:** Renaming the ingestion channel requires updating every row that holds the old value across multiple sellers.
- **Insertion Anomaly:** Adding a new seller requires a `metadata_source` value even when the source is not yet known.
- **Deletion Anomaly:** Removing a seller removes its provenance history permanently.

### Products — `metadata_note`
This column stores labels like `'high-end'`, `'budget'`, `'accessory'`. Despite the `metadata_` prefix, this is actually a product classification (category). It is a business attribute with a misleading name — no anomaly, but the name must be corrected.

### Orders — `metadate_status`
This column is **misspelled** (`metadate_status` instead of `order_status`) and stores order lifecycle states like `'Shipped'`, `'pending'`, `'delivered'`, `'cancelled'`. It is a core business attribute, not metadata.

- **Consistency Anomaly:** The sample data has `'Shipped'` (capitalized) for `order_id = 1` and `'shipped'` (lowercase) for `order_id = 5`. Without a constraint, the same status is stored with different casing, making WHERE clause comparisons unreliable.

### Order_Items — `metadata_flag`
Every single row in the table has `metadata_flag = 'ok'`. A column with one constant value across all rows carries zero information.

- **Update Anomaly:** Any renaming of this flag requires a full-table update for a column that serves no business purpose.
- **Insertion Anomaly:** Every new order item is forced to supply a value for a field that means nothing.

---

## 3. Decomposition Steps

The schema already satisfies **1NF** (atomic values, defined primary keys) and **2NF** (no partial dependencies — all tables use single-column primary keys). The violations are in **3NF** due to metadata columns that depend on external processes rather than the entity's primary key.

### Step 1 — Remove `metadata_created_by` from Customers and `metadata_source` from Sellers

These two columns describe record-creation context, not the entities themselves. They are extracted into a new `Audit_Log` table.

**Customers — Before:**
```sql
CREATE TABLE Customers (
    customer_id         INT PRIMARY KEY,
    name                VARCHAR(100),
    email               VARCHAR(100),
    created_at          DATE,
    metadata_created_by VARCHAR(50)   -- REMOVED
);
```

**Customers — After:**
```sql
CREATE TABLE Customers (
    customer_id INT          PRIMARY KEY,
    name        VARCHAR(100),
    email       VARCHAR(100) UNIQUE,
    created_at  DATE
);
```

**Sellers — Before:**
```sql
CREATE TABLE Sellers (
    seller_id       INT PRIMARY KEY,
    seller_name     VARCHAR(100),
    join_date       DATE,
    metadata_source VARCHAR(50)   -- REMOVED
);
```

**Sellers — After:**
```sql
CREATE TABLE Sellers (
    seller_id   INT          PRIMARY KEY,
    seller_name VARCHAR(100),
    join_date   DATE
);
```

**New Audit_Log table (absorbs both removed columns):**
```sql
CREATE TABLE Audit_Log (
    audit_id    INT         PRIMARY KEY AUTO_INCREMENT,
    table_name  VARCHAR(50) NOT NULL,
    record_id   INT         NOT NULL,
    created_by  VARCHAR(50),
    created_at  DATE
);
```

---

### Step 2 — Rename `metadata_note` to `category` in Products

The column holds meaningful product data (tier/classification). Only the name is wrong.

```sql
-- Before
metadata_note VARCHAR(100)

-- After
category VARCHAR(100)
```

---

### Step 3 — Rename and constrain `metadate_status` in Orders

Fix the typo and rename to reflect what it actually is: a business attribute.

```sql
-- Before (misspelled, no constraint, mixed casing)
metadate_status VARCHAR(50)

-- After
order_status VARCHAR(20) CHECK (order_status IN ('pending','shipped','delivered','cancelled'))
```

---

### Step 4 — Drop `metadata_flag` from Order_Items

The column holds `'ok'` in every row. It provides no information and is removed entirely.

```sql
-- Before
metadata_flag VARCHAR(50)   -- always 'ok'

-- After: column dropped
```

---

## 4. Final Relational Schema

This is the 3NF schema the Python application uses.

```sql
-- Drop in reverse dependency order
DROP TABLE IF EXISTS Audit_Log;
DROP TABLE IF EXISTS Order_Items;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Sellers;
DROP TABLE IF EXISTS Customers;

-- Customers: removed metadata_created_by, added UNIQUE on email
CREATE TABLE Customers (
    customer_id INT          PRIMARY KEY,
    name        VARCHAR(100),
    email       VARCHAR(100) UNIQUE,
    created_at  DATE
);

-- Sellers: removed metadata_source
CREATE TABLE Sellers (
    seller_id   INT          PRIMARY KEY,
    seller_name VARCHAR(100),
    join_date   DATE
);

-- Products: renamed metadata_note → category
CREATE TABLE Products (
    product_id   INT            PRIMARY KEY,
    product_name VARCHAR(100),
    price        DECIMAL(10,2),
    seller_id    INT,
    category     VARCHAR(100),
    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id)
);

-- Orders: fixed typo metadate_status → order_status, added CHECK
CREATE TABLE Orders (
    order_id     INT         PRIMARY KEY,
    customer_id  INT,
    order_date   DATE,
    order_status VARCHAR(20) CHECK (order_status IN
                     ('pending','shipped','delivered','cancelled')),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Order_Items: removed metadata_flag, added total_price (from DML ALTER TABLE)
CREATE TABLE Order_Items (
    order_item_id INT           PRIMARY KEY,
    order_id      INT,
    product_id    INT,
    quantity      INT,
    total_price   DECIMAL(10,2),
    FOREIGN KEY (order_id)   REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Audit_Log (new): holds audit data removed from Customers and Sellers
CREATE TABLE Audit_Log (
    audit_id    INT         PRIMARY KEY AUTO_INCREMENT,
    table_name  VARCHAR(50) NOT NULL,
    record_id   INT         NOT NULL,
    created_by  VARCHAR(50),
    created_at  DATE
);
```

### Summary of What Changed

| Table       | Column               | Change                                      |
|-------------|----------------------|---------------------------------------------|
| Customers   | `metadata_created_by`| Removed → moved to Audit_Log                |
| Sellers     | `metadata_source`    | Removed → moved to Audit_Log                |
| Products    | `metadata_note`      | Renamed to `category`                       |
| Orders      | `metadate_status`    | Renamed to `order_status`, CHECK added      |
| Order_Items | `metadata_flag`      | Dropped (constant value, no business use)   |
| Order_Items | `total_price`        | Added (was introduced via ALTER TABLE in DML)|
| *(new)*     | `Audit_Log`          | New table created for audit metadata        |
