# FlexiMart Database Schema Documentation

## Overview
This document describes the relational database schema designed for the FlexiMart e-commerce analytics system. The schema supports customer management, product catalog, and sales transactions.

---

## Entity-Relationship Description

### ENTITY: customers
**Purpose:** Stores customer demographic and registration information.

**Attributes:**
- customer_id: Unique identifier for each customer (Primary Key)
- first_name: Customer's first name
- last_name: Customer's last name
- email: Unique email address of the customer
- phone: Standardized customer phone number
- city: City of residence
- registration_date: Date when the customer registered

**Relationships:**
- One customer can place MANY orders (1:M relationship with orders)

---

### ENTITY: products
**Purpose:** Stores product catalog information.

**Attributes:**
- product_id: Unique identifier for each product (Primary Key)
- product_name: Name of the product
- category: Product category
- price: Unit price of the product
- stock_quantity: Available inventory count

**Relationships:**
- One product can appear in MANY order items (1:M relationship with order_items)

---

### ENTITY: orders
**Purpose:** Stores high-level order transaction data.

**Attributes:**
- order_id: Unique identifier for each order (Primary Key)
- customer_id: References customers(customer_id)
- order_date: Date the order was placed
- total_amount: Total value of the order
- status: Order status (Completed, Pending, Cancelled)

**Relationships:**
- One order belongs to ONE customer (M:1 with customers)
- One order contains MANY order items (1:M with order_items)

---

### ENTITY: order_items
**Purpose:** Stores detailed line items for each order.

**Attributes:**
- order_item_id: Unique identifier (Primary Key)
- order_id: References orders(order_id)
- product_id: References products(product_id)
- quantity: Number of units purchased
- unit_price: Price per unit at time of sale
- subtotal: Calculated quantity × unit_price

**Relationships:**
- MANY order items belong to ONE order
- MANY order items reference ONE product

---

## Normalization Explanation (Third Normal Form)

The FlexiMart database schema is designed in Third Normal Form (3NF) to eliminate redundancy and ensure data integrity. Each table contains attributes that are fully functionally dependent on the primary key. In the customers table, all attributes depend solely on customer_id, and no non-key attribute depends on another non-key attribute. Similarly, product details such as product_name, category, price, and stock_quantity depend only on product_id.

The orders table stores order-level attributes that depend exclusively on order_id, while order_items contains only line-item-specific details dependent on order_item_id. This separation prevents update anomalies, such as having to modify product prices across multiple rows. Insert anomalies are avoided because new customers or products can be added independently without requiring associated orders. Delete anomalies are prevented because removing an order does not result in the loss of customer or product data.

Overall, the schema ensures minimal redundancy, high consistency, and efficient querying, which is ideal for analytical and transactional workloads.

---

## Sample Data Representation

### customers
| customer_id | first_name | last_name | email | city | registration_date |
|------------|-----------|----------|-------|------|-------------------|
| 1 | Rahul | Sharma | rahul.sharma@gmail.com | Bangalore | 2023-01-15 |
| 2 | Priya | Patel | priya.patel@yahoo.com | Mumbai | 2023-02-20 |

### products
| product_id | product_name | category | price | stock_quantity |
|-----------|--------------|----------|-------|----------------|
| 1 | Samsung Galaxy S21 | Electronics | 45999.00 | 150 |
| 2 | Nike Running Shoes | Fashion | 3499.00 | 80 |

### orders
| order_id | customer_id | order_date | total_amount | status |
|---------|------------|------------|--------------|--------|
| 1 | 1 | 2024-01-15 | 45999.00 | Completed |
| 2 | 2 | 2024-02-01 | 899.00 | Completed |

### order_items
| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|--------------|----------|------------|----------|------------|----------|
| 1 | 1 | 1 | 1 | 45999.00 | 45999.00 |
| 2 | 2 | 6 | 1 | 899.00 | 899.00 |
