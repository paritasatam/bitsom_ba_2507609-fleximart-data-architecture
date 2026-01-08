# Star Schema Design – FlexiMart Data Warehouse

## Section 1: Schema Overview

### FACT TABLE: fact_sales
- **Business Process:** Sales transactions (order line items)
- **Grain:** One row per product per order line item (each item in an order becomes one fact row)
- **Measures (Numeric Facts):**
  - `quantity_sold`: units sold in that line item
  - `unit_price`: selling price per unit at the time of sale
  - `discount_amount`: discount applied to the line item
  - `total_amount`: final amount = (quantity_sold × unit_price) − discount_amount
- **Foreign Keys:**
  - `date_key` → `dim_date(date_key)`
  - `product_key` → `dim_product(product_key)`
  - `customer_key` → `dim_customer(customer_key)`

### DIMENSION TABLE: dim_date
- **Purpose:** Time-based analysis (drill-down from year → quarter → month → day)
- **Type:** Conformed dimension
- **Attributes:**
  - `date_key (PK)`: Surrogate key, integer in YYYYMMDD format
  - `full_date`: actual calendar date
  - `day_of_week`: Monday, Tuesday, etc.
  - `day_of_month`: 1–31
  - `month`: 1–12
  - `month_name`: January, February, etc.
  - `quarter`: Q1, Q2, Q3, Q4
  - `year`: 2023, 2024, etc.
  - `is_weekend`: Boolean flag

### DIMENSION TABLE: dim_product
- **Purpose:** Product-level slicing (category, subcategory, price band)
- **Type:** Slowly changing-friendly structure (can be extended later)
- **Attributes:**
  - `product_key (PK)`: Surrogate key (auto-increment)
  - `product_id`: natural/business product id from source system
  - `product_name`: name of product
  - `category`: Electronics/Fashion/Groceries etc.
  - `subcategory`: finer grouping within a category
  - `unit_price`: reference price for reporting (fact keeps actual sold price)

### DIMENSION TABLE: dim_customer
- **Purpose:** Customer-level slicing (geography and segments)
- **Attributes:**
  - `customer_key (PK)`: Surrogate key (auto-increment)
  - `customer_id`: natural/business customer id from source system
  - `customer_name`: full name
  - `city`: customer city
  - `state`: customer state
  - `customer_segment`: e.g., Retail/Corporate/SMB/VIP (or similar)

---

## Section 2: Design Decisions (≈150 words)

The star schema uses **transaction line-item granularity** because it preserves the most detail for analytics. With one fact row per product per order item, the warehouse can answer questions at multiple levels (product, customer, category, city, month) without losing information. This grain also supports accurate calculations for measures like revenue, units sold, and discounts, and enables flexible drill-down/roll-up reporting across time and product hierarchies.

The design uses **surrogate keys** (`product_key`, `customer_key`, `date_key`) instead of natural keys because surrogate keys are stable even if business identifiers change or source systems introduce new formats. Surrogate keys also improve join performance and make it easier to manage slowly changing dimensions (e.g., product category changes, customer segment updates) without rewriting historical fact rows. Overall, this model supports OLAP-style analysis by enabling fast joins and clean aggregation paths for reporting.

---

## Section 3: Sample Data Flow

**Source Transaction:**
Order #101, Customer "John Doe", Product "Laptop", Qty: 2, Price: 50000

**Becomes in Data Warehouse:**

`dim_date`:
- `{ date_key: 20240115, full_date: '2024-01-15', month: 1, quarter: 'Q1', year: 2024, ... }`

`dim_product`:
- `{ product_key: 5, product_id: 'P007', product_name: 'Laptop', category: 'Electronics', ... }`

`dim_customer`:
- `{ customer_key: 12, customer_id: 'C010', customer_name: 'John Doe', city: 'Mumbai', ... }`

`fact_sales`:
- `{ date_key: 20240115, product_key: 5, customer_key: 12, quantity_sold: 2, unit_price: 50000, discount_amount: 0, total_amount: 100000 }`
