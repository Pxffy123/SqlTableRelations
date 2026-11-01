# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# Verify connection / check tables
print("--- Schema Check ---")
print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))

# ==========================================
# Part 1: Join and Filter
# ==========================================
print("\n--- Part 1: Boston Employees ---")
query_1a = """
SELECT firstName, lastName, jobTitle 
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
"""
print(pd.read_sql(query_1a, conn))

print("\n--- Part 1: Offices with Zero Employees ---")
query_1b = """
SELECT o.* 
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL;
"""
print(pd.read_sql(query_1b, conn))


# ==========================================
# Part 2: Type of Join
# ==========================================
print("\n--- Part 2: All Employees with Office Location ---")
query_2a = """
SELECT e.firstName, e.lastName, o.city, o.state 
FROM employees e
LEFT JOIN offices o ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName;
"""
print(pd.read_sql(query_2a, conn))

print("\n--- Part 2: Customers with No Orders ---")
query_2b = """
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber 
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName;
"""
print(pd.read_sql(query_2b, conn))


# ==========================================
# Part 3: Built-In Function
# ==========================================
print("\n--- Part 3: Customer Payments Sorted by Amount ---")
query_3 = """
SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate 
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC;
"""
print(pd.read_sql(query_3, conn))


# ==========================================
# Part 4: Joining and Grouping
# ==========================================
print("\n--- Part 4: Top 4 Employees by Average Credit Limit > 90k ---")
query_4a = """
SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_customers
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY num_customers DESC
LIMIT 4;
"""
print(pd.read_sql(query_4a, conn))

print("\n--- Part 4: Top-Selling Products ---")
query_4b = """
SELECT p.productName, COUNT(o.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC;
"""
print(pd.read_sql(query_4b, conn))


# ==========================================
# Part 5: Multiple Joins
# ==========================================
print("\n--- Part 5: Product Purchasers Count ---")
query_5a = """
SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC;
"""
print(pd.read_sql(query_5a, conn))

print("\n--- Part 5: Customers per Office ---")
query_5b = """
SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city;
"""
print(pd.read_sql(query_5b, conn))


# ==========================================
# Part 6: Subquery
# ==========================================
print("\n--- Part 6: Employees Selling Products Ordered by < 20 Customers ---")
query_6 = """
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber = ord.customerNumber
JOIN orderdetails od ON ord.orderNumber = od.orderNumber
JOIN offices o ON e.officeCode = o.officeCode
WHERE od.productCode IN (
    SELECT od2.productCode 
    FROM orderdetails od2 
    JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber 
    JOIN customers c2 ON ord2.customerNumber = c2.customerNumber 
    GROUP BY od2.productCode 
    HAVING COUNT(DISTINCT c2.customerNumber) < 20
);
"""
print(pd.read_sql(query_6, conn))

# Close the database connection
conn.close()