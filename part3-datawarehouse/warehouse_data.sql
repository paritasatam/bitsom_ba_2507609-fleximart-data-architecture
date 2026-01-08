USE fleximart_dw;

-- ------------------------
-- dim_date (30 dates: Jan-Feb 2024)
-- date_key format: YYYYMMDD
-- ------------------------
INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,0),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,0),
(20240103,'2024-01-03','Wednesday',3,1,'January','Q1',2024,0),
(20240104,'2024-01-04','Thursday',4,1,'January','Q1',2024,0),
(20240105,'2024-01-05','Friday',5,1,'January','Q1',2024,0),
(20240106,'2024-01-06','Saturday',6,1,'January','Q1',2024,1),
(20240107,'2024-01-07','Sunday',7,1,'January','Q1',2024,1),
(20240108,'2024-01-08','Monday',8,1,'January','Q1',2024,0),
(20240109,'2024-01-09','Tuesday',9,1,'January','Q1',2024,0),
(20240110,'2024-01-10','Wednesday',10,1,'January','Q1',2024,0),
(20240111,'2024-01-11','Thursday',11,1,'January','Q1',2024,0),
(20240112,'2024-01-12','Friday',12,1,'January','Q1',2024,0),
(20240113,'2024-01-13','Saturday',13,1,'January','Q1',2024,1),
(20240114,'2024-01-14','Sunday',14,1,'January','Q1',2024,1),
(20240115,'2024-01-15','Monday',15,1,'January','Q1',2024,0),
(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,0),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,0),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,1),
(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,1),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,0),
(20240206,'2024-02-06','Tuesday',6,2,'February','Q1',2024,0),
(20240207,'2024-02-07','Wednesday',7,2,'February','Q1',2024,0),
(20240208,'2024-02-08','Thursday',8,2,'February','Q1',2024,0),
(20240209,'2024-02-09','Friday',9,2,'February','Q1',2024,0),
(20240210,'2024-02-10','Saturday',10,2,'February','Q1',2024,1),
(20240211,'2024-02-11','Sunday',11,2,'February','Q1',2024,1),
(20240212,'2024-02-12','Monday',12,2,'February','Q1',2024,0),
(20240213,'2024-02-13','Tuesday',13,2,'February','Q1',2024,0),
(20240214,'2024-02-14','Wednesday',14,2,'February','Q1',2024,0),
(20240215,'2024-02-15','Thursday',15,2,'February','Q1',2024,0);

-- ------------------------
-- dim_product (15 products, 3 categories)
-- ------------------------
INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('ELEC001','Laptop Pro 15','Electronics','Laptops',85000.00),
('ELEC002','Smartphone X','Electronics','Mobiles',48000.00),
('ELEC003','Wireless Headphones','Electronics','Audio',3500.00),
('ELEC004','4K Smart TV 55','Electronics','TV',62000.00),
('ELEC005','Gaming Mouse','Electronics','Accessories',1200.00),

('FASH001','Running Shoes','Fashion','Footwear',3200.00),
('FASH002','Denim Jeans','Fashion','Clothing',2400.00),
('FASH003','Casual T-Shirt','Fashion','Clothing',799.00),
('FASH004','Winter Jacket','Fashion','Outerwear',4500.00),
('FASH005','Sunglasses','Fashion','Accessories',999.00),

('GROC001','Organic Almonds 1kg','Groceries','Dry Fruits',900.00),
('GROC002','Basmati Rice 5kg','Groceries','Grains',650.00),
('GROC003','Olive Oil 1L','Groceries','Cooking',1200.00),
('GROC004','Protein Oats 1kg','Groceries','Breakfast',450.00),
('GROC005','Coffee Beans 500g','Groceries','Beverages',550.00);

-- ------------------------
-- dim_customer (12 customers, 4 cities, segments)
-- ------------------------
INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001','Rahul Sharma','Bangalore','Karnataka','Retail'),
('C002','Priya Patel','Mumbai','Maharashtra','Retail'),
('C003','Amit Kumar','Delhi','Delhi','Corporate'),
('C004','Sneha Reddy','Hyderabad','Telangana','Retail'),
('C005','Vikram Singh','Chennai','Tamil Nadu','Retail'),
('C006','Anjali Mehta','Bangalore','Karnataka','Corporate'),
('C007','Ravi Verma','Mumbai','Maharashtra','Retail'),
('C008','Pooja Iyer','Hyderabad','Telangana','Retail'),
('C009','Karthik Nair','Chennai','Tamil Nadu','Corporate'),
('C010','Suresh Patel','Delhi','Delhi','Retail'),
('C011','Divya Menon','Bangalore','Karnataka','Retail'),
('C012','Rajesh Kumar','Mumbai','Maharashtra','Corporate');

-- ------------------------
-- fact_sales (40 transactions)
-- NOTE: product_key and customer_key are AUTO_INCREMENT.
-- Since we inserted products/customers in order, keys will be:
-- product_key: 1..15, customer_key: 1..12
-- total_amount = quantity_sold * unit_price - discount_amount
-- ------------------------
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
-- January (weekends slightly higher qty)
(20240101,  2,  1, 1, 48000.00,  0.00, 48000.00),
(20240102,  6,  2, 2,  3200.00, 50.00,  6350.00),
(20240103, 11,  3, 3,   900.00,  0.00,  2700.00),
(20240104,  1,  4, 1, 85000.00, 500.00, 84500.00),
(20240105,  7,  5, 2,  2400.00,  0.00,  4800.00),
(20240106,  4,  6, 1, 62000.00, 1000.00, 61000.00),
(20240106, 12,  7, 5,   650.00,  0.00,  3250.00),
(20240107,  3,  8, 2,  3500.00, 100.00,  6900.00),
(20240107, 15,  9, 4,   550.00,  0.00,  2200.00),
(20240108,  5, 10, 3,  1200.00,  0.00,  3600.00),

(20240109,  8, 11, 2,   799.00,  0.00,  1598.00),
(20240110, 13, 12, 1,  1200.00,  0.00,  1200.00),
(20240111,  9,  1, 1,  4500.00,  0.00,  4500.00),
(20240112, 10,  2, 2,   999.00,  0.00,  1998.00),
(20240113,  2,  3, 2, 48000.00, 1500.00, 94500.00),
(20240113, 14,  4, 6,   450.00,  0.00,  2700.00),
(20240114,  6,  5, 3,  3200.00, 150.00,  9450.00),
(20240114,  1,  6, 1, 85000.00,  0.00, 85000.00),
(20240115, 11,  7, 2,   900.00,  0.00,  1800.00),
(20240115,  7,  8, 1,  2400.00,  0.00,  2400.00),

-- February
(20240201,  2,  9, 1, 48000.00,  0.00, 48000.00),
(20240202, 12, 10, 4,   650.00,  0.00,  2600.00),
(20240203,  4, 11, 1, 62000.00, 2000.00, 60000.00),
(20240203,  8, 12, 4,   799.00,  0.00,  3196.00),
(20240204,  6,  1, 2,  3200.00,  0.00,  6400.00),
(20240204, 15,  2, 5,   550.00,  0.00,  2750.00),
(20240205,  3,  3, 1,  3500.00,  0.00,  3500.00),
(20240206,  1,  4, 1, 85000.00, 2500.00, 82500.00),
(20240207, 13,  5, 2,  1200.00,  0.00,  2400.00),
(20240208, 11,  6, 3,   900.00,  0.00,  2700.00),

(20240209, 10,  7, 2,   999.00,  0.00,  1998.00),
(20240210,  2,  8, 1, 48000.00,  0.00, 48000.00),
(20240210,  9,  9, 2,  4500.00, 200.00,  8800.00),
(20240211,  7, 10, 3,  2400.00,  0.00,  7200.00),
(20240211, 14, 11, 8,   450.00,  0.00,  3600.00),
(20240212,  5, 12, 2,  1200.00,  0.00,  2400.00),
(20240213,  4,  1, 1, 62000.00,  0.00, 62000.00),
(20240214,  6,  2, 1,  3200.00,  0.00,  3200.00),
(20240215, 12,  3, 6,   650.00,  0.00,  3900.00),
(20240215,  1,  4, 1, 85000.00, 5000.00, 80000.00);
