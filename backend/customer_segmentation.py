# backend/customer_segmentation.py

import pandas as pd
import os

# -------------------------------
# Step 2: Customer Segmentation
# -------------------------------

# Paths
DATA_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\cleaned_data.csv"
OUTPUT_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\customer_segments.csv"

# Load cleaned data
print("Loading cleaned data...")
df = pd.read_csv(DATA_PATH)

# Check the columns
print("Columns in dataset:", df.columns.tolist())

# Keep relevant columns
df_customers = df[['Customer_ID', 'Phase', 'Order_ID']].drop_duplicates()

# Pivot table to count orders per customer per phase
customer_phase = df_customers.pivot_table(
    index='Customer_ID',
    columns='Phase',
    values='Order_ID',
    aggfunc='count',
    fill_value=0
).reset_index()

# Rename columns for clarity (adjust if your Phase names differ)
customer_phase.columns = ['Customer_ID', 'Crisis', 'Pre-Crisis', 'Recovery']

# Function to categorize customer
def categorize_customer(row):
    if row['Pre-Crisis'] > 0 and row['Recovery'] > 0:
        return 'Active'
    elif row['Pre-Crisis'] > 0 and row['Recovery'] == 0:
        return 'Lost'
    elif row['Crisis'] > 0 or (row['Pre-Crisis'] > 0 and row['Recovery'] == 0):
        return 'Recoverable'
    else:
        return 'New/Other'

# Apply categorization
print("Categorizing customers...")
customer_phase['Customer_Type'] = customer_phase.apply(categorize_customer, axis=1)

# Save to CSV
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
customer_phase.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Customer segmentation completed and saved to {OUTPUT_PATH}")
