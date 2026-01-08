
---

# `part2-nosql/README.md`

📍 **Location:**  
`part2-nosql/README.md`

```markdown
# Part 2: NoSQL Database Analysis (MongoDB)

## Overview

This module evaluates the suitability of MongoDB for managing FlexiMart’s dynamic product catalog and implements core NoSQL operations using a document-based approach.

---

## Files Included

- **nosql_analysis.md**  
  Theoretical justification comparing RDBMS and MongoDB, including benefits and trade-offs.

- **products_catalog.json**  
  Sample product catalog with flexible attributes and embedded reviews.

- **mongodb_operations.js**  
  MongoDB shell script performing data load, queries, updates, and aggregations.

---

## MongoDB Operations Implemented

1. Load JSON product catalog into MongoDB
2. Query electronics products below a price threshold
3. Calculate average review ratings using aggregation
4. Add a new review to an existing product
5. Aggregate average price by category

---

## Execution

```bash
mongosh mongodb_operations.js
