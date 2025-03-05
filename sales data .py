import pandas as pd

# Load Excel file
file_path = "enhanced_sales_data.xlsx"  # Replace with your actual file path
df = pd.read_excel(file_path)

# Data Cleaning (Handling missing values, correcting data types)
df.dropna(inplace=True)
df['date'] = pd.to_datetime(df['date'])
df['total_sales'] = df['quantity'] * df['price']

print(df.head())  # Preview cleaned data

import mysql.connector
from sqlalchemy import create_engine

# Database connection details
db_config = {
    "host": "localhost",
    "user": "root",   # Replace with your MySQL username
    "password": "root123",  # Replace with your MySQL password
    "database": "sales_db"
}

# Create SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

# Insert data into MySQL
df.to_sql("saleses", con=engine, if_exists="append", index=False)
print("Data inserted successfully!")

import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Query: Total Sales by Product
query = """
SELECT product_name, SUM(total_sales) as total_revenue
FROM saleses
GROUP BY product_name
ORDER BY total_revenue DESC;
"""
cursor.execute(query)
result = cursor.fetchall()

print("Top Products by Revenue:")
for row in result:
    print(row)

cursor.close()
conn.close()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Fetch sales data from MySQL
query = "SELECT product_name, SUM(total_sales) as total_revenue FROM sales GROUP BY product_name;"
df_sales = pd.read_sql(query, con=engine)

# Set a modern, clean style
sns.set_style("whitegrid")

# Define colors for better aesthetics
palette = sns.color_palette("husl", len(df_sales))

# Create the pie chart
plt.figure(figsize=(10, 6))
plt.pie(
    df_sales["total_revenue"],
    labels=df_sales["product_name"],
    autopct="%1.1f%%",
    colors=palette,
    startangle=140,
    wedgeprops={"edgecolor": "black"}
)

# Add a title
plt.title("💰 Revenue Contribution by Product", fontsize=14, fontweight="bold")

# Show the pie chart
plt.show()

