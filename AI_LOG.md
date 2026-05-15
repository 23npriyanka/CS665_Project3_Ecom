# AI Assistance Log — CS665 Project 3

## Entry 1

**Tool:** Claude
**Promt:**"I need Part 2  complete instructions how to do and all with clear instructions and answers"

**AI Output Summary:**
The AI generated all the requirements to needed for the project

**My Modification**
I got to know what i need to do so started with the project.


## Entry 2
**Promt:**"What and all do i need to setup for the project"
**AI Output Summary:**
The AI provided me what and all do i need to setup and version of all softwares.
**My Modification**
I installed what and all i needed to the project and started with the each part frontend backend and database files.


## Entry 3

**Tool:** Claude (Anthropic, claude.ai)

**Prompt:**
> "I have a Flask e-commerce project with 5 tables: Customers, Sellers, Products, Orders, Order_Items. Generate a SQLAlchemy models file and Flask app with CRUD routes for all four entities."

**AI Output Summary:**
The AI generated a `database.py` with SQLAlchemy model classes using `db.relationship()` for all foreign keys, and an `app.py` with GET/POST routes for listing, adding, editing, and deleting each entity.

**My Modifications:**
- Added server-side validation logic (empty string check, negative price check, email `@` check, duplicate email check)
- Changed column names to match my specific DDL (e.g., `metadate_status` → `status`, `metadata_created_by` → `created_by`)
- Added the transactional order creation route using `db.session.flush()` followed by `db.session.rollback()` on error
- Adjusted relationships to use `back_populates` consistently
- Removed auto-generated test stubs that didn't match my schema

---

## Entry 4

**Tool:** Claude (Anthropic, claude.ai)

**Prompt:**
> "Generate a Bootstrap 5 Jinja2 base template with a dark navbar and flash message support for a Flask app with routes: dashboard, customers, sellers, products, orders."

**AI Output Summary:**
The AI generated a `base.html` with a navbar using `navbar-dark bg-dark`, a collapsible mobile menu, and a flash message block using `get_flashed_messages(with_categories=true)`.

**My Modifications:**
- Added active class logic using `request.endpoint` checks to highlight the current page
- Added Bootstrap Icons CDN link
- Adjusted container class from `container` to `container-fluid px-4` for wider layout
- Added `{% block scripts %}` at the bottom for per-page JavaScript

---

## Entry 5

**Tool:** Claude (Anthropic, claude.ai)

**Prompt:**
> "Write a NORMALIZATION.md for a database schema with tables Customers, Sellers, Products, Orders, Order_Items. Identify functional dependencies, anomalies, and show 3NF analysis."

**AI Output Summary:**
The AI generated a structured normalization report covering 1NF, 2NF, 3NF with a dependency table and anomaly section.

**My Modifications:**
- Updated the anomaly table to reflect the specific typo (`metadate_status`) from my actual DDL
- Added the `total_price` derived-column justification specific to my schema
- Rewrote the final schema section to match the exact column names in my `database.py`
- Added the Many-to-Many note about Orders ↔ Products via Order_Items

---

## Entry 6

**Tool:** Claude (Anthropic, claude.ai)

**Prompt:**
> "Write a dashboard Flask route and Jinja2 template that shows aggregate stats: total customers, sellers, products, orders, total revenue (SUM), average order value (AVG), top customers by order count, and orders grouped by status."

**AI Output Summary:**
The AI generated a dashboard route using `func.count`, `func.sum`, `func.avg` from SQLAlchemy, and a template with Bootstrap cards.

**My Modifications:**
- Fixed the `func.sum` query — the AI used `Order.total` which doesn't exist in my schema; corrected to `func.sum(OrderItem.total_price)`
- Added null-safe fallback `or 0` for SUM/AVG when table is empty
- Added color-coded status badges in the orders-by-status table
- Changed card layout from 3-column to 2-row responsive grid

## Entry 7
**Tool:** Claude

**Prompt:** "Can u give me how can i start with git and how can i do commits in incremental format"

**AI Output Summary:**
Ai gave me the steps how can start with adding new repository and how to commit each file into the git

**My Modification**
Started with commit my codes into the repository.



*All AI-generated code was reviewed, tested, and modified before inclusion in this repository.*
