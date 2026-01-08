# NoSQL Database Analysis – FlexiMart

## Section A: Limitations of RDBMS

Relational databases like MySQL enforce a fixed schema, which makes them unsuitable for highly diverse product catalogs. In FlexiMart’s case, different products have different attributes—electronics require specifications such as RAM and processor, while fashion products need size and color. Representing this variability in an RDBMS requires multiple nullable columns or separate tables, leading to increased complexity and reduced performance.

Frequent schema changes are another challenge. Adding a new product type often requires altering table structures, which is time-consuming and risky in production environments. Additionally, storing customer reviews is difficult because relational databases are not designed for nested or hierarchical data. Reviews would require separate tables and joins, increasing query complexity and reducing flexibility. These limitations make relational databases less adaptable for evolving, attribute-rich product catalogs.

## Section B: NoSQL Benefits

MongoDB addresses these challenges using a flexible document-based schema. Each product is stored as a JSON-like document, allowing different products to have different attributes without requiring schema changes. This makes it easy to add new product types with unique fields.

MongoDB also supports embedded documents, allowing customer reviews to be stored directly inside product documents. This improves data locality and simplifies queries, as reviews can be accessed without joins. Additionally, MongoDB is designed for horizontal scalability using sharding, making it suitable for growing product catalogs and high-traffic applications. These features make MongoDB highly adaptable for modern e-commerce platforms like FlexiMart.

## Section C: Trade-offs

One disadvantage of using MongoDB is the lack of strict schema enforcement, which can lead to inconsistent data if validation rules are not properly implemented. Another drawback is that complex transactional operations and joins are generally better supported in relational databases like MySQL. For scenarios requiring strong ACID guarantees and complex reporting, MongoDB may require additional design effort.
