
---

# `part3-datawarehouse/README.md`

📍 **Location:**  
`part3-datawarehouse/README.md`

```markdown
# Part 3: Data Warehouse & Analytics

## Overview

This module implements a star-schema-based data warehouse for historical sales analysis. It supports OLAP-style queries for business intelligence reporting.

---

## Schema Design

- **Fact Table:** fact_sales  
- **Dimensions:** dim_date, dim_product, dim_customer  
- **Grain:** One row per product per order line item

Detailed design rationale is documented in `star_schema_design.md`.

---

## Files Included

- **warehouse_schema.sql**  
  Creates all dimension and fact tables with constraints.

- **warehouse_data.sql**  
  Populates tables with realistic sample data.

- **analytics_queries.sql**  
  Contains OLAP queries for drill-down, product performance, and customer segmentation.

---

## Analytics Performed

1. Monthly sales drill-down (Year → Quarter → Month)
2. Top 10 products by revenue with contribution percentage
3. Customer value segmentation using CASE statements

---

## Execution

```bash
mysql -u root -p fleximart_dw < warehouse_schema.sql
mysql -u root -p fleximart_dw < warehouse_data.sql
mysql -u root -p fleximart_dw < analytics_queries.sql
