# FlexiMart Data Architecture Project

**Student Name:** Parita Satam
**Student Code:** bitsom_ba_2507609
**Email:** satamparita@gmail.com
**Date:** 07/01/2026

---

## Project Overview

This project implements a complete data architecture solution for FlexiMart, an e-commerce platform. The solution covers an end-to-end ETL pipeline using a relational database, a NoSQL-based product catalog using MongoDB, and a star-schema data warehouse for historical analytics and OLAP reporting. The project demonstrates data cleaning, transformation, storage, and business-oriented analytical querying.

---

## Repository Structure
```
studentID-fleximart-data-architecture/
├── README.md
├── .gitignore
├── data/
│   ├── customers_raw.csv
│   ├── products_raw.csv
│   └── sales_raw.csv
├── part1-database-etl/
│   ├── README.md
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   ├── data_quality_report.txt
│   └── requirements.txt
├── part2-nosql/
│   ├── README.md
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
└── part3-datawarehouse/
    ├── README.md
    ├── star_schema_design.md
    ├── warehouse_schema.sql
    ├── warehouse_data.sql
    └── analytics_queries.sql
```
---

## Technologies Used

- Python 3.x, Pandas, mysql-connector-python  
- MySQL 8.0  
- MongoDB (mongosh)  
- SQL (Analytical and OLAP queries)

---

## Setup Instructions

### Part 1: Relational Database and ETL Pipeline

1. Create the database:
   mysql -u root -p -e "CREATE DATABASE fleximart;"

2. Run the ETL pipeline:
   python part1-database-etl/etl_pipeline.py

3. Execute business queries:
   mysql -u root -p fleximart < part1-database-etl/business_queries.sql

---

### Part 2: NoSQL Database (MongoDB)

1. Execute MongoDB operations script:
   mongosh part2-nosql/mongodb_operations.js

This script loads the product catalog, runs analytical queries, performs updates, and executes aggregation pipelines.

---

### Part 3: Data Warehouse and Analytics

1. Create the data warehouse database:
   mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

2. Create star schema tables:
   mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql

3. Load warehouse data:
   mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql

4. Run OLAP analytics queries:
   mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql

---

## Key Learnings

- Built a robust ETL pipeline with data validation and quality reporting  
- Learned how NoSQL databases support flexible schemas and nested data  
- Designed and implemented a star schema for analytical workloads  
- Wrote OLAP queries for drill-down analysis, product performance, and customer segmentation  

---

## Challenges Faced

1. Inconsistent and missing source data  
   Solved by applying data cleaning, validation rules, and transformation logic in the ETL pipeline.

2. MongoDB execution and authentication issues on Windows  
   Resolved by understanding mongosh execution context and GitHub credential management.

3. Foreign key dependencies during data warehouse loading  
   Addressed by loading dimension tables before fact tables and validating record counts.

---
