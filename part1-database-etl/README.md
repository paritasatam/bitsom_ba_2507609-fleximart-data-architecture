
---

# `part1-database-etl/README.md`

📍 **Location:**  
`part1-database-etl/README.md`

```markdown
# Part 1: Relational Database ETL Pipeline

## Overview

This module implements an ETL (Extract, Transform, Load) pipeline for FlexiMart using MySQL. Raw CSV files are cleaned, standardized, and loaded into a relational schema to support structured business queries.

---

## Components

- **etl_pipeline.py**  
  Extracts CSV data, removes duplicates, handles missing values, standardizes formats, and loads data into MySQL.

- **schema_documentation.md**  
  Documents table structures, relationships, and constraints.

- **business_queries.sql**  
  Contains analytical queries for customer spending, product performance, and sales trends.

- **data_quality_report.txt**  
  Auto-generated report summarizing removed rows and data issues.

---

## Data Quality Handling

- Removed rows with missing critical fields
- Deduplicated customers using unique email constraint
- Standardized dates and phone numbers
- Logged all transformations for auditability

---

## Execution

```bash
python etl_pipeline.py
mysql -u root -p fleximart < business_queries.sql
